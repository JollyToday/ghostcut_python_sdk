# -*- coding: utf-8 -*-

# 5.2 查询图片处理结果
# 接口文档：https://jollytoday.feishu.cn/docx/U73qdBhWbozFdpx4eTvcIO4gn7e#share-NUf2dBNyeoiBmpxohitcididndf

# -*- coding: utf-8 -*-

"""
接口地址：https://api.zhaoli.com/v-w-c/gateway/ve/image/translate/query
"""

from ghostcut_python_sdk.ghostcut.models.ghostcut_model import GhostCutModel


class GhostCutImageTaskQueryRequest(GhostCutModel):
    def __init__(
        self,
        id: int = None,
    ):
        """
        查询图片处理结果请求参数模型

        :param id: (必填) 图片翻译任务id，即创建任务接口返回的任务ID
        """
        self.id = id

    def validate(self):
        """
        校验请求参数合法性，若参数不符合规则，抛出 ValueError 异常
        """
        if self.id is None:
            raise ValueError("id 为必填项")
        if not isinstance(self.id, int):
            raise ValueError("id 必须是整数类型")

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        return {
            "id": self.id,
        }

    def from_map(self, m: dict = None):
        m = m or dict()
        self.id = m.get("id")
        return self
