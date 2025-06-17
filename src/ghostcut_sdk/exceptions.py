class GhostcutApiException(Exception):
    def __init__(self, code: int, msg: str):
        super().__init__(f"API error code: {code}，msg：{msg}")
        self.code = code
        self.msg = msg
