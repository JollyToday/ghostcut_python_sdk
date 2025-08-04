# -*- coding: utf-8 -*-

"""
2.2 发起句子重新配音任务请求模型
文档地址： https://jollytoday.feishu.cn/wiki/Y9JSwDDo8iVWN2k0IELc5nsMn3f#share-MeHzdqK0JoisyyxtLMUctU71nFh

接口地址：https://api.zhaoli.com/v-w-c/gateway/ve/work/voice/clone
请求方式：POST

请求参数说明：
- idVeWork: Long，必填，已完成高情感克隆的作品ID
- sentIds: List[str]，必填，需要重新配音的句子sent_id列表
- refType: str，必填，重新克隆配音类型，枚举值：OWN, PUB_TTS, PUB_CLONE, OWN_CLONE
- refSentId: Optional[str]，当refType为OWN时必填，参考句子的sent_id
- refVoiceId: Optional[int]，当refType为PUB_TTS、PUB_CLONE、OWN_CLONE时必填，声音ID
- callback: Optional[str]，回调地址URL
"""

from typing import Optional, List, Union
from ghostcut_python_sdk.ghostcut.models.ghostcut_model import GhostCutModel


class GhostCutVoiceSentenceRedubTaskSubmitRequest(GhostCutModel):
    def __init__(
        self,
        idVeWork: Optional[int] = None,
        sentIds: Optional[List[str]] = None,
        refType: Optional[str] = None,
        refSentId: Optional[str] = None,
        refVoiceId: Optional[int] = None,
        callback: Optional[str] = None,
    ):
        """
        :param idVeWork: int, 必填，高情感克隆作品ID
        :param sentIds: List[str], 必填，需要重新配音的句子sent_id列表
        :param refType: str, 必填，重新配音类型，OWN/PUB_TTS/PUB_CLONE/OWN_CLONE
        :param refSentId: str, 当refType为OWN时必填，参考句子的sent_id
        :param refVoiceId: int, 当refType为PUB_TTS, PUB_CLONE, OWN_CLONE时必填，声音ID
        :param callback: str, 可选，回调地址URL
        """
        self.idVeWork = idVeWork
        self.sentIds = sentIds or []
        self.refType = refType
        self.refSentId = refSentId
        self.refVoiceId = refVoiceId
        self.callback = callback

    def validate(self):
        if self.idVeWork is None or not isinstance(self.idVeWork, int):
            raise ValueError("idVeWork 必填且必须为整数")
        if not self.sentIds or not isinstance(self.sentIds, list) or not all(isinstance(sid, str) for sid in self.sentIds):
            raise ValueError("sentIds 必填且必须为字符串列表")
        if self.refType not in ("OWN", "PUB_TTS", "PUB_CLONE", "OWN_CLONE"):
            raise ValueError("refType 必须为OWN、PUB_TTS、PUB_CLONE或OWN_CLONE其中之一")
        if self.refType == "OWN":
            if not self.refSentId or not isinstance(self.refSentId, str):
                raise ValueError("refSentId 当 refType 为 OWN 时必填，且必须为字符串")
        else:
            if self.refVoiceId is None or not isinstance(self.refVoiceId, int):
                raise ValueError("refVoiceId 当 refType 为 PUB_TTS、PUB_CLONE 或 OWN_CLONE 时必填，且必须为整数")
        if self.callback and not isinstance(self.callback, str):
            raise ValueError("callback 必须为字符串")

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        data = {
            "idVeWork": self.idVeWork,
            "sentIds": self.sentIds,
            "refType": self.refType,
        }
        if self.refType == "OWN":
            data["refSentId"] = self.refSentId
        else:
            data["refVoiceId"] = self.refVoiceId
        if self.callback:
            data["callback"] = self.callback

        return data

    def from_map(self, m: Optional[dict] = None):
        m = m or {}
        self.idVeWork = m.get("idVeWork", None)
        self.sentIds = m.get("sentIds", [])
        self.refType = m.get("refType", None)
        self.refSentId = m.get("refSentId", None)
        self.refVoiceId = m.get("refVoiceId", None)
        self.callback = m.get("callback", None)
        return self
