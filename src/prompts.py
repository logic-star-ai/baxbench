import logging
import os
import pathlib
import random
import re
import time
import traceback
from enum import Enum
from typing import Any, cast
from venv import logger

from anthropic import Anthropic
from anthropic.types import TextBlock
from openai import NOT_GIVEN, OpenAI, api_key
from openai.types.chat import ChatCompletionMessageParam

from env.base import Env
from scenarios.base import Scenario

_SYSTEM_PROMPT = "You are an experienced full-stack developer"


class KeyLocs(Enum):
    openai_key = "OPENAI_API_KEY"
    anthropic_key = "ANTHROPIC_API_KEY"
    together_key = "TOGETHER_API_KEY"
    openrouter_key = "OPENROUTER_API_KEY"


class Prompter:

    # NOTE: unused because Together expects you to set
    # max_tokens=context_length-numTokens(prompt)
    # so we hardcode below for now
    openai_together_context_lengths = {
        "mistralai/Mixtral-8x22B-Instruct-v0.1": 65536,
        "meta-llama/Llama-3.3-70B-Instruct-Turbo": 131072,
        "deepseek-ai/DeepSeek-V3": 131072,
        "Qwen/Qwen2.5-Coder-32B-Instruct": 32768,
        "Qwen/Qwen2.5-72B-Instruct-Turbo": 32768,
        "Qwen/Qwen2.5-7B-Instruct-Turbo": 32768,
        "gpt-4o": 128000,
        "o1": 200000,
        "o1-mini": 128000,
        "o3-mini": 200000,
        "deepseek-ai/DeepSeek-R1": 164000,
    }

    openai_max_completion_tokens = {
        "gpt-4o": 16384,
        "o1": 100000,
        "o1-mini": 65536,
        "o3-mini": 100000,
    }

    openrouter_remap = {
        "meta-llama/Llama-3.3-70B-Instruct-Turbo": "meta-llama/llama-3.3-70b-instruct",
        "deepseek-ai/DeepSeek-V3": "deepseek/deepseek-chat",
        "Qwen/Qwen2.5-Coder-32B-Instruct": "qwen/qwen-2.5-coder-32b-instruct",
        "Qwen/Qwen2.5-7B-Instruct-Turbo": "qwen/qwen-2.5-7b-instruct",
        "Qwen/Qwen2.5-72B-Instruct-Turbo": "qwen/qwen-2.5-72b-instruct",
    }

    def __init__(
        self,
        env: Env,
        scenario: Scenario,
        model: str,
        spec_type: str,
        safety_prompt: str,
        batch_size: int,
        temperature: float,
        reasoning_effort: str,
        openrouter: bool,
    ):
        self.env = env
        self.scenario = scenario
        self.spec_type = spec_type
        self.safety_prompt = safety_prompt
        self.model = model
        self.batch_size = batch_size
        self.temperature = temperature
        self.reasoning_effort = reasoning_effort

        self.system_prompt = _SYSTEM_PROMPT
        self.o1_o3 = model.startswith("o1") or model.startswith("o3")
        self.anthropic = "claude" in model
        self.openai = self.o1_o3 or self.model.startswith("gpt")
        self.openrouter = openrouter and not (self.anthropic or self.openai)

        self.prompt = self.scenario.build_prompt(
            self.env, self.spec_type, self.safety_prompt
        )

    def prompt_anthropic(self, logger: logging.Logger) -> list[str]:
        client = Anthropic(api_key=os.environ[KeyLocs.anthropic_key.value])
        try:
            response = client.messages.create(
                model=self.model,
                system=self.system_prompt,
                messages=[
                    {"role": "user", "content": self.prompt},
                ],
                temperature=self.temperature,
                max_tokens=8192 if "claude-3-5-" in self.model else 4096,
            )
            assert isinstance(response.content[0], TextBlock)
            if response.usage is not None:
                logger.info(
                    f"Token stats: {response.usage}; around {response.usage.output_tokens} completion tokens per completion"
                )
            if response.stop_reason == "max_tokens":
                logger.warning(f"Completion was cut off due to length.")
            return [response.content[0].text]
        except Exception as e:
            raise e

    def prompt_openrouter(self, logger: logging.Logger) -> list[str]:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ[KeyLocs.openrouter_key.value],
        )
        if self.model in self.openrouter_remap:
            open_router_model = self.openrouter_remap[self.model]
        else:
            open_router_model = self.model
        try:
            response = client.chat.completions.create(
                model=open_router_model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": self.prompt},
                ],
                n=1,
                temperature=self.temperature,
                max_tokens=(
                    8192
                    if self.model not in Prompter.openai_together_context_lengths
                    else Prompter.openai_together_context_lengths[self.model] - 2000
                ),
            )
            if response.choices is None:
                logger.error(f"Response was None: {response}")
                raise Exception("No content")
            content = response.choices[0].message.content
            if content is not None and len(content) > 0:
                if response.usage is not None:
                    logger.info(
                        f"Token stats: {response.usage}; around {response.usage.completion_tokens} completion tokens per completion"
                    )
                else:
                    logger.info(f"Token stats unavailable")
                if response.choices[0].finish_reason == "length":
                    logger.warning(f"Completion was cut off due to length.")
                try:
                    logger.info(f"Inference provided by: {response.provider}")  # type: ignore
                    logger.info(f"Inference id: {response.id}")
                except:
                    pass
                return [content]
            else:
                raise Exception("No content")
        except Exception as e:
            raise e

    def prompt_openai_together_batch(self, logger: logging.Logger) -> list[str]:
        if self.openai:
            client = OpenAI(api_key=os.environ[KeyLocs.openai_key.value])
        else:
            client = OpenAI(
                api_key=os.environ[KeyLocs.together_key.value],
                base_url="https://api.together.xyz/v1",
            )
        try:
            # Prepare extra kwargs
            extra_kwargs: dict[str, Any] = {}
            if self.model == "o1" or self.model.startswith(
                "o3"
            ):  # NOTE: o1-mini does not have this
                extra_kwargs["reasoning_effort"] = self.reasoning_effort
            if self.openai:
                extra_kwargs["max_completion_tokens"] = (
                    Prompter.openai_max_completion_tokens[self.model]
                )
            else:
                extra_kwargs["max_tokens"] = (
                    8192
                    if self.model not in Prompter.openai_together_context_lengths
                    else Prompter.openai_together_context_lengths[self.model] - 2000
                )
            # Prepare the message
            messages: list[Any] = []
            if self.model == "o1" or self.model.startswith("o3"):
                messages.append(
                    cast(
                        ChatCompletionMessageParam,
                        {"role": "developer", "content": self.system_prompt},
                    )
                )
            elif self.model == "o1-mini":
                # No sysprompt
                pass
            else:
                messages.append(
                    cast(
                        ChatCompletionMessageParam,
                        {"role": "system", "content": self.system_prompt},
                    )
                )
            messages.append({"role": "user", "content": self.prompt})

            # Query
            completions = client.chat.completions.create(
                model=self.model,
                messages=messages,
                n=self.batch_size,
                temperature=self.temperature if not self.o1_o3 else NOT_GIVEN,
                **extra_kwargs,
            )
            if completions.usage is not None:
                logger.info(
                    f"Batch token stats: {completions.usage}; around {completions.usage.completion_tokens / self.batch_size:.2f} completion tokens per completion"
                )
            else:
                logger.info(f"Batch token stats unavailable")
            responses = []
            for idx, choice in enumerate(completions.choices):
                if choice.finish_reason == "length":
                    logger.warning(f"Completion {idx} was cut off due to length.")
                if choice.message.content:
                    responses.append(choice.message.content)
            return responses

        except Exception as e:
            raise e

    def prompt_model(self, logger: logging.Logger) -> list[str]:
        if self.anthropic:
            return self.prompt_anthropic(logger)
        elif self.openrouter:
            return self.prompt_openrouter(logger)
        else:
            return self.prompt_openai_together_batch(logger)

    def prompt_model_batch_with_exp_backoff(
        self,
        max_retries: int,
        base_delay: float,
        max_delay: float,
        logger: logging.Logger,
    ) -> list[str]:
        # Anthropic and OpenRouter don't support batching, so we have to sample a single completion multiple times
        n_times_to_sample = self.batch_size if self.openrouter or self.anthropic else 1
        completions = []
        for _ in range(n_times_to_sample):
            retries = 0
            while True:
                try:
                    if retries > 0:
                        logger.info(f"Retrying {retries} times")
                    completion = self.prompt_model(logger)
                    completions.extend(completion)
                    break
                except Exception as e:
                    retries += 1
                    if retries > max_retries:
                        logger.error(f"Max retries reached, raising exception: {e}")
                        raise e
                    delay = min(base_delay * 2**retries, max_delay)
                    delay = random.uniform(0, delay)
                    logger.exception(
                        f"{e}, backing off for {delay} seconds", exc_info=e
                    )
                    time.sleep(delay)
        return completions


class Parser:

    def __init__(self, env: Env, logger: logging.Logger):
        self.env = env
        self.logger = logger

        self.fp_pattern = re.compile(r"<FILEPATH>(.+?)</FILEPATH>", re.DOTALL)
        self.fp_ht_pattern = re.compile(r"^###\s*(.+?)$", re.DOTALL | re.MULTILINE)
        self.md_pattern = re.compile(r"```(?!bash)\w+\n(.*?)\n```", re.DOTALL)
        self.code_pattern = re.compile(r"<CODE>(.+?)</CODE>", re.DOTALL)

    def _invalid(self, response: str) -> dict[pathlib.Path, str]:
        self.logger.warning(f"Format not found")
        return {pathlib.Path("failed"): "Format not found. Full response:\n" + response}

    def _parse_md(self, response: str) -> list[str]:
        return [s.strip() for s in self.md_pattern.findall(response)]

    def _parse_code(self, response: str) -> list[str]:
        return [s.strip() for s in self.code_pattern.findall(response)]

    def _parse_multi_file_response(self, response: str) -> dict[pathlib.Path, str]:
        normal_file_paths = [
            pathlib.Path(s.strip()) for s in self.fp_pattern.findall(response)
        ]
        # NOTE: asserts that these patterns 1) are not mixed with normal filepaths 2) are not mixed with titles
        ht_file_paths = [
            pathlib.Path(s.strip()) for s in self.fp_ht_pattern.findall(response)
        ]
        for file_paths in (
            normal_file_paths,
            ht_file_paths,
        ):
            code_snippets_md = self._parse_md(response)
            code_snippets_code = self._parse_code(response)
            self.logger.info(f"Trying MD parsing")
            if len(file_paths) == len(code_snippets_md) and len(file_paths) > 0:
                return {fp: c for fp, c in zip(file_paths, code_snippets_md)}
            elif len(file_paths) == len(code_snippets_code) and len(file_paths) > 0:
                self.logger.warning(f"MD format not found, trying CODE format")
                # failsave code parsing in case some of them have md and some not
                codes = []
                for code in code_snippets_code:
                    md_parsed = self._parse_md(code)
                    if len(md_parsed) > 0:
                        codes.append(md_parsed[0])
                    else:
                        codes.append(code)
                assert len(codes) == len(code_snippets_code)
                return {fp: c for fp, c in zip(file_paths, codes)}
        self.logger.warning(
            f"Both formats failed, lengths are: files {len(file_paths)}, md {len(code_snippets_md)}, code {len(code_snippets_code)}"
        )
        return self._invalid(response)

    def _parse_single_file_response(self, response: str) -> dict[pathlib.Path, str]:
        assert self.env.code_filename is not None
        code_snippets_md = self._parse_md(response)
        code_snippets_code = self._parse_code(response)
        self.logger.info(f"Trying MD parsing")
        if len(code_snippets_md) > 0:
            return {pathlib.Path(self.env.code_filename): code_snippets_md[0]}
        elif len(code_snippets_code) > 0:
            self.logger.warning(f"MD format not found, trying CODE format")
            return {pathlib.Path(self.env.code_filename): code_snippets_code[0]}
        else:
            self.logger.warning(f"Both formats failed")
            return self._invalid(response)

    def parse_response(self, response: str) -> dict[pathlib.Path, str]:
        if self.env.is_multi_file:
            return self._parse_multi_file_response(response)
        else:
            return self._parse_single_file_response(response)
