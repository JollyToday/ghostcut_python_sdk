# -*- coding: utf-8 -*-

"""
3.6 提交视频克隆任务（普通）请求模型
文档地址：https://jollytoday.feishu.cn/wiki/Y9JSwDDo8iVWN2k0IELc5nsMn3f#share-KEqrdC5mgoCHoTxgV03ces1hnKf

功能简述：
    使用克隆声音和公共音色合成视频，提交视频处理任务。
接口地址：
    https://api.zhaoli.com/v-w-c/gateway/ve/work/voice/incorporate
请求方式：
    POST

请求参数说明：
- urls: List[str]，必填，处理的视频URL数组，当前只支持传1个视频
- names: Optional[List[str]]，非必填，传入urls对应视频的作品命名，查询结果时会返回
- extraOptions: str，必填，声音文件配置项，json字符串格式，至少包含 customer_input 里的 url或content 和 prefix
- wyVoiceParam: Optional[dict]，非必填，可选语音相关配置，指定角色对应声音id及voice_type
- lang: str，必填，目标语言代码，如'en'
- sourceLang: str，必填，源语言代码，如'en'
- callback: Optional[str]，非必填，回调地址，任务完成后我方会POST处理结果

示例中文件结构详细见接口文档。
"""

from typing import List, Optional, Dict, Any
import json
from ghostcut_python_sdk.ghostcut.models.ghostcut_model import GhostCutModel


class GhostCutWorkVoiceIncorporateRequest(GhostCutModel):
    """
    视频克隆任务提交请求模型
    """
    def __init__(
        self,
        urls: List[str],
        extraOptions: str,
        lang: str,
        sourceLang: str,
        names: Optional[List[str]] = None,
        wyVoiceParam: Optional[Dict[str, Any]] = None,
        callback: Optional[str] = None,
    ):
        """
        :param urls: List[str], 必填，视频URL数组，当前支持传1个
        :param extraOptions: str, 必填，声音配置JSON字符串
        :param lang: str, 必填，目标语言代码，如'en'
        :param sourceLang: str, 必填，源语言代码，如'en'
        :param names: Optional[List[str]], 非必填，视频作品命名列表，与urls对应
        :param wyVoiceParam: Optional[dict], 非必填，语音配置字段
        :param callback: Optional[str], 非必填，回调URL
        """
        self.urls = urls
        self.names = names
        self.extraOptions = extraOptions
        self.wyVoiceParam = wyVoiceParam
        self.lang = lang
        self.sourceLang = sourceLang
        self.callback = callback

    def validate(self):
        if not self.urls or not isinstance(self.urls, list) or len(self.urls) == 0:
            raise ValueError("urls 必填，且必须为非空列表，当前只支持一个视频")
        if len(self.urls) > 1:
            raise ValueError("当前接口只支持传1个视频URL")
        for url in self.urls:
            if not isinstance(url, str) or url.strip() == "":
                raise ValueError("urls中的每个元素必须为非空字符串URL")

        if not self.extraOptions or not isinstance(self.extraOptions, str):
            raise ValueError("extraOptions 必填，且必须为JSON字符串")

        # 尝试解析extraOptions为JSON，检查customer_input字段及其url或content必须至少有一个
        try:
            extra_dict = json.loads(self.extraOptions)
        except Exception as e:
            raise ValueError(f"extraOptions 必须是有效的JSON字符串，解析失败: {e}")

        customer_input = extra_dict.get("customer_input")
        if not customer_input or not isinstance(customer_input, dict):
            raise ValueError("extraOptions中必须包含customer_input字段，且为对象")

        if not ("url" in customer_input or "content" in customer_input):
            raise ValueError(
                "customer_input中必须包含url或content字段，至少一项存在"
            )

        if "prefix" not in customer_input or not customer_input["prefix"]:
            raise ValueError("customer_input中必须包含prefix字段，且不能为空")

        if self.names is not None:
            if not isinstance(self.names, list):
                raise ValueError("names必须为列表")
            if len(self.names) != len(self.urls):
                raise ValueError("names列表长度必须和urls列表长度一致")

        if not self.lang or not isinstance(self.lang, str):
            raise ValueError("lang 必填，且必须为字符串")

        if not self.sourceLang or not isinstance(self.sourceLang, str):
            raise ValueError("sourceLang 必填，且必须为字符串")

        if self.callback is not None and not isinstance(self.callback, str):
            raise ValueError("callback非必填，如传必须为字符串")

        if self.wyVoiceParam is not None:
            if not isinstance(self.wyVoiceParam, dict):
                raise ValueError("wyVoiceParam非必填，如传必须为字典")

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        data = {
            "urls": self.urls,
            "extraOptions": self.extraOptions,
            "lang": self.lang,
            "sourceLang": self.sourceLang,
        }

        if self.names is not None:
            data["names"] = self.names

        if self.wyVoiceParam is not None:
            data["wyVoiceParam"] = self.wyVoiceParam

        if self.callback is not None:
            data["callback"] = self.callback

        return data

    def from_map(self, m: Optional[dict] = None):
        m = m or {}
        self.urls = m.get("urls")
        self.names = m.get("names")
        self.extraOptions = m.get("extraOptions")
        self.wyVoiceParam = m.get("wyVoiceParam")
        self.lang = m.get("lang")
        self.sourceLang = m.get("sourceLang")
        self.callback = m.get("callback")
        return self
