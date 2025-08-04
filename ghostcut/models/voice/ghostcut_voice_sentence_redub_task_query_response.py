# -*- coding: utf-8 -*-

"""
2.3 查询重新配音任务结果响应模型
文档地址： https://jollytoday.feishu.cn/wiki/Y9JSwDDo8iVWN2k0IELc5nsMn3f#share-TB5Udga1QozZ7UxnefKcgZYvnJg
接口地址：https://api.zhaoli.com/v-w-c/gateway/ve/work/voice/clone/task/query
请求方式：POST
接口返回：
{
  "body": {
    "task_status": int, // 任务状态，小于1处理中，等于1成功，大于1失败
    "raw_result": str  // JSON字符串，内部包含urls数组，配音结果音频地址
  }
}
"""

from typing import Optional, List, Dict
from ghostcut_python_sdk.ghostcut.models.ghostcut_model import GhostCutModel
import json


class GhostCutVoiceSentenceRedubTaskQueryResponseBody(GhostCutModel):
    def __init__(self, task_status: Optional[int] = None, raw_result: Optional[str] = None):
        """
        :param task_status: int, 任务状态，小于1处理中，等于1成功，大于1失败
        :param raw_result: str, JSON字符串，包含配音结果urls数组
        """
        self.task_status = task_status
        self.raw_result = raw_result

    def get_urls(self) -> Optional[List[str]]:
        """
        解析raw_result，返回urls列表
        """
        if not self.raw_result:
            return None
        try:
            result_dict = json.loads(self.raw_result)
            urls = result_dict.get("urls")
            if isinstance(urls, list):
                return urls
            return None
        except Exception:
            return None

    def from_map(self, m: Optional[Dict] = None):
        m = m or {}
        self.task_status = m.get("task_status", None)
        self.raw_result = m.get("raw_result", None)
        return self


class GhostCutVoiceSentenceRedubTaskQueryResponse(GhostCutModel):
    def __init__(self, body: Optional[GhostCutVoiceSentenceRedubTaskQueryResponseBody] = None):
        self.body = body or GhostCutVoiceSentenceRedubTaskQueryResponseBody()

    def from_map(self, m: Optional[Dict] = None):
        m = m or {}
        body_data = m.get("body", {})
        self.body = GhostCutVoiceSentenceRedubTaskQueryResponseBody().from_map(body_data)
        return self
