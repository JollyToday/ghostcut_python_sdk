from typing import Optional, List, Tuple, Literal
from pydantic import BaseModel, Field


TextStyleAlignment = Literal["left", "center", "right"]


class OcrRegion(BaseModel):
    confidence: float = Field(..., description="OCR confidence score")
    text: str = Field(..., description="Original text content")
    text_region: List[List[int]] = Field(..., description="Text region coordinates")
    lang: str = Field(..., description="Language code")
    clip_size: Tuple[int, int] = Field(..., description="Clip size [width, height]")


class TextStyle(BaseModel):
    fill_color: str = Field(..., description="Text fill color")
    bg_color: str = Field(..., description="Background color")
    stroke_color: str = Field(..., description="Stroke color")
    alignment: TextStyleAlignment = Field(..., description="Text alignment")
    font_size: int = Field(..., description="Font size of source text")
    trans_font_size: int = Field(..., description="Font size of translated text")
    stroke_width: int = Field(..., description="Stroke width")


class AvailableBound(BaseModel):
    left: int = Field(..., description="Left boundary")
    right: int = Field(..., description="Right boundary")
    up: int = Field(..., description="Upper boundary")
    down: int = Field(..., description="Lower boundary")


class Textbox(BaseModel):
    left: float = Field(..., description="Left position")
    top: float = Field(..., description="Top position")
    width: float = Field(..., description="Width")
    height: float = Field(..., description="Height")


class RotateInfo(BaseModel):
    rotate_center: Tuple[int, int] = Field(..., description="Rotate center coordinates")
    rotate_angle: float = Field(..., description="Rotation angle")


class RenderInfo(BaseModel):
    text: str = Field(..., description="Rendered text")
    text_width: float = Field(..., description="Text width")
    anchor_point: list[int] = Field(..., description="Anchor point coordinates")
    is_rotate: bool = Field(..., description="Whether text is rotated")
    rotate_info: Optional[RotateInfo] = Field(
        default=None, description="Rotate information"
    )
    textbox: Optional[Textbox] = Field(default=None, description="Text bounding box")
    font_family: Optional[str] = Field(default=None, description="Font family")


class MetaDataItem(BaseModel):
    ocr_region: OcrRegion = Field(..., description="OCR region information")
    text_style: TextStyle = Field(..., description="Text style information")
    target_width: int = Field(..., description="Target width")
    target_height: int = Field(..., description="Target height")
    image_size: Tuple[int, int] = Field(..., description="Image size (width, height)")
    available_bound: AvailableBound = Field(..., description="Available boundary")
    rotate90: bool = Field(..., description="Whether to rotate 90 degrees")
    tgt_lang: str = Field(..., description="Target language, e.g. 'en'")
    source: str = Field(..., description="Source text")
    translation: str = Field(..., description="Translation of source text")
    is_commodity: bool = Field(..., description="Whether it's a commodity")
    render_infos: Optional[List[RenderInfo]] = Field(
        default=None, description="Render information list"
    )


class ImageTranslateResult(BaseModel):
    meta_data: List[MetaDataItem] = Field(default_factory=list, description="meta data")
    output_osskey: Optional[str] = Field(default=None, description="output osskey")
    output_url: Optional[str] = Field(default=None, description="output url")
    inpaint_osskey: Optional[str] = Field(default=None, description="inpaint osskey")
    inpaint_url: Optional[str] = Field(default=None, description="inpaint url")
    commodity_mask_osskey: Optional[str] = Field(
        default=None, description="commodity mask osskey"
    )
    commodity_url: Optional[str] = Field(default=None, description="commodity url")
