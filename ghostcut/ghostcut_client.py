# -*- coding: utf-8 -*-
from ghostcut.config.const import GHOSTCUT_API_ENDPOINT
import requests
import json

from ghostcut.models.ghostcut_model import GhostCutModel
from typing import Dict, List, Any

from ghostcut.models.video.ghostcut_video_task_create_request import (
    GhostCutVideoTaskCreateRequest,
)
from ghostcut.utils.ghostcut_sign_utils import generate_ghostcut_sign


class GhostCutClient:
    _app_secret: str = None
    _app_key: str = None
    _api_endpoint: str = None

    def __init__(self, app_key, app_secret):
        self._app_key = app_key
        self._app_secret = app_secret
        self._api_endpoint = GHOSTCUT_API_ENDPOINT

    """
    无签名post
    """

    def _do_post(self, path: str, body: Any):
        return requests.post(
            self._api_endpoint + path,
            data=body,
            headers={
                "Content-type": "application/json",
            },
        ).json()

    """
    签名并post
    """

    def _do_post_with_sign(self, path: str, request_model: GhostCutModel):
        body = json.dumps(request_model.to_map())
        return requests.post(
            self._api_endpoint + path,
            data=body,
            headers={
                "Content-type": "application/json",
                "AppKey": self._app_key,
                "AppSign": generate_ghostcut_sign(body, self._app_secret),
            },
        ).json()

    def video_task_create(self, request: GhostCutVideoTaskCreateRequest):
        return self._do_post_with_sign("gateway/ve/work/free", request_model=request)

    def video_task_query(self):
        pass

    def enum_query(self, enum_name):
        return self._do_post("enum/query2", {"text": enum_name})
