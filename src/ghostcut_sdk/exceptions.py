from typing import Optional


# TODO API那边的报错好像还有trace_id，需要记录
class GhostcutApiException(Exception):
    def __init__(self, code: int, msg: str, trace_id: Optional[str] = None):
        super().__init__(f"API error code: {code}，msg：{msg}, trace_id: {trace_id}")
        self.code = code
        self.msg = msg
        self.trace_id = trace_id
