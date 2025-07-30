# -*- coding: utf-8 -*-

"""
4.9.1 创建译制出海项目请求模型
文档地址： https://jollytoday.feishu.cn/docx/U73qdBhWbozFdpx4eTvcIO4gn7e#share-Hqr2d1b9go9vLJxGECrchnfYn2f

功能简述
可以创建译制出海的项目，功能等同于web的译制出海 +新建项目，可以通过这个接口来创建新的项目
这个接口创建的项目会返回id，即为 idSeries
然后通过本地文件上传接口将materialFileType参数设置为video_series，idSeries参数传本接口返回的id，即可向该项目增加素材

接口地址：https://api.zhaoli.com/v-w-c/gateway/ve/series/create
请求方式：POST
"""

from ghostcut_python_sdk.ghostcut.models.ghostcut_model import GhostCutModel
from typing import Optional, Dict, Any


class GhostCutDubbingProjectCreateRequest(GhostCutModel):
    def __init__(self, seriesDto: Optional[Dict[str, Any]] = None):
        """
        创建译制出海项目请求参数模型

        :param seriesDto: 剧集信息字典，必填，示例：
            {
                "seriesName": "项目名称",
                "remark": "备注"
            }
        """
        self.seriesDto = seriesDto or {}

    def validate(self):
        if not self.seriesDto or not isinstance(self.seriesDto, dict):
            raise ValueError("seriesDto 必填且必须是字典")
        if "seriesName" not in self.seriesDto or not self.seriesDto["seriesName"]:
            raise ValueError("seriesDto 中 seriesName 字段必填且不能为空")

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map
        return {
            "seriesDto": self.seriesDto
        }

    def from_map(self, m: Optional[dict] = None):
        m = m or {}
        self.seriesDto = m.get("seriesDto", {})
        return self