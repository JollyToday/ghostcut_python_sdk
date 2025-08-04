# -*- coding: utf-8 -*-

"""
3.3 查询训练的音色列表请求模型
文档地址： https://jollytoday.feishu.cn/wiki/Y9JSwDDo8iVWN2k0IELc5nsMn3f#share-IYDKdjyXcomIInxBDmIc4e9unxf
功能简述：
    分页查询创建的克隆声音列表，每页size默认20条，可指定分页参数和过滤条件。
接口地址：
    https://api.zhaoli.com/v-w-c/gateway/ve/voice/query_clone_voice
请求方式：
    POST

请求参数说明：
- pageNumber: int，必填，页码，从1开始，传1返回第一页数据
- pageSize: int，非必填，每页条数，默认20条
- id: long，非必填，声音ID，精确查询
- idVeVideoParseTask: long，非必填，生成接口任务ID（body的内容）
- prefix: str，非必填，cloneKwargs中的prefix，做筛选
- deleted: int，非必填，是否删除，1表示删除，0表示未删除
"""

from typing import Optional
from ghostcut_python_sdk.ghostcut.models.ghostcut_model import GhostCutModel


class GhostCutVoiceQueryCloneVoiceRequest(GhostCutModel):
    """
    查询训练音色列表请求模型
    """
    def __init__(
        self,
        pageNumber: Optional[int] = None,
        pageSize: Optional[int] = None,
        id: Optional[int] = None,
        idVeVideoParseTask: Optional[int] = None,
        prefix: Optional[str] = None,
        deleted: Optional[int] = None,
    ):
        """
        :param pageNumber: int, 必填，页码，从1开始
        :param pageSize: int, 非必填，每页条数，默认20条
        :param id: int, 非必填，声音ID，精确过滤
        :param idVeVideoParseTask: int, 非必填，生成接口任务ID
        :param prefix: str, 非必填，clone_kwargs中的prefix
        :param deleted: int, 非必填，是否删除，1表示删除，0表示未删除
        """
        self.pageNumber = pageNumber
        self.pageSize = pageSize
        self.id = id
        self.idVeVideoParseTask = idVeVideoParseTask
        self.prefix = prefix
        self.deleted = deleted

    def validate(self):
        """
        校验参数合法性
        """
        if self.pageNumber is None or not isinstance(self.pageNumber, int) or self.pageNumber < 1:
            raise ValueError("pageNumber 必填，且必须为大于等于1的整数")
        if self.pageSize is not None and (not isinstance(self.pageSize, int) or self.pageSize < 1):
            raise ValueError("pageSize 非必填，如传则必须为正整数")
        if self.id is not None and not isinstance(self.id, int):
            raise ValueError("id 非必填，如传必须为整数")
        if self.idVeVideoParseTask is not None and not isinstance(self.idVeVideoParseTask, int):
            raise ValueError("idVeVideoParseTask 非必填，如传必须为整数")
        if self.prefix is not None and not isinstance(self.prefix, str):
            raise ValueError("prefix 非必填，如传必须为字符串")
        if self.deleted is not None and self.deleted not in (0, 1):
            raise ValueError("deleted 非必填，如传必须为0或1")

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map
        data = {
            "pageNumber": self.pageNumber,
        }
        if self.pageSize is not None:
            data["pageSize"] = self.pageSize
        if self.id is not None:
            data["id"] = self.id
        if self.idVeVideoParseTask is not None:
            data["idVeVideoParseTask"] = self.idVeVideoParseTask
        if self.prefix is not None:
            data["prefix"] = self.prefix
        if self.deleted is not None:
            data["deleted"] = self.deleted
        return data

    def from_map(self, m: Optional[dict] = None):
        m = m or {}
        self.pageNumber = m.get("pageNumber", None)
        self.pageSize = m.get("pageSize", None)
        self.id = m.get("id", None)
        self.idVeVideoParseTask = m.get("idVeVideoParseTask", None)
        self.prefix = m.get("prefix", None)
        self.deleted = m.get("deleted", None)
        return self
