# -*- coding: utf-8 -*-

# 5.1 创建图片任务
# https://jollytoday.feishu.cn/docx/U73qdBhWbozFdpx4eTvcIO4gn7e#share-BInTdcm2roNEVvxmDZdctlumnuc


from ghostcut.models.ghostcut_model import GhostCutModel
from typing import Dict, List, Any

class GhostCutImageTaskCreateRequestExtraOption(GhostCutModel):
    def __init__(
        self,
        font_family: str = None,
    ):
        self.font_family = font_family

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.font_family is not None:
            result['font_family'] = self.font_family
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('font_family') is not None:
            self.urls = m.get('font_family')
        return self