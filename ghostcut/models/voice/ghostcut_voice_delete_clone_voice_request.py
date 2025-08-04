# -*- coding: utf-8 -*-

"""
3.5 删除训练的音色请求模型
文档地址：https://jollytoday.feishu.cn/wiki/Y9JSwDDo8iVWN2k0IELc5nsMn3f#share-NIRSdD8IkoTpTRxt5feccXFDnqg

功能简述：
    删除指定的克隆声音，支持通过prefix或id进行删除，二选一。
接口地址：
    https://api.zhaoli.com/v-w-c/gateway/ve/voice/delete_clone_voice
请求方式：
    POST

请求参数说明：
- prefix: str，二选一，声音的prefix，优先使用prefix进行删除
- id: int，二选一，声音的id，当prefix未传时使用
"""

from typing import Optional
from ghostcut_python_sdk.ghostcut.models.ghostcut_model import GhostCutModel


class GhostCutVoiceDeleteCloneVoiceRequest(GhostCutModel):
    """
    删除训练音色请求模型
    """
    def __init__(
        self,
        prefix: Optional[str] = None,
        id: Optional[int] = None,
    ):
        """
        :param prefix: str, 二选一，声音的prefix，优先使用
        :param id: int, 二选一，声音的id，prefix未传时使用
        """
        self.prefix = prefix
        self.id = id

    def validate(self):
        """
        校验参数合法性，必须传prefix或id其中一个，且prefix优先
        """
        if (not self.prefix or self.prefix == "") and self.id is None:
            raise ValueError("prefix和id二选一，必须传入其中一个")
        if self.prefix is not None and not isinstance(self.prefix, str):
            raise ValueError("prefix 必须是字符串")
        if self.id is not None and not isinstance(self.id, int):
            raise ValueError("id 必须是整数")

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map
        data = {}
        if self.prefix is not None and self.prefix != "":
            data["prefix"] = self.prefix
        elif self.id is not None:
            data["id"] = self.id
        return data

    def from_map(self, m: Optional[dict] = None):
        m = m or {}
        self.prefix = m.get("prefix", None)
        self.id = m.get("id", None)
        return self


