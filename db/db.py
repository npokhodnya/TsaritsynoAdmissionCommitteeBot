import aiosqlite as sq


async def initialize_database():
    async with sq.connect("bot.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                telegram_id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                role nvarchar(15) NOT NULL,
                bot_open BOOLEAN DEFAULT FALSE
            )
        """)
        await db.commit()


async def add_user(telegram_id: int, username: str):
    async with sq.connect("bot.db") as db:
        await db.execute("""
            INSERT INTO users (telegram_id, username, role)
            VALUES (?, ?, 'user')
            ON CONFLICT(telegram_id) DO NOTHING
        """, (telegram_id, username))
        await db.commit()


async def get_all_users():
    async with sq.connect("bot.db") as db:
        cursor = await db.execute("SELECT * FROM users")
        rows = await cursor.fetchall()
        users = [
            {
                "telegram_id": row[0],
                "username": row[1],
                "role": row[2],
                "bot_open": bool(row[3])
            }
            for row in rows
        ]
        return users


async def get_role_by_id(tg_id: int) -> str:
    async with sq.connect("bot.db") as db:
        cursor = await db.execute("SELECT role FROM Users where telegram_id == {}".format(tg_id))
        role = await cursor.fetchone()
        return role[0]


async def get_user_by_id(telegram_id: int) -> None | dict:
    async with sq.connect("bot.db") as db:
        cursor = await db.execute("SELECT * FROM Users WHERE telegram_id == ?", (telegram_id,))
        row = await cursor.fetchone()

        if row is None:
            return None
        user = {
            "telegram_id": row[0],
            "username": row[1],
            "role": row[2],
            "bot_open": bool(row[3])
        }
        return user


async def drop_all_closed():
    async with sq.connect("bot.db") as db:
        await db.execute("delete * FROM Users WHERE bot_open == 0")


async def count_of_users():
    async with sq.connect("bot.db") as db:
        cursor = await db.execute("Select count(telegram_id) FROM Users")
        count = await cursor.fetchone()
        return count[0]


async def count_of_closed_users():
    async with sq.connect("bot.db") as db:
        cursor = await db.execute("Select count(telegram_id) FROM Users WHERE bot_open == 0")
        count = await cursor.fetchone()
        return count[0]


async def drop_user_by_id(telegram_id: int):
    async with sq.connect("bot.db") as db:
        await db.execute("delete * FROM Users WHERE telegram_id = ?", (telegram_id,))


async def update_bot_open_status(telegram_id: int, bot_open: bool):
    async with sq.connect("bot.db") as db:
        await db.execute("""
            UPDATE users
            SET bot_open = ?
            WHERE telegram_id = ?
        """, (bot_open, telegram_id))
        await db.commit()


async def set_role(telegram_id: int, role: str):
    async with sq.connect("bot.db") as db:
        await db.execute("""
            UPDATE users
            SET role = ?
            WHERE telegram_id = ?
        """, (role, telegram_id))
        await db.commit()

async def change_bot_open_status(telegram_id: int, status: bool = True):
    async with sq.connect("bot.db") as db:
        await db.execute("""
            UPDATE users
            SET bot_open = ?
            WHERE telegram_id = ?
        """, (status, telegram_id))
        await db.commit()

async def is_admin(telegram_id: int):
    async with sq.connect("bot.db") as db:
        cursor = await db.execute("SELECT role FROM Users where telegram_id = {}".format(telegram_id))
        role = await cursor.fetchone()
        return role[0] in ["admin", "superadmin", 'developer']
