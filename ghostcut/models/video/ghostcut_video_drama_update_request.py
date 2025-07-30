# -*- coding: utf-8 -*-

"""
短剧智能剪辑-合成视频请求模型【4.7.2】
文档地址： https://jollytoday.feishu.cn/docx/U73qdBhWbozFdpx4eTvcIO4gn7e#share-DKa3dmlJWovL1hxVfWqcSlDKnXe
接口地址：https://api.zhaoli.com/v-w-c/gateway/ve/drama/update
请求方式：POST
"""

from ghostcut_python_sdk.ghostcut.models.ghostcut_model import GhostCutModel
from typing import Optional


class GhostCutDramaUpdateRequest(GhostCutModel):
    def __init__(
        self,
        id: int = None,
        wyVoiceParam: Optional[str] = None,
        wyNeedText: Optional[int] = None,
        dramaOutput: Optional[str] = None,
        rhythmParam: Optional[str] = None,
    ):
        """
        短剧智能剪辑-合成视频请求参数

        :param id: 作品id，必填
        :param wyVoiceParam: 配音和字幕配置JSON字符串，必填（VIDEO_NARRATE或TEXT_NARRATE任务类型）
        :param wyNeedText: 是否开启字幕展示，必填，1开启，0关闭
        :param dramaOutput: 校对编辑后的解说词JSON字符串，必填
        :param rhythmParam: 背景音乐参数JSON字符串，选填
        """
        self.id = id
        self.wyVoiceParam = wyVoiceParam
        self.wyNeedText = wyNeedText
        self.dramaOutput = dramaOutput
        self.rhythmParam = rhythmParam

    def validate(self):
        if self.id is None:
            raise ValueError("id 必填")
        if self.wyVoiceParam is None:
            raise ValueError("wyVoiceParam 必填")
        if self.wyNeedText not in (0, 1):
            raise ValueError("wyNeedText 必填且只能为0或1")
        if not self.dramaOutput:
            raise ValueError("dramaOutput 必填")

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map
        d = {
            "id": self.id,
            "wyVoiceParam": self.wyVoiceParam,
            "wyNeedText": self.wyNeedText,
            "dramaOutput": self.dramaOutput,
        }
        if self.rhythmParam is not None:
            d["rhythmParam"] = self.rhythmParam
        return d

    def from_map(self, m: dict = None):
        m = m or dict()
        self.id = m.get("id")
        self.wyVoiceParam = m.get("wyVoiceParam")
        self.wyNeedText = m.get("wyNeedText")
        self.dramaOutput = m.get("dramaOutput")
        self.rhythmParam = m.get("rhythmParam")
        return self
