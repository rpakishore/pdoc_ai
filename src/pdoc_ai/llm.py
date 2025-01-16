"""
LLM class for interacting with language models.
"""

from functools import cached_property
from pathlib import Path
from typing import Type, TypeVar

import instructor
from ollama import Client
from openai import OpenAI
from openai.types.chat import ChatCompletion
from pydantic import BaseModel

_StructuredOutput = TypeVar("_StructuredOutput", bound=BaseModel)


class LLM:
    last_completion = {"prompt": 0, "completion": 0}
    SYSTEM: str = "You are a helpful assistant."

    def __init__(
        self,
        base_url: str = "http://100.99.54.84:11434/v1",
        model: str = "general_small",
        key: str = "ollama",
        **kwargs,
    ) -> None:
        """
        Initialize the LLM class with specified parameters.

        Args:
            base_url (str): The base URL for the language model API.
            model (str): The name of the language model to use.
            key (str): The API key to authenticate with.
            **kwargs: Additional keyword arguments to pass to OpenAI or Ollama clients.
        """
        try:

            self.__api_base = base_url
            self.__model = model
            self.__openai = OpenAI(
                base_url=self.__api_base,
                api_key=key,
                **kwargs,
            )
            self.__instructor = instructor.from_openai(
                self.__openai, mode=instructor.Mode.JSON
            )

            _host = "//".join(Path(self.__api_base).parts[:2])
            if _host.casefold() == "https://api.openai.com":
                self.__ollama = None
            else:
                self.__ollama = Client(host=_host)

        except Exception as e:
            print(f"Exception in `LLM.__init__({kwargs=})`\n{e}")
            raise e

    def response(
        self, messages: list[dict[str]], model: str | None = None, **kwargs
    ) -> str:
        """Get ChatCompletions text from LLM

        Args:
            messages (list[dict[str]]): Input messages
            model (str | None, optional): Name of Model or `None`. Defaults to None.

        Returns:
            str: Response content
        """
        _inputs = {
            "model": model or self.__model,
            "messages": messages,
            "stream": False,
            "temperature": 0,
        }
        for k, v in kwargs.items():
            _inputs[k] = v

        try:
            response = self.__openai.chat.completions.create(**_inputs)

            if _inputs["stream"]:
                res_text = ""
                for chunk in response:
                    res_text += chunk.choices[0].delta.content or ""
            else:
                res_text = response.choices[0].message.content
                self.__update_token_usage(response=response)
            return res_text
        except Exception as e:
            print(f"Error encountered in `LLM.response({_inputs=})`")
            print(str(e))
            raise e

    def structured_response(
        self,
        messages: list[dict[str]],
        response_model: Type[_StructuredOutput],
        model: str | None = None,
    ) -> _StructuredOutput:
        """Chat with LLM to get structured response

        Args:
            messages (list[dict[str]]): `system`, `user` and `assistant`(optional) messages to pass to LLM
            response_model (Type[_StructuredOutput]): Pydantic model for validation
            model (str | None, optional): Name of model. Defaults to model defined in config.toml.

        Returns:
            _StructuredOutput: Instance of `response_model`.
        """

        messages[-1]["content"] += ". return as JSON."
        _inputs = {
            "model": model or self.__model,
            "messages": messages,
            "response_model": response_model,
            "temperature": 0,
        }
        try:
            return self.__instructor.chat.completions.create(**_inputs)
        except Exception as e:
            print(f"Exception in `LLM.structured_response({_inputs=})`\n{e}")
            raise e

    @cached_property
    def models(self) -> list[str]:
        """
        Get a list of available models from the language model API.

        Returns:
            list[str]: A list of model names.
        """
        try:
            return [x.id for x in self.__openai.models.list().data]
        except Exception as e:
            print("Exception in `LLM.models`\n{e}")
            raise e

    def __update_token_usage(self, response: ChatCompletion):
        """
        Update the token usage statistics for the last completion.

        Args:
            response (ChatCompletion): The response from the language model containing token usage information.
        """
        self.last_completion = {
            "prompt": response.usage.completion_tokens,
            "completion": response.usage.prompt_tokens,
        }

    def msg(self, user_content: str) -> list[dict[str]]:
        """
        Create a message structure for the language model.

        Args:
            user_content (str): The content of the user's message.

        Returns:
            list[dict[str]]: A structured message list ready to be sent to the language model.
        """
        return [
            {"role": "system", "content": self.SYSTEM},
            {"role": "user", "content": user_content},
        ]

    def unload_all(self) -> None:
        """
        Unload all models from the language model API to free up resources.
        """
        for model in self.loaded_models:
            self.__ollama.chat(
                model=model, messages=[{"role": "user", "content": ""}], keep_alive=0
            )
        return

    @property
    def loaded_models(self) -> list[str]:
        """
        Get a list of currently loaded models in the language model API.

        Returns:
            list[str]: A list of model names.
        """
        if self.__ollama is not None:
            return [modelinfo.model for modelinfo in self.__ollama.ps().models]
        return []

    def __str__(self) -> str:
        return f"LLM(api_base={self.__api_base}, model={self.__model})"
