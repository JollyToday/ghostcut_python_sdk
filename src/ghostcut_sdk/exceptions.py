class GhostcutApiException(Exception):
    def __init__(self, code: int, msg: str):
        super().__init__(f"API错误码[{code}]，消息：{msg}")
        self.code = code
        self.msg = msg
