from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai.chat_models import ChatOpenAI
from langchain_community.chat_message_histories import FileChatMessageHistory
from dotenv import load_dotenv
import os
import argparse

def get_user_input():
    return input(">> ")

def create_chat_prompt(subject):
    return ChatPromptTemplate.from_messages([
        SystemMessage(content=f"You are a helpful AI assistant specialized in {subject}. Always consider the full conversation history when responding."),
        MessagesPlaceholder(variable_name="history"),
        HumanMessage(content="{input}")
    ])

def process_input(user_input, chain):
    if user_input.lower() in ["quit", "exit", "q"]:
        return False

    response = chain.invoke({"input": user_input})
    print(f"AI: {response['output']}")

    return True

def parse_arguments():
    parser = argparse.ArgumentParser(description="AI Chat Program")
    parser.add_argument("--subject", type=str, default="general knowledge",
                        help="Specify the AI's area of expertise (also used as conversation ID)")
    return parser.parse_args()

def run_program(subject):
    # Load environment variables from .env file
    load_dotenv()

    # Get OpenAI API key from environment variable
    openai_api_key = os.getenv("OPENAI_API_KEY")

    if not openai_api_key:
        print("Please set the OPENAI_API_KEY in your .env file.")
        return

    chat_prompt = create_chat_prompt(subject)
    chat = ChatOpenAI(openai_api_key=openai_api_key, model="gpt-3.5-turbo")

    # Create a directory for chat histories if it doesn't exist
    os.makedirs("chat_histories", exist_ok=True)

    # Use FileChatMessageHistory instead of ChatMessageHistory
    file_history = FileChatMessageHistory(f"chat_histories/{subject}_chat_history.json")

    # Check if the history is empty and add initial system message if it is
    if not file_history.messages:
        file_history.add_message(SystemMessage(content=f"You are a helpful AI assistant specialized in {subject}. Always consider the full conversation history when responding."))

    print(f"Welcome to the AI chat program. The AI is specialized in {subject}.")
    print("Type 'quit', 'exit', or 'q' to end the program.")

    while True:
        user_input = get_user_input()
        if user_input.lower() in ["quit", "exit", "q"]:
            break

        file_history.add_user_message(user_input)

        messages = file_history.messages

        response = chat.invoke(messages)

        response_content = response.content

        file_history.add_ai_message(response_content)

        print(f"AI: {response_content}")

    print("\nThank you for using the AI chat program. The conversation has been saved.")
    print("You can continue this conversation next time you run the program with the same subject.")
    print("Goodbye!")

if __name__ == "__main__":
    args = parse_arguments()
    run_program(args.subject)
