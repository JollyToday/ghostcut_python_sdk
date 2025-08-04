# -*- coding: utf-8 -*-

"""
5.3 使用精修编辑器对图片结果再编辑（免费）
# 接口文档：https://jollytoday.feishu.cn/docx/U73qdBhWbozFdpx4eTvcIO4gn7e#share-QR57dTEyCozvZyxGLhYcGHyhnBf


功能简述：
本功能可以呼起在线编辑器，对鬼手剪辑处理过的图片进行在线编辑，功能类似于官网<我的作品-图片翻译-操作-精修>，主要用于图片翻译的调整，也可以用于图片擦除后，在擦除后的图片上进行二次编辑。
本功能免费。

本功能使用前提是之前已经成功完成图片翻译的任务，呼起编辑器一共需要两步：
1. 第一步，生成指定图片任务id的授权码；
2. 第二步，拼接精修编辑器授权url，并通过浏览器访问。

接口地址：
https://api.zhaoli.com/v-w-c/gateway/ve/image/translate/auth/apply

请求方式：
POST

请求参数：
- id (Long，必填)：图片翻译任务id，即：【创建任务接口】中返回的任务ID
- expireSeconds (Long，必填)：授权码过期时间，单位秒。范围：0~604800，如果小于该范围使用3600秒，超过该范围使用604800秒。

响应参数：
- body (String)：用于呼起编辑器网页的授权码。如果为null，代表授权失败。
"""

from ghostcut_python_sdk.ghostcut.models.ghostcut_model import GhostCutModel


class GhostCutImageEditAuthApplyRequest(GhostCutModel):
    def __init__(
        self,
        id: int = None,
        expireSeconds: int = None,
    ):
        """
        使用精修编辑器对图片结果再编辑请求参数模型

        :param id: (必填) 图片翻译任务id，即创建任务接口返回的任务ID
        :param expireSeconds: (必填) 授权码过期时间，单位秒，范围0~604800，小于范围默认3600，大于范围默认604800
        """
        self.id = id
        self.expireSeconds = expireSeconds

    def validate(self):
        """
        校验请求参数合法性，若参数不符合规则，抛出 ValueError 异常
        """
        if self.id is None:
            raise ValueError("id 为必填项")
        if not isinstance(self.id, int):
            raise ValueError("id 必须是整数类型")

        if self.expireSeconds is None:
            raise ValueError("expireSeconds 为必填项")
        if not isinstance(self.expireSeconds, int):
            raise ValueError("expireSeconds 必须是整数类型")

        if self.expireSeconds < 0:
            raise ValueError("expireSeconds 不能小于0")
        # 这里对范围进行限制，如果不在范围内，前端可以自行处理，接口会按说明默认处理
        # 这里提醒即可，不抛异常
        if self.expireSeconds > 604800:
            # 建议打印警告日志或提示
            pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        return {
            "id": self.id,
            "expireSeconds": self.expireSeconds,
        }

    def from_map(self, m: dict = None):
        m = m or dict()
        self.id = m.get("id")
        self.expireSeconds = m.get("expireSeconds")
        return self
