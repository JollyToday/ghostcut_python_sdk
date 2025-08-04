import unittest
import json

from ghostcut_python_sdk.ghostcut.models.video.ghostcut_video_task_create_request_extra_option import \
    GhostCutVideoTaskCreateRequestExtraOption


class TestGhostCutVideoTaskCreateRequestExtraOption(unittest.TestCase):

    # 短剧二创正常用例
    def test_short_drama_valid(self):
        wyVoiceParam = json.dumps({
            "_recreate": "a",
            "font_param": {
                "style": "tpl-31-1-T",
                "font_size": 32,
                "position": 0.5
            }
        }, ensure_ascii=False)
        option = GhostCutVideoTaskCreateRequestExtraOption(
            needWanyin=1,
            wyTaskType="NO_TTS",
            wyVoiceParam=wyVoiceParam,
            needChineseOcclude=1,
            wyNeedText=1,
            sourceLang="zh",
            lang="en",
            needMask=7,
            extraOptions={
                "extra_need_mask_config": {
                    "progress_bar_on": True,
                    "sticker_on": False,
                    "frame_on": True
                }
            }
        )
        try:
            option.validate(mode="short_drama")
        except Exception as e:
            self.fail(f"Valid short_drama raised an exception: {e}")

    # 短剧二创错误用例：wyVoiceParam缺少_recreate
    def test_short_drama_invalid_wyVoiceParam_missing_recreate(self):
        wyVoiceParam = json.dumps({
            "font_param": {
                "style": "tpl-31-1-T",
                "font_size": 32,
                "position": 0.5
            }
        }, ensure_ascii=False)
        option = GhostCutVideoTaskCreateRequestExtraOption(
            needWanyin=1,
            wyTaskType="NO_TTS",
            wyVoiceParam=wyVoiceParam,
            needChineseOcclude=1,
            wyNeedText=1,
            sourceLang="zh",
            lang="en",
            needMask=7,
        )
        with self.assertRaises(ValueError) as cm:
            option.validate(mode="short_drama")
        self.assertIn("_recreate", str(cm.exception))

    # 解说二创正常用例
    def test_narration_valid(self):
        wyVoiceParam = json.dumps({"_recreate": "b"})
        option = GhostCutVideoTaskCreateRequestExtraOption(
            needWanyin=1,
            wyTaskType="REPHRASE",
            wyVoiceParam=wyVoiceParam,
            needChineseOcclude=1,
            wyNeedText=1,
            sourceLang="zh",
            lang="en",
            extraOptions={
                "extra_need_mask_config": {
                    "progress_bar_on": True,
                    "sticker_on": True,
                    "frame_on": False
                }
            }
        )
        try:
            option.validate(mode="narration")
        except Exception as e:
            self.fail(f"Valid narration raised an exception: {e}")

    # 解说二创错误用例：wyTaskType错误
    def test_narration_invalid_wyTaskType(self):
        wyVoiceParam = json.dumps({"_recreate": "b"})
        option = GhostCutVideoTaskCreateRequestExtraOption(
            needWanyin=1,
            wyTaskType="INVALID",
            wyVoiceParam=wyVoiceParam,
            needChineseOcclude=1,
            wyNeedText=1,
            sourceLang="zh",
            lang="en",
        )
        with self.assertRaises(ValueError):
            option.validate(mode="narration")

    # 字幕压制正常用例
    def test_subtitle_valid(self):
        wyVoiceParam = json.dumps({
            "font_param": {
                "style": "tpl-31-1-T",
                "font_size": 32,
                "position": 0.8
            }
        })
        option = GhostCutVideoTaskCreateRequestExtraOption(
            sourceLang="zh",
            lang="en",
            needWanyin=1,
            wyTaskType="NO_TTS",
            wyNeedText=1,
            wyVoiceParam=wyVoiceParam,
            removeBgAudio=0,
            extraOptions={
                "customer_input_srt": {
                    "source": "https://example.com/source.srt",
                    "translation": "https://example.com/translation.srt"
                }
            }
        )
        try:
            option.validate(mode="subtitle")
        except Exception as e:
            self.fail(f"Valid subtitle raised an exception: {e}")

    # 字幕压制错误用例：extraOptions缺少customer_input_srt
    def test_subtitle_invalid_extraOptions_missing_customer_input_srt(self):
        wyVoiceParam = json.dumps({
            "font_param": {
                "style": "tpl-31-1-T",
                "font_size": 32,
                "position": 0.8
            }
        })
        option = GhostCutVideoTaskCreateRequestExtraOption(
            sourceLang="zh",
            lang="en",
            needWanyin=1,
            wyTaskType="NO_TTS",
            wyNeedText=1,
            wyVoiceParam=wyVoiceParam,
            removeBgAudio=0,
            extraOptions={}  # 缺少customer_input_srt
        )
        with self.assertRaises(ValueError):
            option.validate(mode="subtitle")

    # 背景音乐去除正常用例
    def test_remove_bg_music_valid(self):
        option = GhostCutVideoTaskCreateRequestExtraOption(
            needWanyin=1,
            wyTaskType="NO_TTS",
            wyNeedText=0,
            removeBgAudio=2
        )
        try:
            option.validate(mode="remove_bg_music")
        except Exception as e:
            self.fail(f"Valid remove_bg_music raised an exception: {e}")

    # 背景音乐去除错误用例：wyNeedText错误
    def test_remove_bg_music_invalid_wyNeedText(self):
        option = GhostCutVideoTaskCreateRequestExtraOption(
            needWanyin=1,
            wyTaskType="NO_TTS",
            wyNeedText=1,
            removeBgAudio=2
        )
        with self.assertRaises(ValueError):
            option.validate(mode="remove_bg_music")

    # OCR模式正常用例
    def test_ocr_valid(self):
        option = GhostCutVideoTaskCreateRequestExtraOption(
            needChineseOcclude=14,
            videoInpaintLang="zh",
            videoInpaintMasks=[{
                "type": "trans_only_ocr",
                "region": [[0, 0], [1, 1]]
            }],
            lang="zh"
        )
        try:
            option.validate(mode="ocr")
        except Exception as e:
            self.fail(f"Valid OCR raised an exception: {e}")

    # OCR模式错误用例：videoInpaintLang不合法
    def test_ocr_invalid_videoInpaintLang(self):
        option = GhostCutVideoTaskCreateRequestExtraOption(
            needChineseOcclude=14,
            videoInpaintLang="xx",
            videoInpaintMasks=[{
                "type": "trans_only_ocr",
                "region": [[0, 0], [1, 1]]
            }],
            lang="zh"
        )
        with self.assertRaises(ValueError):
            option.validate(mode="ocr")

    # 智能配乐正常用例
    def test_music_valid(self):
        rhythm_param = json.dumps({"url": "https://example.com/music.mp3"})
        option = GhostCutVideoTaskCreateRequestExtraOption(
            needRhythm=2,
            rhythmParam=rhythm_param
        )
        try:
            option.validate(mode="music")
        except Exception as e:
            self.fail(f"Valid music raised an exception: {e}")

    # 智能配乐错误用例：rhythmParam缺url
    def test_music_invalid_rhythmParam_missing_url(self):
        rhythm_param = json.dumps({})
        option = GhostCutVideoTaskCreateRequestExtraOption(
            needRhythm=2,
            rhythmParam=rhythm_param
        )
        with self.assertRaises(ValueError):
            option.validate(mode="music")

    # 宽松校验用例
    def test_loose_validation(self):
        option = GhostCutVideoTaskCreateRequestExtraOption(
            needWanyin=1,
            needChineseOcclude=1,
            needMask=5
        )
        try:
            option.validate()
        except Exception as e:
            self.fail(f"Loose validation failed: {e}")


if __name__ == '__main__':
    unittest.main()
