from typing import List, Type, Optional
from pydantic import BaseModel, Field
import json
import os
from openai import OpenAI
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

# ---------- 配置 ----------
base_url = "https://api.moonshot.cn/v1"   # Kimi 的 OpenAI-Compatible 入口
api_key  = "sk-qinaQvx23rrThO9LfkZc547KfTB9LUEHHwXYDfTi7nNwXYvJ"    # 环境变量里放 Kimi 的 key
model    = "moonshot-v1-128k"               # 按需选 8k / 32k / 128k

if not api_key:
    raise ValueError("KIMI_API_KEY environment variable is required but not set")

# ② 初始化客户端
client = OpenAI(
    base_url=base_url,
    api_key=api_key,
)


# ---------- 生成函数 ----------
def generate(messages: List[dict], custom_format: Type[BaseModel]) -> Optional[BaseModel]:
    strformat = custom_format.model_json_schema()
    messages.append({
        "role": "system",
        "content": (
            "You must output a single, valid JSON object with exactly these fields:\n"
            "{\n"
            '  "stepsOfTask": ["step1", "step2", ...],\n'
            '  "instructions": [{ "content": "instruction text","degreeOfDetail": 7, "armMention": false, "numOfWords": 15}] \n'
            "No extra keys, no nesting, no markdown code block."
        ),
    })
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=4096,
        temperature=0.8,
        top_p=1.0,
        response_format={"type": "json_object"},   # Kimi 同样支持
    )

    json_content = response.choices[0].message.content
    if json_content:
        parsed = json.loads(json_content)
        return custom_format.model_validate(parsed)
    return None


# ---------- 简单测试 ----------
if __name__ == "__main__":
    class InstructionFormat(BaseModel):
        task: str
        steps: List[str]

    msgs = [{"role": "user", "content": "请生成一个“找盘子”任务的步骤"}]
    print(generate(msgs, InstructionFormat))
