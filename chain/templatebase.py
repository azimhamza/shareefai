from pydantic import BaseModel, Field
from typing import List, Callable, Dict, Union, Any, Optional
import json

from chain.simplebase import LLMSetup, callback_mapping, to_json


# Dummy Language Learning Model for demonstration


# Pydantic Model for Template Chain
class TemplateChain(BaseModel):
    template_prompt: str
    inputs: List[str]
    callback: Optional[Union[Callable[[Dict], Any], str]] = "to_json"
    memory: Optional[str] = None


# Function to execute a chain
def execute_chain(template_chain: TemplateChain) -> Any:
    """
    Execute a chain
    :param template_chain:
    :return:
    """
    try:
        built_prompt = template_chain.template_prompt.format(*template_chain.inputs)
    except IndexError:
        return {"error": "Mismatch between placeholders and inputs."}

    agent = LLMSetup()
    generated_code = agent.generate_prompt(built_prompt, template_chain.memory)

    output = {
        "built_prompt": built_prompt,
        "generated_code": generated_code,
    }

    callback = template_chain.callback
    if isinstance(callback, str):
        callback = callback_mapping.get(callback, to_json)

    if callback:
        output = callback(output)

    return output


# Examples:
"""
# Example 1: With Memory (memory) and Context, and a string-based callback to convert to upper case
chain1 = TemplateChain(template_prompt="Hello {0}", inputs=["World"], callback="to_upper",
                       pre-context="Memory: User says Hi!")
result1 = execute_chain(chain1)
print(f"Example 1 - With Memory and Context: {result1}")

# Example 2: Without Memory but With Context
chain2 = TemplateChain(template_prompt="Hello {0}", inputs=["World"])
result2 = execute_chain(chain2)
print(f"Example 2 - Without Memory but With Context: {result2}")
"""
