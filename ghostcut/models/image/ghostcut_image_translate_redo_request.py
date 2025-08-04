# -*- coding: utf-8 -*-

"""
5.4 通过API直接调整图片翻译结果并重新合成【异步】
# 接口文档：https://jollytoday.feishu.cn/docx/U73qdBhWbozFdpx4eTvcIO4gn7e#share-XaSCd8Q1QoJJGoxzwv2cqaqRnrY

功能简述：
本功能可以修改图片翻译的处理结果并重新发起合成任务（免费），可更改译文内容、译文文字颜色、译文描边颜色、译文字体大小。
如有其他编辑类需求，可通过精修编辑器二次调整。

接口地址：
https://api.zhaoli.com/v-w-c/gateway/ve/image/translate/redo
请求方式：
POST

请求参数：
- id (Long，必填)：图片翻译任务id，即【创建任务接口】中返回的任务ID
- result (String，必填)：编辑后的result值，即在【查询图片处理结果接口】返回值的body中result字段进行修改后的json字符串。
  建议仅修改meta_data中的"translation", "fill_color", "stroke_color", "trans_font_size"4个常用字段。
  注意本接口修改后不会进行自适应排版，文字过长可能导致内容重叠。

响应参数：
- body (Integer)：修改任务的发起是否正常，结果为1则正常(异步，会callback)
"""

from ghostcut_python_sdk.ghostcut.models.ghostcut_model import GhostCutModel


class GhostCutImageTranslateRedoRequest(GhostCutModel):
    def __init__(
        self,
        id: int = None,
        result: str = None,
    ):
        """
        通过API直接调整图片翻译结果并重新合成请求参数模型

        :param id: (必填) 图片翻译任务id，即创建任务接口返回的任务ID
        :param result: (必填) 编辑后的result值，json字符串，建议仅修改特定字段
        """
        self.id = id
        self.result = result

    def validate(self):
        """
        校验请求参数合法性，若参数不符合规则，抛出 ValueError 异常
        """
        if self.id is None:
            raise ValueError("id 为必填项")
        if not isinstance(self.id, int):
            raise ValueError("id 必须是整数类型")

        if self.result is None:
            raise ValueError("result 为必填项")
        if not isinstance(self.result, str):
            raise ValueError("result 必须是字符串类型")

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        return {
            "id": self.id,
            "result": self.result,
        }

    def from_map(self, m: dict = None):
        m = m or dict()
        self.id = m.get("id")
        self.result = m.get("result")
        return self
