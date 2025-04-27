# -*- coding: utf-8 -*-
import json
from typing import Optional, Union, List, Dict, Any
from  ghostcut_python_sdk.ghostcut.client import ZhaoliClient,ZhaoliAPIException
# 4. AI视频相关API 调用示例
# https://jollytoday.feishu.cn/docx/U73qdBhWbozFdpx4eTvcIO4gn7e#share-HwKldyKEUoRGMnxgGTycUamRn0c



class VideoAPI:
    """
    AI视频相关API封装
    支持创建异步视频处理任务，查询任务状态
    """

    def __init__(self, client: ZhaoliClient):
        self.client = client

    def create_task(
        self,
        urls: List[str],
        names: Optional[List[str]] = None,
        resolution: Optional[str] = None,
        callback: Optional[str] = None,
        uid: Optional[str] = None,
        extra_options: Optional[Union[str, Dict[str, Any]]] = None,
        # 视频去文字相关
        need_chinese_occlude: Optional[int] = None,
        video_inpaint_lang: Optional[str] = None,
        video_inpaint_masks: Optional[Union[str, List[Dict[str, Any]]]] = None,
        need_crop: Optional[int] = None,
        need_crop_color: Optional[str] = None,
        # 语音翻译相关
        source_lang: Optional[str] = None,
        lang: Optional[str] = None,
        need_wanyin: Optional[int] = None,
        wy_task_type: Optional[str] = None,
        wy_need_text: Optional[int] = None,
        wy_voice_param: Optional[Union[str, Dict[str, Any]]] = None,
        remove_bg_audio: Optional[int] = None,
        # 文字翻译相关
        bbox_groups: Optional[Union[str, Dict[str, Any]]] = None,
        # 去重相关
        need_trim: Optional[int] = None,
        need_mask: Optional[int] = None,
        need_mirror: Optional[int] = None,
        need_rescale: Optional[int] = None,
        need_shift: Optional[int] = None,
        random_border: Optional[int] = None,
        need_transition: Optional[int] = None,
        # 智能配乐相关
        need_rhythm: Optional[int] = None,
        music_region: Optional[str] = None,
        rhythm_param: Optional[Union[str, Dict[str, Any]]] = None,
        # 短剧二创和解说二创相关
        wy_task_type_extra: Optional[str] = None,
        extra_options_dict: Optional[Dict[str, Any]] = None,
    ) -> int:
        """
        创建视频处理任务接口

        :param urls: 必填，视频URL列表，最多20个
        :param names: 可选，视频对应名称列表，长度和urls对应
        :param resolution: 分辨率，如"480p","720p","1080p"
        :param callback: 回调地址
        :param uid: 用户ID
        :param extra_options: 额外参数，字符串或字典
        :param need_chinese_occlude: 视频去文字功能开关，0~3
        :param video_inpaint_lang: 去文字语言，"zh","en"等
        :param video_inpaint_masks: 视频框设置，json字符串或列表
        :param need_crop: 是否裁剪，0/1
        :param need_crop_color: 裁剪填充色，如"#000000"
        :param source_lang: 语音翻译源语言
        :param lang: 语音翻译目标语言
        :param need_wanyin: 语音翻译参数，必传
        :param wy_task_type: 语音翻译类型
        :param wy_need_text: 是否开启字幕展示
        :param wy_voice_param: 配音参数，字符串或dict
        :param remove_bg_audio: 背景音处理方式
        :param bbox_groups: 文字翻译预设样式，字符串或dict
        :param need_trim: 去重基础开关
        :param need_mask: 去重特效
        :param need_mirror: 镜像翻转
        :param need_rescale: 缩放去重
        :param need_shift: 随机移动
        :param random_border: 随机边框
        :param need_transition: 转场开关（维护中）
        :param need_rhythm: 智能配乐类型
        :param music_region: 配乐区域
        :param rhythm_param: 配乐参数，字符串或dict
        :param wy_task_type_extra: 短剧/解说二创特定类型，如"REPHRASE"
        :param extra_options_dict: 额外复杂配置，优先于extra_options参数
        :return: 任务ID或视频ID（int）
        """
        path = "/ve/work/free"
        params: Dict[str, Any] = {}

        if not urls or not isinstance(urls, list) or len(urls) > 20:
            raise ValueError("urls 必须是非空列表，且最多20个元素")
        params["urls"] = urls

        if names:
            if not isinstance(names, list):
                raise ValueError("names必须是列表")
            # 如果长度与urls不匹配，忽略names
            if len(names) == len(urls):
                params["names"] = names
            else:
                params["names"] = [""] * len(urls)

        if resolution:
            params["resolution"] = resolution

        if callback:
            params["callback"] = callback

        if uid:
            params["uid"] = uid

        # 合并extra_options参数（字符串或字典）
        if extra_options_dict:
            # 优先使用字典形式
            if isinstance(extra_options_dict, dict):
                params["extraOptions"] = json.dumps(extra_options_dict, ensure_ascii=False)
            else:
                raise ValueError("extra_options_dict必须是字典")
        elif extra_options:
            if isinstance(extra_options, dict):
                params["extraOptions"] = json.dumps(extra_options, ensure_ascii=False)
            elif isinstance(extra_options, str):
                params["extraOptions"] = extra_options
            else:
                raise ValueError("extra_options必须是dict或str")

        # 视频去文字相关参数
        if need_chinese_occlude is not None:
            params["needChineseOcclude"] = need_chinese_occlude

        if video_inpaint_lang is not None:
            params["videoInpaintLang"] = video_inpaint_lang

        if video_inpaint_masks is not None:
            if isinstance(video_inpaint_masks, list):
                params["videoInpaintMasks"] = json.dumps(video_inpaint_masks, ensure_ascii=False)
            elif isinstance(video_inpaint_masks, str):
                params["videoInpaintMasks"] = video_inpaint_masks
            else:
                raise ValueError("video_inpaint_masks必须是list或json字符串")

        if need_crop is not None:
            params["needCrop"] = need_crop

        if need_crop_color is not None:
            params["needCropColor"] = need_crop_color

        # 语音翻译参数
        if source_lang is not None:
            params["sourceLang"] = source_lang

        if lang is not None:
            params["lang"] = lang

        if need_wanyin is not None:
            params["needWanyin"] = need_wanyin

        if wy_task_type is not None:
            params["wyTaskType"] = wy_task_type

        if wy_need_text is not None:
            params["wyNeedText"] = wy_need_text

        if wy_voice_param is not None:
            if isinstance(wy_voice_param, dict):
                params["wyVoiceParam"] = json.dumps(wy_voice_param, ensure_ascii=False)
            elif isinstance(wy_voice_param, str):
                params["wyVoiceParam"] = wy_voice_param
            else:
                raise ValueError("wy_voice_param必须是dict或str")

        if remove_bg_audio is not None:
            params["removeBgAudio"] = remove_bg_audio

        # 文字翻译相关样式
        if bbox_groups is not None:
            if isinstance(bbox_groups, dict):
                params["bboxGroups"] = json.dumps(bbox_groups, ensure_ascii=False)
            elif isinstance(bbox_groups, str):
                params["bboxGroups"] = bbox_groups
            else:
                raise ValueError("bbox_groups必须是dict或str")

        # 去重相关参数
        if need_trim is not None:
            params["needTrim"] = need_trim

        if need_mask is not None:
            params["needMask"] = need_mask

        if need_mirror is not None:
            params["needMirror"] = need_mirror

        if need_rescale is not None:
            params["needRescale"] = need_rescale

        if need_shift is not None:
            params["needShift"] = need_shift

        if random_border is not None:
            params["randomBorder"] = random_border

        if need_transition is not None:
            params["needTransition"] = need_transition

        # 智能配乐相关
        if need_rhythm is not None:
            params["needRhythm"] = need_rhythm

        if music_region is not None:
            params["musicRegion"] = music_region

        if rhythm_param is not None:
            if isinstance(rhythm_param, dict):
                params["rhythmParam"] = json.dumps(rhythm_param, ensure_ascii=False)
            elif isinstance(rhythm_param, str):
                params["rhythmParam"] = rhythm_param
            else:
                raise ValueError("rhythm_param必须是dict或str")

        # 短剧/解说二创特殊参数覆盖wyTaskType和extraOptions
        if wy_task_type_extra is not None:
            params["wyTaskType"] = wy_task_type_extra

        # 兼容之前传的extra_options_dict，如果存在覆盖
        if extra_options_dict:
            params["extraOptions"] = json.dumps(extra_options_dict, ensure_ascii=False)

        body = self.client.post(path, params)
        if not isinstance(body, (int, float)):
            raise ZhaoliAPIException(-1, "创建视频处理任务返回异常，期待任务ID")
        return int(body)

    def query_task(self, task_id: int) -> dict:
        """
        查询视频处理任务状态及结果

        :param task_id: 任务ID
        :return: 响应body字典，包含状态和结果详情
        :raises: ZhaoliAPIException
        """
        path = "/ve/work/query"
        params = {"id": task_id}
        body = self.client.post(path, params)
        return body
