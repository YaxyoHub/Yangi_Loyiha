import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, BotCommand, BotCommandScopeDefault
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from states import FeedbackState
import google.generativeai as genai

from states import FeedbackState
from data import API_TOKEN, ADMIN_ID, Gemini
# from buttons import 

bot = Bot(token=API_TOKEN)
gemini_token = Gemini
dp = Dispatcher()
genai.configure(api_key=gemini_token)
model = genai.GenerativeModel('gemini-2.0-flash')


async def menu_button():
    commands = [
        BotCommand(command='start', description='Botni ishga tushirish uchun'),
        BotCommand(command='help', description="Yordam so'rash uchun"),
        BotCommand(command='about', description='Bot haqida'),
        BotCommand(command='feedback', description='Feedback yozish uchun')
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault)

"""Commands"""

@dp.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer(f"Salom {message.from_user.first_name}👋")

@dp.message(Command('help'))
async def help(msg: Message):
    await msg.answer("Bu bot nimalar qila oladi?\n\n"
                     "Siz bu bot orqali hohlagan savolingizga javob topa olasiz")

@dp.message(Command('about'))
async def help(msg: Message):
    await msg.answer("Bu Yaxyo Rahmatullayevning amaliyot uchun yaratgan AI boti")

@dp.message(Command('feedback'))
async def feedback_start(msg: Message, state: FSMContext):
    await msg.answer("Feedback yozing")
    await state.set_state(FeedbackState.feedback)

@dp.message(FeedbackState.feedback)
async def feedback_to_admin(msg: Message, state: FSMContext):
    feedback_text = msg.text
    await bot.send_message(ADMIN_ID, f"Ismi: {msg.from_user.first_name}\n"
                           f"Username: {msg.from_user.username}\n"
                           f"ID: {msg.from_user.id}\n"
                           f"Foydalanuvchidan feedback:\n\n{feedback_text}")

    await msg.answer("Feedback uchun rahmat! Sizning xabaringiz Admin tomonidan ko'rib chiqiladi")
    await state.clear()

"""Message"""

@dp.message(F.text)
async def user_text(msg: Message):
    try:
        answer = model.generate_content(msg.text)
        await msg.answer(answer.text)
    except:
        await msg.answer("Botda xatolik yuz berdi")

async def main():
    await menu_button()
    await dp.start_polling(bot)

if __name__ == "__main__":
    print("Bot is running...")
    asyncio.run(main())