from typing import Optional, Union, Dict, Any
from ghostcut_sdk.api_base import BaseGhostcutApi, GhostcutApiException
from ghostcut_sdk.ghostcut_type.image import (
    ImageTranslateRequest,
    ApplyAuthCodeRequest,
    ImageTranslateResponse,
    ImageTranslateResult,
)
from ghostcut_sdk.config.url import (
    DEFAULT_BASE_URL,
    EDITOR_BASE_URL,
    IMAGE_TRANSLATE_PATH,
    IMAGE_QUERY_TASK_PATH,
    IMAGE_APPLY_QUTH_CODE_PATH,
    IMAGE_REDO_TASK_PATH,
)


"""
5. AI图片相关API 调用示例
https://jollytoday.feishu.cn/docx/U73qdBhWbozFdpx4eTvcIO4gn7e#share-WtRQdwT2xoVyUOxiN98ck8k1nVf
"""


class ImageApi(BaseGhostcutApi):
    def __init__(
        self,
        app_key: Optional[str] = None,
        app_secret: Optional[str] = None,
    ):
        super().__init__(app_key, app_secret)

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
        body = self.post(
            IMAGE_TRANSLATE_PATH,
            request.model_dump(by_alias=True, exclude_none=True),
        )
        # 返回body为任务ID
        if not isinstance(body, (int, float)):
            raise GhostcutApiException(-1, "创建任务接口返回异常，期待任务ID")
        return int(body)

    def query_task(self, task_id: int) -> ImageTranslateResponse:
        """
        query image translate task status and result

        Args:
            task_id (int): task id

        Raises:
            GhostcutApiException: if query task failed

        Returns:
            dict: task status and result
        """
        return ImageTranslateResponse(
            **self.post(IMAGE_QUERY_TASK_PATH, {"id": task_id})
        )

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
        body = self.post(
            IMAGE_APPLY_QUTH_CODE_PATH,
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

    def redo_task(self, task_id: int, modified_result: ImageTranslateResult) -> int:
        """
        modify image translate task result and resynthesize

        Args:
            task_id (int): task id
            modified_result (ImageTranslateResult): modified result

        Raises:
            ValueError: if modified_result is not a valid json string or dict
            GhostcutApiException: if redo task failed

        Returns:
            int: whether redo task is normal, 1 means normal, other means failed
        """

        params = {"id": task_id, "result": modified_result.to_json()}
        body = self.post(IMAGE_REDO_TASK_PATH, params)
        if not isinstance(body, (int, float)):
            raise GhostcutApiException(-1, "重新合成接口返回异常")
        return int(body)
