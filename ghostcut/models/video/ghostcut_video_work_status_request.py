# -*- coding: utf-8 -*-

"""
4.2 查询视频处理任务的处理结果
# 接口文档：https://jollytoday.feishu.cn/docx/U73qdBhWbozFdpx4eTvcIO4gn7e#share-N6gbdyCK8oH10qx0WMScP9FGnEe
功能简述：
本接口为异步接口的第二步，查询视频任务的处理结果，也可以通过在发起视频剪辑请求时传入callback得到回调通知。
回调时会将处理结果以JSON格式POST到callback指定的URL。
本接口仅用于查询视频任务处理结果，不能用于查询图片或声音克隆等结果。

接口地址：
https://api.zhaoli.com/v-w-c/gateway/ve/work/status
请求方式：
POST

分页查询接口地址（可选）：
https://api.zhaoli.com/v-w-c/gateway/ve/work/list
该接口不需传idWorks和idProjects，支持分页查询。

请求参数：
- idWorks (List[int]，与idProjects二选一)：通过作品ID查询结果，可传多个作品ID，优先级最高。
  作品ID即4.1创建视频处理任务响应结果body中的id。
- idProjects (List[int]，与idWorks二选一)：通过任务ID查询结果，可传多个任务ID，不传则按时间降序查询所有视频。
- page (int，非必填)：页码，从0开始，不需要分页传null。
- pageSize (int，非必填)：查询条数，不需要分页传null，最大2000，超过2000只返回2000条。
- createTimeGreaterThanOrEqualTo (int，非必填)：时间戳（毫秒），查询创建时间大于或等于该值的数据。
- createTimeLessThan (int，非必填）：时间戳（毫秒），查询创建时间小于该值的数据。
"""

from typing import List, Optional
from ghostcut_python_sdk.ghostcut.models.ghostcut_model import GhostCutModel


class GhostCutVideoWorkStatusRequest(GhostCutModel):
    def __init__(
        self,
        idWorks: Optional[List[int]] = None,
        idProjects: Optional[List[int]] = None,
        page: Optional[int] = None,
        pageSize: Optional[int] = None,
        createTimeGreaterThanOrEqualTo: Optional[int] = None,
        createTimeLessThan: Optional[int] = None,
    ):
        """
        查询视频处理任务结果请求参数模型

        :param idWorks: 与idProjects二选一，通过作品ID查询结果，可传多个，优先级最高
        :param idProjects: 与idWorks二选一，通过任务ID查询结果，可传多个
        :param page: 页码，从0开始，分页查询时必填，不分页传None
        :param pageSize: 查询条数，最大2000，不分页传None
        :param createTimeGreaterThanOrEqualTo: 时间戳（毫秒），查询创建时间>=该值的数据
        :param createTimeLessThan: 时间戳（毫秒），查询创建时间<该值的数据
        """
        self.idWorks = idWorks
        self.idProjects = idProjects
        self.page = page
        self.pageSize = pageSize
        self.createTimeGreaterThanOrEqualTo = createTimeGreaterThanOrEqualTo
        self.createTimeLessThan = createTimeLessThan

    def validate(self):
        """
        校验参数合法性
        """
        if self.idWorks and self.idProjects:
            # 理论上两个参数二选一，传入两个预警或异常
            pass  # 这里不抛异常，但提示可以加入日志或警告

        if self.page is not None and (not isinstance(self.page, int) or self.page < 0):
            raise ValueError("page 必须为非负整数或None")

        if self.pageSize is not None:
            if not isinstance(self.pageSize, int):
                raise ValueError("pageSize 必须为整数或None")
            if self.pageSize > 2000:
                # 超出最大限制，建议客户端限制，但接口返回会自动截断
                pass

        if self.createTimeGreaterThanOrEqualTo is not None and not isinstance(self.createTimeGreaterThanOrEqualTo, int):
            raise ValueError("createTimeGreaterThanOrEqualTo 必须为整数（时间戳毫秒）或None")

        if self.createTimeLessThan is not None and not isinstance(self.createTimeLessThan, int):
            raise ValueError("createTimeLessThan 必须为整数（时间戳毫秒）或None")

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        d = dict()
        if self.idWorks is not None:
            d["idWorks"] = self.idWorks
        if self.idProjects is not None:
            d["idProjects"] = self.idProjects
        if self.page is not None:
            d["page"] = self.page
        if self.pageSize is not None:
            d["pageSize"] = self.pageSize
        if self.createTimeGreaterThanOrEqualTo is not None:
            d["createTimeGreaterThanOrEqualTo"] = self.createTimeGreaterThanOrEqualTo
        if self.createTimeLessThan is not None:
            d["createTimeLessThan"] = self.createTimeLessThan
        return d

    def from_map(self, m: dict = None):
        m = m or dict()
        self.idWorks = m.get("idWorks")
        self.idProjects = m.get("idProjects")
        self.page = m.get("page")
        self.pageSize = m.get("pageSize")
        self.createTimeGreaterThanOrEqualTo = m.get("createTimeGreaterThanOrEqualTo")
        self.createTimeLessThan = m.get("createTimeLessThan")
        return self
