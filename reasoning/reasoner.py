import os

from chain.templatebase import TemplateChain, execute_chain


class Reasoning:
    """
    Reasoning class to represent a reasoning agent
    """

    def __init__(self, agent_manager, memory_manager):
        self.agent_manager = agent_manager
        self.memory_manager = memory_manager
        self.task_list = []  # To store the list of tasks

    def interpret_objective(self, objective: str):
        """
        Interpret an objective to generate tasks
        :param objective:
        :return:
        """
        # Query buffer memory to get all relevant context
        buffer_memory_contexts = []
        for i in range(-1, -6, -1):  # Loop through the last 5 conversations
            context = self.memory_manager.buffer.get_memory_from_buffer(i)
            if context:
                buffer_memory_contexts.append(context)
            else:
                break

        # Concatenate all buffer memory contexts
        buffer_memory = " | ".join(buffer_memory_contexts)

        # Query Redis to get any other relevant context
        redis_memory = self.memory_manager.redis.query(
            "some_key"
        )  # Replace with your actual query

        pre_context = f"Buffer: {buffer_memory}, Redis: {redis_memory}"

        # Create a TemplateChain object
        task_chain = TemplateChain(
            template_prompt="Given the objective {0}, generate tasks. in following mapped JSON format: "
            + "{{'name': 'task_name', 'function': 'function_to_use', 'input': 'input_to_add'}, "
            + "{'name': 'task_name', 'function': 'function_to_use', 'input': 'input_to_add'}}",
            inputs=[objective],
            memory=pre_context,
        )

        # Execute the chain to generate tasks
        tasks = execute_chain(task_chain)
        # for loop to go through the JSON formats and find the name and details.
        # Then, append to the task_list
        if not hasattr(self, "task_list") or self.task_list is None:
            self.task_list = []

        # Iterate over the JSON-formatted tasks to extract name and details
        for task in tasks:
            task_name = task.get("name")
            task_details = task.get("details")
            task_input = task.get("input")
            if task_name and task_details:  # Ensure both are present
                self.task_list.append(
                    {"name": task_name, "details": task_details, "input": task_input}
                )

        self.task_list.extend(tasks)  # Store the generated tasks

    def execute_first_task(self, input_data=None):
        """
        Execute the first task in the task list
        :param input_data:
        :return:
        """
        if not self.task_list:
            return "No tasks available"

        first_task = self.task_list.pop(0)

        task_name = first_task["name"]
        task_details = first_task["function"]
        task_input = first_task["input"]

        result = self.agent_manager.execute_function(
            task_name, input_data, **task_details
        )

        return result  # Return the result

    def assess_and_update(self, result, original_prompt):
        """
        Assess the result and update the task list
        :param result:
        :param original_prompt:
        :return:
        """
        # Check if the task was successful
        if result.get("success"):
            print(f"Task completed successfully with result: {result.get('result')}")
            return True

        # have the LLM compared the answer here. based on the return JSON it will asess to update the task list

        # If the task was not successful, assess if we need to update the task list
        should_update_tasks = False  # Default to not updating

        # TODO replace with the LLM Version of the checking with JSON return stringify.
        # if result.get('result') != original_prompt:  # Replace this with your actual comparison logic
        #     should_update_tasks = True

        if should_update_tasks:
            print("Updating tasks based on assessment.")
            # Logic to update the task list goes here
            # For example, you can call self.interpret_objective with a new objective
            self.interpret_objective(
                "new_objective"
            )  # Replace 'new_objective' as needed

        return False

    def run(self, original_prompt):
        """
        Run the reasoning agent
        :param original_prompt:
        :return:
        """
        while self.task_list:
            result = self.execute_first_task()
            assessment = self.assess_and_update(result, original_prompt)
            print(assessment)
