# -*- coding: utf-8 -*-

# 3. 基础API 调用示例
# https://jollytoday.feishu.cn/docx/U73qdBhWbozFdpx4eTvcIO4gn7e#share-Mimndtw9NoMllNx09Ruc6V9nnEe

from typing import Optional, Union, Dict, Any

import requests
from  ghostcut_python_sdk.ghostcut.client import ZhaoliClient,ZhaoliAPIException
class BasicAPI:
    """
    基础API接口封装
    """

    def __init__(self, client: ZhaoliClient):
        self.client = client

    def query_enum(self, text: str) -> list:
        """
        3.1 查询枚举（无需签名）

        说明: 此接口无需加签，调用时不需传appId、timestamp、sign。

        :param text: 枚举名字，如 ProcessStatus、musicRegion、sourceLang等，忽略大小写
        :return: 枚举列表，每个元素为dict，包含code、description等信息
        """
        # 该接口不走网关，需要单独请求。根据文档地址：
        url = "https://api.zhaoli.com/v-w-c/enum/query2"

        import requests
        import json

        headers = {"Content-Type": "application/json"}
        payload = {"text": text}

        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=30)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            raise ZhaoliAPIException(-1, f"查询枚举请求异常: {str(e)}")

        code = data.get("code")
        if code != 1000:
            raise ZhaoliAPIException(code, data.get("msg", "未知错误"))

        return data.get("body", [])

    def create_sub_user(
        self,
        phone: Optional[str] = None,
        mail: Optional[str] = None,
        custom_identity: Optional[str] = None,
        uname: Optional[str] = None
    ) -> str:
        """
        3.2 创建子用户

        :param phone: 手机号，非必填
        :param mail: 邮箱，非必填
        :param custom_identity: 自定义唯一标识，非必填
        :param uname: 用户昵称，非必填
        :return: uid 子用户唯一标识
        :raises: ZhaoliAPIException
        """
        # 至少phone/mail/custom_identity三者之一必须传入，校验
        if not any([phone, mail, custom_identity]):
            raise ValueError("phone、mail、custom_identity 三者至少传一个")

        path = "/ve/user/create"
        params = {}
        if phone:
            params["phone"] = phone
        if mail:
            params["mail"] = mail
        if custom_identity:
            params["customIdentity"] = custom_identity
        if uname:
            params["uname"] = uname

        body = self.client.post(path, params)
        uid = body.get("uid")
        if not uid:
            raise ZhaoliAPIException(-1, "创建子用户接口未返回uid")
        return uid

    def query_balance(
        self,
        not_zero: Optional[bool] = False,
        is_valid: Optional[bool] = False
    ) -> dict:
        """
        3.3 查询余额

        :param not_zero: 是否仅包含余额>0的资产，默认False
        :param is_valid: 是否仅包含未过期的资产，默认False
        :return: pointAssets列表及余额详情字典
        """
        path = "/ve/point/query"
        params = {}
        if not_zero:
            params["notZero"] = True
        if is_valid:
            params["isValid"] = True

        # 空参数传空字典或空字符串均可，传params即可
        body = self.client.post(path, params or {})
        return body

    def get_tts_voice_list(
        self,
        is_advanced: Optional[int] = 0
    ) -> list:
        """
        3.5 获取TTS声音列表（基础/高级）

        :param is_advanced: 0基础音色，1高级音色，默认0
        :return: 声音列表数组
        """
        path = "/ve/tts/voice/list"
        params = {}
        if is_advanced in (0, 1):
            params["isAdvanced"] = is_advanced

        body = self.client.post(path, params or {})
        # body 可能是音色列表数组
        return body

    def get_tts_really_voice_list(
        self,
        page_number: int,
        page_size: Optional[int] = 20
    ) -> dict:
        """
        3.6 获取TTS声音列表（超真实）

        :param page_number: 页码，从1开始
        :param page_size: 每页条数，默认20
        :return: 响应字典，含content等字段
        """
        if page_number < 1:
            raise ValueError("page_number必须>=1")

        path = "/ve/voice/query_public_voice"
        params = {"pageNumber": page_number}
        if page_size and page_size > 0:
            params["pageSize"] = page_size

        body = self.client.post(path, params)
        return body

    def upload_local_file(self, file_path: str) -> dict:
        """
        3.4 本地文件上传（您未提供具体接口说明，以下为常见实现示例）
        说明：
        - 具体上传接口地址、参数需根据实际文档补充
        - 这里假设有一个上传接口，支持文件流POST上传

        :param file_path: 本地文件路径
        :return: 上传结果dict，含返回的文件标识等
        """
        # 示例接口地址和参数，需替换成真实接口
        url = "https://api.zhaoli.com/v-w-c/gateway/ve/file/upload"
        files = {"file": open(file_path, "rb")}
        # 需要鉴权参数时补充，简单示例：
        import time
        import hashlib
        import json

        app_id = self.client.app_id
        app_secret = self.client.app_secret
        timestamp = int(time.time() * 1000)

        # 简单签名示例（具体签名规则请根据实际接口调整）
        sign_str = f"appId={app_id}&timestamp={timestamp}&appSecret={app_secret}"
        sign = hashlib.md5(sign_str.encode("utf-8")).hexdigest()

        data = {
            "appId": app_id,
            "timestamp": timestamp,
            "sign": sign
        }

        try:
            resp = requests.post(url, files=files, data=data, timeout=60)
            resp.raise_for_status()
            result = resp.json()
        except Exception as e:
            raise ZhaoliAPIException(-1, f"文件上传失败: {e}")
        finally:
            files["file"].close()

        if result.get("code") != 1000:
            raise ZhaoliAPIException(result.get("code"), result.get("msg"))

        return result.get("body", {})

