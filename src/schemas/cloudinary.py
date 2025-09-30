from pydantic import BaseModel, ConfigDict


class UploadImageResult(BaseModel):
    model_config = ConfigDict(extra="ignore")

    public_id: str
    width: int
    height: int
    format: str
    resource_type: str
    secure_url: str
    asset_folder: str
