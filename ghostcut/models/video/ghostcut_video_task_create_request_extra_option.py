# -*- coding: utf-8 -*-
import json
from typing import Optional, List, Dict, Any
from ghostcut_python_sdk.ghostcut.models.ghostcut_model import GhostCutModel


class GhostCutVideoTaskCreateRequestExtraOption(GhostCutModel):
    """
    任务请求的 extraOptions 参数类，支持：
    - 视频去文字、文字翻译、语音翻译、OCR提取字幕
    - 视频去重
    - 智能配乐
    - 短剧二创
    - 解说二创
    - 字幕压制
    - 背景音乐去除

    主要字段说明：
    - needWanyin (Byte)              是否开启语音合成，必填
    - wyTaskType (String)            语音任务类型，必填，短剧二创和解说二创及字幕压制有不同取值要求
    - wyVoiceParam (String)          JSON字符串，必填，格式根据任务不同有所不同，必须包含特定字段
    - needChineseOcclude (Byte)      去文字开关，不同接口含义不同，部分接口必填
    - wyNeedText (Byte)              是否开启新字幕展示，必填
    - sourceLang (String)            源语言，必填
    - lang (String)                  目标语言，允许空或null表示不翻译
    - removeBgAudio (Byte)           是否去除背景音，部分接口可选
    - needMask (Byte)                去重特效代码，部分接口可选
    - extraOptions (Dict)            扩展配置，JSON结构，内容根据接口不同有所差异
    """

    def __init__(
        self,
        # 视频去文字及OCR
        needChineseOcclude: Optional[int] = None,
        videoInpaintLang: Optional[str] = None,
        videoInpaintMasks: Optional[List[Dict[str, Any]]] = None,

        # 语言相关
        sourceLang: Optional[str] = None,
        lang: Optional[str] = None,

        # 语音相关
        needWanyin: Optional[int] = None,
        wyTaskType: Optional[str] = None,
        wyNeedText: Optional[int] = None,
        wyVoiceParam: Optional[str] = None,
        removeBgAudio: Optional[int] = None,

        # 文字翻译相关
        bboxGroups: Optional[List[List[List[int]]]] = None,

        # 视频去重相关
        needTrim: Optional[int] = None,
        needMask: Optional[int] = None,
        needMirror: Optional[int] = None,
        needRescale: Optional[int] = None,
        needShift: Optional[int] = None,
        randomBorder: Optional[int] = None,
        needTransition: Optional[int] = None,

        # 智能配乐相关
        needRhythm: Optional[int] = None,
        musicRegion: Optional[str] = None,
        rhythmParam: Optional[str] = None,

        # 扩展配置
        extraOptions: Optional[Dict[str, Any]] = None,
    ):
        # 视频去文字、OCR
        self.needChineseOcclude = needChineseOcclude
        self.videoInpaintLang = videoInpaintLang
        self.videoInpaintMasks = videoInpaintMasks or []

        # 语言相关
        self.sourceLang = sourceLang
        self.lang = lang

        # 语音相关
        self.needWanyin = needWanyin
        self.wyTaskType = wyTaskType
        self.wyNeedText = wyNeedText
        self.wyVoiceParam = wyVoiceParam
        self.removeBgAudio = removeBgAudio

        # 文字翻译
        self.bboxGroups = bboxGroups or []

        # 视频去重
        self.needTrim = needTrim
        self.needMask = needMask
        self.needMirror = needMirror
        self.needRescale = needRescale
        self.needShift = needShift
        self.randomBorder = randomBorder
        self.needTransition = needTransition

        # 智能配乐
        self.needRhythm = needRhythm
        self.musicRegion = musicRegion
        self.rhythmParam = rhythmParam

        # 扩展配置
        self.extraOptions = extraOptions or {}

    def validate(self, mode: Optional[str] = None):
        """
        参数校验，支持不同接口模式：
        - mode="short_drama": 短剧二创
        - mode="narration": 解说二创
        - mode="subtitle": 字幕压制
        - mode="remove_bg_music": 背景音乐去除
        - mode="music": 智能配乐
        - mode="ocr": OCR模式
        - mode=None: 宽松校验
        """

        def check_json_fields(json_str: str, required_fields: Dict[str, type]) -> dict:
            try:
                obj = json.loads(json_str)
            except Exception:
                raise ValueError("字段必须是合法的JSON字符串")
            for k, v in required_fields.items():
                if k not in obj:
                    raise ValueError(f"JSON缺少必填字段: {k}")
                if v is not None and not isinstance(obj[k], v):
                    raise ValueError(f"字段 {k} 类型错误，应为{v}")
            return obj

        valid_langs = {
            "zh", "en", "ja", "ko", "id", "ms", "fil",
            "de", "fr", "ar", "es", "pt", "it", "tr"
        }

        # OCR模式特殊校验
        if mode == "ocr":
            if self.needChineseOcclude != 14:
                raise ValueError("OCR模式需needChineseOcclude=14")
            if not self.videoInpaintLang or self.videoInpaintLang not in valid_langs:
                raise ValueError("OCR模式videoInpaintLang不合法")
            if not self.lang or not isinstance(self.lang, str):
                raise ValueError("OCR模式lang必须是非空字符串")
            if not (self.videoInpaintMasks and isinstance(self.videoInpaintMasks, list)):
                raise ValueError("OCR模式videoInpaintMasks必须是非空列表")
            for mask in self.videoInpaintMasks:
                if not isinstance(mask, dict):
                    raise ValueError("videoInpaintMasks元素必须是字典")
                if mask.get("type") != "trans_only_ocr":
                    raise ValueError("videoInpaintMasks中type必须是'trans_only_ocr'")
                if "region" not in mask or not isinstance(mask["region"], list):
                    raise ValueError("videoInpaintMasks中必须包含region字段为列表")
            return

        # 智能配乐模式校验
        if mode == "music":
            if self.needRhythm not in (1, 2, 3):
                raise ValueError("智能配乐needRhythm必须是1, 2或3")
            if self.needRhythm == 1:
                if self.musicRegion is not None and not isinstance(self.musicRegion, str):
                    raise ValueError("musicRegion需为字符串或None")
            elif self.needRhythm == 2:
                if not self.rhythmParam or not isinstance(self.rhythmParam, str):
                    raise ValueError("rhythmParam必须为非空字符串")
                rp_obj = json.loads(self.rhythmParam)
                if "url" not in rp_obj or not rp_obj["url"]:
                    raise ValueError("rhythmParam中url字段不能为空")
            return

        # 短剧二创模式校验
        if mode == "short_drama":
            if self.needWanyin not in (0, 1):
                raise ValueError("短剧二创needWanyin必须是0或1")
            if not (self.wyTaskType and isinstance(self.wyTaskType, str)):
                raise ValueError("短剧二创wyTaskType必填且为字符串")
            if self.wyNeedText not in (0, 1):
                raise ValueError("短剧二创wyNeedText必须是0或1")
            if not (self.wyVoiceParam and isinstance(self.wyVoiceParam, str)):
                raise ValueError("短剧二创wyVoiceParam必填且为字符串")
            wyvp_obj = check_json_fields(self.wyVoiceParam, {"_recreate": str, "font_param": dict})
            font_param = wyvp_obj["font_param"]
            if "style" not in font_param or not isinstance(font_param["style"], str):
                raise ValueError("wyVoiceParam.font_param中缺少style或类型错误")
            if "font_size" not in font_param or not isinstance(font_param["font_size"], (int, float)):
                raise ValueError("wyVoiceParam.font_param中缺少font_size或类型错误")
            if "position" not in font_param or not (0 <= font_param["position"] <= 1):
                raise ValueError("wyVoiceParam.font_param.position范围应为0~1")

            if self.needChineseOcclude not in (0, 1):
                raise ValueError("短剧二创needChineseOcclude必须是0或1")
            if not (self.sourceLang and isinstance(self.sourceLang, str)):
                raise ValueError("短剧二创sourceLang必填且为字符串")
            if self.lang is not None and not (isinstance(self.lang, str) or self.lang == "" or self.lang is None):
                raise ValueError("短剧二创lang必须是字符串或空")
            if self.needMask is not None and self.needMask not in range(0, 11):
                raise ValueError("短剧二创needMask范围0-10")

            # extraOptions中extra_need_mask_config字段bool校验
            if self.extraOptions is not None:
                if not isinstance(self.extraOptions, dict):
                    raise ValueError("extraOptions必须是字典")
                extra_mask_cfg = self.extraOptions.get("extra_need_mask_config")
                if extra_mask_cfg is not None:
                    if not isinstance(extra_mask_cfg, dict):
                        raise ValueError("extra_need_mask_config必须是字典")
                    for k in ("progress_bar_on", "sticker_on", "frame_on"):
                        if k in extra_mask_cfg and not isinstance(extra_mask_cfg[k], bool):
                            raise ValueError(f"extra_need_mask_config中{k}必须是bool")
            return

        # 解说二创模式校验
        if mode == "narration":
            if self.needWanyin != 1:
                raise ValueError("解说二创needWanyin必须为1")
            if self.wyTaskType not in ("REPHRASE", "FULL"):
                raise ValueError("解说二创wyTaskType必须是REPHRASE或FULL")
            if not (self.wyVoiceParam and isinstance(self.wyVoiceParam, str)):
                raise ValueError("解说二创wyVoiceParam必填且为字符串")
            wyvp_obj = check_json_fields(self.wyVoiceParam, {"_recreate": str})
            if wyvp_obj["_recreate"] != "b":
                raise ValueError("解说二创wyVoiceParam._recreate必须是'b'")
            if self.needChineseOcclude != 1:
                raise ValueError("解说二创needChineseOcclude必须为1")
            if self.wyNeedText != 1:
                raise ValueError("解说二创wyNeedText必须为1")
            if not (self.sourceLang and isinstance(self.sourceLang, str)):
                raise ValueError("解说二创sourceLang必填且为字符串")
            if self.lang is not None and not (isinstance(self.lang, str) or self.lang == "" or self.lang is None):
                raise ValueError("解说二创lang必须是字符串或空")

            if self.extraOptions is not None:
                if not isinstance(self.extraOptions, dict):
                    raise ValueError("extraOptions必须是字典")
                extra_mask_cfg = self.extraOptions.get("extra_need_mask_config")
                if extra_mask_cfg is not None:
                    if not isinstance(extra_mask_cfg, dict):
                        raise ValueError("extra_need_mask_config必须是字典")
                    for k in ("progress_bar_on", "sticker_on", "frame_on"):
                        if k in extra_mask_cfg and not isinstance(extra_mask_cfg[k], bool):
                            raise ValueError(f"extra_need_mask_config中{k}必须是bool")
            return

        # 字幕压制模式校验
        if mode == "subtitle":
            if not (self.sourceLang and isinstance(self.sourceLang, str)):
                raise ValueError("字幕压制sourceLang必填且为字符串")
            if not (self.lang and isinstance(self.lang, str)):
                raise ValueError("字幕压制lang必填且为字符串")
            if self.needWanyin != 1:
                raise ValueError("字幕压制needWanyin必须为1")
            if self.wyTaskType != "NO_TTS":
                raise ValueError("字幕压制wyTaskType必须是NO_TTS")
            if self.wyNeedText not in (0, 1):
                raise ValueError("字幕压制wyNeedText必须是0或1")
            if not (self.wyVoiceParam and isinstance(self.wyVoiceParam, str)):
                raise ValueError("字幕压制wyVoiceParam必填且为字符串")
            try:
                wyvp_obj = json.loads(self.wyVoiceParam)
            except Exception:
                raise ValueError("字幕压制wyVoiceParam必须是合法JSON")
            font_param = wyvp_obj.get("font_param")
            if not (font_param and isinstance(font_param, dict)):
                raise ValueError("wyVoiceParam必须包含font_param且为字典")
            if "style" not in font_param or not isinstance(font_param["style"], str):
                raise ValueError("font_param缺少style或类型错误")
            if "font_size" not in font_param or not isinstance(font_param["font_size"], (int, float)):
                raise ValueError("font_param缺少font_size或类型错误")
            if "position" not in font_param or not (0 <= font_param["position"] <= 1):
                raise ValueError("font_param.position范围应为0~1")

            if self.removeBgAudio is not None and self.removeBgAudio not in (0, 1, 2):
                raise ValueError("removeBgAudio取值必须是0,1,2")

            if self.extraOptions is not None:
                if not isinstance(self.extraOptions, dict):
                    raise ValueError("extraOptions必须是字典")
                cis = self.extraOptions.get("customer_input_srt")
                if not (cis and isinstance(cis, dict)):
                    raise ValueError("extraOptions必须包含customer_input_srt且为字典")
                if "source" not in cis or not cis["source"]:
                    raise ValueError("customer_input_srt必须含非空source字段")
                if "translation" in cis and cis["translation"] is not None and not isinstance(cis["translation"], str):
                    raise ValueError("customer_input_srt.translation必须是字符串或None")
            return

        # 背景音乐去除模式校验
        if mode == "remove_bg_music":
            if self.needWanyin != 1:
                raise ValueError("背景音乐去除needWanyin必须为1")
            if self.wyTaskType != "NO_TTS":
                raise ValueError("背景音乐去除wyTaskType必须是NO_TTS")
            if self.wyNeedText != 0:
                raise ValueError("背景音乐去除wyNeedText必须是0")
            if self.removeBgAudio is not None and self.removeBgAudio not in (0, 1, 2):
                raise ValueError("removeBgAudio取值必须是0,1,2")
            return

        # 宽松校验，仅做简单值域检查
        if self.needWanyin is not None and self.needWanyin not in (0, 1):
            raise ValueError("needWanyin仅支持0或1")
        if self.needChineseOcclude is not None and self.needChineseOcclude not in (0,1,2,11,14):
            raise ValueError("needChineseOcclude取值异常")
        if self.needMask is not None and not (0 <= self.needMask <= 10):
            raise ValueError("needMask取值范围0-10")

    def to_map(self) -> dict:
        _map = {}

        if self.needChineseOcclude is not None:
            _map["needChineseOcclude"] = self.needChineseOcclude
        if self.videoInpaintLang is not None:
            _map["videoInpaintLang"] = self.videoInpaintLang
        if self.videoInpaintMasks:
            _map["videoInpaintMasks"] = json.dumps(self.videoInpaintMasks, ensure_ascii=False)

        if self.sourceLang is not None:
            _map["sourceLang"] = self.sourceLang
        if self.lang is not None:
            _map["lang"] = self.lang

        if self.needWanyin is not None:
            _map["needWanyin"] = self.needWanyin
        if self.wyTaskType is not None:
            _map["wyTaskType"] = self.wyTaskType
        if self.wyNeedText is not None:
            _map["wyNeedText"] = self.wyNeedText
        if self.wyVoiceParam is not None:
            _map["wyVoiceParam"] = self.wyVoiceParam
        if self.removeBgAudio is not None:
            _map["removeBgAudio"] = self.removeBgAudio

        if self.bboxGroups:
            _map["bboxGroups"] = json.dumps(self.bboxGroups, ensure_ascii=False)

        if self.needTrim is not None:
            _map["needTrim"] = self.needTrim
        if self.needMask is not None:
            _map["needMask"] = self.needMask
        if self.needMirror is not None:
            _map["needMirror"] = self.needMirror
        if self.needRescale is not None:
            _map["needRescale"] = self.needRescale
        if self.needShift is not None:
            _map["needShift"] = self.needShift
        if self.randomBorder is not None:
            _map["randomBorder"] = self.randomBorder
        if self.needTransition is not None:
            _map["needTransition"] = self.needTransition

        if self.needRhythm is not None:
            _map["needRhythm"] = self.needRhythm
        if self.musicRegion is not None:
            _map["musicRegion"] = self.musicRegion
        if self.rhythmParam is not None:
            _map["rhythmParam"] = self.rhythmParam

        if self.extraOptions:
            _map["extraOptions"] = json.dumps(self.extraOptions, ensure_ascii=False)

        return _map

    def from_map(self, m: Optional[dict] = None):
        m = m or {}

        self.needChineseOcclude = m.get("needChineseOcclude")
        self.videoInpaintLang = m.get("videoInpaintLang")

        vim = m.get("videoInpaintMasks")
        if vim is not None:
            if isinstance(vim, str):
                try:
                    self.videoInpaintMasks = json.loads(vim)
                except Exception:
                    self.videoInpaintMasks = vim
            else:
                self.videoInpaintMasks = vim
        else:
            self.videoInpaintMasks = []

        self.sourceLang = m.get("sourceLang")
        self.lang = m.get("lang")

        self.needWanyin = m.get("needWanyin")
        self.wyTaskType = m.get("wyTaskType")
        self.wyNeedText = m.get("wyNeedText")
        self.wyVoiceParam = m.get("wyVoiceParam")
        self.removeBgAudio = m.get("removeBgAudio")

        bboxs = m.get("bboxGroups")
        if bboxs is not None:
            if isinstance(bboxs, str):
                try:
                    self.bboxGroups = json.loads(bboxs)
                except Exception:
                    self.bboxGroups = bboxs
            else:
                self.bboxGroups = bboxs
        else:
            self.bboxGroups = []

        self.needTrim = m.get("needTrim")
        self.needMask = m.get("needMask")
        self.needMirror = m.get("needMirror")
        self.needRescale = m.get("needRescale")
        self.needShift = m.get("needShift")
        self.randomBorder = m.get("randomBorder")
        self.needTransition = m.get("needTransition")

        self.needRhythm = m.get("needRhythm")
        self.musicRegion = m.get("musicRegion")
        self.rhythmParam = m.get("rhythmParam")

        eo = m.get("extraOptions")
        if eo is not None:
            if isinstance(eo, str):
                try:
                    self.extraOptions = json.loads(eo)
                except Exception:
                    self.extraOptions = eo
            else:
                self.extraOptions = eo
        else:
            self.extraOptions = {}

        return self
