import time
import hashlib
import requests
import json


class ZhaoliAPIException(Exception):
    """API调用异常封装"""

    def __init__(self, code: int, msg: str):
        super().__init__(f"API错误码[{code}]，消息：{msg}")
        self.code = code
        self.msg = msg


class ZhaoliClient:
    """
    API基础客户端，负责请求签名和发送请求
    """

    def __init__(self, app_id: str, app_secret: str, base_url: str = "https://api.zhaoli.com/v-w-c/gateway"):
        self.app_id = app_id
        self.app_secret = app_secret
        self.base_url = base_url.rstrip("/")

    def _sign(self, params: dict) -> str:
        """
        生成签名，规则：
        - 排序参数(按key字母序)
        - 拼接key=value&key2=value2...
        - 拼接后添加appSecret
        - MD5加密（小写）
        """
        sorted_items = sorted(params.items())
        sign_str = "&".join(f"{k}={v}" for k, v in sorted_items)
        sign_str += self.app_secret
        md5 = hashlib.md5()
        md5.update(sign_str.encode("utf-8"))
        return md5.hexdigest()

    def post(self, path: str, params: dict) -> dict:
        """
        发送POST请求，自动添加公共参数和签名
        """
        url = self.base_url + path

        # 添加公共参数
        params = params.copy()
        params.setdefault("appId", self.app_id)
        params.setdefault("timestamp", int(time.time() * 1000))

        # 生成签名
        sign = self._sign(params)
        params["sign"] = sign

        headers = {"Content-Type": "application/json"}

        try:
            resp = requests.post(url, json=params, headers=headers, timeout=30)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            raise ZhaoliAPIException(-1, f"请求异常: {e}")

        code = data.get("code")
        if code != 1000:
            raise ZhaoliAPIException(code, data.get("msg", "未知错误"))

        return data.get("body")

