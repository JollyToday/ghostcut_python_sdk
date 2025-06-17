import os
import time
import hashlib
import requests
from typing import Optional, Dict, Any
from ghostcut_sdk.config.path import DEFAULT_BASE_URL
from ghostcut_sdk.exceptions import GhostcutApiException


class BaseGhostcutApi:
    """
    API基础客户端，负责请求签名和发送请求
    """

    def __init__(
        self,
        app_id: Optional[str] = None,
        app_secret: Optional[str] = None,
        base_url: str = DEFAULT_BASE_URL,
    ):
        self.app_id = app_id if app_id else os.environ.get("GHOSTCUT_APP_ID")
        self.app_secret = (
            app_secret if app_secret else os.environ.get("GHOSTCUT_APP_SECRET")
        )
        if self.app_id is None or self.app_secret is None:
            raise ValueError("app id or secret is not supplied")
        self.base_url = base_url.rstrip("/")

    def post(
        self,
        path: str,
        params: Optional[Dict] = None,
        files: Optional[Dict] = None,
        use_auth: bool = True,
        timeout: float = 30,
    ) -> Dict:
        """
        发送POST请求，自动添加公共参数和签名
        """
        url = self.base_url + path

        # 添加公共参数
        if use_auth:
            params = params.copy() if params else dict()
            params["appId"] = self.app_id
            params["timestamp"] = int(time.time() * 1000)
            # 生成签名
            sign = self._sign(params)
            params["sign"] = sign
        elif params:
            params = params.copy()
        headers = {"Content-Type": "application/json"}

        try:
            resp = requests.post(
                url,
                json=params,
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

    def _sign(self, params: Dict[str, Any]) -> str:
        """
        Generate signature, rules:
        - Sort parameters (by key in alphabetical order)
        - Concatenate as key=value&key2=value2...
        - Append appSecret after concatenation
        - MD5 encryption (lowercase)
        """
        sorted_items = sorted(params.items())
        sign_str = "&".join(f"{k}={v}" for k, v in sorted_items)
        sign_str += self.app_secret
        md5 = hashlib.md5()
        md5.update(sign_str.encode("utf-8"))
        return md5.hexdigest()
