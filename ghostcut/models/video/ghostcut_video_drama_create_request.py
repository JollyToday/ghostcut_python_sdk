# -*- coding: utf-8 -*-

"""
短剧智能剪辑-创建任务请求模型【4.7.1】
文档地址：https://jollytoday.feishu.cn/docx/U73qdBhWbozFdpx4eTvcIO4gn7e#share-N7L1dQ7bRo3eMBxqSH7cjes6nCb

接口地址：https://api.zhaoli.com/v-w-c/gateway/ve/drama/create
请求方式：POST
"""

from ghostcut_python_sdk.ghostcut.models.ghostcut_model import GhostCutModel
from typing import Optional


class GhostCutDramaCreateRequest(GhostCutModel):
    def __init__(
        self,
        dramaTaskType: str = None,
        dramaInput: str = None,
        dramaSourceLang: str = None,
        dramaLang: str = None,
        isOneStep: bool = False,
        wyVoiceParam: Optional[str] = None,
        wyNeedText: Optional[int] = None,
        callback: Optional[str] = None,
        workName: Optional[str] = None,
        uid: Optional[str] = None,
        rhythmParam: Optional[str] = None,
    ):
        """
        短剧智能剪辑-创建任务请求参数

        :param dramaTaskType: 任务类型，必填，取值：TEXT_NARRATE、VIDEO_NARRATE、HIGHLIGHT_MERGE
        :param dramaInput: 视频和字幕文件JSON字符串，必填，格式示例：
            {
               "files": [{
                   "video": {"url": "视频链接"},
                   "srt"或"annotated_srt": {"url": "字幕链接"}
               }]
            }
        :param dramaSourceLang: 源语言，必填，如"zh"
        :param dramaLang: 目标语言，必填，如"zh"
        :param isOneStep: 是否一步合成，必填，True或False
        :param wyVoiceParam: isOneStep为True且任务类型为TEXT_NARRATE或VIDEO_NARRATE时必填，配音与字幕配置JSON字符串
        :param wyNeedText: isOneStep为True且任务类型为TEXT_NARRATE或VIDEO_NARRATE时必填，1开启字幕，0关闭字幕
        :param callback: 回调地址，选填
        :param workName: 作品名称，选填
        :param uid: 用户ID，选填
        :param rhythmParam: 背景音乐参数JSON字符串，选填
        """
        self.dramaTaskType = dramaTaskType
        self.dramaInput = dramaInput
        self.dramaSourceLang = dramaSourceLang
        self.dramaLang = dramaLang
        self.isOneStep = isOneStep
        self.wyVoiceParam = wyVoiceParam
        self.wyNeedText = wyNeedText
        self.callback = callback
        self.workName = workName
        self.uid = uid
        self.rhythmParam = rhythmParam

    def validate(self):
        if not self.dramaTaskType:
            raise ValueError("dramaTaskType 必填")
        if self.dramaTaskType not in ("TEXT_NARRATE", "VIDEO_NARRATE", "HIGHLIGHT_MERGE"):
            raise ValueError("dramaTaskType 值错误")
        if not self.dramaInput:
            raise ValueError("dramaInput 必填")
        if not self.dramaSourceLang:
            raise ValueError("dramaSourceLang 必填")
        if not self.dramaLang:
            raise ValueError("dramaLang 必填")
        if self.isOneStep:
            if self.dramaTaskType in ("TEXT_NARRATE", "VIDEO_NARRATE"):
                if not self.wyVoiceParam:
                    raise ValueError("isOneStep为True且任务类型为TEXT_NARRATE/VIDEO_NARRATE时，wyVoiceParam必填")
                if self.wyNeedText not in (0, 1):
                    raise ValueError("isOneStep为True且任务类型为TEXT_NARRATE/VIDEO_NARRATE时，wyNeedText必填且只能为0或1")

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map
        d = {
            "dramaTaskType": self.dramaTaskType,
            "dramaInput": self.dramaInput,
            "dramaSourceLang": self.dramaSourceLang,
            "dramaLang": self.dramaLang,
            "isOneStep": self.isOneStep,
        }
        if self.wyVoiceParam is not None:
            d["wyVoiceParam"] = self.wyVoiceParam
        if self.wyNeedText is not None:
            d["wyNeedText"] = self.wyNeedText
        if self.callback is not None:
            d["callback"] = self.callback
        if self.workName is not None:
            d["workName"] = self.workName
        if self.uid is not None:
            d["uid"] = self.uid
        if self.rhythmParam is not None:
            d["rhythmParam"] = self.rhythmParam
        return d

    def from_map(self, m: dict = None):
        m = m or dict()
        self.dramaTaskType = m.get("dramaTaskType")
        self.dramaInput = m.get("dramaInput")
        self.dramaSourceLang = m.get("dramaSourceLang")
        self.dramaLang = m.get("dramaLang")
        self.isOneStep = m.get("isOneStep", False)
        self.wyVoiceParam = m.get("wyVoiceParam")
        self.wyNeedText = m.get("wyNeedText")
        self.callback = m.get("callback")
        self.workName = m.get("workName")
        self.uid = m.get("uid")
        self.rhythmParam = m.get("rhythmParam")
        return self
