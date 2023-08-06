from typing import Optional

from pydantic import BaseModel, root_validator, validator

from fief.crypto.encryption import decrypt
from fief.db.types import DatabaseType
from fief.errors import APIErrorCode
from fief.schemas.generics import UUIDSchema
from fief.settings import settings


def validate_all_database_settings(cls, values):
    database_type = values.get("database_type")
    database_settings = [
        values.get("database_host"),
        values.get("database_port"),
        values.get("database_username"),
        values.get("database_password"),
        values.get("database_name"),
    ]

    if database_type is None and not any(database_settings):
        return values

    if database_type is None and any(database_settings):
        raise ValueError(APIErrorCode.WORKSPACE_CREATE_MISSING_DATABASE_SETTINGS)

    database_name = values.get("database_name")
    if database_type == DatabaseType.SQLITE:
        if database_name is None:
            raise ValueError(APIErrorCode.WORKSPACE_CREATE_MISSING_DATABASE_SETTINGS)
    else:
        if not all(database_settings):
            raise ValueError(APIErrorCode.WORKSPACE_CREATE_MISSING_DATABASE_SETTINGS)

    return values


class WorkspaceCheckConnection(BaseModel):
    database_type: DatabaseType
    database_host: str
    database_port: int
    database_username: str
    database_password: str
    database_name: str

    _validate_all_database_settings = root_validator(allow_reuse=True)(
        validate_all_database_settings
    )


class WorkspaceCreate(BaseModel):
    name: str
    database_type: Optional[DatabaseType]
    database_host: Optional[str]
    database_port: Optional[int]
    database_username: Optional[str]
    database_password: Optional[str]
    database_name: Optional[str]

    _validate_all_database_settings = root_validator(allow_reuse=True)(
        validate_all_database_settings
    )


class BaseWorkspace(UUIDSchema):
    name: str
    domain: str


class Workspace(BaseWorkspace):
    database_type: Optional[DatabaseType]
    database_host: Optional[str]
    database_port: Optional[int]
    database_username: Optional[str]
    database_password: Optional[str]
    database_name: Optional[str]

    @validator(
        "database_host",
        "database_username",
        "database_password",
        "database_name",
        pre=True,
    )
    def decrypt_database_setting(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        return decrypt(value, settings.encryption_key)

    @validator("database_port", pre=True)
    def decrypt_database_port(cls, value: Optional[str]) -> Optional[int]:
        if value is None:
            return value
        return int(decrypt(value, settings.encryption_key))


class WorkspacePublic(BaseWorkspace):
    pass
