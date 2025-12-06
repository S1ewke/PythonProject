import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from deep_translator import GoogleTranslator


# 🔐 ВСТАВЬ СЮДА СВОЙ ТОКЕН ОТ BOTFATHER
BOT_TOKEN = "8554093184:AAGrOdGNcymtJnN-_Oo8T4Six3mHkWYC7V4"

# здесь будем хранить язык для каждого юзера: {user_id: "en", "ru", "de", ...}
user_lang = {}

# язык по умолчанию
DEFAULT_LANG = "en"


def translate_text(text: str, target_lang: str) -> str:
    """
    Перевод текста (source=auto) на target_lang через GoogleTranslator.
    """
    try:
        translator = GoogleTranslator(source="auto", target=target_lang)
        translated = translator.translate(text)
        return translated
    except Exception as e:
        logging.exception("Ошибка при переводе: %s", e)
        return "❌ Ошибка при переводе. Попробуйте ещё раз позже."


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # /start
    @dp.message(CommandStart())
    async def cmd_start(message: Message):
        user_lang[message.from_user.id] = DEFAULT_LANG
        await message.answer(
            "Привет! 👋\n\n"
            "Я бот-переводчик.\n"
            "Отправь мне любой текст — я переведу его.\n\n"
            "По умолчанию перевожу на английский (EN).\n\n"
            "Команды:\n"
            "/to_en – переводить на английский 🇬🇧\n"
            "/to_ru – переводить на русский 🇷🇺\n"
            "/to_de – переводить на немецкий 🇩🇪\n"
            "/lang – показать текущий язык перевода"
        )

    # /lang – показать текущий язык
    @dp.message(Command("lang"))
    async def cmd_lang(message: Message):
        lang = user_lang.get(message.from_user.id, DEFAULT_LANG)
        await message.answer(f"Текущий язык перевода: {lang.upper()}")

    # /to_en – на английский
    @dp.message(Command("to_en"))
    async def cmd_to_en(message: Message):
        user_lang[message.from_user.id] = "en"
        await message.answer("Теперь перевожу на английский 🇬🇧")

    # /to_ru – на русский
    @dp.message(Command("to_ru"))
    async def cmd_to_ru(message: Message):
        user_lang[message.from_user.id] = "ru"
        await message.answer("Теперь перевожу на русский 🇷🇺")

    # /to_de – на немецкий
    @dp.message(Command("to_de"))
    async def cmd_to_de(message: Message):
        user_lang[message.from_user.id] = "de"
        await message.answer("Теперь перевожу на немецкий 🇩🇪")

    # обработчик любого текста
    @dp.message(F.text)
    async def translate_message(message: Message):
        lang = user_lang.get(message.from_user.id, DEFAULT_LANG)
        original_text = message.text

        translated = translate_text(original_text, lang)

        await message.answer(
            f"🔤 Оригинал:\n{original_text}\n\n"
            f"🌐 Перевод ({lang.upper()}):\n{translated}"
        )

    # запуск бота
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
