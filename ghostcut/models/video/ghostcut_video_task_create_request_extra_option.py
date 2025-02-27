# -*- coding: utf-8 -*-
from ghostcut.models.ghostcut_model import GhostCutModel

from typing import Dict, List, Any

class GhostCutVideoTaskCreateRequestExtraOption(GhostCutModel):
    def __init__(
        self,
        range: List[int] = None,
        write_options: Dict[str, str] = None,
        subtitle_format: str = None,
    ):
        self.range = range
        self.write_options = write_options
        self.subtitle_format = subtitle_format

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.range is not None:
            result['range'] = self.range
        if self.write_options is not None:
            result['write_options'] = self.write_options
        if self.subtitle_format is not None:
            result['subtitle_format'] = self.subtitle_format
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('range') is not None:
            self.range = m.get('range')
        if m.get('write_options') is not None:
            self.write_options = m.get('write_options')
        if m.get('subtitle_format') is not None:
            self.subtitle_format = m.get('subtitle_format')
        return self