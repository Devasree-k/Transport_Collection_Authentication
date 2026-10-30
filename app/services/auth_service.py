from datetime import datetime, timedelta, timezone
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import REFRESH_TOKEN_EXPIRE_DAYS
from app.core.security import (create_access_token, create_refresh_token,
    hash_password, hash_refresh_token, verify_password)
from app.exceptions.custom_exception import AuthenticationError, RegistrationConflict
from app.models.refresh_token_model import RefreshToken
from app.models.user_model import User
from app.repositories.interfaces.user_repository_interface import UserRepositoryInterface
from app.repositories.interfaces.refresh_token_repository_interface import RefreshTokenRepositoryInterface
from app.schemas.auth_schema import RegisterRequest
import uuid


class AuthService:
    def __init__(self, db: AsyncSession, users: UserRepositoryInterface,
                 refresh_tokens: RefreshTokenRepositoryInterface) -> None:
        self.db = db
        self.users = users
        self.refresh_tokens = refresh_tokens

    async def register(self, data: RegisterRequest) -> User:

        if await self.users.get_by_username(data.username):
            raise RegistrationConflict("Username is already registered.")
        
        email = str(data.email)
        if await self.users.get_by_email(email):
            raise RegistrationConflict("Email is already registered.")
        
        user = User(username=data.username, 
                    email=email,
                    hashed_password=hash_password(data.password),
                    role="driver", 
                    is_active=True
                    )
        
        try:
            await self.users.create(user)
            await self.db.commit()
            await self.db.refresh(user)
        except IntegrityError as exc:
            await self.db.rollback()
            raise RegistrationConflict("Username or email is already registered.") from exc
        return user

    async def authenticate(self, username: str, password: str) -> User:
        user = await self.users.get_by_username(username)

        if (user is None or not verify_password(password, user.hashed_password)
                or not user.is_active):
            raise AuthenticationError("Invalid username or password.")
        
        return user

    async def _issue_token_pair(self, user: User) -> dict[str, str]:
        raw_refresh = create_refresh_token()
        jti = str(uuid.uuid4())

        refresh_record = RefreshToken(
            user_id=user.id,
            jti=jti,
            token_hash=hash_refresh_token(raw_refresh),
            expires_at=datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        )
        await self.refresh_tokens.create(refresh_record)
        await self.db.commit()
        return {"access_token": create_access_token(user.id, user.role),
                "refresh_token": raw_refresh, "token_type": "bearer"}

    async def login(self, username: str, password: str) -> dict[str, str]:
        user = await self.authenticate(username, password)
        return await self._issue_token_pair(user)

    async def refresh(self, raw_token: str) -> dict[str, str]:

        record = await self.refresh_tokens.get_by_hash(hash_refresh_token(raw_token))
        now = datetime.now(timezone.utc)

        if record is None or record.revoked:
            raise AuthenticationError("Invalid or revoked refresh token.")
        expires_at = record.expires_at

        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)

        if expires_at <= now:
            record.revoked = True
            await self.db.commit()
            raise AuthenticationError("Refresh token has expired.")
        
        user = await self.users.get_by_id(record.user_id)
        if user is None or not user.is_active:
            raise AuthenticationError("User is unavailable.")
        # Rotate: revoke the old token before issuing a replacement.

        record.revoked = True
        result = await self._issue_token_pair(user)
        return result

    async def logout(self, raw_token: str) -> None:
        record = await self.refresh_tokens.get_by_hash(hash_refresh_token(raw_token))
        if record is None or record.revoked:
            raise AuthenticationError("Invalid or already revoked refresh token.")
        record.revoked = True
        await self.db.commit()
