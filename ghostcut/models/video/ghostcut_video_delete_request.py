# -*- coding: utf-8 -*-

"""
4.8 删除视频作品请求模型
文档地址：https://jollytoday.feishu.cn/docx/U73qdBhWbozFdpx4eTvcIO4gn7e#share-TWxddmMiuo5W2ixideSccosLnsf
接口地址：https://api.zhaoli.com/v-w-c/gateway/ve/work/delete
请求方式：POST
"""

from ghostcut_python_sdk.ghostcut.models.ghostcut_model import GhostCutModel
from typing import List


class GhostCutWorkDeleteRequest(GhostCutModel):
    def __init__(self, idWorks: List[int] = None):
        """
        删除视频作品请求参数模型

        :param idWorks: 作品id列表，必填，类型为List[int]
        """
        self.idWorks = idWorks or []

    def validate(self):
        if not self.idWorks or not isinstance(self.idWorks, list):
            raise ValueError("idWorks 必须是非空的整数列表")
        if not all(isinstance(i, int) for i in self.idWorks):
            raise ValueError("idWorks 列表中所有元素必须是整数")

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map
        return {
            "idWorks": self.idWorks
        }

    def from_map(self, m: dict = None):
        m = m or dict()
        self.idWorks = m.get("idWorks", [])
        return self
