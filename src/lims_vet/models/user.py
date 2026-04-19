from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Enum
import enum
from .base import Base, UUIDMixin

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    MEDICO = "medico"
    AUXILIAR = "auxiliar"

class User(Base, UUIDMixin):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False, default=UserRole.AUXILIAR)
    full_name: Mapped[str] = mapped_column(String(255), nullable=True)