from typing import Dict, Callable, Any
import asyncio

from agents.agent_manager import AgentManager, DynamicAgent


# Your existing DynamicAgent and AgentManager classes here ...


class Assignment:
    """
    Assignment class to represent an assignment that can be dynamically loaded
    """

    def __init__(
        self,
        name: str,
        description: str,
        agent_manager,
        agent_name: str,
        function_name: str,
        expected_input_type: str = "JSON",
        *args,
        **kwargs,
    ):
        self.name = name
        self.description = description
        self.agent_manager = agent_manager
        self.agent_name = agent_name
        self.function_name = function_name
        self.expected_input_type = expected_input_type  # New field
        self.args = args
        self.kwargs = kwargs
        self.running = True

    async def start(
        self,
        interval: int,
        condition_check: Callable[..., bool],
        action: Callable[..., Any],
    ):
        while self.running:
            result = self.agent_manager.execute_function(
                self.agent_name, self.function_name, *self.args, **self.kwargs
            )
            if condition_check(result):
                action()
                self.running = False  # Stop this assignment
            await asyncio.sleep(interval)

    def generate_async_prompt(self):
        prompt_parts = [
            f"You also have access to these special agents {self.agent_name} that can complete the assignment '{self.name}"
            f"' available:\n",
            f"1. Name: {self.name}",
            f"   Description: {self.description}",
            f"   Function: {self.function_name} (Expected Input: {self.expected_input_type})\n",
            "What would you like to do?",
        ]

        return "".join(prompt_parts)


# Condition check function


"""
-- How to Use the Assignment Class --
def has_person_x_entered(result):
    return result.get("result") == "x_entered"

 -- Action to be performed -- 
def person_x_entered_action():
    print("Person X has entered the room! Performing the assigned action.")

 -- Initialize AgentManager and agents -- 
agent_manager = AgentManager()

def check_if_x_entered():
    # Simulate the check (you can replace this with real code)
    return {"result": "x_entered"}  # For demonstration purposes, we assume "x" always enters

agent_manager.register_agent(DynamicAgent("SecurityAgent", "Monitors room entrance", {"check_if_x_entered": check_if_x_entered}))

-- Initialize Assignment --
assignment = Assignment("MonitorEntrance", "Monitor the room entrance for person X", agent_manager, "SecurityAgent", "check_if_x_entered")
assignment.start(5, has_person_x_entered, person_x_entered_action)

"""
