from langchain.agents import AgentExecutor
from langchain.agents import create_tool_calling_agent
from company_name.chatbot.tools.create_order import Tool1
from company_name.chatbot.tools.get_order import Tool2
from company_name.chatbot.chains.base import generate_agent_prompt_template, PromptTemplate


class Agent1:
    def __init__(self, llm):
        self.llm = llm
        self._agent_executor = None  # Placeholder for lazy initialization

        create_order_tool = Tool1()
        check_order_tool = Tool2()
        self.tools = [create_order_tool, check_order_tool]

        # Define the prompt template for product identification
        prompt_template = PromptTemplate(
            system_template="""
            You are now connected to the e-commerce database. You can use the following tools to interact with the database:

            1. Create Order: Create a new order in the database
            2. Get Order: Retrieve details of an existing order based on the order ID

            The user_id is 
            {customer_id}

            If none of the above tools are needed, you can answer the customer in a polite manner.
            """,
            human_template="Customer Query: {customer_input}",
        )

        self.prompt = generate_agent_prompt_template(prompt_template)
        self.agent = create_tool_calling_agent(self.llm, self.tools, self.prompt)

    @property
    def agent_executor(self):
        """
        Lazily initialize and return the agent_executor.
        This ensures it's only created when accessed for the first time.
        """
        if self._agent_executor is None:
            self._agent_executor = AgentExecutor(agent=self.agent, tools=self.tools)
        return self._agent_executor
