from enum import Enum
from pydantic import BaseModel


class PermissionType(Enum):
    USER_ID = "USER_ID"
    GROUP = "GROUP"
    ROLE = "ROLE"


class PermissionRequest(BaseModel):
    resource_id: str
    permission_type: PermissionType
    permission_id: str
    view: bool
    edit: bool
    delete: bool
    edit_permission: bool