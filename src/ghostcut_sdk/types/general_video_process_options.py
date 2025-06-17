from typing import List, Optional, Union, Dict, Any
from pydantic import BaseModel, Field
from ghostcut_sdk.types.literals import Resolution


class GeneralVideoProcessOptions(BaseModel):
    urls: List[str] = Field(description="视频URL列表")
    names: Optional[List[str]] = Field(default=None, description="视频名称列表")
    resolution: Resolution = Field(default="720p", description="视频分辨率")
    callback: Optional[str] = Field(default=None, description="回调URL")
    uid: Optional[str] = Field(default=None, description="用户ID")
    extra_options: Optional[Union[str, Dict[str, Any]]] = Field(default=None, description="额外选项")
    # 视频去文字相关
    need_chinese_occlude: Optional[int] = None
    video_inpaint_lang: Optional[str] = None
    video_inpaint_masks: Optional[Union[str, List[Dict[str, Any]]]] = None
    need_crop: Optional[int] = None
    need_crop_color: Optional[str] = None
    # 语音翻译相关
    source_lang: Optional[str] = None
    lang: Optional[str] = None
    need_wanyin: Optional[int] = None
    wy_task_type: Optional[str] = None
    wy_need_text: Optional[int] = None
    wy_voice_param: Optional[Union[str, Dict[str, Any]]] = None
    remove_bg_audio: Optional[int] = None
    # 文字翻译相关
    bbox_groups: Optional[Union[str, Dict[str, Any]]] = None
    # 去重相关
    need_trim: Optional[int] = None
    need_mask: Optional[int] = None
    need_mirror: Optional[int] = None
    need_rescale: Optional[int] = None
    need_shift: Optional[int] = None
    random_border: Optional[int] = None
    need_transition: Optional[int] = None
    # 智能配乐相关
    need_rhythm: Optional[int] = None
    music_region: Optional[str] = None
    rhythm_param: Optional[Union[str, Dict[str, Any]]] = None
    # 短剧二创和解说二创相关
    wy_task_type_extra: Optional[str] = None
    extra_options_dict: Optional[Dict[str, Any]] = None
