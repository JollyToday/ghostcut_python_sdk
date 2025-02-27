class SDKError(Exception):
    """SDK基础错误类型"""
    print("SDK参数使用错误")
    pass

class UploadError(SDKError):
    """上传错误"""
    print("上传文件异常")
    pass
class PolicyError(SDKError):
    """凭证信息异常"""
    print("凭证信息异常")
    pass