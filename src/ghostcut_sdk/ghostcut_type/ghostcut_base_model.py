from pydantic import BaseModel, ConfigDict


class GhostcutBaseModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)