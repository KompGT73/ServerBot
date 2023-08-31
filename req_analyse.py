import requests
from config import ALL_MESSAGES, CHANNEL_ID
from tgbot import bot
import asyncio


last_message_id = -1


async def get(call):
    try:
        req = requests.get(call).json()
        return req
    except Exception as exc:
        print(f"ERROR! Невозможно получить данные по ссылке {call}")
        print(exc)
        return None


async def get_data(json_value, data_names):
    data_list = []
    for data_name in data_names:
        try:
            if json_value[data_name]:
                data_list.append(json_value[data_name])
            else:
                data_list.append("-")
        except Exception as exc:
            print(f"ERROR! В {json_value} нет данных с названием {data_name}")
            print(exc)
            data_list.append("'no data'")
    return data_list


async def get_changes(last_id, call, *value_data_names):
    json_values = await get(call)
    if json_values:
        new_values_data = []
        max_id = last_id
        for value in json_values:
            if value["id"] > last_id:
                if max_id < value["id"]:
                    max_id = value["id"]
                new_values_data.append(await get_data(value, value_data_names))
        if new_values_data:
            return new_values_data, max_id
    return 0


async def send_message_to_admins(message):
    await bot.send_message(
        chat_id=CHANNEL_ID,
        text=message
    )


async def check_changes():
    while True:
        global last_message_id
        await asyncio.sleep(20)

        all_new_messages_c = await get_changes(last_message_id, ALL_MESSAGES, "email", "support_url", "message")

        if all_new_messages_c:
            all_new_messages, last_message_id = all_new_messages_c
            for new_message in all_new_messages:
                email, support_url, message = new_message
                mess = (
                    f"<b>НОВИЙ ЗАПИТ У САПОРТ</b>\n\n<b>Пошта:</b> {email}\n<b>Повідомлення:</b> "
                    f"{message}\n<b>Посилання:</b> {support_url}"
                )
                await send_message_to_admins(mess)


