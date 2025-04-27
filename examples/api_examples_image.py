# -*- coding: utf-8 -*-

# 5. AI图片相关API 调用示例
# https://jollytoday.feishu.cn/docx/U73qdBhWbozFdpx4eTvcIO4gn7e#share-WtRQdwT2xoVyUOxiN98ck8k1nVf

import json
from typing import Optional, Union, Dict, Any
from  ghostcut_python_sdk.ghostcut.client import ZhaoliClient,ZhaoliAPIException


class ImageAPI:
    """
    AI图片相关API封装：
    - 创建图片处理任务（擦除/翻译）
    - 查询任务结果
    - 申请编辑授权码
    - 获取编辑器URL
    - 重新提交翻译结果进行合成
    """

    def __init__(self, client: ZhaoliClient):
        self.client = client

    def create_task(
        self,
        download_info: Union[str, Dict[str, str]],
        translate_on: int,
        src_lang: str,
        tgt_lang: Union[str, None],
        synthesis_on: int = 1,
        commodity_filter_on: int = 0,
        callback: Optional[str] = None,
        extra_options: Optional[Dict[str, Any]] = None,
    ) -> int:
        """
        创建图片处理任务（异步）

        :param download_info: 图片URL字符串或dict，如{"url":"http://..."}。注意要转成json字符串。
        :param translate_on: 是否开启翻译，0关闭，1开启
        :param src_lang: 源语言代码，如"zh"
        :param tgt_lang: 目标语言代码，如"en"，仅擦除时可传空字符串或None
        :param synthesis_on: 是否开启图片合成，默认开启1
        :param commodity_filter_on: 是否开启商品文字保护，默认关闭0
        :param callback: 回调url，可不传
        :param extra_options: 额外配置，如字体等，字典格式
        :return: 图片任务ID（long）
        :raises: ZhaoliAPIException
        """
        path = "/ve/image/translate"

        # 参数downloadInfo必须是符合JSON格式的字符串
        if isinstance(download_info, dict):
            download_info_str = json.dumps(download_info, ensure_ascii=False)
        elif isinstance(download_info, str):
            try:
                # 校验是否为json字符串
                json.loads(download_info)
                download_info_str = download_info
            except Exception:
                # 若不是json字符串，尝试封装成json字符串
                download_info_str = json.dumps({"url": download_info}, ensure_ascii=False)
        else:
            raise ValueError("download_info必须为字符串或dict")

        params = {
            "downloadInfo": download_info_str,
            "translateOn": translate_on,
            "srcLang": src_lang,
            "tgtLang": tgt_lang if tgt_lang else "",
            "synthesisOn": synthesis_on,
            "commodityFilterOn": commodity_filter_on,
        }
        if callback:
            params["callback"] = callback
        if extra_options:
            # 额外参数需字符串格式传递
            # extraOptions字段是JSON字符串
            if isinstance(extra_options, dict):
                params["extraOptions"] = json.dumps(extra_options, ensure_ascii=False)
            elif isinstance(extra_options, str):
                params["extraOptions"] = extra_options

        body = self.client.post(path, params)
        # 返回body为任务ID
        if not isinstance(body, (int, float)):
            raise ZhaoliAPIException(-1, "创建任务接口返回异常，期待任务ID")
        return int(body)

    def query_task(self, task_id: int) -> dict:
        """
        查询图片处理任务状态及结果

        :param task_id: 图片任务ID
        :return: 接口返回body字典，包含status、result等字段
        :raises: ZhaoliAPIException
        """
        path = "/ve/image/translate/query"
        params = {"id": task_id}
        body = self.client.post(path, params)
        return body

    def apply_auth_code(self, task_id: int, expire_seconds: int = 3600) -> Optional[str]:
        """
        申请图片任务授权码，用于在线编辑器授权访问

        :param task_id: 图片任务ID
        :param expire_seconds: 授权码过期秒数，范围0~604800，默认3600秒
        :return: 授权码字符串，失败返回None
        :raises: ZhaoliAPIException
        """
        path = "/ve/image/translate/auth/apply"
        # 限制过期时间范围
        expire = expire_seconds
        if expire < 0 or expire > 604800:
            expire = 3600
        params = {
            "id": task_id,
            "expireSeconds": expire,
        }
        body = self.client.post(path, params)
        # body是授权码字符串或null
        if body is None:
            return None
        return str(body)

    def get_editor_url(self, auth_code: str, lang: str = "zh", show_logo: bool = True) -> str:
        """
        根据授权码拼接精修编辑器URL

        :param auth_code: 授权码
        :param lang: 编辑器语言，如"zh"或"en"
        :param show_logo: 是否显示GhostCut logo，False时加上&PURE
        :return: 编辑器完整URL字符串
        """
        base_url = "https://editor.jollytoday.com/"
        url = f"{base_url}?l={lang}&c={auth_code}"
        if not show_logo:
            url += "&PURE"
        return url

    def redo_task(self, task_id: int, result_json: Union[str, dict]) -> int:
        """
        修改翻译结果重新合成（异步）

        :param task_id: 任务ID
        :param result_json: 修改后的result字段，json字符串或dict形式
        :return: 1表示任务已正常发起
        :raises: ZhaoliAPIException
        """
        path = "/ve/image/translate/redo"
        if isinstance(result_json, dict):
            result_str = json.dumps(result_json, ensure_ascii=False)
        elif isinstance(result_json, str):
            # 尝试解析确认是合法json字符串
            try:
                json.loads(result_json)
            except Exception as e:
                raise ValueError(f"result_json不是合法的json字符串: {e}")
            result_str = result_json
        else:
            raise ValueError("result_json参数必须是json字符串或dict")

        params = {
            "id": task_id,
            "result": result_str
        }
        body = self.client.post(path, params)
        if not isinstance(body, (int, float)):
            raise ZhaoliAPIException(-1, "重新合成接口返回异常")
        return int(body)
