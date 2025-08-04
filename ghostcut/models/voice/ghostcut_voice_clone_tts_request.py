# -*- coding: utf-8 -*-

"""
4.1 TTS文本转语音请求模型
文档地址：https://jollytoday.feishu.cn/wiki/Y9JSwDDo8iVWN2k0IELc5nsMn3f#share-LVh7db9yjopW9PxtLuvctGlhnBf
功能简述：
    传入声音id及文本列表，进行语音合成。
接口地址：
    https://api.zhaoli.com/v-w-c/gateway/ve/voice/clone_tts
请求方式：
    POST

请求参数说明：
- callback: Optional[str]，回调URL，任务完成后通过此URL通知结果
- cloneKwargs: str，必填，Json字符串，包含以下字段：
    - texts: List[str]，要合成的文本列表
    - lang: str，语言代码，如"zh"
    - id: int，克隆声音的id
"""

from typing import List, Optional
import json
from ghostcut_python_sdk.ghostcut.models.ghostcut_model import GhostCutModel


class GhostCutVoiceCloneTtsRequest(GhostCutModel):
    """
    TTS文本转语音请求模型
    """
    def __init__(
        self,
        cloneKwargs: str,
        callback: Optional[str] = None,
    ):
        """
        :param cloneKwargs: str，必填，JSON字符串，包含texts、lang、id。例如：
            {
                "texts": ["这是一条测试!", "这是测试2？"],
                "lang": "zh",
                "id": 773
            }
        :param callback: Optional[str]，回调地址，非必填
        """
        self.callback = callback
        self.cloneKwargs = cloneKwargs

    @classmethod
    def from_params(
        cls,
        texts: List[str],
        lang: str,
        voice_id: int,
        callback: Optional[str] = None,
    ):
        clone_kwargs_dict = {
            "texts": texts,
            "lang": lang,
            "id": voice_id,
        }
        clone_kwargs_str = json.dumps(clone_kwargs_dict, ensure_ascii=False)
        return cls(cloneKwargs=clone_kwargs_str, callback=callback)

    def validate(self):
        if not self.cloneKwargs or not isinstance(self.cloneKwargs, str):
            raise ValueError("cloneKwargs 必填，且必须为JSON字符串")
        try:
            clone_kwargs_obj = json.loads(self.cloneKwargs)
        except Exception as e:
            raise ValueError(f"cloneKwargs 必须是有效的JSON字符串，解析失败: {e}")

        if "texts" not in clone_kwargs_obj or not isinstance(clone_kwargs_obj["texts"], list) or len(clone_kwargs_obj["texts"]) == 0:
            raise ValueError("cloneKwargs中必须包含非空texts列表")
        for text in clone_kwargs_obj["texts"]:
            if not isinstance(text, str):
                raise ValueError("cloneKwargs中texts列表元素必须是字符串")

        if "lang" not in clone_kwargs_obj or not isinstance(clone_kwargs_obj["lang"], str) or clone_kwargs_obj["lang"].strip() == "":
            raise ValueError("cloneKwargs中必须包含非空lang字符串")

        if "id" not in clone_kwargs_obj or not isinstance(clone_kwargs_obj["id"], int):
            raise ValueError("cloneKwargs中必须包含id且为整数")

        if self.callback is not None and not isinstance(self.callback, str):
            raise ValueError("callback非必填，如传必须为字符串")

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map
        data = {
            "cloneKwargs": self.cloneKwargs,
        }
        if self.callback is not None:
            data["callback"] = self.callback
        return data

    def from_map(self, m: Optional[dict] = None):
        m = m or {}
        self.callback = m.get("callback", None)
        self.cloneKwargs = m.get("cloneKwargs", None)
        return self
