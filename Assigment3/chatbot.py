"""
Terminal-based chatbot client using Django and ChatterBot.

This script:
- Initializes a minimal Django environment (to satisfy assignment requirement).
- Creates and trains a ChatterBot chatbot.
- Starts a simple chat loop in the terminal where the user can type messages.
- Prints out the bot's responses until the user types 'quit' or 'exit'.

"""

import os
import django

# --- 1. Set up Django environment (required because Django is installed) ---
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()

# --- 2. Import ChatterBot components ---
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

from training_data import basic_conversations


def create_chatbot():
    """
    Create and configure a ChatterBot instance.
    We focus on:
    - Using BestMatch with a default response
    - Enabling simple math evaluation
    """
    bot = ChatBot(
        "TerminalBot",
        read_only=False,
        logic_adapters=[
            {
                "import_path": "chatterbot.logic.BestMatch",
                "default_response": (
                    "I'm not sure how to respond to that yet. "
                    "I'm still learning. Try asking me something else!"
                ),
                "maximum_similarity_threshold": 0.80,
            },
            "chatterbot.logic.MathematicalEvaluation",
        ],
        database_uri="sqlite:///chatbot_database.sqlite3",
    )
    return bot


def train_chatbot(bot: ChatBot):
    """
    Train the chatbot only with our curated conversations.

    This avoids noisy random answers coming from large generic corpora
    and keeps the bot focused on what we want it to do.
    """
    trainer = ListTrainer(bot)

    for conversation in basic_conversations:
        trainer.train(conversation)




def run_chat_loop(bot: ChatBot):
    """
    Start the terminal chat loop.

    The user can type messages and receive responses from the chatbot.
    Typing 'quit' or 'exit' will end the program.
    """
    print("====================================")
    print("    Terminal ChatBot (ChatterBot)   ")
    print(" Type 'quit' or 'exit' to stop.     ")
    print("====================================\n")

    while True:
        try:
            user_input = input("user: ").strip()
        except (KeyboardInterrupt, EOFError):
            # Handle Ctrl+C or Ctrl+D nicely
            print("\nExiting chat. Goodbye!")
            break

        if user_input.lower() in {"quit", "exit"}:
            print("bot: Goodbye! Have a great day.")
            break

        if not user_input:
            # If user just presses Enter, skip
            continue

        # Get response from the bot
        bot_response = bot.get_response(user_input)
        print(f"bot: {bot_response}")


def main():
    """
    Main entry point for the script.
    Creates, trains, and then runs the chatbot loop.
    """
    # 1. Create a chatbot instance
    chatbot = create_chatbot()

    # 2. Train the chatbot with our predefined conversations
    train_chatbot(chatbot)

    # 3. Start the interactive chat loop
    run_chat_loop(chatbot)


if __name__ == "__main__":
    main()
