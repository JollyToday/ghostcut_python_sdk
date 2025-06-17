from pydantic import BaseModel, Field, field_validator, ConfigDict
from ghostcut_sdk.ghostcut_type.ghostcut_base_model import PopulateByNameGhostcutBaseModel


class ApplyAuthCodeRequest(PopulateByNameGhostcutBaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int = Field(description="task id", alias="id")
    expire_seconds: int = Field(
        default=3600,
        description="Authorization code expiration time in seconds. "
        "If expired, using the authorization code to access the editor will fail. Range: 0~604800. "
        "If less than this range, 3600 will be used. If greater than this range, 604800 will be used",
        alias="expireSeconds",
    )

    @field_validator("expire_seconds")
    @classmethod
    def validate_expire_seconds(cls, v: int) -> int:
        print(f"field validate: v: {v}")
        if v < 0:
            return 3600
        if v > 604800:
            return 604800
        return v


if __name__ == "__main__":
    for request in [
        ApplyAuthCodeRequest(id=123, expireSeconds=1000),
        ApplyAuthCodeRequest(id=123, expire_seconds=1000),
        ApplyAuthCodeRequest(id=123, expire_seconds=-1),
        ApplyAuthCodeRequest(id=123, expire_seconds=604801),
    ]:
        print(request.model_dump_json(indent=4, by_alias=True, exclude_none=True))
