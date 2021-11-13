from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from parasiteSearch import checker, getCounter
from aiogram.utils.markdown import text, bold, italic, code, pre, underline, strikethrough
from aiogram.types import ParseMode, InputMediaPhoto, InputMediaVideo, ChatActions
from audio import audioToString
import telebot
import os

telegramToken = "2099303179:AAFz7K_5gEkVAICMOyNJO9aIaCpaCqr2vGM"
bot = Bot(token=telegramToken)
dp = Dispatcher(bot)


def adding(txt):
    file = open("dictionary.txt", "r+", encoding="utf-8")
    resultText = file.read()
    if txt.lower() in resultText:
        return "Слово которое вы хотите добавить уже есть в словаре."
    else:
        file.write("," + txt.lower())
        return "Ваше слово успешно добавлено в словарь"


def check(texit):
    if "<" in texit:
        texit = texit.replace("<", "")
        texit = texit.replace(">", "")
        texit = text(code(texit))
    elif "*" in texit:
        texit = texit.replace("*", "")
        texit = text(italic(texit))
    else:
        texit = texit
    return texit


def constructMessage():
    checker()
    file = open("output.txt", "r", encoding="utf-8")
    txt = file.readline()
    file.close()
    texxt = txt.split(" ")
    txt = ""
    txt = text(txt)
    try:
        texxt.remove("\n")
    except ValueError:
        pass
    for i in range(len(texxt)):
        txt += check(texxt[i]) + " "
    txt = text(txt)
    txt.replace("*", "")
    txt.replace("\\", "")
    txt.replace("<", "")
    txt.replace(">", "")
    print(txt)
    result = txt + "\n"
    result += str(getCounter())
    return result


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    print(message.text + "\n")
    await bot.send_message(message.from_user.id,
                           "Напишите или скажите какое-то предложение, и бот вам ответит, если в предложении будут"
                           " слова паразиты он их вам выделит и посчитает.\n"
                           "Если вы хотите добавить какое-то слово паразит которого нет в нашем словаре, напишите "
                           "команду /add <Ваше слово>.\n "
                           "Если вы хотите увидеть полный список слов паразитов напишите комманду /dict.",
                           parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(commands=['dict'])
async def process_help_command(msg: types.Message):
    print(msg.text + "\n")
    file = open("dictionary.txt", "r", encoding="utf-8")
    result = file.read().split(",")
    await bot.send_message(msg.from_user.id, result, parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(commands=['add'])
async def process_help_command(msg: types.Message):
    print(msg.text + "\n")
    txt = msg.text[5:]
    if len(txt) == 0:
        result = "Впишите слово которое вы хотите добавить сразу после команды. Формат сообщения: '/add <Ваше слово>'."
    else:
        result = adding(txt)
    await bot.send_message(msg.from_user.id, result, parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(content_types=['voice'])
async def voice_processing(msg: types.Message):
    print("voice" + "\n")
    file_info = await bot.get_file(msg.voice.file_id)
    numb = file_info.file_path.split("_")
    numb = numb[1].split(".")
    numb = numb[0]
    print(numb)
    await file_info.download()
    file = open("input.txt", "w", encoding="utf-8")
    try:
        file.write(audioToString(file_info.file_path))
        file.close()
        result = constructMessage()
        os.remove(file_info.file_path)
        name = file_info.file_path[:(len(file_info.file_path) - 4)] + ".flac"
        os.remove(name)
    except:
        result = "Отправьте сообщение содержащее хоть какие-то слова"
    await bot.send_message(msg.from_user.id, result, parse_mode=ParseMode.MARKDOWN)


@dp.message_handler()
async def replyMessage(msg: types.Message):
    print(msg.text + "\n")
    file = open("input.txt", "w", encoding="utf-8")
    file.write(msg.text)
    file.close()
    result = constructMessage()
    await bot.send_message(msg.from_user.id, result, parse_mode=ParseMode.MARKDOWN)


if __name__ == '__main__':
    executor.start_polling(dp)
