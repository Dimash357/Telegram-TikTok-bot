import asyncio
import logging
import sys
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Filter, CommandStart
from aiogram.types import Message, URLInputFile

TOKEN = "7059499041:AAFqlC3pWtWTWwUmRKCwfpi4uC57MS00N58"

dp = Dispatcher()


class LinkFilter(Filter):
    async def __call__(self, message: Message):
        return message.text.startswith("http")


@dp.message(LinkFilter())
async def link_handler(message: Message) -> None:
    link = message.text

    msg = await message.answer("Пожалуйста, подождите, мы обрабатываем ваш запрос")

    # Добавлены строки для отладки
    print("URL:", link)

    url = "https://tiktok-video-no-watermark2.p.rapidapi.com/"
    querystring = {"url": link, "hd": "1"}
    headers1 = {
        "X-RapidAPI-Key": "e1bf90f97amsh469a9c3305ede8bp15ca3ejsnbf0d7f4a2fbd",
        "X-RapidAPI-Host": "tiktok-video-no-watermark2.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers1, params=querystring)

    # Добавлены строки для отладки
    print("Response:", response.text)

    try:
        video_link = response.json()['data']['play']
    except KeyError:
        await msg.edit_text("Ссылка оказалась неверной")
        return

    await msg.edit_text("Отправляем видео")
    await msg.delete()
    await message.answer_video(URLInputFile(video_link))


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer("Отправьте ссылку на видео")


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
