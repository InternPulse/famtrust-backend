"""Models for external auth service."""

from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel, EmailStr


class Role(BaseModel):
    """Role model for external auth service."""
    id: str
    permissions: List[str]


class User(BaseModel):
    """User model for external auth service."""
    id: UUID
    email: EmailStr
    role: Role
    defaultGroup: UUID
    has2FA: bool
    isVerified: bool
    isFreezed: bool  # TODO: Change to isFrozen once the API is updated
    lastLogin: datetime
    isAdmin: bool
