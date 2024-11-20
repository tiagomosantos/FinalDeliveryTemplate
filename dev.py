from company_name import DevChatbot # Import the development version of the chatbot
from dotenv import load_dotenv  # Import dotenv to load environment variables


def main(bot: DevChatbot):
    """Main interaction loop for the development version of the chatbot.

    Args:
        bot: An instance of the DevChatbot.
    """
    while True:
        # Prompt the user for input
        user_input = input("You: ").strip()

        # Allow the user to exit the conversation
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        try:
            # Process the user's input using the bot and display the response
            response = bot.process_user_input({"customer_input": user_input})
            print(f"Bot: {response}")
        except Exception as e:
            # Handle any exceptions and prompt the user to try again
            print(f"Error: {str(e)}")
            print("Please try again with a different query.")


if __name__ == "__main__":
    # Load environment variables from a .env file
    load_dotenv()

    # Notify the user that the bot is running in development mode
    print("RUNNING IN DEV MODE.")
    print("Starting the bot...")

    # Define a list of intentions for the development bot
    intentions = ["intention1", "intention2", "intention3"]

    # Initialize the development version of the CustomerServiceBot
    bot = DevChatbot(
        user_id="user_123", conversation_id="conversation_123", intentions=intentions
    )

    # Display instructions for ending the conversation
    print(
        "Developement Bot initialized. Type 'exit' or 'quit' to end the development process."
    )

    # Start the main interaction loop
    main(bot)
