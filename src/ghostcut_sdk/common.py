# 3. 基础API 调用示例
# https://jollytoday.feishu.cn/docx/U73qdBhWbozFdpx4eTvcIO4gn7e#share-Mimndtw9NoMllNx09Ruc6V9nnEe
from typing import Optional, Dict, List, Literal
from ghostcut_sdk.config.path import (
    DEFAULT_BASE_URL,
    CREATE_SUB_USER_PATH,
    QUERY_ENUM_PATH,
    QUERY_BALANCE_PATH,
    QUERY_TTS_VOICE_LIST_PATH,
    QUERY_NATURAL_VOICE_LIST_PATH,
    UPLOAD_LOCAL_FILE_PATH,
)
from ghostcut_sdk.ghostcut_type import IsAdvanced
from ghostcut_sdk.client import BaseGhostcutApi
from ghostcut_sdk.exceptions import GhostcutApiException


AvailableEnumText = Literal[
    "ProcessStatus", "sourceLang", "Lang", "ImageTaskStatus", "musicRegion"
]

# TODO 使用pydantic定义返回的类型
# TODO 英文注释

class CommonApi(BaseGhostcutApi):
    """
    基础API接口封装
    """
    def __init__(
        self,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        base_url: str = DEFAULT_BASE_URL,
    ):
        super().__init__(api_key, api_secret, base_url)

    def create_sub_user(
        self,
        phone: Optional[str] = None,
        mail: Optional[str] = None,
        custom_identity: Optional[str] = None,
        uname: Optional[str] = None,
    ) -> str:
        """
        3.2 创建子用户

        :param phone: 手机号，非必填
        :param mail: 邮箱，非必填
        :param custom_identity: 自定义唯一标识，非必填
        :param uname: 用户昵称，非必填
        :return: uid 子用户唯一标识
        :raises: GhostcutApiException
        """
        # 至少phone/mail/custom_identity三者之一必须传入，校验
        if not any([phone, mail, custom_identity]):
            raise ValueError("phone、mail、custom_identity 三者至少传一个")

        path = CREATE_SUB_USER_PATH
        params = {}
        if phone:
            params["phone"] = phone
        if mail:
            params["mail"] = mail
        if custom_identity:
            params["customIdentity"] = custom_identity
        if uname:
            params["uname"] = uname

        body = self.post(path, params)
        uid = body.get("uid")
        if not uid:
            raise GhostcutApiException(-1, "创建子用户接口未返回uid")
        return uid

    def query_enum(self, text: AvailableEnumText) -> Optional[List]:
        """
        3.1 查询枚举（无需签名）

        说明: 此接口无需加签，调用时不需传appId、timestamp、sign。

        :param text: 枚举名字，如 ProcessStatus、musicRegion、sourceLang等，忽略大小写
        :return: 枚举列表，每个元素为dict，包含code、description等信息
        """
        # 该接口不走网关，需要单独请求。根据文档地址：
        path = QUERY_ENUM_PATH
        params = {"text": text}
        return self.post(path, params, use_auth=False)

    def query_balance(self, not_zero: bool = False, is_valid: bool = False) -> Dict:
        """
        3.3 查询余额

        :param not_zero: 是否仅包含余额>0的资产，默认False
        :param is_valid: 是否仅包含未过期的资产，默认False
        :return: pointAssets列表及余额详情字典
        """
        path = QUERY_BALANCE_PATH
        params = {}
        if not_zero:
            params["notZero"] = True
        if is_valid:
            params["isValid"] = True

        # 空参数传空字典或空字符串均可，传params即可
        body = self.post(path, params or {})
        return body

    def query_tts_voice_list(self, is_advanced: IsAdvanced = 0) -> List:
        """
        3.5 获取TTS声音列表（基础/高级）

        :param is_advanced: 0基础音色，1高级音色，默认0
        :return: 声音列表数组
        """
        path = QUERY_TTS_VOICE_LIST_PATH
        params = {}
        params["isAdvanced"] = min(max(is_advanced, 0), 1)

        body = self.post(path, params or {})
        # body 可能是音色列表数组
        return body

    def query_natural_voice_list(
        self, page_number: int = 1, page_size: int = 20
    ) -> Dict:
        """
        3.6 获取TTS声音列表（超真实）

        :param page_number: 页码，从1开始
        :param page_size: 每页条数，默认20
        :return: 响应字典，含content等字段
        """
        if page_number < 1:
            raise ValueError("page_number必须>=1")

        path = QUERY_NATURAL_VOICE_LIST_PATH
        params = {"pageNumber": page_number}
        if page_size and page_size > 0:
            params["pageSize"] = page_size
        return self.post(path, params)

    def upload_local_file(self, file_path: str) -> Dict:
        """
        3.4 本地文件上传（您未提供具体接口说明，以下为常见实现示例）
        说明：
        - 具体上传接口地址、参数需根据实际文档补充
        - 这里假设有一个上传接口，支持文件流POST上传

        :param file_path: 本地文件路径
        :return: 上传结果dict，含返回的文件标识等
        """
        path = UPLOAD_LOCAL_FILE_PATH
        with open(file_path, "rb") as fp:
            files = {"file": fp}
            body = self.post(path, files=files)
        return body
