import requests
import json
from ghostcut_python_sdk.examples.utils import generate_nonce, calculate_md5
from ghostcut_python_sdk.examples.exceptions import UploadError, PolicyError

class FileUploader:
    def __init__(self, app_key: str, app_secret: str):
        self.app_key = app_key
        self.app_secret = app_secret
        self.upload_policy_url = "https://api.zhaoli.com/v-w-c/gateway/ve/file/upload/policy/apply"

    def get_upload_policy(self) -> dict:
        """获取上传凭证"""
        nonce = generate_nonce()

        data = {
            "nonce": nonce,
            "materialFileType": "image",  # 可选，默认为 "image"
            "expireSeconds": 3600  # 可选，默认为 3600
        }

        data_json = json.dumps(data)
        body_md5hex = calculate_md5(data_json)

        # 拼接 AppSecret 进行第二次 MD5 计算
        sign = calculate_md5(body_md5hex + self.app_secret)

        headers = {
            'Content-Type': 'application/json',
            'AppKey': self.app_key,
            'AppSign': sign,
        }

        response = requests.post(self.upload_policy_url, json=data, headers=headers)

        if response.status_code == 200:
            return response.json().get("body", {})
        else:
            raise PolicyError(f"获取上传凭证失败，状态码: {response.status_code}, 响应内容: {response.text}")

    def upload_file(self, file_path: str, filename: str) -> str:
        """上传文件"""
        body = self.get_upload_policy()

        # 准备文件上传参数
        files = {
            "key": f"{body['dir']}{filename}",
            "OSSAccessKeyId": body["accessid"],
            "policy": body["policy"],
            "signature": body["signature"],
            "callback": body["base64CallbackBody"],
            "success_action_status": 200,
            "file": open(file_path, "rb"),
        }

        upload_response = requests.post(body["host"], files=files)

        if upload_response.status_code == 200:
            upload_result = upload_response.json()
            if upload_result.get("Status") == "OK":
                complete_url = body["urlPrefix"] + filename
                return complete_url
            else:
                raise UploadError(f"文件上传失败: {upload_result}")
        else:
            raise UploadError(f"文件上传请求失败，状态码: {upload_response.status_code}, 响应内容: {upload_response.text}")
