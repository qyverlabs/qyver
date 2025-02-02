# Copyright 2024 qyver, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

from abc import ABC, abstractmethod

from beartype.typing import Generic, Sequence
from typing_extensions import override

from qyver.framework.common.dag.context import ExecutionContext
from qyver.framework.common.dag.node import NT, NodeDataT
from qyver.framework.common.parser.parsed_schema import ParsedSchema
from qyver.framework.online.dag.batched_chunk_input_item import (
    BatchedChunkInputItem,
)
from qyver.framework.online.dag.evaluation_result import (
    EvaluationResult,
    SingleEvaluationResult,
)
from qyver.framework.online.dag.online_node import OnlineNode
from qyver.framework.online.dag.parent_results import ParentResults


class DefaultOnlineNode(OnlineNode[NT, NodeDataT], ABC, Generic[NT, NodeDataT]):
    @override
    def evaluate_self(
        self,
        parsed_schemas: Sequence[ParsedSchema],
        context: ExecutionContext,
    ) -> list[EvaluationResult[NodeDataT] | None]:
        batch_size = len(parsed_schemas)
        if batch_size == 0:
            return []

        parent_results = self.evaluate_parents(self.parents, parsed_schemas, context)
        main_inputs: list[ParentResults] = [
            {node: result.main for node, result in parent_result.items()} for parent_result in parent_results
        ]

        mains: list[SingleEvaluationResult] = self._get_single_evaluation_results(
            self._evaluate_single_with_fallback(parsed_schemas, context, main_inputs)
        )
        chunk_results_per_parsed_schema: list[list[NodeDataT]] = self.__get_chunk_results_per_parsed_schema(
            parsed_schemas, context, parent_results
        )
        return [
            EvaluationResult(
                mains[i],
                [
                    self._get_single_evaluation_result(chunk_result)
                    for chunk_result in chunk_results_per_parsed_schema[i]
                ],
            )
            for i in range(batch_size)
        ]

    def __get_chunk_results_per_parsed_schema(
        self,
        parsed_schemas: Sequence[ParsedSchema],
        context: ExecutionContext,
        parent_results: Sequence[dict[OnlineNode, EvaluationResult]],
    ) -> list[list[NodeDataT]]:
        batch_size = len(parsed_schemas)
        chunked_parent_results = self.__filter_chunked_parent_results(parent_results)
        chunk_inputs_per_parsed_schema: list[list[ParentResults]] = [
            [
                self.__get_chunk_input(parent_results[i], chunked_parent, chunked_result)
                for chunked_parent, chunked_results in chunked_parent_results[i].items()
                for chunked_result in chunked_results.chunks
            ]
            for i in range(batch_size)
        ]
        chunks_per_parsed_schema: list[list[NodeDataT]] = [[] for i in range(batch_size)]
        for batched_inputs in self.__batch_chunk_inputs_by_size(chunk_inputs_per_parsed_schema, batch_size):
            chunked_batched_parent_results: list[ParentResults] = [
                batched_input.input_ for batched_input in batched_inputs
            ]
            batch_results = self._evaluate_single_with_fallback(parsed_schemas, context, chunked_batched_parent_results)

            for batched_input, batch_result in zip(batched_inputs, batch_results):
                chunks_per_parsed_schema[batched_input.parsed_schema_index].append(batch_result)
        return chunks_per_parsed_schema

    def __batch_chunk_inputs_by_size(
        self,
        inputs_per_parsed_schema: Sequence[Sequence[ParentResults]],
        batch_size: int,
    ) -> list[list[BatchedChunkInputItem]]:
        result: list[list[BatchedChunkInputItem]] = []
        counter = 0
        current_batch: list[BatchedChunkInputItem] = []
        for i, inputs in enumerate(inputs_per_parsed_schema):
            for input_ in inputs:
                counter += 1
                current_batch.append(BatchedChunkInputItem(i, input_))
                if counter % batch_size == 0:
                    result.append(current_batch)
                    current_batch = []
        if current_batch:
            result.append(current_batch)
        return result

    def _get_single_evaluation_results(self, values: Sequence[NodeDataT]) -> list[SingleEvaluationResult[NodeDataT]]:
        return [self._get_single_evaluation_result(value) for value in values]

    def __filter_chunked_parent_results(
        self,
        parent_results: Sequence[dict[OnlineNode, EvaluationResult]],
    ) -> list[dict[OnlineNode, EvaluationResult]]:
        return [
            {parent: result for parent, result in parent_result_dict.items() if result.chunks}
            for parent_result_dict in parent_results
        ]

    def __get_chunk_input(
        self,
        parent_results: dict[OnlineNode, EvaluationResult],
        chunked_parent: OnlineNode,
        chunked_result: SingleEvaluationResult,
    ) -> ParentResults:
        input_parent_results = {
            parent: result.main for parent, result in parent_results.items() if parent.node_id != chunked_parent.node_id
        }
        input_parent_results[chunked_parent] = chunked_result
        return input_parent_results

    def _evaluate_single_with_fallback(
        self,
        parsed_schemas: Sequence[ParsedSchema],
        context: ExecutionContext,
        parent_results: Sequence[ParentResults],
    ) -> list[NodeDataT]:
        single_result_all = self._evaluate_singles(parent_results, context)
        return [
            (single_result if single_result is not None else self.get_fallback_result(parsed_schemas[i]))
            for i, single_result in enumerate(single_result_all)
        ]

    @abstractmethod
    def _evaluate_singles(
        self,
        parent_results: Sequence[ParentResults],
        context: ExecutionContext,
    ) -> Sequence[NodeDataT | None]:
        pass

    def get_fallback_result(
        self,
        parsed_schema: ParsedSchema,
    ) -> NodeDataT:
        return self.load_stored_result_or_raise_exception(parsed_schema)
