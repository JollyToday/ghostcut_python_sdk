from typing import Optional
from pydantic import BaseModel, Field, model_validator, field_validator
from ghostcut_sdk.ghostcut_type.ghostcut_base_model import GhostcutBaseModel


class ImageExtraOptions(BaseModel):
    font_family: str


class DownloadInfo(BaseModel):
    url: str


class ImageTranslateRequest(GhostcutBaseModel):
    url: Optional[str] = Field(default=None, description="image url", exclude=True)
    src_lang: str = Field(description="source language", alias="srcLang")
    tgt_lang: str = Field(description="target language", alias="tgtLang")
    translate_on: int = Field(
        default=1, description="是否开启翻译，0关闭，1开启", alias="translateOn"
    )
    synthesis_on: int = Field(
        default=1, description="是否开启合成，0关闭，1开启", alias="synthesisOn"
    )
    commodity_filter_on: int = Field(
        default=0,
        description="是否开启商品过滤，0关闭，1开启",
        alias="commodityFilterOn",
    )
    callback: str = Field(default="", description="回调地址", alias="callback")
    extra_options: Optional[ImageExtraOptions] = Field(
        default=None, description="额外选项", alias="extraOptions"
    )
    download_info: Optional[DownloadInfo] = Field(
        default=None, description="下载信息", alias="downloadInfo"
    )

    @field_validator("translate_on", "synthesis_on", "commodity_filter_on")
    @classmethod
    def validate_on_off(cls, v: int):
        if v not in [0, 1]:
            raise ValueError(
                "translate_on, synthesis_on, commodity_filter_on must be 0 or 1"
            )
        return v

    @model_validator(mode="after")
    def validate_download_info(self):
        if self.download_info is None:
            if self.url is None:
                raise AttributeError(
                    "download_info and url can not be None at the same time"
                )
            else:
                self.download_info = DownloadInfo(url=self.url)


if __name__ == "__main__":
    image_translate_request = {
        "url": "https://www.baidu.com/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png",
        "srcLang": "zh",
        "tgtLang": "en",
        "translateOn": 1,
        "synthesisOn": 0,
        "commodityFilterOn": 1,
        "callback": "https://www.baidu.com",
        "extraOptions": {"font_family": "Arial"},
    }
    # req = ImageTranslateRequest.model_validate(image_translate_request)
    req = ImageTranslateRequest(**image_translate_request)
    print(f"req:\n\t{req}")
    print(f"{req.model_dump_json(indent=4, by_alias=True, exclude_none=True)}")

    req2 = ImageTranslateRequest(
        url="https://www.baidu.com/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png",
        src_lang="en",
        tgt_lang="ja",
        synthesis_on=0,
    )
    print(f"{req2.model_dump_json(indent=4, exclude_none=True, by_alias=True)}")
