from app.db.base import Base
from app.models.mixins import TimestampedMixin, UUIDMixin, AbstractTelegramUser


class TelegramUser(UUIDMixin, TimestampedMixin, AbstractTelegramUser, Base):
    """Модель телеграм пользователя"""

    __tablename__ = "telegram_users"

    def __repr__(self) -> str:
        return f"Пользователь: {self.user_id}"
