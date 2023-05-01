import asyncio
from handlers import user_handlers
from config_data.config import token
from aiogram import Bot, Dispatcher
import logging


async def main():
    API_TOKEN: str = token

    bot: Bot = Bot(token=API_TOKEN)
    dp: Dispatcher = Dispatcher()
    dp.include_router(user_handlers.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)



def logger():
    logging.basicConfig(level=logging.INFO)


    handler = logging.StreamHandler()
    handler.setLevel(logging.ERROR)


    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)


    logger = logging.getLogger('aiogram')
    logger.addHandler(handler)
logger()



if __name__ == '__main__':
    asyncio.run(main())
