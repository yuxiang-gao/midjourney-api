from enum import Enum


class TriggerStatus(str, Enum):
    start = "start"  # 首次触发 MessageType.chat_input_command
    generating = "generating"  # 生成中
    end = "end"  # 生成结束 MessageType.default
    error = "error"  # 生成错误
    banned = "banned"  # 提示词被禁
    text = "text"  # 文本内容：describe
    verify = "verify"  # 需人工验证


class TaskType(str, Enum):
    generate = "generate"
    upscale = "upscale"
    variation = "variation"
    solo_variation = "solo_variation"
    solo_low_variation = "solo_low_variation"
    solo_high_variation = "solo_high_variation"
    max_upscale = "max_upscale"
    reset = "reset"
    describe = "describe"
    expand = "expand"
    zoomout = "zoomout"
