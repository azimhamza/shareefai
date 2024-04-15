from pydantic import BaseModel, Field
from typing import Callable, Dict, Union, Any, Optional
import json


# Dummy Language Learning Model for demonstration
class LLMSetup:
    @staticmethod
    def generate_prompt(prompt: str, pre_context: Optional[str] = None) -> str:
        return f"Answer the following for prompt: {prompt}. Pre-context: {pre_context}"


def to_json(data: Dict) -> str:
    return json.dumps(data)


def to_upper(data: Dict) -> Dict:
    return {
        key.upper(): value.upper() if isinstance(value, str) else value
        for key, value in data.items()
    }


# Mapping of string callbacks to function
callback_mapping = {
    "to_json": to_json,
    "to_upper": to_upper,
}


# Pydantic Model for Chain without template
class SimpleChain(BaseModel):
    """
    Pydantic Model for Simple Chain
    """

    prompt: str
    callback: Optional[Union[Callable[[Dict], Any], str]] = "to_json"
    memory: Optional[str] = None


# Function to execute a simple chain
def execute_simple_chain(simple_chain: SimpleChain) -> Any:
    """
    Execute a simple chain
    :param simple_chain:
    :return:
    """
    agent = LLMSetup()
    generated_code = agent.generate_prompt(simple_chain.prompt, simple_chain.memory)

    output = {
        "prompt": simple_chain.prompt,
        "generated_code": generated_code,
    }

    callback = simple_chain.callback
    if isinstance(callback, str):
        callback = callback_mapping.get(callback, to_json)

    if callback:
        output = callback(output)

    return output


# Examples:


"""
# Example 1: With Memory (pre-context) and a string-based callback to convert to upper case
chain1 = SimpleChain(prompt="Hello World", callback="to_upper", memory="Memory: User says Hi!")
result1 = execute_simple_chain(chain1)
print(f"Example 1 - With Memory: {result1}")

# Example 2: Without Memory
chain2 = SimpleChain(prompt="Hello World")
result2 = execute_simple_chain(chain2)
print(f"Example 2 - Without Memory: {result2}")
"""
