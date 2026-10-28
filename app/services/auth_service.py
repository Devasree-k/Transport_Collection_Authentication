from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.user_model import User
from app.repositories.interfaces.user_repository_interface import (
    UserRepositoryInterface,
)
from app.schemas.auth_schema import RegisterRequest
from app.exceptions.custom_exception import AuthenticationError,RegistrationConflict

class AuthService:

    def __init__(self, db: AsyncSession,
        users: UserRepositoryInterface,
    ) -> None:
        self.db = db
        self.users = users

    async def register(self, data: RegisterRequest) -> User:
        if await self.users.get_by_username(data.username):
            raise RegistrationConflict(
                "Username is already registered."
            )

        email = str(data.email)
        if await self.users.get_by_email(email):
            raise RegistrationConflict(
                "Email is already registered."
            )

        user = User(
            username=data.username,
            email=email,
            hashed_password=hash_password(data.password),
            role="driver",
            is_active=True,
        )

        try:
            await self.users.create(user)
            await self.db.commit()
            await self.db.refresh(user)
        except IntegrityError as exc:
            await self.db.rollback()
            raise RegistrationConflict(
                "Username or email is already registered."
            ) from exc

        return user

    async def authenticate(
        self,
        username: str,
        password: str,
    ) -> User:
        user = await self.users.get_by_username(username)

        if user is None:
            raise AuthenticationError(
                "Invalid username or password."
            )

        if not verify_password(password, user.hashed_password):
            raise AuthenticationError(
                "Invalid username or password."
            )

        if not user.is_active:
            raise AuthenticationError(
                "Invalid username or password."
            )

        return user

    async def issue_access_token(self, user: User) -> dict[str, str]:
        return {
            "access_token": create_access_token(user.id, user.role),
            "token_type": "bearer",
        }

    async def login(
        self,
        username: str,
        password: str,
    ) -> dict[str, str]:
        user = await self.authenticate(username, password)

        return await self.issue_access_token(user)
