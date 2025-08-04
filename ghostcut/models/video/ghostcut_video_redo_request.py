# -*- coding: utf-8 -*-

"""
4.6 失败状态的重新处理【异步】
# 接口文档：https://jollytoday.feishu.cn/docx/U73qdBhWbozFdpx4eTvcIO4gn7e#share-FohTdeAABopZrIxs4W5cFQRMnAh

功能简述：
尝试对处理失败的作品重新处理。某些状态的作品可通过重试成功（如点卡不足充值后）。
注意并非所有失败都能重试成功，如遇问题请联系官方支持。

接口地址：
https://api.zhaoli.com/v-w-c/gateway/ve/work/video/redo
请求方式：
POST

请求参数：
- id (Long，必填)：需要重新处理的作品workid

响应参数：
- body (Boolean)：true表示发起成功，false表示失败。
"""

from ghostcut_python_sdk.ghostcut.models.ghostcut_model import GhostCutModel


class GhostCutVideoRedoRequest(GhostCutModel):
    def __init__(
        self,
        id: int = None,
    ):
        """
        失败状态的重新处理请求参数模型

        :param id: (必填) 需要重新处理的作品workid
        """
        self.id = id

    def validate(self):
        if self.id is None:
            raise ValueError("id 为必填项")
        if not isinstance(self.id, int):
            raise ValueError("id 必须是整数类型")

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        return {"id": self.id}

    def from_map(self, m: dict = None):
        m = m or dict()
        self.id = m.get("id")
        return self
