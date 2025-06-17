from ghostcut_sdk.api_base import BaseGhostcutApi
from ghostcut_sdk.basic import BasicApi
from ghostcut_sdk.image import ImageApi
from ghostcut_sdk.config.url import DEFAULT_BASE_URL


class GhostcutApi(BaseGhostcutApi):
    """
    Ghostcut API
    >>> from ghostcut_sdk import GhostcutApi
    >>> app_key = "replace with your app key"
    >>> app_secret = "replace with your app secret"
    >>> api = GhostcutApi(app_key, app_secret)
    >>> api.basic.query_enum("ProcessStatus")
    
    or config your app_key and app_secret in environment variables
    >>> import os
    >>> os.environ["GHOSTCUT_APP_KEY"] = "replace with your app key"
    >>> os.environ["GHOSTCUT_APP_SECRET"] = "replace with your app secret"
    >>> api = GhostcutApi()
    >>> api.basic.query_enum("ProcessStatus")
    """

    def __init__(
        self, app_key: str, app_secret: str, *, base_url: str = DEFAULT_BASE_URL
    ):
        super().__init__(app_key, app_secret, base_url)
        self.basic = BasicApi(app_key, app_secret, base_url)
        self.image = ImageApi(app_key, app_secret, base_url)
        # TODO video待完成
