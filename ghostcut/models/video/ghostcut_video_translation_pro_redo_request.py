# -*- coding: utf-8 -*-

"""
4.5 语音/文字翻译的重新处理【异步】
# 接口文档：https://jollytoday.feishu.cn/docx/U73qdBhWbozFdpx4eTvcIO4gn7e#share-OZf5d7JJroXR8uxfgdmcbkicn1g

功能简述：
修改视频翻译后的字幕并重新合成，仅支持与4.1.4视频语音翻译或4.1.5视频文字翻译搭配使用。
前3次免费调整，超出后扣点。

接口地址：
https://api.zhaoli.com/v-w-c/gateway/ve/work/translationPro/redo
请求方式：
POST

请求参数说明：

- id (Long，必填)：需要重新处理的作品ID。
- ttsMetaResult (String，当调整【语音翻译】时必填)：修改后的语音翻译字幕元数据(JSON字符串)，注意保留原始字段，
  修改过的句子需加"is_modified": true，且删除与tts相关的字段，具体格式请参考接口说明。
- wyNeedText (Byte，当调整【语音翻译】时选填)：是否开启字幕，0否，1是。
- wyVoiceParam (String，当调整【语音翻译】时必填)：配音及字幕配置JSON字符串，包括配音角色id和字幕样式font_param。
- idVeOcrTranslateTask (Long，当调整【文字翻译】时必填)：视频文字翻译专用ID，通过4.2查询处理结果接口获得。
- bboxGroups (String，当调整【文字翻译】时必填)：修改后的bboxGroups字段(JSON字符串)，由4.3查询文字翻译任务信息接口获得，修改后提交。

响应参数：
- body (Boolean)：true表示发起成功，false表示失败。
"""

from ghostcut_python_sdk.ghostcut.models.ghostcut_model import GhostCutModel
from typing import Optional


class GhostCutTranslationProRedoRequest(GhostCutModel):
    def __init__(
        self,
        id: int = None,
        ttsMetaResult: Optional[str] = None,
        wyNeedText: Optional[int] = None,
        wyVoiceParam: Optional[str] = None,
        idVeOcrTranslateTask: Optional[int] = None,
        bboxGroups: Optional[str] = None,
    ):
        """
        语音/文字翻译的重新处理请求参数模型

        :param id: (必填) 需要重新处理的作品ID
        :param ttsMetaResult: (调整语音翻译时必填) 修改后的ttsMetaResult JSON字符串，格式详见接口文档
        :param wyNeedText: (调整语音翻译时选填) 是否开启字幕，0否，1是
        :param wyVoiceParam: (调整语音翻译时必填) 配音及字幕配置JSON字符串
        :param idVeOcrTranslateTask: (调整文字翻译时必填) 视频文字翻译专用ID
        :param bboxGroups: (调整文字翻译时必填) 修改后的bboxGroups JSON字符串
        """
        self.id = id
        self.ttsMetaResult = ttsMetaResult
        self.wyNeedText = wyNeedText
        self.wyVoiceParam = wyVoiceParam
        self.idVeOcrTranslateTask = idVeOcrTranslateTask
        self.bboxGroups = bboxGroups

    def validate(self):
        """
        参数校验
        """
        if self.id is None:
            raise ValueError("id 为必填项")
        if not isinstance(self.id, int):
            raise ValueError("id 必须是整数类型")

        # 语音翻译相关参数校验
        if self.ttsMetaResult is not None or self.wyVoiceParam is not None or self.wyNeedText is not None:
            if self.ttsMetaResult is None:
                raise ValueError("调整语音翻译时 ttsMetaResult 必填")
            if self.wyVoiceParam is None:
                raise ValueError("调整语音翻译时 wyVoiceParam 必填")
            if self.wyNeedText is not None and self.wyNeedText not in (0, 1):
                raise ValueError("wyNeedText 只能为0或1")

        # 文字翻译相关参数校验
        if self.idVeOcrTranslateTask is not None or self.bboxGroups is not None:
            if self.idVeOcrTranslateTask is None:
                raise ValueError("调整文字翻译时 idVeOcrTranslateTask 必填")
            if self.bboxGroups is None:
                raise ValueError("调整文字翻译时 bboxGroups 必填")

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        d = {"id": self.id}

        if self.ttsMetaResult is not None:
            d["ttsMetaResult"] = self.ttsMetaResult
        if self.wyNeedText is not None:
            d["wyNeedText"] = self.wyNeedText
        if self.wyVoiceParam is not None:
            d["wyVoiceParam"] = self.wyVoiceParam
        if self.idVeOcrTranslateTask is not None:
            d["idVeOcrTranslateTask"] = self.idVeOcrTranslateTask
        if self.bboxGroups is not None:
            d["bboxGroups"] = self.bboxGroups

        return d

    def from_map(self, m: dict = None):
        m = m or dict()
        self.id = m.get("id")
        self.ttsMetaResult = m.get("ttsMetaResult")
        self.wyNeedText = m.get("wyNeedText")
        self.wyVoiceParam = m.get("wyVoiceParam")
        self.idVeOcrTranslateTask = m.get("idVeOcrTranslateTask")
        self.bboxGroups = m.get("bboxGroups")
        return self
