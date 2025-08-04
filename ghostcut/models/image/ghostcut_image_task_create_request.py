# -*- coding: utf-8 -*-

# 5.1 创建图片任务
# 接口文档：https://jollytoday.feishu.cn/docx/U73qdBhWbozFdpx4eTvcIO4gn7e#share-BInTdcm2roNEVvxmDZdctlumnuc

from ghostcut_python_sdk.ghostcut.models.ghostcut_model import GhostCutModel
from ghostcut_python_sdk.ghostcut.models.image.ghostcut_image_task_create_request_extra_option import (
    GhostCutImageTaskCreateRequestExtraOption,
)
import json


class GhostCutImageTaskCreateRequest(GhostCutModel):
    def __init__(
        self,
        downloadInfo: str = None,
        translateOn: int = None,
        commodityFilterOn: int = 0,
        synthesisOn: int = 1,
        srcLang: str = None,
        tgtLang: str = None,
        callback: str = None,
        needTrim: int = None,
        needMask: int = None,
        extraOptions: GhostCutImageTaskCreateRequestExtraOption = None,
    ):
        """
        创建单张图片任务请求参数模型

        :param downloadInfo: (必填) 单张图片下载信息，JSON字符串格式，示例：
                             '{"url":"https://example.com/your_image.png"}'
                             长度不超过1000字符，url不能包含中文字符
        :param translateOn: (必填) 是否开启翻译，0=否，仅擦除；1=是，擦除+翻译
        :param commodityFilterOn: (可选，默认0) 是否开启商品文字保护，0=否，1=是
        :param synthesisOn: (必填，默认1) 是否开启图片合成，0=否，1=是
        :param srcLang: (必填) 源语言代码，如："zh"、"auto"等
        :param tgtLang: (必填) 目标语言代码，如："en"、"zh-hant"等；不翻译时可传空字符串""
        :param callback: (可选) 处理完成后的回调地址URL
        :param needTrim: (可选) 是否需要裁剪（接口文档未详细说明）
        :param needMask: (可选) 是否需要蒙版（接口文档未详细说明）
        :param extraOptions: (可选) 额外剪辑配置，封装为GhostCutImageTaskCreateRequestExtraOption对象
        """
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
        """
        校验请求参数合法性，若参数不符合规则，抛出 ValueError 异常
        """
        if not self.downloadInfo:
            raise ValueError("downloadInfo 为必填项")
        if not isinstance(self.downloadInfo, str):
            raise ValueError("downloadInfo 必须是 JSON 字符串")
        if len(self.downloadInfo) > 1000:
            raise ValueError("downloadInfo 长度不能超过1000字符")
        try:
            di_obj = json.loads(self.downloadInfo)
        except json.JSONDecodeError:
            raise ValueError("downloadInfo 必须是合法的 JSON 字符串")
        if not isinstance(di_obj, dict):
            raise ValueError("downloadInfo JSON 必须是一个对象")
        url_val = di_obj.get("url")
        if not url_val or not isinstance(url_val, str):
            raise ValueError("downloadInfo 中必须包含非空字符串 url 字段")
        if any('\u4e00' <= ch <= '\u9fff' for ch in url_val):
            raise ValueError("downloadInfo 中 url 不能包含中文字符")

        if self.translateOn not in (0, 1):
            raise ValueError("translateOn 必须是 0 或 1")

        if not self.srcLang or not isinstance(self.srcLang, str):
            raise ValueError("srcLang 为必填字符串")

        if self.tgtLang is None or not isinstance(self.tgtLang, str):
            raise ValueError("tgtLang 必须是字符串（可为空字符串）")

        if self.commodityFilterOn not in (0, 1):
            raise ValueError("commodityFilterOn 必须是 0 或 1")

        if self.synthesisOn not in (0, 1):
            raise ValueError("synthesisOn 必须是 0 或 1")

        if self.callback is not None and not isinstance(self.callback, str):
            raise ValueError("callback 必须是字符串")

        if self.extraOptions is not None:
            if not isinstance(self.extraOptions, GhostCutImageTaskCreateRequestExtraOption):
                raise ValueError("extraOptions 必须是 GhostCutImageTaskCreateRequestExtraOption 类型")
            self.extraOptions.validate()

        for attr_name in ['needTrim', 'needMask']:
            val = getattr(self, attr_name)
            if val is not None and val not in (0, 1):
                raise ValueError(f"{attr_name} 必须是 0 或 1")

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
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
            result["extraOptions"] = self.extraOptions.to_map()
        if self.needTrim is not None:
            result["needTrim"] = self.needTrim
        if self.needMask is not None:
            result["needMask"] = self.needMask
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.downloadInfo = m.get("downloadInfo")
        self.translateOn = m.get("translateOn")
        self.commodityFilterOn = m.get("commodityFilterOn", 0)
        self.synthesisOn = m.get("synthesisOn", 1)
        self.srcLang = m.get("srcLang")
        self.tgtLang = m.get("tgtLang")
        self.callback = m.get("callback")
        if m.get("extraOptions") is not None:
            eo = GhostCutImageTaskCreateRequestExtraOption()
            if isinstance(m.get("extraOptions"), dict):
                self.extraOptions = eo.from_map(m.get("extraOptions"))
            else:
                try:
                    eo_dict = json.loads(m.get("extraOptions"))
                    self.extraOptions = eo.from_map(eo_dict)
                except Exception:
                    self.extraOptions = None
        self.needTrim = m.get("needTrim")
        self.needMask = m.get("needMask")
        return self
