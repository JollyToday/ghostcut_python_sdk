# -*- coding: utf-8 -*-

# 6. 声音克隆相关API 调用示例
# https://jollytoday.feishu.cn/docx/U73qdBhWbozFdpx4eTvcIO4gn7e#share-MEiqdbIeGoWUE8xDq4jclw38nDf
import json
from typing import List, Optional, Dict, Any
from  ghostcut_python_sdk.ghostcut.client import ZhaoliClient,ZhaoliAPIException


class VoiceCloneAPI:
    def __init__(self, client: ZhaoliClient):
        self.client = client

    def create_incorporate_task(
        self,
        urls: List[str],
        incorporate_pro: bool,
        lang: str,
        source_lang: str,
        names: Optional[List[str]] = None,
        extra_options: Optional[Dict[str, Any]] = None,
        callback: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        提交视频高情感克隆任务

        :param urls: 视频URL列表，当前仅支持1个视频
        :param incorporate_pro: 是否开启情感加强，True开启
        :param lang: 目标语言代码，如 "en"
        :param source_lang: 源语言代码，如 "zh"
        :param names: 视频作品名称列表（可选）
        :param extra_options: 额外配置，必须包含customer_input字段
        :param callback: 回调地址（可选）
        :return: 作品信息字典
        :raises: ZhaoliAPIException
        """
        if not urls or len(urls) != 1:
            raise ValueError("urls 必须是长度为1的列表，仅支持单视频")

        params: Dict[str, Any] = {
            "urls": urls,
            "incorporatePro": incorporate_pro,
            "lang": lang,
            "sourceLang": source_lang,
        }
        if names:
            if len(names) == len(urls):
                params["names"] = names
            else:
                params["names"] = [""] * len(urls)

        if extra_options:
            params["extraOptions"] = extra_options

        if callback:
            params["callback"] = callback

        path = "/ve/work/voice/incorporate"
        body = self.client.post(path, params)
        return body

    def query_task_status(self, work_ids: List[int]) -> Dict[str, Any]:
        """
        查询视频处理任务状态

        :param work_ids: 作品ID列表
        :return: 查询结果字典
        """
        path = "/ve/work/status"
        params = {"idWorks": work_ids}
        body = self.client.post(path, params)
        return body

    def redo_sentence_dubbing(
        self,
        id_ve_work: int,
        sent_ids: List[str],
        ref_type: str,
        ref_sent_id: Optional[str] = None,
        ref_voice_id: Optional[int] = None,
        callback: Optional[str] = None,
    ) -> int:
        """
        发起句子重新配音任务

        :param id_ve_work: 高情感克隆作品ID
        :param sent_ids: 需要重新配音的句子sent_id列表
        :param ref_type: 重新克隆类型 OWN/PUB_TTS/PUB_CLONE/OWN_CLONE
        :param ref_sent_id: refType=OWN时必填
        :param ref_voice_id: refType为其他时必填
        :param callback: 回调地址
        :return: 重新配音任务ID
        """
        params = {
            "idVeWork": id_ve_work,
            "sentIds": sent_ids,
            "refType": ref_type,
        }
        if ref_type == "OWN":
            if not ref_sent_id:
                raise ValueError("refSentId必填，当refType为OWN时")
            params["refSentId"] = ref_sent_id
        elif ref_type in ("PUB_TTS", "PUB_CLONE", "OWN_CLONE"):
            if ref_voice_id is None:
                raise ValueError("refVoiceId必填，当refType为PUB_TTS/PUB_CLONE/OWN_CLONE时")
            params["refVoiceId"] = ref_voice_id
        else:
            raise ValueError("无效的refType值")

        if callback:
            params["callback"] = callback

        path = "/ve/work/voice/clone"
        body = self.client.post(path, params)
        if not isinstance(body, (int, float)):
            raise ZhaoliAPIException(-1, "重新配音任务接口返回异常，期待任务ID数字")
        return int(body)

    def query_redubbing_task(self, task_id: int) -> Dict[str, Any]:
        """
        查询重新配音任务结果

        :param task_id: 重新配音任务ID
        :return: 任务状态和结果信息字典
        """
        path = "/ve/work/voice/clone/task/query"
        params = {"id": task_id}
        body = self.client.post(path, params)
        return body

    def synthesize_redubbing(self, id_ve_work: int, tts_meta_result: Any) -> bool:
        """
        使用新的配音信息重新合成视频

        :param id_ve_work: 作品ID
        :param tts_meta_result: 修改后的ttsMetaResult JSON字符串或对象
        :return: True成功发起，False失败
        """
        if isinstance(tts_meta_result, (dict, list)):
            tts_meta_str = json.dumps(tts_meta_result, ensure_ascii=False)
        elif isinstance(tts_meta_result, str):
            # 简单校验是否JSON字符串
            try:
                json.loads(tts_meta_result)
                tts_meta_str = tts_meta_result
            except Exception:
                raise ValueError("tts_meta_result不是有效JSON字符串")
        else:
            raise ValueError("tts_meta_result参数必须是JSON字符串或dict/list对象")

        params = {
            "id": id_ve_work,
            "ttsMetaResult": tts_meta_str,
        }
        path = "/ve/work/voice/clone/synthesize"
        body = self.client.post(path, params)
        if not isinstance(body, bool):
            raise ZhaoliAPIException(-1, "重新合成接口返回异常，期待bool值")
        return body

    def apply_auth_code(
        self, id_ve_work: int, expire_seconds: int = 3600, allow_clone: bool = False
    ) -> Optional[str]:
        """
        申请编辑授权码（用于在线精修编辑器）

        :param id_ve_work: 作品ID
        :param expire_seconds: 过期时间，单位秒，范围0~604800
        :param allow_clone: 是否开放私有克隆声音
        :return: 授权码字符串，失败返回None
        """
        if expire_seconds < 0 or expire_seconds > 604800:
            expire_seconds = 3600

        params = {
            "id": id_ve_work,
            "expireSeconds": expire_seconds,
            "allowClone": allow_clone,
        }
        path = "/ve/work/auth/apply"
        body = self.client.post(path, params)
        if body is None:
            return None
        return str(body)

    @staticmethod
    def get_editor_url(auth_code: str, domain: str = "jollytoday.com") -> str:
        """
        拼接编辑器访问URL

        :param auth_code: 授权码
        :param domain: 网站域名，默认英文站
        :return: 编辑器URL
        """
        return f"https://{domain}/auth/editor?token={auth_code}"
