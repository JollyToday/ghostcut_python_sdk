from pydantic import Field
from ghostcut_sdk.ghostcut_type.ghostcut_base_model import (
    PopulateByNameGhostcutBaseModel,
)


class PointAsset(PopulateByNameGhostcutBaseModel):
    """Point asset model for balance query response"""

    id: int = Field(..., description="Asset ID")
    point_amount: float = Field(
        ..., alias="pointAmount", description="Total point amount"
    )
    company: str = Field(..., description="Company identifier")
    expire_time: int = Field(
        ..., alias="expireTime", description="Expiration timestamp"
    )
    id_zl_point_package: int = Field(
        ..., alias="idZlPointPackage", description="ZL point package ID"
    )
    order_no: str = Field(..., alias="orderNo", description="Order number")
    point_balance: float = Field(
        ..., alias="pointBalance", description="Remaining point balance"
    )
    remark: str = Field(..., description="Asset remark/description")
    ctime: int = Field(..., description="Creation timestamp")
    lutime: int = Field(..., description="Last update timestamp")
