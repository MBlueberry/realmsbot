import asyncio
import random

from aiogram import types
from aiogram.types import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from misc import dp, bot, allow_chats, group_error_msg, realms_link, first, third, second, valutamsg


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    # Проверка на группу
    if f'{message.chat.id}' not in allow_chats:
        return await message.reply(group_error_msg)

    text = f"Привет, {message.from_user.first_name}!"
    await message.answer(text, parse_mode=ParseMode.HTML)


@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    # Проверка на группу
    if f'{message.chat.id}' not in allow_chats:
        return await message.reply(group_error_msg)

    text = "Гайд к серверу: <code>!инфа</code>\n" \
           "Ссылка на сервер: <code>!сурв</code>\n" \
           "Сыграть в бан рулетку: <code>!бан рулетка</code>"
    await message.answer(text, parse_mode=ParseMode.HTML)


@dp.message_handler(commands=['сурв'], commands_prefix='!/')
async def surv(message: types.Message):
    # Проверка на группу
    if f'{message.chat.id}' not in allow_chats:
        return await message.reply(group_error_msg)

    t = f" ➤ Актуальная ссылка на сервер: {realms_link}"
    msg = await message.reply(t)
    kb = InlineKeyboardMarkup().add(InlineKeyboardButton('Закрыть', callback_data=f'close {msg.message_id}'
                                                                                  f' {message.from_user.id}'
                                                                                  f' {message.message_id}'))
    delay = 6 # Задержка удаления (*10 секунд) 6 = 60 секунд
    for i in range(0, delay):
        try:
            await msg.edit_text(t + f"\n\n<i>(Автоудаление через {(delay-i)*10} секунд)</i>",
                                parse_mode=ParseMode.HTML, reply_markup = kb)
            await asyncio.sleep(10)
        except Exception: break
    try: await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except Exception: pass
    try: await bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)
    except Exception: pass


@dp.message_handler(commands=['инфа'], commands_prefix='!')
async def infa(message: types.Message):
    # Проверка на группу
    if f'{message.chat.id}' not in allow_chats:
        return await message.reply(group_error_msg)

    msg = await message.reply("Привет, сейчас я расскажу тебе о нашем Realms")
    args = f' {msg.message_id} {message.from_user.id} {message.message_id}'
    # Готовим кнопки
    kb = InlineKeyboardMarkup(row_width=1)
    kb.insert(InlineKeyboardButton('Основные правила', callback_data=f'infa rules' + args))
    kb.insert(InlineKeyboardButton('О налогах', callback_data=f'infa nalogi' + args))
    kb.insert(InlineKeyboardButton('О паспорте', callback_data=f'infa pasport' + args))
    kb.insert(InlineKeyboardButton('Валюта', callback_data=f'infa valuta' + args))
    btn_close = InlineKeyboardButton('Закрыть', callback_data=f'close {msg.message_id}'
                                                              f' {message.from_user.id}'
                                                              f' {message.message_id}')
    kb.insert(btn_close)
    await asyncio.sleep(3)
    await msg.edit_text(text='Выберите то что Вас интересует', reply_markup=kb)


# КНОПКИ ОТ КОМАНДЫ ИНФА
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('infa'))
async def process_callback_infa(callback_query: types.CallbackQuery):
    args = str(callback_query.data).split()
    msg = args[2]
    sender_id = args[3]
    interactor_id = callback_query.from_user.id
    btn_close = InlineKeyboardButton('Закрыть', callback_data=f'close {args[2]}'
                                                f' {args[3]}'
                                                f' {args[4]}')
    kb = InlineKeyboardMarkup(row_width=1).add(btn_close)
    if f'{sender_id}' != f'{interactor_id}' or f'{interactor_id}' not in allow_chats: await bot.answer_callback_query(
        callback_query.id, text="Взаимодействовать с сообщением может только отправитель", show_alert=True)

    await bot.answer_callback_query(callback_query.id)
    if f'{args[1]}' == 'rules':
        text = random.choice(third)
        await bot.edit_message_text(text, chat_id=callback_query.message.chat.id, message_id=msg, reply_markup=kb)
    elif f'{args[1]}' == 'nalogi':
        text = random.choice(second)
        await bot.edit_message_text(text, chat_id=callback_query.message.chat.id, message_id=msg, reply_markup=kb)
    elif f'{args[1]}' == 'pasport':
        text = random.choice(first)
        await bot.edit_message_text(text, chat_id=callback_query.message.chat.id, message_id=msg, reply_markup=kb)
    elif f'{args[1]}' == 'valuta':
        text = random.choice(valutamsg)
        await bot.edit_message_text(text, chat_id=callback_query.message.chat.id, message_id=msg, reply_markup=kb)


# КНОПКА ЗАКРЫТЬ - УДАЛЯЕТ СООБЩЕНИЕ
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('close'))
async def process_callback_close(callback_query: types.CallbackQuery):
    msg = str(callback_query.data).split()
    sender_id = msg[2]
    deleter_id = callback_query.from_user.id
    if f'{sender_id}' == f'{deleter_id}' or f'{deleter_id}' in allow_chats:
        await bot.answer_callback_query(callback_query.id)
        try: await bot.delete_message(message_id=msg[1], chat_id = callback_query.message.chat.id)
        except Exception: pass
        await bot.delete_message(message_id=msg[3], chat_id = callback_query.message.chat.id)
    else: await bot.answer_callback_query(callback_query.id, text="Закрыть сообщение может только отправитель",
                                          show_alert=True)
