from ghostcut_python_sdk.ghostcut.models.video.ghostcut_video_task_create_request import GhostCutVideoTaskCreateRequest
from ghostcut_python_sdk.ghostcut.models.video.ghostcut_video_task_create_request_extra_option import GhostCutVideoTaskCreateRequestExtraOption
from ghostcut_python_sdk.ghostcut.ghostcut_client import GhostCutClient
from ghostcut_python_sdk.ghostcut.config.const import GHOSTCUT_APPKEY, GHOSTCUT_APPSECRET

def test_video_occlude_task():
    client = GhostCutClient(app_key=GHOSTCUT_APPKEY, app_secret=GHOSTCUT_APPSECRET)

    extra_options = GhostCutVideoTaskCreateRequestExtraOption(
        needChineseOcclude=1,
        videoInpaintLang="zh",
        videoInpaintMasks=[
            {
                "type": "remove_only_ocr",
                "region": [10, 20, 300, 100],
                "range": [0, 15]
            },
            {
                "type": "keep",
                "region": [400, 50, 100, 50],
                "range": [0, 30]
            }
        ],
        needCrop=1,
        needCropColor="#000000"
    )

    request = GhostCutVideoTaskCreateRequest(
        urls=["https://example.com/sample_video.mp4"],
        names=["测试视频"],
        resolution="1080p",
        callback="https://yourcallback.url",
        extraOptions=extra_options,
        needTrim=0,
        needMask=0,
    )

    resp = client.video_task_create(request)
    print(resp)

if __name__ == "__main__":
    test_video_occlude_task()
