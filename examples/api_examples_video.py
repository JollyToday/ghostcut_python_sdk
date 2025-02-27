# -*- coding: utf-8 -*-
import os

from ghostcut.ghostcut_client import GhostCutClient

from ghostcut.models.video.ghostcut_video_task_create_request import (
    GhostCutVideoTaskCreateRequest,
)
from ghostcut.models.video.ghostcut_video_task_create_request_extra_option import (
    GhostCutVideoTaskCreateRequestExtraOption,
)

# 4. AI视频相关API 调用示例
# https://jollytoday.feishu.cn/docx/U73qdBhWbozFdpx4eTvcIO4gn7e#share-HwKldyKEUoRGMnxgGTycUamRn0c

if __name__ == "__main__":
    # 推荐将AppKey和AppSecret配置到环境变量提高安全性
    # 创建client
    client = GhostCutClient(
        os.environ["GHOSTCUT_APPKEY"], os.environ["GHOSTCUT_APPSECRET"]
    )

    # 4.1.1.7 视频去重
    # https://jollytoday.feishu.cn/docx/U73qdBhWbozFdpx4eTvcIO4gn7e#share-E5JLdmSnmo5tQ5x7jxOcEQ7MnXe
    request = GhostCutVideoTaskCreateRequest()
    extraOptions = GhostCutVideoTaskCreateRequestExtraOption()
    extraOptions.from_map(
        {
            "extra_trim_config": {
                # 修改md5，True开启，false关闭
                "modify_md5": True,
                # 智能抽帧，True开启，false关闭
                "extract_frame_on": True,
                # 智能调色，True开启，false关闭
                "adjust_color_on": True,
                # 画面锐化，True开启，false关闭
                "adjust_sharpness_on": True,
                # 掐头去尾，True开启，false关闭
                "crop_trailer_on": True,
                # 随机加速，True开启，false关闭
                "speedup_on": True,
            }
        }
    )
    request.from_map(
        {
            "callback": "https://xxx.com/tool/api/ghost-cut/call-back",
            "needTrim": 1,
            "resolution": "1080p",
            "urls": ["https://v.douyin.com/Sqv7vgw/"],
            "extraOptions": extraOptions,
        }
    )
    print(client.video_task_create(request))
    """
    响应内容示例：
    {"msg":"success","trace":"a6b7c8618f0c46b1bd4923c4a7ced265","code":1000,"body":{"idProject":220928008,"dataList":[{"url":"https://v.douyin.com/Sqv7vgw/","id":476997163}]}} 
    """
