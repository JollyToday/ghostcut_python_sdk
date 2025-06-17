from typing import Dict, Optional
from pydantic import BaseModel, ConfigDict


class GhostcutBaseModel(BaseModel):
    def to_dict(self) -> Dict:
        """
        Convert the model to a dictionary.

        Returns:
            Dict: The dictionary of the model.
        """
        return self.model_dump(exclude_none=True, by_alias=True)

    def to_json(self, indent: Optional[int] = None) -> str:
        """
        Convert the model to a JSON string.

        Args:
            indent (Optional[int], optional): The number of spaces to use for indentation. Defaults to None which means no indentation.

        Returns:
            str: The JSON string of the model.
        """
        return self.model_dump_json(indent=indent, exclude_none=True, by_alias=True)


class PopulateByNameGhostcutBaseModel(GhostcutBaseModel):
    model_config = ConfigDict(populate_by_name=True)
