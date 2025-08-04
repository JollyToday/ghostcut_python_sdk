# -*- coding: utf-8 -*-

"""
4.2 查询TTS合成任务请求模型
文档地址： https://jollytoday.feishu.cn/wiki/Y9JSwDDo8iVWN2k0IELc5nsMn3f#share-W6otd2wgRofa9xxrJf6cmtshnzc
功能简述：
    查询指定任务id的TTS合成任务状态和结果。
接口地址：
    https://api.zhaoli.com/v-w-c/gateway/ve/parse/task/query
请求方式：
    POST

请求参数说明：
- id: int，必填，任务id，即4.1接口响应中的body值
"""

from typing import Optional
from ghostcut_python_sdk.ghostcut.models.ghostcut_model import GhostCutModel


class GhostCutParseTaskQueryRequest(GhostCutModel):
    """
    TTS合成任务查询请求模型
    """
    def __init__(self, id: int):
        """
        :param id: int, 必填，任务id
        """
        self.id = id

    def validate(self):
        if not isinstance(self.id, int) or self.id <= 0:
            raise ValueError("id 必须是大于0的整数")

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map
        return {"id": self.id}

    def from_map(self, m: Optional[dict] = None):
        m = m or {}
        self.id = m.get("id", None)
        return self

