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


from functools import partial

import structlog
from beartype.typing import Mapping, Sequence

from qyver.framework.common.dag.context import ExecutionContext
from qyver.framework.common.dag.dag import Dag
from qyver.framework.common.data_types import Vector
from qyver.framework.compiler.query.query_dag_compiler import QueryDagCompiler
from qyver.framework.query.query_node_input import QueryNodeInput

logger = structlog.get_logger()


class QueryDagEvaluator:
    def __init__(self, dag: Dag) -> None:
        self._dag = dag
        self._query_dag = QueryDagCompiler().compile_dag(dag)
        logger.info(
            "initialized entity dag",
            node_ids=[node.node_id for node in self._dag.nodes],
            node_types=[node.class_name for node in self._dag.nodes],
        )

    def evaluate(
        self,
        inputs: Mapping[str, Sequence[QueryNodeInput]],
        context: ExecutionContext,
    ) -> Vector:
        result = self._query_dag.evaluate(inputs, context)
        logger.info(
            "evaluated query",
            pii_inputs=inputs,
            pii_vector=partial(str, result),
        )
        return result
