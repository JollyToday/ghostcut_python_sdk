# -*- coding: utf-8 -*-

"""
3.4 查询公共的音色列表请求模型
文档地址：https://jollytoday.feishu.cn/wiki/Y9JSwDDo8iVWN2k0IELc5nsMn3f#share-C0bWd9ZzGoxfZjxzzZGcU9kRntg

功能简述：
    分页查询公共声音列表，每页默认20条。
接口地址：
    https://api.zhaoli.com/v-w-c/gateway/ve/voice/query_public_voice
请求方式：
    POST

请求参数说明：
- pageNumber: int，必填，页码，从1开始，传1返回第一页数据
- pageSize: int，非必填，每页条数，默认20条
"""

from typing import Optional
from ghostcut_python_sdk.ghostcut.models.ghostcut_model import GhostCutModel


class GhostCutVoiceQueryPublicVoiceRequest(GhostCutModel):
    """
    查询公共音色列表请求模型
    """
    def __init__(
        self,
        pageNumber: Optional[int] = None,
        pageSize: Optional[int] = None,
    ):
        """
        :param pageNumber: int, 必填，页码，从1开始
        :param pageSize: int, 非必填，每页条数，默认20条
        """
        self.pageNumber = pageNumber
        self.pageSize = pageSize

    def validate(self):
        if self.pageNumber is None or not isinstance(self.pageNumber, int) or self.pageNumber < 1:
            raise ValueError("pageNumber 必填，且必须为大于等于1的整数")
        if self.pageSize is not None and (not isinstance(self.pageSize, int) or self.pageSize < 1):
            raise ValueError("pageSize 非必填，如传则必须为正整数")

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map
        data = {
            "pageNumber": self.pageNumber,
        }
        if self.pageSize is not None:
            data["pageSize"] = self.pageSize
        return data

    def from_map(self, m: Optional[dict] = None):
        m = m or {}
        self.pageNumber = m.get("pageNumber", None)
        self.pageSize = m.get("pageSize", None)
        return self