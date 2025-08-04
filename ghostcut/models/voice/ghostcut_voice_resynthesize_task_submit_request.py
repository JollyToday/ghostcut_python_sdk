# ghostcut_voice_resynthesize_task_submit_request.py
# -*- coding: utf-8 -*-

"""
2.4 使用新声音重新合成视频请求模型
文档地址：https://jollytoday.feishu.cn/wiki/Y9JSwDDo8iVWN2k0IELc5nsMn3f#share-CzRWdCnkRoG3LKxLnBpcLvDPnld

接口地址：https://api.zhaoli.com/v-w-c/gateway/ve/work/voice/clone/synthesize
请求方式：POST

请求参数说明：
- id: Long，必填，原作品视频的id
- ttsMetaResult: str，必填，修改后的配音信息JSON字符串
  说明：
    需将重新配音任务结果中的urls字段，替换到原始ttsMetaResult对应句子的tgt_vocal_url中，
    其他参数一般无需修改。
"""

from typing import Optional
from ghostcut_python_sdk.ghostcut.models.ghostcut_model import GhostCutModel
import json


class GhostCutVoiceResynthesizeTaskSubmitRequest(GhostCutModel):
    def __init__(
        self,
        id: Optional[int] = None,
        ttsMetaResult: Optional[str] = None,
    ):
        """
        :param id: int, 必填，原作品视频ID
        :param ttsMetaResult: str, 必填，修改后的配音信息JSON字符串
        """
        self.id = id
        self.ttsMetaResult = ttsMetaResult

    def validate(self):
        if self.id is None or not isinstance(self.id, int):
            raise ValueError("id 必填且必须为整数")
        if not self.ttsMetaResult or not isinstance(self.ttsMetaResult, str):
            raise ValueError("ttsMetaResult 必填且必须为字符串")
        try:
            json.loads(self.ttsMetaResult)
        except Exception:
            raise ValueError("ttsMetaResult 必须是合法的JSON字符串")

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map
        return {
            "id": self.id,
            "ttsMetaResult": self.ttsMetaResult
        }

    def from_map(self, m: Optional[dict] = None):
        m = m or {}
        self.id = m.get("id", None)
        self.ttsMetaResult = m.get("ttsMetaResult", None)
        return self
