from typing import Dict
from pydantic import BaseModel, ConfigDict


class GhostcutBaseModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    def to_dict(self) -> Dict:
        return self.model_dump(exclude_none=True, by_alias=True)

    def to_json(self, indent: int = 4) -> str:
        return self.model_dump_json(indent=indent, exclude_none=True, by_alias=True)
