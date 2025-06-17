import os
import time
import json
import hashlib
import requests
import logging
from typing import Optional, Dict, Any, Union, List
from ghostcut_sdk.config.path import DEFAULT_BASE_URL
from ghostcut_sdk.exceptions import GhostcutApiException

ZL_LOGGER = logging.getLogger(__name__)


class BaseGhostcutApi:
    """
    API基础客户端，负责请求签名和发送请求
    """

    def __init__(
        self,
        app_key: Optional[str] = None,
        app_secret: Optional[str] = None,
        base_url: str = DEFAULT_BASE_URL,
    ):
        self.app_key = app_key if app_key else os.environ.get("GHOSTCUT_APP_KEY")
        self.app_secret = (
            app_secret if app_secret else os.environ.get("GHOSTCUT_APP_SECRET")
        )
        if self.app_key is None or self.app_secret is None:
            raise ValueError("app id or secret is not supplied")
        self.base_url = base_url.rstrip("/")

    def _calc_sign(self, body: str) -> str:
        md5_1 = hashlib.md5()
        md5_1.update(body.encode("utf-8"))
        body_md5hex = md5_1.hexdigest()
        md5_2 = hashlib.md5()
        body_md5hex = (body_md5hex + self.app_secret).encode("utf-8")
        md5_2.update(body_md5hex)
        return md5_2.hexdigest()

    def post(
        self,
        path: str,
        params: Optional[Dict] = None,
        files: Optional[Dict] = None,
        timeout: float = 30,
    ) -> Union[Dict[str, Any], List, str, int]:
        """
        发送POST请求，自动添加公共参数和签名
        """
        body = json.dumps(params)
        url = self.base_url + path
        sign = self._calc_sign(body)

        headers = {
            "Content-Type": "application/json",
            "AppKey": self.app_key,
            "AppSign": self._calc_sign(body),
        }

        ZL_LOGGER.debug(f"Sending POST request to {url}")
        ZL_LOGGER.debug(f"Headers: {headers}")
        ZL_LOGGER.debug(f"Body: {body}")
        ZL_LOGGER.debug(f"Sign: {sign}")

        try:
            resp = requests.post(
                self.base_url + path,
                data=body,
                headers=headers,
                files=files,
                timeout=timeout,
            )
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            raise GhostcutApiException(-1, f"请求异常: {e}")

        code = data.get("code")
        if code != 1000:
            raise GhostcutApiException(code, data.get("msg", "未知错误"))
        return data.get("body")
