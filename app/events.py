from app.db import database


async def startup():
    await database.connect()


async def shutdown():
    await database.disconnect()
