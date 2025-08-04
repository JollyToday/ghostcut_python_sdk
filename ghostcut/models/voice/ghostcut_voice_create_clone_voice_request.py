# -*- coding: utf-8 -*-

"""
3.2 创建训练音色任务请求模型
文档地址：https://jollytoday.feishu.cn/wiki/Y9JSwDDo8iVWN2k0IELc5nsMn3f#share-Kwe9decRhoVppSxknkMcWcBcneg
功能简述：
    提交角色和对应声音url，生成克隆声音供后续合成视频使用。
    建议每次调用只克隆一个声音，未来不支持单次调用克隆多个声音。
接口地址：
    https://api.zhaoli.com/v-w-c/gateway/ve/voice/create_clone_voice
请求方式：
    POST

请求参数说明：
- callback: str，非必填，回调地址URL，任务结果会通过该callback通知
  回调示例：
{
    "raw_result": {
        "cloned_voices": [
            {
                "id": 10,
                "prefix": "用鬼手剪辑的短剧克隆一定火火火",
                "character": "摄影师",
                "is_load": true
            },
            {
                "id": 11,
                "prefix": "用鬼手剪辑的短剧克隆一定火火火",
                "character": "海彤"
            },
            ...
        ]
    }
}

- cloneKwargs: str，必填，json字符串，标记prefix和voice_infos列表
"""

from typing import Optional, List
from ghostcut_python_sdk.ghostcut.models.ghostcut_model import GhostCutModel
import json


class VoiceCreateCloneVoiceInfo(GhostCutModel):
    """
    单个声音信息模型，用于提交角色的声音信息
    """
    def __init__(
        self,
        character: Optional[str] = None,
        audio_url: Optional[str] = None,
        recommend_clone: Optional[bool] = True,
        annote_duration: Optional[int] = None,
        audio_duration: Optional[int] = None,
    ):
        """
        :param character: str, 角色名，非必填（但推荐填写）
        :param audio_url: str, 必填，音频URL
        :param recommend_clone: bool, 非必填，是否推荐克隆，默认True，不传等同True
        :param annote_duration: int, 非必填，标注时长，单位毫秒
        :param audio_duration: int, 非必填，音频总时长，单位秒
        """
        self.character = character
        self.audio_url = audio_url
        self.recommend_clone = recommend_clone if recommend_clone is not None else True
        self.annote_duration = annote_duration
        self.audio_duration = audio_duration

    def validate(self):
        if not self.audio_url or not isinstance(self.audio_url, str):
            raise ValueError("audio_url 必填且必须为字符串")
        if self.character is not None and not isinstance(self.character, str):
            raise ValueError("character 必须为字符串或None")
        if not isinstance(self.recommend_clone, bool):
            raise ValueError("recommend_clone 必须为布尔值")
        if self.annote_duration is not None and not isinstance(self.annote_duration, int):
            raise ValueError("annote_duration 必须为整数或None")
        if self.audio_duration is not None and not isinstance(self.audio_duration, int):
            raise ValueError("audio_duration 必须为整数或None")

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map
        res = {
            "audio_url": self.audio_url,
            "recommend_clone": self.recommend_clone,
        }
        if self.character:
            res["character"] = self.character
        if self.annote_duration is not None:
            res["annote_duration"] = self.annote_duration
        if self.audio_duration is not None:
            res["audio_duration"] = self.audio_duration
        return res

    def from_map(self, m: Optional[dict] = None):
        m = m or {}
        self.character = m.get("character", None)
        self.audio_url = m.get("audio_url", None)
        self.recommend_clone = m.get("recommend_clone", True)
        self.annote_duration = m.get("annote_duration", None)
        self.audio_duration = m.get("audio_duration", None)
        return self


class VoiceCreateCloneCloneKwargs(GhostCutModel):
    """
    clone_kwargs字段模型，包含prefix和voice_infos列表
    """
    def __init__(
        self,
        prefix: Optional[str] = None,
        voice_infos: Optional[List[VoiceCreateCloneVoiceInfo]] = None,
    ):
        """
        :param prefix: str, 必填，唯一标识，建议传剧名
        :param voice_infos: List[VoiceCreateCloneVoiceInfo], 必填，声音信息列表，建议单个声音
        """
        self.prefix = prefix
        self.voice_infos = voice_infos or []

    def validate(self):
        if not self.prefix or not isinstance(self.prefix, str):
            raise ValueError("prefix 必填且必须为字符串")
        if not isinstance(self.voice_infos, list) or len(self.voice_infos) == 0:
            raise ValueError("voice_infos 必填且必须为非空列表")
        for vi in self.voice_infos:
            if not isinstance(vi, VoiceCreateCloneVoiceInfo):
                raise ValueError("voice_infos 列表元素必须为 VoiceCreateCloneVoiceInfo 类型")
            vi.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map
        return {
            "prefix": self.prefix,
            "voice_infos": [vi.to_map() for vi in self.voice_infos],
        }

    def from_map(self, m: Optional[dict] = None):
        m = m or {}
        self.prefix = m.get("prefix", None)
        voice_infos_list = m.get("voice_infos", [])
        self.voice_infos = [VoiceCreateCloneVoiceInfo().from_map(item) for item in voice_infos_list]
        return self


class GhostCutVoiceCreateCloneVoiceRequest(GhostCutModel):
    def __init__(
        self,
        cloneKwargs: Optional[str] = None,
        callback: Optional[str] = None,
        clone_kwargs_obj: Optional[VoiceCreateCloneCloneKwargs] = None,
    ):
        """
        :param cloneKwargs: str, 必填，clone_kwargs的json字符串
        :param callback: str, 非必填，回调URL
        :param clone_kwargs_obj: VoiceCreateCloneCloneKwargs, 可选，自动生成cloneKwargs字符串
        """
        if clone_kwargs_obj:
            clone_kwargs_obj.validate()
            self.cloneKwargs = json.dumps({"clone_kwargs": clone_kwargs_obj.to_map()}, ensure_ascii=False)
        else:
            self.cloneKwargs = cloneKwargs
        self.callback = callback

    def validate(self):
        if not self.cloneKwargs or not isinstance(self.cloneKwargs, str):
            raise ValueError("cloneKwargs 必填且必须是字符串")
        # 尝试解析JSON并确认包含clone_kwargs
        try:
            json_obj = json.loads(self.cloneKwargs)
            if "clone_kwargs" not in json_obj:
                raise ValueError("cloneKwargs JSON中必须包含 clone_kwargs 字段")
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
