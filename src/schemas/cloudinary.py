from enum import Enum
from typing import Annotated, Literal, Self

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    model_validator,
)


class UploadImageResult(BaseModel):
    model_config = ConfigDict(extra="ignore")

    public_id: str
    width: int
    height: int
    format: str
    resource_type: str
    secure_url: str
    asset_folder: str


class CropEnum(str, Enum):
    FILL = "fill"
    FIT = "fit"
    SCALE = "scale"
    LIMIT = "limit"
    PAD = "pad"
    THUMB = "thumb"


class GravityEnum(str, Enum):
    AUTO = "auto"
    FACE = "face"
    FACES = "faces"
    NORTH_EAST = "north_east"
    NORTH = "north"
    NORTH_WEST = "north_west"
    WEST = "west"
    SOUTH_WEST = "south_west"
    SOUTH = "south"
    SOUTH_EAST = "south_east"
    EAST = "east"
    CENTER = "center"


class FormatEnum(str, Enum):
    AUTO = "auto"
    JPG = "jpg"
    PNG = "png"
    WEBP = "webp"


class QualityEnum(str, Enum):
    AUTO = "auto"
    AUTO_BEST = "auto:best"
    AUTO_GOOD = "auto:good"
    AUTO_ECO = "auto:eco"
    AUTO_LOW = "auto:low"
    AUTO_LOW_SENSITIVE = "auto:low:sensitive"


class EffectsEnum(str, Enum):
    GRAYSCALE = "grayscale"
    SEPIA = "sepia"
    BLUR = "blur"
    SHARPEN = "sharpen"
    CONTRAST = "contrast"
    SATURATION = "saturation"
    VIGNETTE = "vignette"
    PIXELATE = "pixelate"


PixelDim = Annotated[int, Field(strict=True, ge=1)]
RelativeDim = Annotated[float, Field(strict=True, gt=0.0, le=2.0)]


def dim_kind(v: PixelDim | RelativeDim | Literal["iw", "ih"] | None) -> str:
    if v is None:
        return "none"
    if isinstance(v, int):
        return "px"
    if isinstance(v, float):
        return "rel"
    return "intrinsic"


class BaseModelWithConfig(BaseModel):
    model_config = ConfigDict(use_enum_values=True)


class TResize(BaseModelWithConfig):
    kind: Literal["resize"] = Field(default="resize", exclude=True)
    crop: CropEnum
    gravity: GravityEnum
    width: PixelDim | RelativeDim | Literal["iw"] | None = None
    height: PixelDim | RelativeDim | Literal["ih"] | None = None

    @model_validator(mode="after")
    def at_least_one_dim(self) -> Self:
        if self.width is None and self.height is None:
            raise ValueError("width or height must be provided")
        return self

    @model_validator(mode="after")
    def validate_types(self) -> Self:
        if self.width and self.height:
            width_kind = dim_kind(self.width)
            height_kind = dim_kind(self.height)
            if width_kind != height_kind:
                raise ValueError("width and height must be of the same type")
        return self

    @model_validator(mode="after")
    def validate_crop_values(self) -> Self:
        if self.crop in (CropEnum.FILL, CropEnum.THUMB):
            if not self.width or not self.height:
                raise ValueError(
                    "width and height are required for crop modes fill/thumb"
                )
            if not isinstance(self.width, int) or not isinstance(self.height, int):
                raise ValueError("crop modes fill/thumb require pixel dimensions")
        return self


class TQuality(BaseModelWithConfig):
    kind: Literal["quality"] = Field(default="quality", exclude=True)
    quality: QualityEnum | Annotated[int, Field(ge=1, le=100)] = QualityEnum.AUTO.value


class TFormat(BaseModelWithConfig):
    kind: Literal["format"] = Field(default="format", exclude=True)
    format: FormatEnum = FormatEnum.AUTO.value


class TEffect(BaseModelWithConfig):
    kind: Literal["effect"] = Field(default="effect", exclude=True)
    effect: EffectsEnum


class TAngle(BaseModelWithConfig):
    kind: Literal["angle"] = Field(default="angle", exclude=True)
    angle: Annotated[int, Field(ge=0, le=360)]


class TRadius(BaseModelWithConfig):
    kind: Literal["radius"] = Field(default="radius", exclude=True)
    radius: Annotated[int, Field(gt=0, le=200)] | Literal["max"] = "max"


Transformation = Annotated[
    TResize | TQuality | TFormat | TEffect | TAngle | TRadius,
    Field(discriminator="kind"),
]


class TransformRequest(BaseModel):
    transformation: Annotated[list[Transformation], Field(min_length=1, max_length=8)]
