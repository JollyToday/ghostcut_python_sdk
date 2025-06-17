from ghostcut_sdk.api_base import BaseGhostcutApi
from ghostcut_sdk.common import CommonApi
from ghostcut_sdk.image import ImageApi
from ghostcut_sdk.config.url import DEFAULT_BASE_URL


class GhostcutApi(BaseGhostcutApi):
    """
    Ghostcut API
    """

    def __init__(self, app_key: str, app_secret: str, base_url: str = DEFAULT_BASE_URL):
        super().__init__(app_key, app_secret, base_url)
        self.common = CommonApi(app_key, app_secret, base_url)
        self.image = ImageApi(app_key, app_secret, base_url)
        # TODO video待完成
