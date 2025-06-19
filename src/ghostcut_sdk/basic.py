# 3. 基础API 调用示例
# https://jollytoday.feishu.cn/docx/U73qdBhWbozFdpx4eTvcIO4gn7e#share-Mimndtw9NoMllNx09Ruc6V9nnEe
from typing import Optional, Dict, List, Literal, Union, Any
from ghostcut_sdk.config.url import (
    DEFAULT_BASE_URL,
    BASIC_CREATE_SUB_USER_PATH,
    BASIC_QUERY_ENUM_PATH,
    BASIC_QUERY_BALANCE_PATH,
    BASIC_QUERY_TTS_VOICE_LIST_PATH,
    BASIC_QUERY_NATURAL_VOICE_LIST_PATH,
    BASIC_UPLOAD_LOCAL_FILE_PATH,
)
from ghostcut_sdk.ghostcut_type.basic import (
    TtsVoiceItem,
    NaturalVoiceItem,
    CreateSubUserRequest,
)
from ghostcut_sdk.api_base import BaseGhostcutApi
from ghostcut_sdk.exceptions import GhostcutApiException
from ghostcut_sdk.ghostcut_type.basic.point_asset import PointAsset


AvailableEnumText = Literal[
    "ProcessStatus", "sourceLang", "Lang", "ImageTaskStatus", "musicRegion"
]

# TODO 使用pydantic定义返回的类型
# TODO 英文注释


class BasicApi(BaseGhostcutApi):
    """
    基础API接口封装
    """

    def __init__(
        self,
        app_key: Optional[str] = None,
        app_secret: Optional[str] = None,
    ):
        super().__init__(app_key, app_secret)

    def create_sub_user(
        self,
        request: Union[CreateSubUserRequest, Dict[str, Any]],
    ) -> str:
        body = self.post(BASIC_CREATE_SUB_USER_PATH, request.to_dict())
        uid = body.get("uid")
        if not uid:
            raise GhostcutApiException(-1, "创建子用户接口未返回uid")
        return uid

    def query_enum(self, text: AvailableEnumText) -> Optional[List]:
        """
        3.1 查询枚举（无需签名）
        TODO 无需加签

        说明: 此接口无需加签，调用时不需传appId、timestamp、sign。

        :param text: 枚举名字，如 ProcessStatus、musicRegion、sourceLang等，忽略大小写
        :return: 枚举列表，每个元素为dict，包含code、description等信息
        """
        # 该接口不走网关，需要单独请求。根据文档地址：
        params = {"text": text}
        return self.post_without_sign(BASIC_QUERY_ENUM_PATH, params)

    def query_balance(
        self, not_zero: bool = False, is_valid: bool = False
    ) -> List[PointAsset]:
        """
        3.3 查询余额

        :param not_zero: 是否仅包含余额>0的资产，默认False
        :param is_valid: 是否仅包含未过期的资产，默认False
        :return: pointAssets列表及余额详情字典
        """
        params = {}
        if not_zero:
            params["notZero"] = True
        if is_valid:
            params["isValid"] = True

        # 空参数传空字典或空字符串均可，传params即可
        body = self.post(BASIC_QUERY_BALANCE_PATH, params or {})
        return [PointAsset(**item) for item in body]

    def query_tts_voice_list(self, is_advanced: bool = 0) -> List[TtsVoiceItem]:
        """
        3.5 获取TTS声音列表（基础/高级）

        :param is_advanced: 0基础音色，1高级音色，默认0
        :return: 声音列表数组
        """
        params = {"isAdvanced": 1 if is_advanced else 0}
        body = self.post(BASIC_QUERY_TTS_VOICE_LIST_PATH, params)
        # body 可能是音色列表数组
        return [TtsVoiceItem(**item) for item in body]

    def query_natural_voice_list(
        self,
        page_number: int = 1,
        page_size: int = 20,
        with_language_limit_voice: bool = False,
    ) -> List[NaturalVoiceItem]:
        """
        3.6 获取TTS声音列表（超真实）

        :param page_number: 页码，从1开始
        :param page_size: 每页条数，默认20
        :return: 响应字典，含content等字段
        """
        if page_number < 1:
            raise ValueError("page_number必须>=1")
        params = {
            "pageNumber": page_number,
            "pageSize": page_size,
            "withLanguageLimitVoice": with_language_limit_voice,
        }
        return [
            NaturalVoiceItem(**item)
            for item in self.post(BASIC_QUERY_NATURAL_VOICE_LIST_PATH, params)
        ]

    def upload_local_file(self, file_path: str) -> Dict:
        """
        TODO
        3.4 本地文件上传（您未提供具体接口说明，以下为常见实现示例）
        说明：
        - 具体上传接口地址、参数需根据实际文档补充
        - 这里假设有一个上传接口，支持文件流POST上传

        :param file_path: 本地文件路径
        :return: 上传结果dict，含返回的文件标识等
        """
        with open(file_path, "rb") as fp:
            files = {"file": fp}
            body = self.post(BASIC_UPLOAD_LOCAL_FILE_PATH, files=files)
        return body
