import unittest
from ghostcut_python_sdk.ghostcut.uploader import FileUploader
from ghostcut_python_sdk.ghostcut.errors.exceptions import  UploadError,PolicyError

class TestFileUploader(unittest.TestCase):

    def setUp(self):
        self.app_key = ""  # Appkey
        self.app_secret = ""  # sign
        self.uploader = FileUploader(app_key=self.app_key, app_secret=self.app_secret)

    def test_get_upload_policy(self):
        """测试获取上传凭证"""
        try:
            policy = self.uploader.get_upload_policy()
            self.assertIn("accessid", policy)
        except PolicyError as e:
            self.fail(f"凭证异常: {e}")

    def test_upload_file(self):
        """测试文件上传"""
        # 替换为实际文件路径和文件名
        file_path = "path/to/your/file.jpg"
        filename = "file.jpg"

        try:
            url = self.uploader.upload_file(file_path, filename)
            self.assertTrue(url.startswith("http"))  # 检查返回 URL 是否有效
        except UploadError as e:
            self.fail(f"上传异常: {e}")


if __name__ == "__main__":
    unittest.main()
