import asyncio
import random

import aiogram
from aiogram import types, exceptions
from aiogram.types import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from misc import dp, bot, allow_chats, group_error_msg

random.seed()


@dp.message_handler(commands=['банрулетка'], commands_prefix='!')
async def ban_ruletka(message: types.Message):
    # Проверка на группу
    if f'{message.chat.id}' not in allow_chats:
        return await message.reply(group_error_msg)

    await message.answer_photo(photo="https://imgur.com/HfxZRPC?r",
                                   caption="Крутим рулетку...")
    await asyncio.sleep(2)
    msg = await message.answer(text='Вам...')
    await asyncio.sleep(2)
    ban = random.randint(0, 1)
    if ban:
        await msg.edit_text(text='Вам бан!')
        await asyncio.sleep(2)
        try:
            await bot.kick_chat_member(user_id=message.from_user.id, chat_id=message.chat.id)
        except aiogram.utils.exceptions.NotEnoughRightsToRestrict:
            return await msg.edit_text(text='Вам бан! Но у меня нет права банить людей и вам повезло!')
        except aiogram.utils.exceptions.BadRequest:
            return await msg.edit_text(text='Вам бан! Но так как вы администратор вам повезло!')
    else:
        await msg.edit_text(text='Вам повезло, бан не выпал!')


