from openai import OpenAI

from bot.config import load_env_credentials

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=load_env_credentials().get("AI_API_TOKEN"),
)

SYSTEM_PROMPT = load_env_credentials().get("AI_PROMPT")

user_histories = {}

message_history = [{"role": "system", "content": SYSTEM_PROMPT}]


def get_respond(user_id: int, user_prompt: str):
    if user_id not in user_histories:
        user_histories[user_id] = [{"role": "system", "content": SYSTEM_PROMPT}]

    user_histories[user_id].append({"role": "user", "content": user_prompt})

    completion = client.chat.completions.create(
        model="nousresearch/deephermes-3-llama-3-8b-preview:free",
        messages=user_histories[user_id],
    )

    reply = completion.choices[0].message.content.strip()

    # Add reply to message history
    user_histories[user_id].append({"role": "assistant", "content": reply})

    return reply
