# -*- coding: utf-8 -*-

# 4.1.1.1 基础参数(必看)
# https://jollytoday.feishu.cn/docx/U73qdBhWbozFdpx4eTvcIO4gn7e#share-O8YRdF0OZogmbAxNF4vcaxZtnnb


from ghostcut.models.ghostcut_model import GhostCutModel
from typing import Dict, List, Any

from ghostcut.models.video.ghostcut_video_task_create_request_extra_option import GhostCutVideoTaskCreateRequestExtraOption


class GhostCutVideoTaskCreateRequest(GhostCutModel):
    def __init__(
        self,
        urls: List[str] = None,
        names: List[str] = None,
        resolution: str = None,
        callback: str = None,
        uid: str = None,
        extraOptions: GhostCutVideoTaskCreateRequestExtraOption = None,

        needTrim: int = None,
        needMask: int = None,
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
        pass

    def to_map(self):
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
            result['extraOptions'] = self.extraOptions
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
            self.extraOptions = m.get('extraOptions')
        if m.get("needTrim") is not None:
            self.needTrim = m.get("needTrim")
        if m.get("needMask") is not None:
            self.needMask = m.get("needMask")
        return self