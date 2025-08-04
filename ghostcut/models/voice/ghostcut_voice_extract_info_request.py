# -*- coding: utf-8 -*-

"""
3.1 普通克隆接口 - 人声抽取请求模型
文档地址： https://jollytoday.feishu.cn/wiki/Y9JSwDDo8iVWN2k0IELc5nsMn3f#share-TjCRd65bKoKXQYx74DZcJZ2ZnCi
功能简述：
    提交声音和标注文件，抽取用于克隆的音频和时长等相关信息，用于后续声音克隆及角色声音ID映射。
接口地址：
    https://api.zhaoli.com/v-w-c/gateway/ve/voice/extract_info
请求方式：
    POST

请求参数说明：
- callback: String，非必填，回调地址URL
- cloneKwargs: String，必填，json字符串，结构示例：
{
    "clone_kwargs": {
        "prefix": "用鬼手剪辑的短剧克隆一定火火火",
        "urls": [
            {
                "annote_url": "https://gc100.cdn.izhaoli.cn/dl_task/x_3.json",
                "audio_url": "https://gc100.cdn.izhaoli.cn/dl_task/source_separate/task__10147087__audio_separate__raw_audio__1701908762716.mp3"
            },
            ...
        ]
    }
}
"""

from typing import Optional, List
from ghostcut_python_sdk.ghostcut.models.ghostcut_model import GhostCutModel
import json


class VoiceExtractUrlItem(GhostCutModel):
    def __init__(
        self,
        annote_url: Optional[str] = None,
        audio_url: Optional[str] = None,
    ):
        """
        :param annote_url: str, 必填，标注文件URL
        :param audio_url: str, 必填，音频文件URL
        """
        self.annote_url = annote_url
        self.audio_url = audio_url

    def validate(self):
        if not self.annote_url or not isinstance(self.annote_url, str):
            raise ValueError("annote_url 必填且必须为字符串")
        if not self.audio_url or not isinstance(self.audio_url, str):
            raise ValueError("audio_url 必填且必须为字符串")

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map
        return {
            "annote_url": self.annote_url,
            "audio_url": self.audio_url,
        }

    def from_map(self, m: Optional[dict] = None):
        m = m or {}
        self.annote_url = m.get("annote_url", None)
        self.audio_url = m.get("audio_url", None)
        return self


class VoiceExtractCloneKwargs(GhostCutModel):
    def __init__(
        self,
        prefix: Optional[str] = None,
        urls: Optional[List[VoiceExtractUrlItem]] = None,
    ):
        """
        :param prefix: str, 必填，唯一标识，建议传剧名
        :param urls: List[VoiceExtractUrlItem], 必填，标注文件和对应音频列表
        """
        self.prefix = prefix
        self.urls = urls or []

    def validate(self):
        if not self.prefix or not isinstance(self.prefix, str):
            raise ValueError("prefix 必填且必须为字符串")
        if not isinstance(self.urls, list) or not all(isinstance(u, VoiceExtractUrlItem) for u in self.urls):
            raise ValueError("urls 必填且必须是 VoiceExtractUrlItem 列表")
        for url_item in self.urls:
            url_item.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map
        return {
            "prefix": self.prefix,
            "urls": [url_item.to_map() for url_item in self.urls],
        }

    def from_map(self, m: Optional[dict] = None):
        m = m or {}
        self.prefix = m.get("prefix", None)
        urls_list = m.get("urls", [])
        self.urls = [VoiceExtractUrlItem().from_map(item) for item in urls_list]
        return self


class GhostCutVoiceExtractInfoRequest(GhostCutModel):
    def __init__(
        self,
        cloneKwargs: Optional[str] = None,
        callback: Optional[str] = None,
        clone_kwargs_obj: Optional[VoiceExtractCloneKwargs] = None,
    ):
        """
        :param cloneKwargs: str, 必填，clone_kwargs的json字符串
        :param callback: str, 非必填，回调地址URL
        :param clone_kwargs_obj: VoiceExtractCloneKwargs, 可选，用来自动生成cloneKwargs字符串
        """
        if clone_kwargs_obj:
            clone_kwargs_obj.validate()
            self.cloneKwargs = json.dumps({"clone_kwargs": clone_kwargs_obj.to_map()}, ensure_ascii=False)
        else:
            self.cloneKwargs = cloneKwargs
        self.callback = callback

    def validate(self):
        if not self.cloneKwargs or not isinstance(self.cloneKwargs, str):
            raise ValueError("cloneKwargs 必填且必须为字符串")
        # 尝试解析验证 cloneKwargs 是否为合法JSON
        try:
            json_obj = json.loads(self.cloneKwargs)
            if "clone_kwargs" not in json_obj:
                raise ValueError("cloneKwargs JSON中必须含有clone_kwargs字段")
        except Exception as e:
            raise ValueError(f"cloneKwargs 必须是合法的JSON字符串，解析失败: {e}")
        if self.callback is not None and not isinstance(self.callback, str):
            raise ValueError("callback 必须是字符串或None")

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map
        data = {"cloneKwargs": self.cloneKwargs}
        if self.callback:
            data["callback"] = self.callback
        return data

    def from_map(self, m: Optional[dict] = None):
        m = m or {}
        self.cloneKwargs = m.get("cloneKwargs", None)
        self.callback = m.get("callback", None)
        return self
