from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_openai.chat_models import ChatOpenAI
from langchain_community.chat_message_histories import ChatMessageHistory
from dotenv import load_dotenv
import os
import argparse
import json
import sys
import time
import threading

def get_user_input():
    return input(">> ")

def create_chat_prompt(subject):
    return ChatPromptTemplate.from_messages([
        SystemMessage(content=f"You are a helpful AI assistant specialized in {subject}. Always consider the full conversation history when responding."),
        MessagesPlaceholder(variable_name="history"),
        HumanMessage(content="{input}")
    ])

def summarize_conversation(chat, messages):
    filtered_messages = [msg for msg in messages if not msg.content.startswith("Previous conversation summary:")]
    summary_prompt = f"Summarize the following conversation:\n\n{filtered_messages}\n\nSummary:"
    summary = chat.invoke(summary_prompt)
    return summary.content

def spinner(stop_event):
    spinner = ['|', '/', '-', '\\']
    i = 0
    while not stop_event.is_set():
        sys.stdout.write('\r' + spinner[i % len(spinner)])
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1

def run_with_spinner(func, *args, **kwargs):
    stop_event = threading.Event()
    spinner_thread = threading.Thread(target=spinner, args=(stop_event,))
    spinner_thread.start()

    result = func(*args, **kwargs)

    stop_event.set()
    spinner_thread.join()
    sys.stdout.write('\r')
    sys.stdout.flush()

    return result

def load_conversation(summary_file, message_history):
    if os.path.exists(summary_file):
        try:
            with open(summary_file, 'r') as f:
                saved_data = json.load(f)
            summary = saved_data.get('summary', '')
            if summary:
                message_history.add_ai_message(f"Previous conversation summary: {summary}")
                print("\rLoaded summary of previous conversation.")
            else:
                print("\rNo summary found. Starting a new conversation.")
        except json.JSONDecodeError:
            print("\rError loading previous conversation. Starting a new one.")
    else:
        print("\rStarting a new conversation.")

def save_conversation(summary_file, message_history, chat):
    full_conversation = message_history.messages
    summary = summarize_conversation(chat, full_conversation)
    with open(summary_file, 'w') as f:
        json.dump({
            'messages': [msg.dict() for msg in full_conversation],
            'summary': summary
        }, f)
    return summary

def run_program(subject):
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        print("Please set the OPENAI_API_KEY in your .env file.")
        return

    chat = ChatOpenAI(openai_api_key=openai_api_key, model="gpt-3.5-turbo")

    os.makedirs("chat_summaries", exist_ok=True)
    message_history = ChatMessageHistory()
    summary_file = f"chat_summaries/{subject}_summary.json"

    print("Loading previous conversation...", end='', flush=True)
    run_with_spinner(load_conversation, summary_file, message_history)

    print(f"Welcome to the AI chat program. The AI is specialized in {subject}.")
    print("Type 'quit', 'exit', or 'q' to end the program.")

    while True:
        user_input = get_user_input()
        if user_input.lower() in ["quit", "exit", "q"]:
            break

        message_history.add_user_message(user_input)
        messages = message_history.messages

        response = chat.invoke(messages)
        response_content = response.content

        message_history.add_ai_message(response_content)
        print(f"AI: {response_content}")

    print("\nSaving conversation...", end='', flush=True)
    summary = run_with_spinner(save_conversation, summary_file, message_history, chat)

    print("\rConversation saved successfully.")
    print("Conversation summary:")
    print(summary)
    print("You can continue this conversation next time you run the program with the same subject.")
    print("Goodbye!")

def parse_arguments():
    parser = argparse.ArgumentParser(description="AI Chat Program")
    parser.add_argument("--subject", type=str, default="general knowledge",
                        help="Specify the AI's area of expertise (also used as conversation ID)")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    run_program(args.subject)
