# -*- coding: utf-8 -*-

"""
2.1 提交视频克隆任务（高情感）的请求模型
文档地址： https://jollytoday.feishu.cn/wiki/Y9JSwDDo8iVWN2k0IELc5nsMn3f#share-Ow9Zd7BR9oC4fLx9dGfcuXuXntc

接口地址：https://api.zhaoli.com/v-w-c/gateway/ve/work/voice/incorporate
请求方式：POST

请求参数说明：
- urls: List[str]，必填，待处理视频URL数组，目前每次支持传1个视频
- incorporatePro: bool，必填，是否开启情感加强，true开启
- names: Optional[List[str]]，可选，给urls对应生成作品的命名
- extraOptions: str，必填，声音文件配置项，json字符串，包含角色标注文件url或content
- lang: str，必填，目标语言代码，如'en'
- sourceLang: str，必填，源语言代码，如'en'
- callback: Optional[str]，回调地址url，可选
"""

from typing import Optional, List
from ghostcut_python_sdk.ghostcut.models.ghostcut_model import GhostCutModel
import json


class GhostCutHighEmotionCloneTaskSubmitRequest(GhostCutModel):
    def __init__(
            self,
            urls: Optional[List[str]] = None,
            incorporatePro: bool = True,
            names: Optional[List[str]] = None,
            extraOptions: Optional[str] = None,
            lang: Optional[str] = None,
            sourceLang: Optional[str] = None,
            callback: Optional[str] = None,
    ):
        """
        :param urls: List[str], 必填，视频URL数组，目前每次支持传1个视频
        :param incorporatePro: bool, 必填，是否开启情感加强，true开启
        :param names: Optional[List[str]], 非必填，作品命名列表
        :param extraOptions: str, 必填，声音文件配置项JSON字符串，必须包含customer_input.url或customer_input.content
        :param lang: str, 必填，目标语言代码
        :param sourceLang: str, 必填，源语言代码
        :param callback: str, 可选，回调地址URL
        """
        self.urls = urls or []
        self.incorporatePro = incorporatePro
        self.names = names or []
        self.extraOptions = extraOptions
        self.lang = lang
        self.sourceLang = sourceLang
        self.callback = callback

    def validate(self):
        if not self.urls or not isinstance(self.urls, list) or len(self.urls) != 1:
            raise ValueError("urls 必填且为长度为1的列表")
        if not isinstance(self.incorporatePro, bool):
            raise ValueError("incorporatePro 必须为布尔类型")
        if self.names and not isinstance(self.names, list):
            raise ValueError("names 必须为列表类型")
        if not self.extraOptions:
            raise ValueError("extraOptions 为必填，且必须是JSON字符串")
        else:
            try:
                extra_opts_dict = json.loads(self.extraOptions)
            except Exception:
                raise ValueError("extraOptions 必须是合法的JSON字符串")
            # 校验customer_input中必须有url或content
            customer_input = extra_opts_dict.get("customer_input", {})
            if not ("url" in customer_input or "content" in customer_input):
                raise ValueError("extraOptions 中 customer_input 必须包含 url 或 content 之一")
        if not self.lang or not isinstance(self.lang, str):
            raise ValueError("lang 必填且为字符串")
        if not self.sourceLang or not isinstance(self.sourceLang, str):
            raise ValueError("sourceLang 必填且为字符串")
        if self.callback and not isinstance(self.callback, str):
            raise ValueError("callback 必须为字符串")

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        data = {
            "urls": self.urls,
            "incorporatePro": self.incorporatePro,
            "extraOptions": self.extraOptions,
            "lang": self.lang,
            "sourceLang": self.sourceLang,
        }
        if self.names:
            data["names"] = self.names
        if self.callback:
            data["callback"] = self.callback

        return data

    def from_map(self, m: Optional[dict] = None):
        m = m or {}
        self.urls = m.get("urls", [])
        self.incorporatePro = m.get("incorporatePro", True)
        self.names = m.get("names", [])
        self.extraOptions = m.get("extraOptions", None)
        self.lang = m.get("lang", None)
        self.sourceLang = m.get("sourceLang", None)
        self.callback = m.get("callback", None)
        return self
