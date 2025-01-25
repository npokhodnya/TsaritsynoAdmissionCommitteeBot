import csv
import pandas as pd
import aiosqlite as sq


class Database:
    def __init__(self, db_path="bot_db.db"):
        self.db_path = db_path
    async def initialize_database(self):
        async with sq.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS Users_t1  (
                    telegram_id  INTEGER PRIMARY KEY,
                    username TEXT,
                    role_id INTEGER NOT NULL,
                    bot_open BOOLEAN DEFAULT FALSE
                );
            """)
            await db.commit()
        async with sq.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS Users_t2 (
                    role_id INTEGER PRIMARY KEY,
                    role TEXT NOT NULL 
                );
            """)
            await db.commit()
        async with sq.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO Users_t2 (role_id, role)
                VALUES (0, 'user'), (1, 'admin'), (2, 'super-admin'), (3, 'developer')
                ON CONFLICT(role_id) DO NOTHING
            """)
            await db.commit()


    async def add_user(self, telegram_id: int, username: str):
        async with sq.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO Users_t1 (telegram_id, username, role_id)
                VALUES (?, ?, 0)
                ON CONFLICT(telegram_id) DO NOTHING
            """, (telegram_id, username))
            await db.commit()


    async def get_csv(self):
        async with sq.connect(self.db_path) as db:
            cursor = await db.execute("""
            SELECT telegram_id, username, bot_open, role
            FROM Users_t1
            JOIN Users_t2 on Users_t1.role_id = Users_t2.role_id
            """)
            data = await cursor.fetchall()
            with open('db_csv.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([i[0] for i in cursor.description])  # Write header
                writer.writerows(data)
                cursor.close()


    async def get_xlsx(self):
        async with sq.connect(self.db_path) as db:
            df = pd.read_csv("db_csv.csv")
            df.to_excel('db_xlsx.xlsx', index=False)


    async def get_all_users(self):
        async with sq.connect(self.db_path) as db:
            cursor = await db.execute("SELECT * FROM Users_t1")
            rows = await cursor.fetchall()
            users = [
                {
                    "telegram_id": row[0],
                    "username": row[1],
                    "role_id": row[2],
                    "bot_open": bool(row[3])
                }
                for row in rows
            ]
            return users


    async def get_all_sadmins(self):
        async with sq.connect(self.db_path) as db:
            cursor = await db.execute("SELECT * FROM Users_t1 where role_id > 1")
            rows = await cursor.fetchall()
            users = [
                {
                    "telegram_id": row[0],
                    "username": row[1],
                    "role_id": row[2],
                    "bot_open": bool(row[3])
                }
                for row in rows
            ]
            return users


    async def get_role_by_id(self, telegram_id: int) -> str:
        async with sq.connect(self.db_path) as db:
            cursor = await db.execute("""
            SELECT role 
            FROM Users_t2 
            join Users_t1 on Users_t2.role_id = Users_t1.role_id 
            where telegram_id == {}
            """.format(telegram_id))
            role = await cursor.fetchone()
            return role[0]


    async def get_user_by_id(self, telegram_id: int) -> None | dict:
        async with sq.connect(self.db_path) as db:
            cursor = await db.execute("SELECT * FROM Users_t1 WHERE telegram_id == ?", (telegram_id,))
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


    async def drop_all_closed(self):
        async with sq.connect(self.db_path) as db:
            await db.execute("delete FROM Users_t1 WHERE bot_open == 0")


    async def count_of_users(self):
        async with sq.connect(self.db_path) as db:
            cursor = await db.execute("Select count(telegram_id) FROM Users_t1")
            count = await cursor.fetchone()
            return count[0]


    async def count_of_closed_users(self):
        async with sq.connect(self.db_path) as db:
            cursor = await db.execute("Select count(telegram_id) FROM Users_t1 WHERE bot_open = 0")
            count = await cursor.fetchone()
            return count[0]


    async def drop_user_by_id(self, telegram_id: int):
        async with sq.connect(self.db_path) as db:
            await db.execute("delete * FROM Users_t1 WHERE telegram_id = ?", (telegram_id,))


    async def update_bot_open_status(self, telegram_id: int, bot_open: bool):
        async with sq.connect(self.db_path) as db:
            await db.execute("""
                UPDATE Users_t1
                SET bot_open = ?
                WHERE telegram_id = ?
            """, (bot_open, telegram_id))
            await db.commit()


    async def set_role(self, telegram_id: int, role: int):
        async with sq.connect(self.db_path) as db:
            await db.execute("""
                UPDATE Users_t1
                SET role_id = ?
                WHERE telegram_id = ?
            """, (role, telegram_id))
            await db.commit()


    async def change_bot_open_status(self, telegram_id: int, status: bool = True):
        async with sq.connect(self.db_path) as db:
            await db.execute("""
                UPDATE Users_t1
                SET bot_open = ?
                WHERE telegram_id = ?
            """, (status, telegram_id))
            await db.commit()


    async def is_admin(self, telegram_id: int):
        async with sq.connect(self.db_path) as db:
            cursor = await db.execute("""
            SELECT role 
            FROM Users_t2 
            join Users_t1 on Users_t2.role_id = Users_t1.role_id 
            where telegram_id = {}
            """.format(telegram_id))
            role = await cursor.fetchone()
            return role[0] in ["admin", "super-admin", 'developer']


    async def is_super_admin(self, telegram_id: int):
        async with sq.connect(self.db_path) as db:
            cursor = await db.execute("""
            SELECT role 
            FROM Users_t2 
            join Users_t1 on Users_t2.role_id = Users_t1.role_id 
            where telegram_id == {}""".format(telegram_id))
            role = await cursor.fetchone()
            return role[0] in ["super-admin", 'developer']


    async def is_developer(self, telegram_id):
        async with sq.connect(self.db_path) as db:
            cursor = await db.execute("""
            SELECT role 
            FROM Users_t2 
            join Users_t1 on Users_t2.role_id = Users_t1.role_id 
            where telegram_id == {}""".format(telegram_id))
            role = await cursor.fetchone()
            return role[0] == "developer"
