from typing import Dict, Callable, Any


class DynamicAgent:
    """
    Dynamic Agent class to represent an agent that can be dynamically loaded
    """

    def __init__(
        self,
        name: str,
        description: str,
        input_type: str,
        functions: Dict[str, Callable[..., Any]],
    ):
        self.name = name
        self.description = description
        self.functions = functions
        self.input_type = input_type

    def execute_function(self, function_name: str, input_data=None, *args, **kwargs):
        """
        Execute a function in the agent
        :param input_data:
        :param function_name:
        :param args:
        :param kwargs:
        :return:
        """
        if function_name in self.functions:
            return self.functions[function_name](
                input_data, *args, **kwargs
            )  # Pass the optional input_data
        else:
            return {"error": f"Function {function_name} not found in {self.name}"}


class AgentManager:
    """
    Agent Manager class to manage multiple agents
    """

    def __init__(self, expected_input_type: str = "JSON"):
        """
        Initialize the agent manager
        """
        self.agents: Dict[str, DynamicAgent] = {}
        self.expected_input_type = expected_input_type

    def register_agent(self, agent: DynamicAgent):
        """
        Register an agent
        :param agent:
        :return:
        """
        self.agents[agent.name] = agent

    def execute_function(
        self, agent_name: str, function_name: str, input_data=None, *args, **kwargs
    ):
        """
        Execute a function in an agent
        :param input_data:
        :param agent_name:
        :param function_name:
        :param args:
        :param kwargs:
        :return:
        """
        agent = self.agents.get(agent_name)
        if agent is not None:
            return agent.execute_function(
                function_name, input_data, *args, **kwargs
            )  # Pass the optional input_data
        return {"error": f"Agent {agent_name} not found"}

    def generate_prompt(self):
        """
        Generate a prompt for the user
        :return:
        """
        prompt = "You have access to multiple specialized agents with unique functionalities:\n\n"
        for agent_name, agent in self.agents.items():
            prompt += (
                f"- {agent_name}: {agent.description} with the following capabilities:\n. "
                f"It requires that the input looks like this: "
                f"{agent.input_type}\n"
            )
            for function_name in agent.functions.keys():
                prompt += f"  - {function_name}\n"
        prompt += (
            "\nYou can instruct these agents to perform tasks for you. What would you like to do? "
            "Remember to return the answer in the following format: {'result': 'your answer', 'success': True}"
        )
        return prompt


"""
Use Cases for Dynamic Agents

 Define some complex functions for Agent

Ex: 
def complex_hello():
    return {"result": "Hello, this is complex!"}

def add_and_multiply(x, y):
    return {"result": (x + y) * 2}

 Define some functions for Agent2
def say_goodbye():
    return {"result": "Goodbye!"}

def multiply_numbers(x, y):
    return {"result": x * y}

-- Initialize Agents -- 

agents = {
    "Agent1": DynamicAgent(
        name="Agent1",
        description="This is Agent1",
        functions={
            "complex_hello": complex_hello,
            "add_and_multiply": add_and_multiply
        }
    ),
    "Agent2": DynamicAgent(
        name="Agent2",
        description="This is Agent2",
        functions={
            "say_goodbye": say_goodbye,
            "multiply_numbers": multiply_numbers
        }
    )
    # You can easily add more agents here
}

-- Register agents with AgentManager -- 

manager = AgentManager()
for agent in agents.values():
    manager.register_agent(agent)

-- Generate the dynamic prompt -- 
dynamic_prompt = manager.generate_prompt()
print(dynamic_prompt)

You have access to multiple specialized agents with unique functionalities:

- Agent1: This is Agent1 with the following capabilities:
  - complex_hello
  - add_and_multiply

- Agent2: This is Agent2 with the following capabilities:
  - say_goodbye
  - multiply_numbers

 -- You can instruct these agents to perform tasks for you. -- 
 


 -- This updated prompt can serve as the dynamic context for an LLM, helping it to understand which agents and 
functionalities are currently available. --

"""
