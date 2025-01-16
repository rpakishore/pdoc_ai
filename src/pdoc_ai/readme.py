from pdoc_ai.ingester import generate_context
from pdoc_ai.llm import LLM, BaseModel
from pydantic import Field
from pathlib import Path


def update_readme(
    package: Path,
    readme: Path,
    include_patterns: list[str] = [],
    exclude_patterns: list[str] = [],
    llm_baseurl: str = "http://100.99.54.84:11434/v1",
    llm_key: str = "ollama",
    llm_model: str = "code_assist_large",
    **kwargs,
) -> None:
    """Update the README file with generated content based on the package structure.

    Args:
        package (Path): The path to the package directory.
        readme (Path): The path to the README file to be updated.
        include_patterns (list[str], optional): Patterns for files to include. Defaults to [].
        exclude_patterns (list[str], optional): Patterns for files to exclude. Defaults to [].
        llm_baseurl (str, optional): The base URL for the LLM service. Defaults to "http://100.99.54.84:11434/v1".
        llm_key (str, optional): The key for the LLM service. Defaults to "ollama".
        llm_model (str, optional): The model to use for the LLM service. Defaults to "code_assist_large".
        **kwargs: Additional keyword arguments.
    """

    with open(readme, "r") as f:
        content = f.read()

    class Readme(BaseModel):
        title: str = Field(description="Title for the python package")
        description: str = Field(
            description="Brief description of the package under 20 tokens"
        )
        features: list[str] = Field(
            description="List of features of the package  in markdown format"
        )
        usage: str = Field(
            description="A description of how to use the package, including examples"
        )

    llm = LLM(base_url=llm_baseurl, model=llm_model, key=llm_key)

    llm.SYSTEM = """You are a helpful coding assistant.
    """
    resp = llm.structured_response(
        messages=llm.msg(
            user_content=f"""You are given a python project layout and contents below. 
    Using this information You are tasked with creating generating contents for README.md file.
    The information presented should be useful for anyone who wants to use the package.
    {generate_context(package=package, include_patterns=include_patterns, exclude_patterns=exclude_patterns)}
    """
        ),
        response_model=Readme,
    )

    content = content.replace("{title}", resp.title)
    content = content.replace("{description}", resp.description)
    content = content.replace("{features}", "\n".join(resp.features))
    content = content.replace("{usage}", resp.usage)

    with open(readme, "w") as f:
        f.write(content)
