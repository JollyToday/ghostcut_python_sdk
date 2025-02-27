# -*- coding: utf-8 -*-

# 5.1 创建图片任务
# https://jollytoday.feishu.cn/docx/U73qdBhWbozFdpx4eTvcIO4gn7e#share-BInTdcm2roNEVvxmDZdctlumnuc


from ghostcut.models.ghostcut_model import GhostCutModel
from typing import Dict, List, Any

from ghostcut.models.image.ghostcut_image_task_create_request_extra_option import (
    GhostCutImageTaskCreateRequestExtraOption,
)


class GhostCutImageTaskCreateRequest(GhostCutModel):
    def __init__(
        self,
        urls: List[str] = None,
        downloadInfos: List[str] = None,
        downloadInfo: str = None,
        translateOn: int = None,
        commodityFilterOn: int = None,
        synthesisOn: int = None,
        srcLang: str = None,
        tgtLang: str = None,
        callback: str = None,
        needTrim: int = None,
        needMask: int = None,
        extraOptions: GhostCutImageTaskCreateRequestExtraOption = None,
    ):
        self.urls = urls
        self.downloadInfos = downloadInfos
        self.downloadInfo = downloadInfo
        self.translateOn = translateOn
        self.commodityFilterOn = commodityFilterOn
        self.synthesisOn = synthesisOn
        self.srcLang = srcLang
        self.tgtLang = tgtLang
        self.callback = callback
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
            result["urls"] = self.urls
        if self.downloadInfos is not None:
            result["downloadInfos"] = self.downloadInfos
        if self.downloadInfo is not None:
            result["downloadInfo"] = self.downloadInfo
        if self.translateOn is not None:
            result["translateOn"] = self.translateOn
        if self.commodityFilterOn is not None:
            result["commodityFilterOn"] = self.commodityFilterOn
        if self.synthesisOn is not None:
            result["synthesisOn"] = self.synthesisOn
        if self.srcLang is not None:
            result["srcLang"] = self.srcLang
        if self.tgtLang is not None:
            result["tgtLang"] = self.tgtLang
        if self.callback is not None:
            result["callback"] = self.callback
        if self.extraOptions is not None:
            result["extraOptions"] = self.extraOptions
        if self.needTrim is not None:
            result["needTrim"] = self.needTrim
        if self.needMask is not None:
            result["needMask"] = self.needMask
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get("urls") is not None:
            self.urls = m.get("urls")
        if m.get("downloadInfos") is not None:
            self.downloadInfos = m.get("downloadInfos")
        if m.get("downloadInfo") is not None:
            self.downloadInfo = m.get("downloadInfo")
        if m.get("translateOn") is not None:
            self.translateOn = m.get("translateOn")
        if m.get("commodityFilterOn") is not None:
            self.commodityFilterOn = m.get("commodityFilterOn")
        if m.get("synthesisOn") is not None:
            self.synthesisOn = m.get("synthesisOn")
        if m.get("srcLang") is not None:
            self.srcLang = m.get("srcLang")
        if m.get("tgtLang") is not None:
            self.tgtLang = m.get("tgtLang")
        if m.get("callback") is not None:
            self.callback = m.get("callback")
        if m.get("extraOptions") is not None:
            self.extraOptions = m.get("extraOptions")
        if m.get("needTrim") is not None:
            self.needTrim = m.get("needTrim")
        if m.get("needMask") is not None:
            self.needMask = m.get("needMask")

        return self
