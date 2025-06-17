import json
from typing import Optional, Union, Dict, Any
from ghostcut_sdk.client import BaseGhostcutApi, GhostcutApiException
from ghostcut_sdk.ghostcut_type.image import (
    ImageTranslateRequest,
    ApplyAuthCodeRequest,
)
from ghostcut_sdk.config.path import (
    EDITOR_BASE_URL,
    VE_IMAGE_TRANSLATE_PATH,
    VE_IMAGE_TRANSLATE_QUERY_PATH,
    VE_IMAGE_TRANSLATE_AUTH_APPLY_PATH,
    VE_IMAGE_TRANSLATE_REDO_PATH,
)


"""
5. AI图片相关API 调用示例
https://jollytoday.feishu.cn/docx/U73qdBhWbozFdpx4eTvcIO4gn7e#share-WtRQdwT2xoVyUOxiN98ck8k1nVf
"""


class ImageAPI:
    """
    AI图片相关API封装：
    - 创建图片处理任务（擦除/翻译）
    - 查询任务结果
    - 申请编辑授权码
    - 获取编辑器URL
    - 重新提交翻译结果进行合成
    """

    def __init__(self, client: BaseGhostcutApi):
        self.client = client

    def translate(
        self,
        request: Union[ImageTranslateRequest, Dict[str, Any]],
    ) -> int:
        """
        create image translate task, will return task id.
        You can use task id to query task status and result.

        Args:
            request (Union[ImageTranslateRequest, Dict[str, Any]]): image translate request

        Raises:
            GhostcutApiException: if create task failed

        Returns:
            int: task id
        """
        if isinstance(request, Dict):
            request = ImageTranslateRequest(**request)
        body = self.client.post(
            VE_IMAGE_TRANSLATE_PATH,
            request.model_dump(by_alias=True, exclude_none=True),
        )
        # 返回body为任务ID
        if not isinstance(body, (int, float)):
            raise GhostcutApiException(-1, "创建任务接口返回异常，期待任务ID")
        return int(body)

    def query_task(self, task_id: int) -> Dict:
        """
        query image translate task status and result

        Args:
            task_id (int): task id

        Raises:
            GhostcutApiException: if query task failed

        Returns:
            dict: task status and result
        """
        body = self.client.post(VE_IMAGE_TRANSLATE_QUERY_PATH, {"id": task_id})
        # TODO 返回的数据比较复杂，创建一个类来处理
        return body

    def apply_auth_code(
        self, request: Union[ApplyAuthCodeRequest, Dict[str, Any]]
    ) -> Optional[str]:
        """
        apply image translate task auth code, for online editor access

        Args:
            request (Union[ApplyAuthCodeRequest, Dict[str, Any]]): apply auth code request

        Raises:
            GhostcutApiException: if apply auth code failed

        Returns:
            Optional[str]: auth code string, None if failed
        """
        if isinstance(request, Dict):
            request = ApplyAuthCodeRequest(**request)
        body = self.client.post(
            VE_IMAGE_TRANSLATE_AUTH_APPLY_PATH,
            request.model_dump(by_alias=True, exclude_none=True),
        )
        # body是授权码字符串或null
        return str(body) if body else None

    def get_editor_url(
        self, auth_code: str, lang: str = "zh", show_logo: bool = True
    ) -> str:
        """
        generate editor url with auth code

        Args:
            auth_code (str): auth code
            lang (str, optional): editor language, e.g. "zh" or "en". Defaults to "zh".
            show_logo (bool, optional): whether to show GhostCut logo, False will add &PURE. Defaults to True.

        Returns:
            str: editor url
        """
        extra = "" if show_logo else "&PURE"
        return f"{EDITOR_BASE_URL}?l={lang}&c={auth_code}{extra}"

    def redo_task(self, task_id: int, result_json: Union[str, dict]) -> int:
        """
        修改翻译结果重新合成（异步）

        :param task_id: 任务ID
        :param result_json: 修改后的result字段，json字符串或dict形式
        :return: 1表示任务已正常发起
        :raises: GhostcutApiException
        """
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

        params = {"id": task_id, "result": result_str}
        body = self.client.post(VE_IMAGE_TRANSLATE_REDO_PATH, params)
        if not isinstance(body, (int, float)):
            raise GhostcutApiException(-1, "重新合成接口返回异常")
        return int(body)
