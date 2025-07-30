# -*- coding: utf-8 -*-

"""
4.3 查询视频文字翻译任务信息
# 接口文档：https://jollytoday.feishu.cn/docx/U73qdBhWbozFdpx4eTvcIO4gn7e#share-Tqz9dVXAuob5ssxgLRmcTu1wnQb

功能简述：
查询视频文字翻译的任务信息，可查阅视频文字翻译的原始文本数据，方便后续修改字幕并合成。

接口地址：
https://api.zhaoli.com/v-w-c/gateway/ve/work/getVeOcrTranslateTask
请求方式：
POST

请求参数：
- id (Long，必填)：视频文字翻译的任务id，通过【查询处理结果接口】中的idVeOcrTranslateTask获得。

响应参数：
- bboxGroup (Array)：关键参数，用于【4.4 文字翻译的重新处理接口】。
  其他响应参数可以忽略。
"""

from ghostcut_python_sdk.ghostcut.models.ghostcut_model import GhostCutModel


class GhostCutVeOcrTranslateTaskRequest(GhostCutModel):
    def __init__(
        self,
        id: int = None,
    ):
        """
        查询视频文字翻译任务信息请求参数模型

        :param id: (必填) 视频文字翻译任务ID，通过【查询处理结果接口】中的idVeOcrTranslateTask获得
        """
        self.id = id

    def validate(self):
        """
        校验请求参数合法性
        """
        if self.id is None:
            raise ValueError("id 为必填项")
        if not isinstance(self.id, int):
            raise ValueError("id 必须是整数类型")

    def to_map(self):
        """
        转换为字典，用于请求体json序列化
        """
        _map = super().to_map()
        if _map is not None:
            return _map

        return {
            "id": self.id,
        }

    def from_map(self, m: dict = None):
        """
        从字典初始化对象
        """
        m = m or dict()
        self.id = m.get("id")
        return self
