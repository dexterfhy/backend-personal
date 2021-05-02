import random

BOT_USER_TYPE = "BOT"
AGENT_USER_TYPE = "AGENT"
MESSAGE_SOCKET_EVENT = "message"
AGENT_SOCKET_EVENT = "agent"
LIVE_CHAT_SOCKET_EVENT = "live-chat"

DEFAULT_DIALOGFLOW_LANGUAGE_CODE = "en"
DEFAULT_FALLBACK_MESSAGE = 'Sorry, I did not understand you. What were you saying?'
DEFAULT_ERROR_MESSAGE = 'Sorry, something went wrong. Please try again later!'

# Change the following to suit your project
DIALOGFLOW_PROJECT_ID = ""
GOOGLE_SERVICE_ACCOUNT_FILE_PATH = ""
START_EVENT = "START_CONVERSATION_EVENT"
END_EVENT = "END_CONVERSATION_EVENT"
CUSTOM_EVENTS = [
    START_EVENT,
    END_EVENT,
    "TELEGRAM_QUESTION_FEEDBACK_START_EVENT",
    "TELEGRAM_QUESTION_FEEDBACK_CANCEL_EVENT"
]

TELEGRAM_API_TOKEN = ""
TELEGRAM_USER_ID = 0

RANDOM_PROMPTS_SIZE = 3
PROMPTS = [
    "Thank you!",
    "Who are you?",
    "What is your name?",
    "Where are you from?",
    "Are you on Linkedin?",
    "Can I see your Github profile?",
    "How can I contact you?",
    "Can I see your cats?",
    "What did you study?",
    "What is your job?",
    "What do you do?",
    "Where do you work at?",
    "What do you code in?",
    "What technologies do you use?",
    "What do you do at your job?",
    "Can I learn more about your chatbot?"
]

GET_CHATBOT_RESPONSES = {
    "GREETING_WITH_NAME": lambda name: random.choice([
        "Hello {}, it's nice to meet you!",
        "Nice to meet you, {}!",
        "Hey there {}! I hope you are doing well.",
    ]).format(name),
    "CONTACT_DETAILS": lambda: "You can email me at dexterfonghy@gmail.com or call/text me at +65 92221243.\n\n"
                               "Alternatively, you can Whatsapp me too by clicking on that button below.",
    "EDUCATION": lambda: "I graduated with a Bsc in Computer Science Murdoch University, "
                         "and I'm currently pursuing a Masters in Computing at National University of Singapore.\n\n"
                         "Here's more info about my educational background!",
    "EMPLOYMENT": lambda: "I'm currently working as a Software Engineer at a tech logistics company, Ninja Van, "
                          "where I build a chatbot that allows customers to track the status of their orders "
                          "and speak to live agents via their preferred social media channels."
                          "\n\nHere are some other companies I've worked at in the past!",
    "CHATBOT": lambda: "I make chatbots! I wrote some articles about what I did using Google's Dialogflow "
                       "(just like what I used to build this) - "
                       "feel free to check them out in the links provided below.",
    "KITTIES": lambda: random.choice([
        "Thought you'd never ask. Here's Rylee (flamepoint) and Rubick (tabby):",
        "Sure, here are some photos of the kitties - Rylee the flamepoint and Rubick the tabby:",
        "Here they are! Rylee (flamepoint) and Rubick (tabby)"
    ]),
    "CONFIRM_FEEDBACK": lambda feedback: "Submit this feedback?\n\n\"{}\"".format(feedback),
}

GET_CHATBOT_OPTIONS = {
    "WHATSAPP": {
        "type": "URL",
        "items": [{
            "text": "Whatsapp",
            "type": "URL",
            "url": "https://api.whatsapp.com/send?phone=6592221243&text=Hello"
        }]
    },
    "EDUCATION": {
        "type": "TIMELINE",
        "items": [
            {
                "date": "2021 - 2023",
                "text": "MComp (Computer Science) @ National University of Singapore"
            },
            {
                "date": "2017 - 2019",
                "text": "Bsc in Computer Science @ Murdoch University"
            },
            {
                "date": "2008 - 2013",
                "text": "GCE A-Levels @ Raffles Institution"
            }
        ]
    },
    "EMPLOYMENT": {
        "type": "TIMELINE",
        "items": [
            {
                "date": "Oct 2019 – Present",
                "text": "Software Engineer @ Ninja Van"
            },
            {
                "date": "Jul 2019 – Sep 2019",
                "text": "Software Engineer Intern @ iWonder"
            }
        ]
    },
    "CHATBOT": {
        "type": "URL",
        "items": [
            {
                "text": "Designing NinjaChat",
                "type": "URL",
                "url": "https://medium.com/ninjavan-tech/designing-ninjachat-bfa2445e84ce"
            },
            {
                "text": "Basics with Dialogflow",
                "type": "URL",
                "url": "https://medium.com/ninjavan-tech/ninjachat-basics-with-dialogflow-b8d64e71c49b"
            },
            {
                "text": "When Things Go Wrong",
                "type": "URL",
                "url": "https://medium.com/ninjavan-tech/when-things-go-wrong-with-ninjachat-also-localization-c541192b7335"
            },
            {
                "text": "Testing and the Future",
                "type": "URL",
                "url": "https://medium.com/ninjavan-tech/testing-and-the-future-of-ninjachat-8c09e11827f3"
            }
        ]
    },
    "KITTIES": {
        "type": "IMAGE",
        "items": [
            {
                "url": "https://dexter-website.s3-ap-southeast-1.amazonaws.com/cat1.jpg"
            },
            {
                "url": "https://dexter-website.s3-ap-southeast-1.amazonaws.com/cat2.jpg"
            },
            {
                "url": "https://dexter-website.s3-ap-southeast-1.amazonaws.com/cat3.jpg"
            }
        ]
    },
    "CANCEL": {
        "type": "DEFAULT",
        "items": [
            {
                "text": "Cancel",
                "payload": "TELEGRAM_QUESTION_FEEDBACK_CANCEL_EVENT"
            }
        ]
    },
    "CONFIRM_FEEDBACK": {
        "type": "DEFAULT",
        "items": [
            {
                "text": "Yes"
            },
            {
                "text": "No"
            },
            {
                "text": "Cancel",
                "payload": "TELEGRAM_QUESTION_FEEDBACK_CANCEL_EVENT"
            }
        ]
    },
}

FEEDBACK_TEMPLATE = "[FEEDBACK RECEIVED]\nSession ID: {}\nEmail/Phone Number: {}\n\n{}"
ONGOING_LIVE_CHAT_TEMPLATE = "[LIVE CHAT]\nSession ID: {}\n\n{}"
