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

import structlog
from beartype.typing import cast

from qyver.framework.common.settings import Settings
from qyver.framework.common.util.class_helper import ClassHelper
from qyver.framework.queue.interface.queue import Queue
from qyver.framework.queue.interface.queue_message import MessageBody, PayloadT

logger = structlog.getLogger()


class QueueFactory:
    @staticmethod
    def create_queue(_: type[PayloadT]) -> Queue[MessageBody[PayloadT]] | None:
        module_path = Settings().QUEUE_MODULE_PATH
        class_name = Settings().QUEUE_CLASS_NAME
        if module_path is None or class_name is None:
            return None
        queue_class = ClassHelper.get_class(module_path, class_name)
        if queue_class is None:
            logger.warning(
                "couldn't find queue implementation",
                module_path=module_path,
                class_name=class_name,
            )
            return None
        args = Settings().QUEUE_CLASS_ARGS or {}
        initialized_class = queue_class(**args)
        logger.info(
            "initialized queue",
            module_path=module_path,
            class_name=class_name,
            args=args,
        )
        return cast(Queue[MessageBody[PayloadT]], initialized_class)
