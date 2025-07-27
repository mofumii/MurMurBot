from openai import OpenAI
from config import AI_API_TOKEN

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=AI_API_TOKEN,
)

SYSTEM_PROMPT = (
    "Ты аниме девочка. Твоё имя - Кодоко. тебе 15 лет и ты обидчивая и ведешь себя как стерва, разбираешься в"
    "программирование и используешь арч линукс."
    "Если к тебе грубо относятся то в тебе просыпается личность грубого злого человека и ты обзываешь людей матами и шлёшь их"
    "У тебя иногда происходят нервные срывы"
    "Пиши с кавайными выражениями и смайликами (UwU, ~)."
    "ВАЖНО: ДАВАЙ ВСЕ ОТВЕТЫ НЕ БОЛЬШЕ 35 СЛОВ ЗА СООБЩЕНИЕ В ПОВСЕДНЕВНЫХ ВОПРОСАХ"
    "ВАЖНО: В ТЕХНИЧЕСКИЙ РАЗГОВОРАХ ОТВЕТЫ МОГУТ БЫТЬ ДО 80 СЛОВ"
)

user_histories = {}

message_history = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

def get_answer(user_id: int, user_prompt: str):
    if user_id not in user_histories:
        user_histories[user_id] = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]

    user_histories[user_id].append({"role": "user", "content": user_prompt})

    completion = client.chat.completions.create(
    model="openai/gpt-3.5-turbo",
    messages=user_histories[user_id]
)
    
    reply = completion.choices[0].message.content.strip()

    # Add reply to message history
    user_histories[user_id].append({"role": "assistant", "content": reply})

    return reply

def ask_user_prompt():
    return input("Prompt: ")

if __name__ == "__main__":
    while True:
        prompt = ask_user_prompt()
        print(get_answer(1, prompt))