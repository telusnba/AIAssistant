import g4f
from g4f.client import Client

client = Client()


def get_gpt_response(chat_history):
    try:
        response = client.chat.completions.create(
            model=g4f.models.gpt_35_turbo,
            messages=chat_history,
        )

        chat_gpt_response = response.choices[0].message.content
    except Exception as e:
        print(e)
        chat_gpt_response = "Извините, произошла ошибка."
    return chat_gpt_response


def trim_history(history, max_length=4096):
    current_length = sum(len(message["content"]) for message in history)
    while history and current_length > max_length:
        removed_message = history.pop(0)
        current_length -= len(removed_message["content"])
    return history

