# -*- coding: utf-8 -*-

"""
4.4 视频去文字的重新处理【异步】
# 接口文档：https://jollytoday.feishu.cn/docx/U73qdBhWbozFdpx4eTvcIO4gn7e#share-PWb2dtxOnoG1KsxfG31c7C9Rnmb

功能简述：
修改去文字区域并重新合成，支持所有带videoInpaintMasks参数的剪辑请求。
开发者可自行调整文字区域，也可通过鬼手剪辑网站二次调整。
前3次免费调整，超出后会扣点。

接口地址：
https://api.zhaoli.com/v-w-c/gateway/ve/work/video/inpaint/redo
请求方式：
POST

请求参数：
- id (Long，必填)：需要重新处理的作品id
- videoInpaintMasks (String，非必填)：JSON字符串，视频去文字区域设置。
  支持多框同时设置不同区域，每个区域可设置时间段。
  视频框类型type支持：
    * remove：全擦除区域，不管有无文字；
    * keep：保护区域，不处理；
    * remove_only_ocr：仅擦除检测出的文本区域。

响应参数：
- body (Boolean)：true表示发起成功，false表示失败。
"""

from ghostcut_python_sdk.ghostcut.models.ghostcut_model import GhostCutModel


class GhostCutVideoInpaintRedoRequest(GhostCutModel):
    def __init__(
        self,
        id: int = None,
        videoInpaintMasks: str = None,
    ):
        """
        视频去文字的重新处理请求参数模型

        :param id: (必填) 需要重新处理的作品ID
        :param videoInpaintMasks: (非必填) JSON字符串，视频去文字区域设置
        """
        self.id = id
        self.videoInpaintMasks = videoInpaintMasks

    def validate(self):
        if self.id is None:
            raise ValueError("id 为必填项")
        if not isinstance(self.id, int):
            raise ValueError("id 必须是整数类型")

        if self.videoInpaintMasks is not None and not isinstance(self.videoInpaintMasks, str):
            raise ValueError("videoInpaintMasks 必须是字符串类型或None")

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        d = {
            "id": self.id,
        }
        if self.videoInpaintMasks is not None:
            d["videoInpaintMasks"] = self.videoInpaintMasks
        return d

    def from_map(self, m: dict = None):
        m = m or dict()
        self.id = m.get("id")
        self.videoInpaintMasks = m.get("videoInpaintMasks")
        return self
