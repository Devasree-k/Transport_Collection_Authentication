import asyncio
from getpass import getpass

from sqlalchemy import select

from app.core.security import hash_password
from app.database.connection import SessionLocal
from app.models.user_model import User


async def create_admin() -> None:
    username = input("Admin username: ").strip()
    email = input("Admin email: ").strip()
    password = getpass("Admin password (12+ characters): ")

    if len(password) < 12:
        print("Password must be at least 12 characters.")
        return

    async with SessionLocal() as db:
        existing = await db.scalar(
            select(User).where(
                (User.username == username)
                | (User.email == email)
            )
        )

        if existing is not None:
            print("A user with that username or email already exists.")
            return

        admin = User(
            username=username,
            email=email,
            hashed_password=hash_password(password),
            role="admin",
            is_active=True,
        )

        try:
            db.add(admin)
            await db.commit()
            print("Administrator created successfully.")
        except Exception:
            await db.rollback()
            raise


if __name__ == "__main__":
    asyncio.run(create_admin())