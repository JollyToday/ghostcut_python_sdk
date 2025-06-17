from __future__ import annotations
from typing import Optional
from pydantic import Field, model_validator
from ghostcut_sdk.ghostcut_type.ghostcut_base_model import (
    PopulateByNameGhostcutBaseModel,
)


class CreateSubUserRequest(PopulateByNameGhostcutBaseModel):
    """Create sub user request model"""

    uname: Optional[str] = Field(default=None, description="User name")
    phone: Optional[str] = Field(default=None, description="Phone number")
    mail: Optional[str] = Field(default=None, description="Email address")
    custom_identity: Optional[str] = Field(
        default=None, alias="customIdentity", description="Custom identity"
    )

    @model_validator(mode="after")
    def validate_at_least_one_identifier(self) -> CreateSubUserRequest:
        """
        Validate at least one identifier (phone, mail, custom_identity) is not None

        Raises:
            ValueError: if all identifiers are None

        Returns:
            CreateSubUser: _description_
        """
        if not any([self.phone, self.mail, self.custom_identity]):
            raise ValueError("phone, mail, custom_identity can not all be None")
        return self
