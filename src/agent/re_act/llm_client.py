import os
from openai import OpenAI
from typing import Dict
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), "../../env/.env")
load_dotenv(env_path)


class AgentCilent:
    def __init__(self, model: str=None, api_key: str=None, base_url: str=None) -> None:
        self.model = model or os.getenv("MODEL_ID")
        self.api_key = api_key or os.getenv("API_KEY")
        self.base_url = base_url or os.getenv("BASE_URL")

        if not all([self.model, self.api_key, self.base_url]):
            raise ValueError("model, api_key, and base_url must be set")

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )

    def thinking(self, msg: Dict[str, str], temperature: float = 0.5) -> str:
        """
        调用 LLM 进行思考
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[msg],
                max_tokens=1024,
                temperature=temperature,
                stream=True
            )

            collected_content = []
            print("LLM 正在响应: ", end="", flush=True)
            for chunk in response:
                if chunk.choices:
                    content = chunk.choices[0].delta.content or ""
                    print(content, end="", flush=True)
                    collected_content.append(content)
            print()  # 在流式输出结束后换行
            return "".join(collected_content)
        except Exception as e:
            print("调用 LLM 时遇到问题:", e)
            return None

if __name__ == "__main__":
    agent = AgentCilent()
    msg = {"role": "user", "content": "你好"}
    print(agent.thinking(msg))