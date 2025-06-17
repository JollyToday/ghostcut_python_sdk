import json
from typing import Union
from pydantic import Field, field_validator
from ghostcut_sdk.ghostcut_type.ghostcut_base_model import PopulateByNameGhostcutBaseModel
from ghostcut_sdk.ghostcut_type.error_info import ErrorInfo
from .image_translate_result import ImageTranslateResult
from .download_info import DownloadInfo


class TaskStatusEnum(PopulateByNameGhostcutBaseModel):
    """任务状态枚举"""

    code: int = Field(..., description="状态码")
    description: str = Field(..., description="中文描述")
    description_en: str = Field(alias="descriptionEn", description="英文描述")
    description_pt: str = Field(alias="descriptionPt", description="葡萄牙语描述")


class ImageTranslateResponse(PopulateByNameGhostcutBaseModel):
    """Image translation response"""

    app: str = Field(..., description="Application identifier")
    callback: str = Field(default="", description="Callback URL")
    commodity_filter_on: int = Field(
        alias="commodityFilterOn", description="Commodity filter switch"
    )
    company: str = Field(..., description="Company identifier")
    ctime: int = Field(..., description="Creation timestamp")
    deleted: int = Field(..., description="Delete flag")
    download_info: DownloadInfo = Field(
        alias="downloadInfo", description="Download info"
    )
    examine_status: str = Field(alias="examineStatus", description="Review status")
    extra_options: str = Field(alias="extraOptions", description="Extra options")
    id: int = Field(..., description="Task ID")
    id_project: int = Field(alias="idProject", description="Project ID")
    is_free_trial: int = Field(
        alias="isFreeTrial", description="Whether it's free trial"
    )
    lutime: int = Field(..., description="Last update timestamp")
    oss_deleted: int = Field(
        alias="ossDeleted",
        description="OSS delete flag, 0 means not deleted, 1 means deleted",
    )
    paid_point: float = Field(alias="paidPoint", description="Paid points")
    # priority: int = Field(..., description="Priority")
    result: Union[ImageTranslateResult, ErrorInfo] = Field(
        ..., description="Translation result"
    )
    src_lang: str = Field(alias="srcLang", description="Source language, e.g. 'zh'")
    status: int = Field(..., description="Task status")
    synthesis_on: int = Field(alias="synthesisOn", description="Synthesis switch")
    task_status_enum: TaskStatusEnum = Field(
        alias="taskStatusEnum", description="Task status enumeration"
    )
    tgt_lang: str = Field(alias="tgtLang", description="Target language, e.g. 'en'")
    translate_on: int = Field(alias="translateOn", description="Translation switch")
    uid: str = Field(..., description="User ID")

    @field_validator("result", mode="before")
    @classmethod
    def validate_result(
        cls, v: Union[str, ImageTranslateResult, ErrorInfo]
    ) -> Union[ImageTranslateResult, ErrorInfo]:
        """验证并转换result字段"""
        if isinstance(v, (ImageTranslateResult, ErrorInfo)):
            return v
        elif isinstance(v, str):
            try:
                data = json.loads(v)
                if "error" in data:
                    return ErrorInfo(**data)
                else:
                    return ImageTranslateResult(**data)
            except (json.JSONDecodeError, ValueError) as e:
                raise ValueError(f"Invalid result JSON string: {e}")
        else:
            raise ValueError(
                "result must be a JSON string or ImageTranslateResult object"
            )

    @field_validator("download_info", mode="before")
    @classmethod
    def validate_download_info(cls, v: str) -> DownloadInfo:
        if isinstance(v, str):
            return DownloadInfo(**json.loads(v))
        return v