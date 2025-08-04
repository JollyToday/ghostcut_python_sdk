# -*- coding: utf-8 -*-

"""
2.5 使用精修编辑器对配音结果再编辑
文档地址 ：https://jollytoday.feishu.cn/wiki/Y9JSwDDo8iVWN2k0IELc5nsMn3f#share-LgBXdc4sFoPahOxYNBcciNG5nwh
功能：
    1. 生成指定作品id的任务授权码
    2. 拼接精修编辑器授权URL并通过浏览器访问

接口地址：
    生成授权码：https://api.zhaoli.com/v-w-c/gateway/ve/work/auth/apply
请求方式：
    POST

授权码URL格式：
    https://{domain}/auth/editor?token={授权码}
    domain支持：
        - 中文版：cn.jollytoday.com
        - 英文版：jollytoday.com
        - 巴西版：br.jollytoday.com
"""

import requests
import webbrowser
from typing import Optional
from ghostcut_python_sdk.ghostcut.models.ghostcut_model import GhostCutModel


class GhostCutVoiceEditorAuthApplyRequest(GhostCutModel):
    """
    生成精修编辑器授权码请求模型
    """

    def __init__(
            self,
            id: Optional[int] = None,
            expireSeconds: int = 3600,
            allowClone: bool = False,
    ):
        """
        :param id: int, 必填，高情感克隆作品ID
        :param expireSeconds: int, 授权码过期时间，单位秒，范围0~604800，超出范围自动修正
        :param allowClone: bool, 是否开放私有配音角色声音，默认False
        """
        self.id = id
        self.expireSeconds = expireSeconds
        self.allowClone = allowClone

    def validate(self):
        """
        校验请求参数合法性，自动修正超范围expireSeconds
        """
        if self.id is None or not isinstance(self.id, int):
            raise ValueError("id 必填且必须为整数")
        if not isinstance(self.expireSeconds, int):
            raise ValueError("expireSeconds 必须为整数")
        if self.expireSeconds < 0:
            self.expireSeconds = 3600  # 小于范围使用默认3600秒
        elif self.expireSeconds > 604800:
            self.expireSeconds = 604800  # 大于范围使用最大604800秒
        if not isinstance(self.allowClone, bool):
            raise ValueError("allowClone 必须为布尔值")

    def to_dict(self) -> dict:
        """
        转换请求参数为字典
        """
        return {
            "id": self.id,
            "expireSeconds": self.expireSeconds,
            "allowClone": self.allowClone,
        }


class GhostCutVoiceEditorAuthApplyResponse:
    """
    生成精修编辑器授权码响应模型
    """

    def __init__(self, body: Optional[str] = None):
        """
        :param body: str，授权码，null表示授权失败
        """
        self.body = body

    @classmethod
    def from_dict(cls, data: dict):
        """
        从字典解析响应模型
        """
        body = data.get("body")
        return cls(body=body)


def generate_editor_auth_token(
        work_id: int,
        expire_seconds: int = 3600,
        allow_clone: bool = False,
) -> Optional[str]:
    """
    调用接口生成精修编辑器授权码

    :param work_id: 高情感克隆作品ID
    :param expire_seconds: 授权码过期时间，单位秒
    :param allow_clone: 是否开放私有配音角色声音
    :return: 授权码字符串，失败返回None
    """
    request_model = GhostCutVoiceEditorAuthApplyRequest(
        id=work_id,
        expireSeconds=expire_seconds,
        allowClone=allow_clone,
    )
    request_model.validate()
    request_data = request_model.to_dict()

    url = "https://api.zhaoli.com/v-w-c/gateway/ve/work/auth/apply"
    try:
        resp = requests.post(url, json=request_data, timeout=10)
        resp.raise_for_status()
        resp_json = resp.json()
    except Exception as e:
        print(f"请求授权码接口失败: {e}")
        return None

    response_model = GhostCutVoiceEditorAuthApplyResponse.from_dict(resp_json)
    if response_model.body:
        return response_model.body
    else:
        print("授权码生成失败，接口返回body为null")
        return None


def build_editor_url(token: str, language: str = "cn") -> str:
    """
    根据授权码和语言构造精修编辑器访问URL

    :param token: 授权码字符串
    :param language: 语言版本，支持 "cn"(中文), "en"(英文), "br"(巴西)
    :return: 编辑器访问URL
    """
    domain_map = {
        "cn": "cn.jollytoday.com",
        "en": "jollytoday.com",
        "br": "br.jollytoday.com",
    }
    domain = domain_map.get(language.lower(), "cn.jollytoday.com")
    return f"https://{domain}/auth/editor?token={token}"


def open_editor_in_browser(url: str):
    """
    使用默认浏览器打开编辑器链接
    """
    print(f"即将打开编辑器网页：{url}")
    webbrowser.open(url)
