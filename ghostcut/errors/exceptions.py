class SDKError(Exception):
    """SDK基础错误类型"""

    def __init__(self, message=None):
        default_message = "SDK参数使用错误"
        super().__init__(message or default_message)
        self.message = message or default_message

    def __str__(self):
        return f"SDKError: {self.message}"


class UploadError(SDKError):
    """上传错误"""

    def __init__(self, message=None):
        default_message = "上传文件异常"
        super().__init__(message or default_message)

    def __str__(self):
        return f"UploadError: {self.message}"


class PolicyError(SDKError):
    """凭证信息异常"""

    def __init__(self, message=None):
        default_message = "凭证信息异常"
        super().__init__(message or default_message)

    def __str__(self):
        return f"PolicyError: {self.message}"
