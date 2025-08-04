# -*- coding: utf-8 -*-

from ghostcut_python_sdk.ghostcut.models.ghostcut_model import GhostCutModel
from typing import Dict, List, Any, Optional
from ghostcut_python_sdk.ghostcut.models.video.ghostcut_video_task_create_request_extra_option import GhostCutVideoTaskCreateRequestExtraOption


class GhostCutVideoTaskCreateRequest(GhostCutModel):
    def __init__(
        self,
        urls: Optional[List[str]] = None,
        names: Optional[List[str]] = None,
        resolution: Optional[str] = None,
        callback: Optional[str] = None,
        uid: Optional[str] = None,
        extraOptions: Optional[GhostCutVideoTaskCreateRequestExtraOption] = None,
        needTrim: Optional[int] = None,
        needMask: Optional[int] = None,
    ):
        self.urls = urls
        self.names = names
        self.resolution = resolution
        self.callback = callback
        self.uid = uid
        self.extraOptions = extraOptions
        self.needTrim = needTrim
        self.needMask = needMask

    def validate(self):
        # 验证 urls 必填且数量不超过20
        if not self.urls or not isinstance(self.urls, list) or len(self.urls) == 0:
            raise ValueError("urls字段为必填，且不能为空列表")
        if len(self.urls) > 20:
            raise ValueError("urls列表长度不能超过20个")

        # names 如果传入，长度要和 urls 对应
        if self.names:
            if not isinstance(self.names, list):
                raise ValueError("names必须是列表")
            if len(self.names) != len(self.urls):
                raise ValueError("names列表长度必须与urls长度一致")

        # resolution 验证是否为允许的值
        allowed_resolutions = ['480p', '720p', '1080p', None]
        if self.resolution not in allowed_resolutions:
            raise ValueError(f"resolution字段不合法，只支持{allowed_resolutions}")

        # extraOptions 必须是 GhostCutVideoTaskCreateRequestExtraOption 类型或者 None
        if self.extraOptions and not isinstance(self.extraOptions, GhostCutVideoTaskCreateRequestExtraOption):
            raise ValueError("extraOptions必须是GhostCutVideoTaskCreateRequestExtraOption类型")

        # needTrim 和 needMask 可以是0或1（根据业务定义）
        if self.needTrim not in (None, 0, 1):
            raise ValueError("needTrim只能为0或1")
        if self.needMask not in (None, 0, 1):
            raise ValueError("needMask只能为0或1")

    def to_map(self):
        # 先调用父类的 to_map，如果有值直接返回
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.urls is not None:
            result['urls'] = self.urls
        if self.names is not None:
            result['names'] = self.names
        if self.resolution is not None:
            result['resolution'] = self.resolution
        if self.callback is not None:
            result['callback'] = self.callback
        if self.uid is not None:
            result['uid'] = self.uid
        if self.extraOptions is not None:
            # 这里调用 extraOptions 的 to_map 方法，转换成字典
            result['extraOptions'] = self.extraOptions.to_map()
        if self.needTrim is not None:
            result["needTrim"] = self.needTrim
        if self.needMask is not None:
            result["needMask"] = self.needMask
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('urls') is not None:
            self.urls = m.get('urls')
        if m.get('names') is not None:
            self.names = m.get('names')
        if m.get('resolution') is not None:
            self.resolution = m.get('resolution')
        if m.get('callback') is not None:
            self.callback = m.get('callback')
        if m.get('uid') is not None:
            self.uid = m.get('uid')

        if m.get('extraOptions') is not None:
            # 这里判断 extraOptions 是字典，调用 from_map 转成对象
            if isinstance(m.get('extraOptions'), dict):
                eo = GhostCutVideoTaskCreateRequestExtraOption()
                self.extraOptions = eo.from_map(m.get('extraOptions'))
            else:
                # 如果不是字典，直接赋值（可能是字符串，视具体情况）
                self.extraOptions = m.get('extraOptions')

        if m.get("needTrim") is not None:
            self.needTrim = m.get("needTrim")
        if m.get("needMask") is not None:
            self.needMask = m.get("needMask")
        return self
