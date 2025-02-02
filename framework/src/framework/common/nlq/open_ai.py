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

import os
import sys
import threading
from contextlib import contextmanager
from dataclasses import dataclass

import instructor
from beartype.typing import Any, Generator
from openai import OpenAI
from pydantic import BaseModel

TEMPERATURE_VALUE: float = 0.0


@dataclass
class OpenAIClientConfig:
    api_key: str
    model: str


@contextmanager
def suppress_tokenizer_warnings() -> Generator[None, Any, None]:
    """
    https://github.com/huggingface/tokenizers/blob/14a07b06e4a8bd8f80d884419ae4630f5a3d8098/bindings/python/src/lib.rs
    This function is necessary because the `tokenizers` library from Hugging Face, which is written in Rust,
    can emit warnings when the current process is forked. This can be common in multiprocessing environments.
    These warnings can clutter the stderr output and are often not useful for end users. Redirecting stderr
    to a pipe and filtering out specific messages is an effective way to handle these warnings.
    """
    msgs_to_filter = [
        "huggingface/tokenizers: The current process just got forked",
        "To disable this warning, you can either:",
        "Avoid using `tokenizers` before the fork if possible",
        "Explicitly set the environment variable TOKENIZERS_PARALLELISM=(true | false)",
    ]
    read_fd, write_fd = os.pipe()
    old_stderr_fd = os.dup(2)
    os.dup2(write_fd, 2)
    os.close(write_fd)

    def filter_stderr() -> None:
        with os.fdopen(read_fd) as f:
            for line in f:
                if not any(msg in line for msg in msgs_to_filter) and sys.__stderr__ is not None:
                    sys.__stderr__.write(line)

    thread = threading.Thread(target=filter_stderr)
    thread.start()
    try:
        yield
    finally:
        os.dup2(old_stderr_fd, 2)
        thread.join()
        os.close(old_stderr_fd)


class OpenAIClient:
    def __init__(self, config: OpenAIClientConfig) -> None:
        super().__init__()
        open_ai = OpenAI(api_key=config.api_key)
        self._client = instructor.from_openai(open_ai)
        self._openai_model = config.model

    def query(self, prompt: str, instructor_prompt: str, response_model: type[BaseModel]) -> dict[str, Any]:
        with suppress_tokenizer_warnings():
            response: BaseModel = self._client.chat.completions.create(
                model=self._openai_model,
                response_model=response_model,
                max_retries=3,
                messages=[
                    {"role": "system", "content": instructor_prompt},
                    {"role": "user", "content": prompt},
                ],
                temperature=TEMPERATURE_VALUE,
            )
        return response.model_dump()
