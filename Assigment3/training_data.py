
# training_data.py
# defines small, focused conversations you want your bot to know.
# Each inner list is a sequence of alternating user/bot messages.

basic_conversations = [
    # Greetings and intros
    [
        "hi",
        "Hello! It's nice to talk to you.",
        "hello",
        "Hello! How can I help you today?",
        "good morning",
        "Good morning! How are you today?",
        "good afternoon",
        "Good afternoon! What would you like to talk about?",
    ],

    # How are you
    [
        "how are you",
        "I am doing very well, thank you for asking.",
        "how are you doing",
        "I am doing very well, thank you for asking.",
        "are you okay",
        "Yes, I'm doing great, thanks for checking!",
    ],

    # About the bot
    [
        "what is your name",
        "I am a simple AI chatbot created with Python and ChatterBot for an AI homework assignment.",
        "who created you",
        "I was created by a student using Python, Django, and ChatterBot.",
        "do you know me",
        "I don't really know who you are, but it's nice chatting with you!",
    ],

    # Capability
    [
        "what is your capability",
        "I can chat with you, answer simple questions, and do basic calculations.",
        "what can you do",
        "I can chat with you, answer basic questions, and help with simple math problems like 2 + 2.",
        "what kind of basic questions can you answer",
        "I can answer simple questions about who I am, what I can do, and I can help with easy math.",
        "what kind of basic questions that you can answer",
        "I can answer simple questions about who I am, what I can do, and I can help with easy math.",
        "can you do calculation",
        "Yes, I can do simple calculations. Try asking me something like: what is 10 + 25?",
    ],

    # Friendly phrases
    [
        "nice to meet you",
        "Nice to meet you too!",
        "it is nice to meet you",
        "Nice to meet you too!",
        "are you kidding me",
        "No, I'm not kidding. I'm still learning, so sometimes my answers might be a bit off.",
        "really",
        "Yes, really. I'm just a class project chatbot, but I'm trying my best!",
    ],

    # Word problem example (explicit)
    [
        "if i have 2 apples then i eat 1 how many apples remain",
        "If you have 2 apples and eat 1, you will have 1 apple left.",
        "if i have two apples and i eat one how many do i have left",
        "If you start with 2 apples and eat 1, you have 1 apple remaining.",
    ],

    # Goodbye
    [
        "goodbye",
        "Goodbye! Have a great day!",
        "bye",
        "Bye! It was nice talking to you.",
    ],
]
