from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
import aioschedule
import asyncio
from parser import parser
from config import bot_token


bot = Bot(token=bot_token, parse_mode='HTML')
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_command(msg: types.Message):
    """Обработка команды старт"""
    
    
    
    user_id = msg.from_id
    result = await check_user_in_db(str(user_id))
    if result is None:
        await msg.answer('Бот присылающий уведомления с сайта Apple Gaming Wiki.\nОбновления приходят раз в день в 19:00 по МСК. Если нужно получить список изменений за последние дни, напишите просто число дней.')
        await write_user_id(user_id)
    else:
        await msg.answer('Не балуй. Ты уже есть в списке на рассылку. ')
    
async def check_user_in_db(user_id):
    """Проверка наличия пользователя в так называемой базе данных :)
    
    Keyword arguments:
    user_id -- Айди пользователя
    Return: результат
    """
    
    
    result = None
    try:
        with open('users.txt', 'r') as file:
            for f in file:
                if user_id == f[:-1]:
                    result = 'Not None'
                    break
                
        return result
    except:
        return None
    
async def write_user_id(user_id):
    """Записываем айди пользователя в файл
    
    Keyword arguments:
    user_id -- айди пользователя
    """
    
    
    with open('users.txt', 'a') as file:
        file.write(f'{user_id}\n' )
        
async def send_new_records(user_id=None, days='1'):
    """отправка новых записей пользовтелю/пользователям
    
    Keyword arguments:
    user_id -- айди пользователя
    days -- количество дней за какое надо получить записи
    """
    
    if user_id:
        users_id = []
        users_id.append(user_id)
    else:
        users_id = await get_users_id()
    new_records = parser(days)
    if new_records == []:
        message = 'К сожалению новых записей сегодня нет.'
    else:
        message = await make_message(new_records)
    for user in users_id:
        await bot.send_message(user, message)
        
async def make_message(new_records):
    """Формируем сообщение
    
    Keyword arguments:
    new_records -- список новых записей
    Return: сформированное сообщение с новыми записями для отправки пользователям
    """
    
    records = []
    for record in new_records:
        title = record['record_title']
        url = record['record_url']
        records.append(f'<a href="{url}">{title}</a>\n')
    message = ' '.join(records)
    
    return message

@dp.message_handler(Text)
async def get_last_records(msg: types.message):
    """Обработка количества дней за которое надо отправить сообщение"""
    
    days = msg.text
    user_id = msg.from_id
    try:
        int(days)
        await send_new_records(user_id, days)
    except:
        await msg.answer(f'Это по твоему число? ну серьезно. \nКак вот это - "<b>{days}</b>" можно принять за количество дней, ты что дурной?')
    
async def get_users_id():
    """Получаем айди пользователей для рассылки
    
    Keyword arguments:
    Return: список пользователей
    """
    
    users_id = []
    with open('users.txt', 'r') as file:
        for f in file:
            users_id.append(f[:-1])
            
    return users_id
        
async def scheduler():
    """Расписание рассылки"""
    
    aioschedule.every().day.at('19:00').do(send_new_records)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
        
async def on_startup(_):
    """Выполнение задания при старте бота"""
    asyncio.create_task(scheduler())



if __name__=='__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)