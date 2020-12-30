from time import strftime, localtime

import discord
from asyncio import sleep

from config import SEND_TIME, SEND_MESSAGE, SEND_IMG, SEND_IDS, TOKEN


# Функция текущее время
def time_now():
    return strftime('%d.%m.%Y-%H:%M', localtime())


class CLient(discord.Client):
    # Инициализация фоновой задачи my_background_task
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bg_task = self.loop.create_task(self.my_background_task())

    # Функция реакции на старт бота
    async def on_ready(self):
        print(f'Запущен, как {self.user.name}')

    # Функция реакции на сообщения
    async def on_message(self, message):

        # Исключаем реакцию бота на самого себя
        if message.author.id == self.user.id:
            return

        # Реакция на команду "проверка"
        if message.content.startswith('проверка'):
            text = f'Сообщение:\n{SEND_MESSAGE}\nБудет отправлено следующим:\n'
            for user_id in SEND_IDS:
                user1 = str(self.get_user(user_id))
                text = text + user1 + '\n'
            await message.channel.send(text)

        # Реакция на команду !
        if message.content.startswith('!hhh'):
            await message.channel.send(f'Hello {message.author.mention}')
            for user_id in SEND_IDS:
                user = self.get_user(user_id)
                await user.create_dm()
                await user.send(SEND_MESSAGE)

    # Фоновая задача
    async def my_background_task(self):
        await self.wait_until_ready()
        while not self.is_closed():
            if time_now() == SEND_TIME:
                for user_id in SEND_IDS:
                    user = await self.fetch_user(user_id)
                    await user.create_dm()
                    embed = discord.Embed(color=0x72BAB6,
                                          title=SEND_MESSAGE)  # Создание оформления
                    embed.set_image(url=SEND_IMG)  # Устанавливаем картинку
                    await user.send(embed=embed)
                    print('Отпраляю сообщения')
            await sleep(60)  # Задача запускается каждые 60 секунд


if __name__ == '__main__' or True:
    client = CLient()
    client.run(TOKEN)
