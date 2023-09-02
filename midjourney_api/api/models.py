import re
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import AnyHttpUrl, BaseModel

from midjourney_api.discord.enums import TaskType
from midjourney_api.settings import settings


# extract url and text
def extract_url(text: str) -> tuple[Optional[str], str]:
    chunks = text.split(" ")
    for chunk in chunks:
        if chunk.startswith("http://") or chunk.startswith("https://"):
            return chunk, text.replace(chunk, "").strip()
    return None, text


class TaskId(BaseModel):
    id: str

    def to_prompt(self) -> str:
        return f"{settings.prompt_id_prefix}{self.id}{settings.prompt_id_suffix}"

    @classmethod
    def from_prompt(cls, prompt: str) -> "TaskId":
        match = re.search(rf"{settings.prompt_id_prefix}(.+?){settings.prompt_id_suffix}", prompt)
        if match:
            return cls(id=match.group(1))
        else:
            raise ValueError(f"Invalid prompt: {prompt}")

    def __repr__(self):
        return self.id

    def __str__(self):
        return self.id


class TaskStatus(str, Enum):
    queued = "queued"
    waiting = "waiting"
    running = "running"
    finished = "finished"
    failed = "failed"
    cancelled = "cancelled"


class TaskInfo(BaseModel):
    id: str
    status: TaskStatus
    actions: list[str] = []
    attachments: list[str] = []
    progress: Optional[float] = None
    created_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None


class TaskImagine(BaseModel):
    prompt: str
    picurl: Optional[AnyHttpUrl] = None

    def build_prompt(self, unique_id: str) -> str:
        url, prompt = extract_url(self.prompt)
        prompt = prompt.replace("\n", " ").replace("\r", " ").replace("\t", " ").strip()

        return f"{self.picurl or url or ''} {TaskId(id=unique_id).to_prompt()} {prompt}"


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
    task_id: str
    task_type: TaskType | None = None


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
