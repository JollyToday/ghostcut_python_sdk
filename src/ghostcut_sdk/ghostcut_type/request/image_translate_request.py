from pydantic import BaseModel
from ghostcut_sdk.ghostcut_type.literals import OnOff


class ImageTranslateRequest(BaseModel):
    download_info: str
    src_lang: str
    tgt_lang: str
    translate_on: OnOff = 1
    synthesis_on: OnOff = 1
    commodity_filter_on: OnOff = 0
    callback: str = ""
    extra_options: dict | None = None
