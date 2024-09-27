# AI Chat Program

This AI Chat Program is a command-line interface (CLI) application that allows users to engage in conversations with an AI assistant specialized in a specific subject. The program uses OpenAI's GPT model and provides features like conversation history, summarization, and persistence.

## Features

- Engage in conversations with an AI assistant specialized in a user-defined subject
- Save and load conversation history
- Automatically summarize conversations
- Display a loading spinner for better user experience
- Support for environment variables using .env file

## Prerequisites

- Python 3.6+
- OpenAI API key

## Installation

1. Clone this repository:

   ```sh

   git clone https://github.com/yourusername/ai-chat-program.git
   cd ai-chat-program
   ```

2. Install the required packages:

   ```sh

   pip install langchain langchain-openai python-dotenv
   ```

3. Create a `.env` file in the project root and add your OpenAI API key:

   ```sh

   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

Run the program with the following command:

```sh

python main.py --subject "your_subject_here"
```

Replace `"your_subject_here"` with the desired area of expertise for the AI assistant. If not specified, it defaults to "general knowledge".

During the conversation:

- Type your messages and press Enter to send them to the AI.
- Type 'quit', 'exit', or 'q' to end the program.

The program will automatically save the conversation summary when you exit, allowing you to continue the conversation in future sessions.

## File Structure

- `main.py`: The main script containing the AI chat program logic.
- `chat_summaries/`: Directory where conversation summaries are stored.
- `.env`: File for storing environment variables (not included in the repository).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).
