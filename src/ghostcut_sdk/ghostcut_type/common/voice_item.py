from pydantic import Field
from ghostcut_sdk.ghostcut_type.ghostcut_base_model import (
    PopulateByNameGhostcutBaseModel,
)


class TtsVoiceItem(PopulateByNameGhostcutBaseModel):
    """TTS voice item model"""

    id: int = Field(..., description="Voice ID for API requests")
    language: str = Field(..., description="Language code")
    locale: str = Field(..., description="Language locale")
    is_advanced: int = Field(
        ...,
        alias="isAdvanced",
        description="Advanced voice flag: 1 for advanced, 0 for basic",
    )
    avatar_url: str = Field(..., alias="avatarUrl", description="Avatar URL")
    demo_text: str = Field(..., alias="demoText", description="Demo audio text")
    demo_url: str = Field(..., alias="demoUrl", description="Demo audio URL")
    display_name: str = Field(..., alias="displayName", description="Display name")
    display_name2: str = Field(..., alias="displayName2", description="Display name 2")
    display_name2_en: str = Field(
        ..., alias="displayName2En", description="Display name 2 English"
    )
    display_name_en: str = Field(
        ..., alias="displayNameEn", description="Display name English"
    )
    gender: str = Field(..., description="Gender: female or male")


class NaturalVoiceItem(PopulateByNameGhostcutBaseModel):
    """Natural voice item model"""

    id: int = Field(..., description="Voice ID for API requests")
    age_segment: str = Field(..., alias="ageSegment", description="Age segment")
    avatar_oss_key: str = Field(..., alias="avatarOssKey", description="Avatar OSS key")
    character: str = Field(..., description="Character description")
    deleted: int = Field(..., description="Deleted flag")
    demo_osskey: str = Field(..., alias="demoOsskey", description="Demo OSS key")
    demo_text: str = Field(..., alias="demoText", description="Demo audio text")
    demo_url: str = Field(..., alias="demoUrl", description="Demo audio URL")
    display_name: str = Field(..., alias="displayName", description="Display name")
    display_name2: str = Field(..., alias="displayName2", description="Display name 2")
    display_name2_en: str = Field(
        ..., alias="displayName2En", description="Display name 2 English"
    )
    display_name2_pt: str = Field(
        ..., alias="displayName2Pt", description="Display name 2 Portuguese"
    )
    display_name_en: str = Field(
        ..., alias="displayNameEn", description="Display name English"
    )
    display_name_pt: str = Field(
        ..., alias="displayNamePt", description="Display name Portuguese"
    )
    gender: str = Field(..., description="Gender: female or male")
    oss_bucket: str = Field(..., alias="ossBucket", description="OSS bucket name")
    oss_endpoint: str = Field(..., alias="ossEndpoint", description="OSS endpoint")
    prefix: str = Field(..., description="Prefix")
    ref_oss_info: str = Field(..., alias="refOssInfo", description="Reference OSS info")
    status: int = Field(..., description="Status flag")
    voice_status: int = Field(..., alias="voiceStatus", description="Voice status flag")
    ctime: int = Field(..., description="Creation timestamp")
    lutime: int = Field(..., description="Last update timestamp")
