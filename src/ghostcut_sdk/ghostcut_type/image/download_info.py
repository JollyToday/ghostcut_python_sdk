from typing import Optional
from pydantic import Field
from ghostcut_sdk.ghostcut_type.ghostcut_base_model import PopulateByNameGhostcutBaseModel


class DownloadInfo(PopulateByNameGhostcutBaseModel):
    """下载信息"""

    url: str = Field(..., description="download url")
    file_name: Optional[str] = Field(
        default=None, alias="fileName", description="file name"
    )
    id: Optional[int] = Field(default=None, description="file id")
    material_name: Optional[str] = Field(
        default=None, alias="materialName", description="material name"
    )
