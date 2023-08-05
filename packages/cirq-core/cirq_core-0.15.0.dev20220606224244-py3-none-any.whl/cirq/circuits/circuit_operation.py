# Copyright 2020 The Cirq Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""A structure for encapsulating entire circuits in an operation.

A CircuitOperation is an Operation object that wraps a FrozenCircuit. When
applied as part of a larger circuit, a CircuitOperation will execute all
component operations in order, including any nested CircuitOperations.
"""
import dataclasses
import math
from typing import (
    AbstractSet,
    Callable,
    cast,
    Dict,
    FrozenSet,
    Iterator,
    List,
    Optional,
    Tuple,
    TYPE_CHECKING,
    Union,
)

import numpy as np
import sympy

from cirq import circuits, ops, protocols, value, study
from cirq._compat import proper_repr

if TYPE_CHECKING:
    import cirq


INT_CLASSES = (int, np.integer)
INT_TYPE = Union[int, np.integer]
IntParam = Union[INT_TYPE, sympy.Expr]
REPETITION_ID_SEPARATOR = '-'


def default_repetition_ids(repetitions: IntParam) -> Optional[List[str]]:
    if isinstance(repetitions, INT_CLASSES) and abs(repetitions) != 1:
        return [str(i) for i in range(abs(repetitions))]
    return None


def _full_join_string_lists(
    list1: Optional[List[str]], list2: Optional[List[str]]
) -> Optional[List[str]]:
    if list1 is None and list2 is None:
        return None  # coverage: ignore
    if list1 is None:
        return list2  # coverage: ignore
    if list2 is None:
        return list1
    return [f'{first}{REPETITION_ID_SEPARATOR}{second}' for first in list1 for second in list2]


@dataclasses.dataclass(frozen=True)
class CircuitOperation(ops.Operation):
    """An operation that encapsulates a circuit.

    This class captures modifications to the contained circuit, such as tags
    and loops, to support more condensed serialization. Similar to
    GateOperation, this type is immutable.

    Args:
        circuit: The FrozenCircuit wrapped by this operation.
        repetitions: How many times the circuit should be repeated. This can be
            integer, or a sympy expression. If sympy, the expression must
            resolve to an integer, or float within 0.001 of integer, at
            runtime.
        qubit_map: Remappings for qubits in the circuit.
        measurement_key_map: Remappings for measurement keys in the circuit.
            The keys and values should be unindexed (i.e. without repetition_ids).
            The values cannot contain the `MEASUREMENT_KEY_SEPARATOR`.
        param_resolver: Resolved values for parameters in the circuit.
        repetition_ids: List of identifiers for each repetition of the
            CircuitOperation. If populated, the length should be equal to the
            repetitions. If not populated and abs(`repetitions`) > 1, it is
            initialized to strings for numbers in `range(repetitions)`.
        parent_path: A tuple of identifiers for any parent CircuitOperations
            containing this one.
        extern_keys: The set of measurement keys defined at extern scope. The
            values here are used by decomposition and simulation routines to
            cache which external measurement keys exist as possible binding
            targets for unbound `ClassicallyControlledOperation` keys. This
            field is not intended to be set or changed manually, and should be
            empty in circuits that aren't in the middle of decomposition.
        use_repetition_ids: When True, any measurement key in the subcircuit
            will have its path prepended with the repetition id for each
            repetition. When False, this will not happen and the measurement
            key will be repeated.
        repeat_until: A condition that will be tested after each iteration of
            the subcircuit. The subcircuit will repeat until condition returns
            True, but will always run at least once, and the measurement key
            need not be defined prior to the subcircuit (but must be defined in
            a measurement within the subcircuit). This field is incompatible
            with repetitions or repetition_ids.
    """

    _hash: Optional[int] = dataclasses.field(default=None, init=False)
    _cached_measurement_key_objs: Optional[AbstractSet['cirq.MeasurementKey']] = dataclasses.field(
        default=None, init=False
    )
    _cached_control_keys: Optional[AbstractSet['cirq.MeasurementKey']] = dataclasses.field(
        default=None, init=False
    )
    _cached_mapped_single_loop: Optional['cirq.Circuit'] = dataclasses.field(
        default=None, init=False
    )

    circuit: 'cirq.FrozenCircuit'
    repetitions: IntParam = 1
    qubit_map: Dict['cirq.Qid', 'cirq.Qid'] = dataclasses.field(default_factory=dict)
    measurement_key_map: Dict[str, str] = dataclasses.field(default_factory=dict)
    param_resolver: study.ParamResolver = study.ParamResolver()
    repetition_ids: Optional[List[str]] = dataclasses.field(default=None)
    parent_path: Tuple[str, ...] = dataclasses.field(default_factory=tuple)
    extern_keys: FrozenSet['cirq.MeasurementKey'] = dataclasses.field(default_factory=frozenset)
    use_repetition_ids: bool = True
    repeat_until: Optional['cirq.Condition'] = dataclasses.field(default=None)

    def __post_init__(self):
        if not isinstance(self.circuit, circuits.FrozenCircuit):
            raise TypeError(f'Expected circuit of type FrozenCircuit, got: {type(self.circuit)!r}')

        # Ensure that the circuit is invertible if the repetitions are negative.
        if isinstance(self.repetitions, float):
            if math.isclose(self.repetitions, round(self.repetitions)):
                object.__setattr__(self, 'repetitions', round(self.repetitions))
        if isinstance(self.repetitions, INT_CLASSES):
            if self.repetitions < 0:
                try:
                    protocols.inverse(self.circuit.unfreeze())
                except TypeError:
                    raise ValueError('repetitions are negative but the circuit is not invertible')

            # Initialize repetition_ids to default, if unspecified. Else, validate their length.
            loop_size = abs(self.repetitions)
            if not self.repetition_ids:
                object.__setattr__(self, 'repetition_ids', self._default_repetition_ids())
            elif len(self.repetition_ids) != loop_size:
                raise ValueError(
                    f'Expected repetition_ids to be a list of length {loop_size}, '
                    f'got: {self.repetition_ids}'
                )
        elif isinstance(self.repetitions, sympy.Expr):
            if self.repetition_ids is not None:
                raise ValueError('Cannot use repetition ids with parameterized repetitions')
        else:
            raise TypeError(
                f'Only integer or sympy repetitions are allowed.\n'
                f'User provided: {self.repetitions}'
            )

        # Disallow mapping to keys containing the `MEASUREMENT_KEY_SEPARATOR`
        for mapped_key in self.measurement_key_map.values():
            if value.MEASUREMENT_KEY_SEPARATOR in mapped_key:
                raise ValueError(
                    f'Mapping to invalid key: {mapped_key}. "{value.MEASUREMENT_KEY_SEPARATOR}" '
                    'is not allowed for measurement keys in a CircuitOperation'
                )

        # Disallow qid mapping dimension conflicts.
        for q, q_new in self.qubit_map.items():
            if q_new.dimension != q.dimension:
                raise ValueError(f'Qid dimension conflict.\nFrom qid: {q}\nTo qid: {q_new}')

        if self.repeat_until:
            if self.use_repetition_ids or self.repetitions != 1:
                raise ValueError('Cannot use repetitions with repeat_until')
            if protocols.measurement_key_objs(self._mapped_single_loop()).isdisjoint(
                self.repeat_until.keys
            ):
                raise ValueError('Infinite loop: condition is not modified in subcircuit.')

        # Ensure that param_resolver is converted to an actual ParamResolver.
        object.__setattr__(self, 'param_resolver', study.ParamResolver(self.param_resolver))

    def base_operation(self) -> 'cirq.CircuitOperation':
        """Returns a copy of this operation with only the wrapped circuit.

        Key and qubit mappings, parameter values, and repetitions are not copied.
        """
        return CircuitOperation(self.circuit)

    def replace(self, **changes) -> 'cirq.CircuitOperation':
        """Returns a copy of this operation with the specified changes."""
        return dataclasses.replace(self, **changes)

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return (
            self.circuit == other.circuit
            and self.qubit_map == other.qubit_map
            and self.measurement_key_map == other.measurement_key_map
            and self.param_resolver == other.param_resolver
            and self.repetitions == other.repetitions
            and self.repetition_ids == other.repetition_ids
            and self.parent_path == other.parent_path
            and self.use_repetition_ids == other.use_repetition_ids
            and self.repeat_until == other.repeat_until
        )

    # Methods for getting post-mapping properties of the contained circuit.

    @property
    def qubits(self) -> Tuple['cirq.Qid', ...]:
        """Returns the qubits operated on by this object."""
        ordered_qubits = ops.QubitOrder.DEFAULT.order_for(self.circuit.all_qubits())
        return tuple(self.qubit_map.get(q, q) for q in ordered_qubits)

    def _default_repetition_ids(self) -> Optional[List[str]]:
        return default_repetition_ids(self.repetitions) if self.use_repetition_ids else None

    def _qid_shape_(self) -> Tuple[int, ...]:
        return tuple(q.dimension for q in self.qubits)

    def _is_measurement_(self) -> bool:
        return self.circuit._is_measurement_()

    def _has_unitary_(self) -> bool:
        # Return false if parameterized for early exit of has_unitary protocol.
        # Otherwise return NotImplemented instructing the protocol to try alternate strategies
        if self._is_parameterized_() or self.repeat_until:
            return False
        return NotImplemented

    def _ensure_deterministic_loop_count(self):
        if self.repeat_until or isinstance(self.repetitions, sympy.Expr):
            raise ValueError('Cannot unroll circuit due to nondeterministic repetitions')

    def _measurement_key_objs_(self) -> AbstractSet['cirq.MeasurementKey']:
        if self._cached_measurement_key_objs is None:
            circuit_keys = protocols.measurement_key_objs(self.circuit)
            if circuit_keys and self.use_repetition_ids:
                self._ensure_deterministic_loop_count()
                if self.repetition_ids is not None:
                    circuit_keys = {
                        key.with_key_path_prefix(repetition_id)
                        for repetition_id in self.repetition_ids
                        for key in circuit_keys
                    }
            circuit_keys = {key.with_key_path_prefix(*self.parent_path) for key in circuit_keys}
            object.__setattr__(
                self,
                '_cached_measurement_key_objs',
                {
                    protocols.with_measurement_key_mapping(key, self.measurement_key_map)
                    for key in circuit_keys
                },
            )
        return self._cached_measurement_key_objs  # type: ignore

    def _measurement_key_names_(self) -> AbstractSet[str]:
        return {str(key) for key in self._measurement_key_objs_()}

    def _control_keys_(self) -> AbstractSet['cirq.MeasurementKey']:
        if self._cached_control_keys is None:
            keys = (
                frozenset()
                if not protocols.control_keys(self.circuit)
                else protocols.control_keys(self._mapped_single_loop())
            )
            if self.repeat_until is not None:
                keys |= frozenset(self.repeat_until.keys) - self._measurement_key_objs_()
            object.__setattr__(self, '_cached_control_keys', keys)
        return self._cached_control_keys  # type: ignore

    def _is_parameterized_(self) -> bool:
        return any(self._parameter_names_generator())

    def _parameter_names_(self) -> AbstractSet[str]:
        return frozenset(self._parameter_names_generator())

    def _parameter_names_generator(self) -> Iterator[str]:
        yield from protocols.parameter_names(self.repetitions)
        for symbol in protocols.parameter_symbols(self.circuit):
            for name in protocols.parameter_names(
                protocols.resolve_parameters(symbol, self.param_resolver, recursive=False)
            ):
                yield name

    def _mapped_single_loop(self, repetition_id: Optional[str] = None) -> 'cirq.Circuit':
        if self._cached_mapped_single_loop is None:
            circuit = self.circuit.unfreeze()
            if self.qubit_map:
                circuit = circuit.transform_qubits(lambda q: self.qubit_map.get(q, q))
            if isinstance(self.repetitions, INT_CLASSES) and self.repetitions < 0:
                circuit = circuit**-1
            if self.measurement_key_map:
                circuit = protocols.with_measurement_key_mapping(circuit, self.measurement_key_map)
            if self.param_resolver:
                circuit = protocols.resolve_parameters(
                    circuit, self.param_resolver, recursive=False
                )
            object.__setattr__(self, '_cached_mapped_single_loop', circuit)
        circuit = cast(circuits.Circuit, self._cached_mapped_single_loop)
        if repetition_id:
            circuit = protocols.with_rescoped_keys(circuit, (repetition_id,))
        return protocols.with_rescoped_keys(
            circuit, self.parent_path, bindable_keys=self.extern_keys
        )

    def mapped_circuit(self, deep: bool = False) -> 'cirq.Circuit':
        """Applies all maps to the contained circuit and returns the result.

        Args:
            deep: If true, this will also call mapped_circuit on any
                CircuitOperations this object contains.

        Returns:
            The contained circuit with all other member variables (repetitions,
            qubit mapping, parameterization, etc.) applied to it. This behaves
            like `cirq.decompose(self)`, but preserving moment structure.
        """
        self._ensure_deterministic_loop_count()
        if self.repetitions == 0:
            return circuits.Circuit()
        circuit = (
            circuits.Circuit(self._mapped_single_loop(rep) for rep in self.repetition_ids)
            if self.repetition_ids is not None
            and self.use_repetition_ids
            and protocols.is_measurement(self.circuit)
            else self._mapped_single_loop() * abs(self.repetitions)
        )
        if deep:
            circuit = circuit.map_operations(
                lambda op: op.mapped_circuit(deep=True) if isinstance(op, CircuitOperation) else op
            )
        return circuit

    def mapped_op(self, deep: bool = False) -> 'cirq.CircuitOperation':
        """As `mapped_circuit`, but wraps the result in a CircuitOperation."""
        return CircuitOperation(circuit=self.mapped_circuit(deep=deep).freeze())

    def _decompose_(self) -> Iterator['cirq.Operation']:
        return self.mapped_circuit(deep=False).all_operations()

    def _act_on_(self, sim_state: 'cirq.SimulationStateBase') -> bool:
        if self.repeat_until:
            circuit = self._mapped_single_loop()
            while True:
                for op in circuit.all_operations():
                    protocols.act_on(op, sim_state)
                if self.repeat_until.resolve(sim_state.classical_data):
                    break
        else:
            for op in self._decompose_():
                protocols.act_on(op, sim_state)
        return True

    # Methods for string representation of the operation.

    def __repr__(self):
        args = f'\ncircuit={self.circuit!r},\n'
        if self.repetitions != 1:
            args += f'repetitions={self.repetitions},\n'
        if self.qubit_map:
            args += f'qubit_map={proper_repr(self.qubit_map)},\n'
        if self.measurement_key_map:
            args += f'measurement_key_map={proper_repr(self.measurement_key_map)},\n'
        if self.param_resolver:
            args += f'param_resolver={proper_repr(self.param_resolver)},\n'
        if self.parent_path:
            args += f'parent_path={proper_repr(self.parent_path)},\n'
        if self.repetition_ids != self._default_repetition_ids():
            # Default repetition_ids need not be specified.
            args += f'repetition_ids={proper_repr(self.repetition_ids)},\n'
        if not self.use_repetition_ids:
            args += 'use_repetition_ids=False,\n'
        if self.repeat_until:
            args += f'repeat_until={self.repeat_until!r},\n'
        indented_args = args.replace('\n', '\n    ')
        return f'cirq.CircuitOperation({indented_args[:-4]})'

    def __str__(self):
        # TODO: support out-of-line subcircuit definition in string format.
        msg_lines = str(self.circuit).split('\n')
        msg_width = max([len(line) for line in msg_lines])
        circuit_msg = '\n'.join(
            '[ {line:<{width}} ]'.format(line=line, width=msg_width) for line in msg_lines
        )
        args = []

        def dict_str(d: Dict) -> str:
            pairs = [f'{k}: {v}' for k, v in sorted(d.items())]
            return '{' + ', '.join(pairs) + '}'

        if self.qubit_map:
            args.append(f'qubit_map={dict_str(self.qubit_map)}')
        if self.measurement_key_map:
            args.append(f'key_map={dict_str(self.measurement_key_map)}')
        if self.param_resolver:
            args.append(f'params={self.param_resolver.param_dict}')
        if self.parent_path:
            args.append(f'parent_path={self.parent_path}')
        if self.repetition_ids != self._default_repetition_ids():
            # Default repetition_ids need not be specified.
            args.append(f'repetition_ids={self.repetition_ids}')
        elif self.repetitions != 1:
            # Only add loops if we haven't added repetition_ids.
            args.append(f'loops={self.repetitions}')
        if not self.use_repetition_ids:
            args.append('no_rep_ids')
        if self.repeat_until:
            args.append(f'until={self.repeat_until}')
        if not args:
            return circuit_msg
        return f'{circuit_msg}({", ".join(args)})'

    def __hash__(self):
        if self._hash is None:
            object.__setattr__(
                self,
                '_hash',
                hash(
                    (
                        self.circuit,
                        self.repetitions,
                        frozenset(self.qubit_map.items()),
                        frozenset(self.measurement_key_map.items()),
                        self.param_resolver,
                        self.parent_path,
                        tuple([] if self.repetition_ids is None else self.repetition_ids),
                        self.use_repetition_ids,
                    )
                ),
            )
        return self._hash

    def _json_dict_(self):
        resp = {
            'circuit': self.circuit,
            'repetitions': self.repetitions,
            # JSON requires mappings to have keys of basic types.
            # Pairs must be sorted to ensure consistent serialization.
            'qubit_map': sorted(self.qubit_map.items()),
            'measurement_key_map': self.measurement_key_map,
            'param_resolver': self.param_resolver,
            'repetition_ids': self.repetition_ids,
            'parent_path': self.parent_path,
        }
        if not self.use_repetition_ids:
            resp['use_repetition_ids'] = False
        if self.repeat_until:
            resp['repeat_until'] = self.repeat_until
        return resp

    @classmethod
    def _from_json_dict_(
        cls,
        circuit,
        repetitions,
        qubit_map,
        measurement_key_map,
        param_resolver,
        repetition_ids,
        parent_path=(),
        use_repetition_ids=True,
        repeat_until=None,
        **kwargs,
    ):
        return (
            cls(circuit, use_repetition_ids=use_repetition_ids, repeat_until=repeat_until)
            .with_qubit_mapping(dict(qubit_map))
            .with_measurement_key_mapping(measurement_key_map)
            .with_params(param_resolver)
            .with_key_path(tuple(parent_path))
            .repeat(repetitions, repetition_ids)
        )

    # Methods for constructing a similar object with one field modified.

    def repeat(
        self, repetitions: Optional[IntParam] = None, repetition_ids: Optional[List[str]] = None
    ) -> 'CircuitOperation':
        """Returns a copy of this operation repeated 'repetitions' times.
         Each repetition instance will be identified by a single repetition_id.

        Args:
            repetitions: Number of times this operation should repeat. This
                is multiplied with any pre-existing repetitions. If unset, it
                defaults to the length of `repetition_ids`.
            repetition_ids: List of IDs, one for each repetition. If unset,
                defaults to `default_repetition_ids(repetitions)`.

        Returns:
            A copy of this operation repeated `repetitions` times with the
            appropriate `repetition_ids`. The output `repetition_ids` are the
            cartesian product of input `repetition_ids` with the base
            operation's `repetition_ids`. If the base operation has unset
            `repetition_ids` (indicates {-1, 0, 1} `repetitions` with no custom
            IDs), the input `repetition_ids` are directly used.

        Raises:
            TypeError: `repetitions` is not an integer value.
            ValueError: Unexpected length of `repetition_ids`.
            ValueError: Both `repetitions` and `repetition_ids` are None.
        """
        if repetitions is None:
            if repetition_ids is None:
                raise ValueError('At least one of repetitions and repetition_ids must be set')
            repetitions = len(repetition_ids)

        if isinstance(repetitions, INT_CLASSES):
            if repetitions == 1 and repetition_ids is None:
                # As CircuitOperation is immutable, this can safely return the original.
                return self

            expected_repetition_id_length = abs(repetitions)

            if repetition_ids is None:
                if self.use_repetition_ids:
                    repetition_ids = default_repetition_ids(expected_repetition_id_length)
            elif len(repetition_ids) != expected_repetition_id_length:
                raise ValueError(
                    f'Expected repetition_ids={repetition_ids} length to be '
                    f'{expected_repetition_id_length}'
                )

        # If either self.repetition_ids or repetitions is None, it returns the other unchanged.
        repetition_ids = _full_join_string_lists(repetition_ids, self.repetition_ids)

        # The eventual number of repetitions of the returned CircuitOperation.
        final_repetitions = protocols.mul(self.repetitions, repetitions)
        return self.replace(repetitions=final_repetitions, repetition_ids=repetition_ids)

    def __pow__(self, power: IntParam) -> 'cirq.CircuitOperation':
        return self.repeat(power)

    def _with_key_path_(self, path: Tuple[str, ...]):
        return dataclasses.replace(self, parent_path=path)

    def _with_key_path_prefix_(self, prefix: Tuple[str, ...]):
        return dataclasses.replace(self, parent_path=prefix + self.parent_path)

    def _with_rescoped_keys_(
        self, path: Tuple[str, ...], bindable_keys: FrozenSet['cirq.MeasurementKey']
    ):
        # The following line prevents binding to measurement keys in previous repeated subcircuits
        # "just because their repetition ids matched". If we eventually decide to change that
        # requirement and allow binding across subcircuits (possibly conditionally upon the key or
        # the subcircuit having some 'allow_cross_circuit_binding' field set), this is the line to
        # change or remove.
        bindable_keys = frozenset(k for k in bindable_keys if len(k.path) <= len(path))
        bindable_keys |= {k.with_key_path_prefix(*path) for k in self.extern_keys}
        path += self.parent_path
        return dataclasses.replace(self, parent_path=path, extern_keys=bindable_keys)

    def with_key_path(self, path: Tuple[str, ...]):
        return self._with_key_path_(path)

    def with_repetition_ids(self, repetition_ids: List[str]) -> 'cirq.CircuitOperation':
        return self.replace(repetition_ids=repetition_ids)

    def with_qubit_mapping(
        self, qubit_map: Union[Dict['cirq.Qid', 'cirq.Qid'], Callable[['cirq.Qid'], 'cirq.Qid']]
    ) -> 'cirq.CircuitOperation':
        """Returns a copy of this operation with an updated qubit mapping.

        Users should pass either 'qubit_map' or 'transform' to this method.

        Args:
            qubit_map: A mapping of old qubits to new qubits. This map will be
                composed with any existing qubit mapping.

        Returns:
            A copy of this operation targeting qubits as indicated by qubit_map.

        Raises:
            TypeError: qubit_map was not a function or dict mapping qubits to
                qubits.
            ValueError: The new operation has a different number of qubits than
                this operation.
        """
        if callable(qubit_map):
            transform = qubit_map
        elif isinstance(qubit_map, dict):
            transform = lambda q: qubit_map.get(q, q)  # type: ignore
        else:
            raise TypeError('qubit_map must be a function or dict mapping qubits to qubits.')
        new_map = {}
        for q in self.circuit.all_qubits():
            q_new = transform(self.qubit_map.get(q, q))
            if q_new != q:
                if q_new.dimension != q.dimension:
                    raise ValueError(f'Qid dimension conflict.\nFrom qid: {q}\nTo qid: {q_new}')
                new_map[q] = q_new
        new_op = self.replace(qubit_map=new_map)
        if len(set(new_op.qubits)) != len(set(self.qubits)):
            raise ValueError(
                f'Collision in qubit map composition. Original map:\n{self.qubit_map}'
                f'\nMap after changes: {new_op.qubit_map}'
            )
        return new_op

    def with_qubits(self, *new_qubits: 'cirq.Qid') -> 'cirq.CircuitOperation':
        """Returns a copy of this operation with an updated qubit mapping.

        Args:
            *new_qubits: A list of qubits to target. Qubits in this list are
                matched to qubits in the circuit following default qubit order,
                ignoring any existing qubit map.

        Returns:
            A copy of this operation targeting `new_qubits`.

        Raises:
            ValueError: `new_qubits` has a different number of qubits than
                this operation.
        """
        expected = protocols.num_qubits(self.circuit)
        if len(new_qubits) != expected:
            raise ValueError(f'Expected {expected} qubits, got {len(new_qubits)}.')
        return self.with_qubit_mapping(dict(zip(self.qubits, new_qubits)))

    def with_measurement_key_mapping(self, key_map: Dict[str, str]) -> 'cirq.CircuitOperation':
        """Returns a copy of this operation with an updated key mapping.

        Args:
            key_map: A mapping of old measurement keys to new measurement keys.
                This map will be composed with any existing key mapping.
                The keys and values of the map should be unindexed (i.e. without
                repetition_ids).

        Returns:
            A copy of this operation with measurement keys updated as specified
                by key_map.

        Raises:
            ValueError: The new operation has a different number of measurement
                keys than this operation.
        """
        new_map = {}
        for k_obj in protocols.measurement_keys_touched(self.circuit):
            k = k_obj.name
            k_new = self.measurement_key_map.get(k, k)
            k_new = key_map.get(k_new, k_new)
            if k_new != k:
                new_map[k] = k_new
        new_op = self.replace(measurement_key_map=new_map)
        if len(protocols.measurement_keys_touched(new_op)) != len(
            protocols.measurement_keys_touched(self)
        ):
            raise ValueError(
                f'Collision in measurement key map composition. Original map:\n'
                f'{self.measurement_key_map}\nApplied changes: {key_map}'
            )
        return new_op

    def _with_measurement_key_mapping_(self, key_map: Dict[str, str]) -> 'cirq.CircuitOperation':
        return self.with_measurement_key_mapping(key_map)

    def with_params(
        self, param_values: 'cirq.ParamResolverOrSimilarType', recursive: bool = False
    ) -> 'cirq.CircuitOperation':
        """Returns a copy of this operation with an updated ParamResolver.

        Any existing parameter mappings will have their values updated given
        the provided mapping, and any new parameters will be added to the
        ParamResolver.

        Note that any resulting parameter mappings with no corresponding
        parameter in the base circuit will be omitted. These parameters do not
        apply to the `repetitions` field if that is parameterized.

        Args:
            param_values: A map or ParamResolver able to convert old param
                values to new param values. This map will be composed with any
                existing ParamResolver via single-step resolution.
            recursive: If True, resolves parameter values recursively over the
                resolver; otherwise performs a single resolution step. This
                behavior applies only to the passed-in mapping, for the current
                application. Existing parameters are never resolved recursively
                because a->b and b->a needs to be a valid mapping.

        Returns:
            A copy of this operation with its ParamResolver updated as specified
                by param_values.
        """
        new_params = {}
        for k in protocols.parameter_symbols(self.circuit):
            v = self.param_resolver.value_of(k, recursive=False)
            v = protocols.resolve_parameters(v, param_values, recursive=recursive)
            if v != k:
                new_params[k] = v
        return self.replace(param_resolver=new_params)

    def _resolve_parameters_(
        self, resolver: 'cirq.ParamResolver', recursive: bool
    ) -> 'cirq.CircuitOperation':
        resolved = self.with_params(resolver.param_dict, recursive)
        return resolved.replace(repetitions=resolver.value_of(self.repetitions, recursive))
