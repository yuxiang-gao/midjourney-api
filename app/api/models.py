import re
from typing import Optional

from pydantic import AnyHttpUrl, BaseModel

from app.discord.enums import TriggerType


# extract url and text
def extract_url(text: str) -> tuple[Optional[str], str]:
    chunks = text.split(" ")
    for chunk in chunks:
        if chunk.startswith("http://") or chunk.startswith("https://"):
            return chunk, text.replace(chunk, "").strip()
    return None, text


class TaskImagine(BaseModel):
    prompt: str
    picurl: Optional[AnyHttpUrl] = None

    def build_prompt(self, unique_id: str) -> str:
        url, prompt = extract_url(self.prompt)
        prompt = prompt.replace("\n", " ").replace("\r", " ").replace("\t", " ").strip()

        return f"{self.picurl or url or ''} <#{unique_id}#> {prompt}"


class SubTask(BaseModel):
    msg_id: str
    msg_hash: str
    trigger_id: str  # 供业务定位触发ID，/trigger/imagine 接口返回的 trigger_id


class TaskUV(SubTask):
    index: int


TaskReset = SubTask


class TaskExpand(SubTask):
    direction: str  # right/left/up/down


class TaskZoomOut(SubTask):
    zoomout: int  # 2x: 50; 1.5x: 75


class TaskDescribe(BaseModel):
    upload_filename: str
    trigger_id: str


class QueueRelease(BaseModel):
    trigger_id: str


class TaskResponse(BaseModel):
    message: str = "success"
    status: str
    trigger_id: str
    trigger_type: TriggerType


class UploadResponse(BaseModel):
    message: str = "success"
    upload_filename: str = ""
    upload_url: str = ""
    trigger_id: str


class Message(BaseModel):
    upload_filename: str


class MessageResponse(BaseModel):
    message: str = "success"
    picurl: str
