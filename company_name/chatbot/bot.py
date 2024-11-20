# Import necessary classes and modules for chatbot functionality
from typing import Dict
from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory
from company_name.chatbot.memory import MemoryManager
from company_name.chatbot.router.loader import load_intention_classifier
from company_name.chatbot.chains.chain3 import (
    ResponseChain3,
    ReasoningChain3,
)
from company_name.chatbot.agents.agent1 import Agent1


class MainChatbot:
    """A bot that handles customer service interactions by processing user inputs and
    routing them through configured reasoning and response chains.
    """

    def __init__(self, user_id: str, conversation_id: str):
        """Initialize the bot with session and language model configurations.

        Args:
            user_id: Identifier for the user.
            conversation_id: Identifier for the conversation.
        """
        # Initialize the memory manager to manage session history
        self.memory = MemoryManager(user_id, conversation_id)
        self.user_id = user_id
        self.conversation_id = conversation_id

        # Configure the language model with specific parameters for response generation
        self.llm = ChatOpenAI(temperature=0.0, model="gpt-4o-mini")

        # Map intent names to their corresponding reasoning and response chains
        self.chain_map = {
            "product_information": {
                "reasoning": ReasoningChain3(llm=self.llm),  # Reasoning chain
                "response": self.add_memory_to_runnable(
                    ResponseChain3(llm=self.llm)  # Response chain with memory
                ),
            }
        }

        self.agent_map = {
            "order": self.add_memory_to_runnable(
                Agent1(llm=self.llm).agent_executor
            )
        }

        # Load the intention classifier to determine user intents
        self.intention_classifier = load_intention_classifier()

    def add_memory_to_runnable(self, original_runnable):
        """Wrap a runnable with session history functionality.

        Args:
            original_runnable: The runnable instance to which session history will be added.

        Returns:
            An instance of RunnableWithMessageHistory that incorporates session history.
        """
        return RunnableWithMessageHistory(
            original_runnable,
            self.memory.get_session_history,  # Retrieve session history
            input_messages_key="customer_input",  # Key for user inputs
            history_messages_key="chat_history",  # Key for chat history
            history_factory_config=self.memory.get_history_factory_config(),  # Config for history factory
        ).with_config(
            {
                "run_name": original_runnable.__class__.__name__
            }  # Add runnable name for tracking
        )

    def get_chain(self, intent: str):
        """Retrieve the reasoning and response chains based on user intent.

        Args:
            intent: The identified intent of the user input.

        Returns:
            A tuple containing the reasoning and response chain instances for the intent.
        """
        return self.chain_map[intent]["reasoning"], self.chain_map[intent]["response"]

    def get_agent(self, intent: str):
        """Retrieve the agent based on user intent.

        Args:
            intent: The identified intent of the user input.

        Returns:
            The agent instance for the intent.
        """
        return self.agent_map[intent]

    def get_user_intent(self, user_input: Dict):
        """Classify the user intent based on the input text.

        Args:
            user_input: The input text from the user.

        Returns:
            The classified intent of the user input.
        """
        # Retrieve possible routes for the user's input using the classifier
        intent_routes = self.intention_classifier.retrieve_multiple_routes(
            user_input["customer_input"]
        )

        # Handle cases where no intent is identified
        if len(intent_routes) == 0:
            return None
        else:
            intention = intent_routes[0].name  # Use the first matched intent

        # Validate the retrieved intention and handle unexpected types
        if intention is None:
            return None
        elif isinstance(intention, str):
            return intention
        else:
            # Log the intention type for unexpected cases
            intention_type = type(intention).__name__
            print(
                f"I'm sorry, I didn't understand that. The intention type is {intention_type}."
            )
            return None

    def handle_product_information(self, user_input: Dict):
        """Handle the product information intent by processing user input and providing a response.

        Args:
            user_input: The input text from the user.

        Returns:
            The content of the response after processing through the chains.
        """
        # Retrieve reasoning and response chains for the product information intent
        reasoning_chain, response_chain = self.get_chain("product_information")

        # Process user input through the reasoning chain
        reasoning_output = reasoning_chain.invoke(user_input)

        # Generate a response using the output of the reasoning chain
        response = response_chain.invoke(
            reasoning_output, config=self.memory.get_memory_config()
        )

        return response.content

    def handle_order_intent(self, user_input: Dict):
        """Handle the order intent by processing user input and providing a response.

        Args:
            user_input: The input text from the user.

        Returns:
            The content of the response after processing through the chains.
        """
        # Retrieve the agent for the order intent
        agent = self.get_agent("order")

        # Process user input through the agent
        response = agent.invoke(
            {
                "customer_id": self.user_id,
                "customer_input": user_input["customer_input"],
            },
            config=self.memory.get_memory_config(),
        )

        return response["output"]

    def process_user_input(self, user_input: Dict):
        """Process user input by routing through the appropriate intention pipeline.

        Args:
            user_input: The input text from the user.

        Returns:
            The content of the response after processing through the chains.
        """
        # Classify the user's intent based on their input
        intention = self.get_user_intent(user_input)

        print(f"Intention: {intention}")

        # Check if the intention is a string or None
        if intention is None:
            return "I'm sorry, I don't understand that intention."
        else:
            # Route the input based on the identified intention
            if intention == "product_information":
                response = self.handle_product_information(user_input)
            elif intention == "create_order" or intention == "get_order":
                response = self.handle_order_intent(user_input)
            else:
                # Default response for unrecognized intents
                response = "Not implemented yet."
            return response
