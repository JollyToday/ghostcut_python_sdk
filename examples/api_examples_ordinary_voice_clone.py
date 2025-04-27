import json
from typing import List, Optional, Dict, Any
from  ghostcut_python_sdk.ghostcut.client import ZhaoliClient


class OrdinaryVoiceCloneAPI:
    """
    普通克隆接口封装
    """

    def __init__(self, client: ZhaoliClient):
        self.client = client

    def extract_voice_info(
        self,
        prefix: str,
        urls: List[Dict[str, str]],
        callback: Optional[str] = None,
    ) -> int:
        """
        人声抽取接口

        :param prefix: 剧的唯一标识
        :param urls: 列表，每项是字典包含annote_url和audio_url
        :param callback: 回调url
        :return: 任务id（long）
        """
        clone_kwargs = {
            "prefix": prefix,
            "urls": urls,
        }
        params = {
            "cloneKwargs": {"clone_kwargs": clone_kwargs}
        }
        if callback:
            params["callback"] = callback

        path = "/ve/voice/extract_info"
        body = self.client.post(path, params)
        return int(body)

    def create_clone_voice_task(
        self,
        prefix: str,
        voice_infos: List[Dict[str, Any]],
        callback: Optional[str] = None,
    ) -> int:
        """
        创建训练音色任务接口（建议单个声音调用）

        :param prefix: 剧的唯一标识
        :param voice_infos: 角色声音列表，每个元素包含 character, audio_url, recommend_clone(可选)
        :param callback: 回调url
        :return: 任务id（long）
        """
        clone_kwargs = {
            "prefix": prefix,
            "voice_infos": voice_infos,
        }
        params = {
            "cloneKwargs": {"clone_kwargs": clone_kwargs}
        }
        if callback:
            params["callback"] = callback

        path = "/ve/voice/create_clone_voice"
        body = self.client.post(path, params)
        return int(body)

    def query_clone_voice_list(
        self,
        page_number: int,
        page_size: Optional[int] = None,
        id: Optional[int] = None,
        id_ve_video_parse_task: Optional[int] = None,
        prefix: Optional[str] = None,
        deleted: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        查询训练的音色列表

        :param page_number: 页码，从1开始
        :param page_size: 每页条数，默认20
        :param id: 声音id
        :param id_ve_video_parse_task: 生成接口产生的任务id
        :param prefix: 剧唯一标识
        :param deleted: 是否删除，1是0否
        :return: 返回body内容
        """
        params: Dict[str, Any] = {"pageNumber": page_number}
        if page_size is not None:
            params["pageSize"] = page_size
        if id is not None:
            params["id"] = id
        if id_ve_video_parse_task is not None:
            params["idVeVideoParseTask"] = id_ve_video_parse_task
        if prefix is not None:
            params["prefix"] = prefix
        if deleted is not None:
            params["deleted"] = deleted

        path = "/ve/voice/query_clone_voice"
        body = self.client.post(path, params)
        return body

    def query_public_voice_list(
        self,
        page_number: int,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        查询公共的音色列表

        :param page_number: 页码，从1开始
        :param page_size: 每页条数，默认20
        :return: 返回body内容
        """
        params = {"pageNumber": page_number}
        if page_size is not None:
            params["pageSize"] = page_size

        path = "/ve/voice/query_public_voice"
        body = self.client.post(path, params)
        return body

    def delete_clone_voice(
        self,
        prefix: Optional[str] = None,
        id: Optional[int] = None,
    ) -> int:
        """
        删除训练的音色

        :param prefix: 剧的唯一标识，优先使用
        :param id: 声音id
        :return: 成功删除的记录条数
        """
        if not prefix and not id:
            raise ValueError("prefix和id二选一必须传一个")
        params = {}
        if prefix:
            params["prefix"] = prefix
        else:
            params["id"] = id

        path = "/ve/voice/delete_clone_voice"
        body = self.client.post(path, params)
        return int(body)

    def submit_video_clone_task(
        self,
        urls: List[str],
        lang: str,
        source_lang: str,
        extra_options: Dict[str, Any],
        names: Optional[List[str]] = None,
        wy_voice_param: Optional[Dict[str, Any]] = None,
        callback: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        提交视频克隆任务（普通）

        :param urls: 视频URL列表，目前支持单个视频
        :param lang: 目标语言
        :param source_lang: 源语言
        :param extra_options: extraOptions字段，必须包含customer_input.url或content和prefix
        :param names: 作品名称列表（可选）
        :param wy_voice_param: 可选语音相关配置
        :param callback: 回调地址
        :return: 作品信息字典
        """
        if not urls or len(urls) != 1:
            raise ValueError("urls 必须是长度为1的列表，目前仅支持单视频")

        params = {
            "urls": urls,
            "lang": lang,
            "sourceLang": source_lang,
            "extraOptions": extra_options,
        }
        if names:
            if len(names) == len(urls):
                params["names"] = names
            else:
                params["names"] = [""] * len(urls)

        if wy_voice_param:
            params["wyVoiceParam"] = wy_voice_param

        if callback:
            params["callback"] = callback

        path = "/ve/work/voice/incorporate"
        body = self.client.post(path, params)
        return body

    def query_video_task_status(self, work_ids: List[int]) -> Dict[str, Any]:
        """
        查询视频处理任务状态

        :param work_ids: 作品id列表
        :return: 任务状态信息
        """
        path = "/ve/work/status"
        params = {"idWorks": work_ids}
        body = self.client.post(path, params)
        return body
