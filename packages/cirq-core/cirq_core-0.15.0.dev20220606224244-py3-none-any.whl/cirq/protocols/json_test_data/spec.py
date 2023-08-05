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

import pathlib

import cirq
from cirq.json_resolver_cache import _class_resolver_dictionary
from cirq.testing.json import ModuleJsonTestSpec

TestSpec = ModuleJsonTestSpec(
    name="cirq",
    packages=[cirq, cirq.work],
    test_data_path=pathlib.Path(__file__).parent,
    resolver_cache=_class_resolver_dictionary(),
    not_yet_serializable=[
        'Alignment',
        'AxisAngleDecomposition',
        'CircuitDag',
        'CircuitDiagramInfo',
        'CircuitDiagramInfoArgs',
        'CircuitSampleJob',
        'CliffordSimulatorStepResult',
        'CliffordTrialResult',
        'DensityMatrixSimulator',
        'DensityMatrixSimulatorState',
        'DensityMatrixStepResult',
        'DensityMatrixTrialResult',
        'ExpressionMap',
        'InsertStrategy',
        'IonDevice',
        'KakDecomposition',
        'LinearCombinationOfGates',
        'LinearCombinationOfOperations',
        'Linspace',
        'ListSweep',
        'NeutralAtomDevice',
        'PauliSumCollector',
        'PauliSumExponential',
        'PauliTransform',
        'PeriodicValue',
        'PointOptimizationSummary',
        'Points',
        'Product',
        'QasmArgs',
        'QasmOutput',
        'QuantumState',
        'QubitOrder',
        'QuilFormatter',
        'QuilOutput',
        'SimulationTrialResult',
        'SimulationTrialResultBase',
        'SparseSimulatorStep',
        'StateVectorMixin',
        'TextDiagramDrawer',
        'Timestamp',
        'TwoQubitGateTabulationResult',
        'UnitSweep',
        'StateVectorSimulatorState',
        'StateVectorTrialResult',
        'ZerosSampler',
        'Zip',
    ],
    should_not_be_serialized=[
        # Heatmaps
        'Heatmap',
        'TwoQubitInteractionHeatmap',
        # Intermediate states with work buffers and unknown external prng guts.
        'ActOnArgs',
        'ActOnArgsContainer',
        'ActOnCliffordTableauArgs',
        'ActOnDensityMatrixArgs',
        'ActOnStabilizerArgs',
        'ActOnStabilizerCHFormArgs',
        'ActOnStateVectorArgs',
        'ApplyChannelArgs',
        'ApplyMixtureArgs',
        'ApplyUnitaryArgs',
        'CliffordTableauSimulationState',
        'DensityMatrixSimulationState',
        'OperationTarget',
        'SimulationProductState',
        'SimulationState',
        'SimulationStateBase',
        'StabilizerChFormSimulationState',
        'StabilizerSimulationState',
        'StateVectorSimulationState',
        # Abstract base class for creating compilation targets.
        'CompilationTargetGateset',
        'TwoQubitCompilationTargetGateset',
        # Circuit optimizers are function-like. Only attributes
        # are ignore_failures, tolerance, and other feature flags
        'AlignLeft',
        'AlignRight',
        'ConvertToCzAndSingleGates',
        'ConvertToIonGates',
        'ConvertToNeutralAtomGates',
        'DropEmptyMoments',
        'DropNegligible',
        'EjectPhasedPaulis',
        'EjectZ',
        'ExpandComposite',
        'MEASUREMENT_KEY_SEPARATOR',
        'MergeInteractions',
        'MergeInteractionsToSqrtIswap',
        'MergeSingleQubitGates',
        'PointOptimizer',
        'SynchronizeTerminalMeasurements',
        # Transformers
        'TransformerLogger',
        'TransformerContext',
        # global objects
        'CONTROL_TAG',
        'PAULI_BASIS',
        'PAULI_STATES',
        # abstract, but not inspect.isabstract():
        'Device',
        'InterchangeableQubitsGate',
        'Pauli',
        'SingleQubitGate',
        'ABCMetaImplementAnyOneOf',
        'SimulatesAmplitudes',
        'SimulatesExpectationValues',
        'SimulatesFinalState',
        'StateVectorStepResult',
        'StepResultBase',
        'NamedTopology',
        # protocols:
        'HasJSONNamespace',
        'SupportsActOn',
        'SupportsActOnQubits',
        'SupportsApplyChannel',
        'SupportsApplyMixture',
        'SupportsApproximateEquality',
        'SupportsCircuitDiagramInfo',
        'SupportsCommutes',
        'SupportsConsistentApplyUnitary',
        'SupportsControlKey',
        'SupportsDecompose',
        'SupportsDecomposeWithQubits',
        'SupportsEqualUpToGlobalPhase',
        'SupportsExplicitHasUnitary',
        'SupportsExplicitNumQubits',
        'SupportsExplicitQidShape',
        'SupportsJSON',
        'SupportsKraus',
        'SupportsMeasurementKey',
        'SupportsMixture',
        'SupportsParameterization',
        'SupportsPauliExpansion',
        'SupportsPhase',
        'SupportsQasm',
        'SupportsQasmWithArgs',
        'SupportsQasmWithArgsAndQubits',
        'SupportsTraceDistanceBound',
        'SupportsUnitary',
        # mypy types:
        'CIRCUIT_LIKE',
        'DURATION_LIKE',
        'JsonResolver',
        'LabelEntity',
        'NOISE_MODEL_LIKE',
        'OP_TREE',
        'PAULI_GATE_LIKE',
        'PAULI_STRING_LIKE',
        'ParamResolverOrSimilarType',
        'PauliSumLike',
        'QUANTUM_STATE_LIKE',
        'QubitOrderOrList',
        'RANDOM_STATE_OR_SEED_LIKE',
        'STATE_VECTOR_LIKE',
        'Sweepable',
        'TParamKey',
        'TParamVal',
        'TParamValComplex',
        'TRANSFORMER',
        'ParamDictType',
        # utility:
        'CliffordSimulator',
        'NoiseModelFromNoiseProperties',
        'Simulator',
        'StabilizerSampler',
        'Unique',
        'DEFAULT_RESOLVERS',
    ],
    deprecated={
        'GlobalPhaseOperation': 'v0.16',
        'CrossEntropyResult': 'v0.16',
        'CrossEntropyResultDict': 'v0.16',
    },
    tested_elsewhere=[
        # SerializableByKey does not follow common serialization rules.
        # It is tested separately in test_context_serialization.
        'SerializableByKey'
    ],
)
