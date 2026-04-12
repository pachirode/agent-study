import os
import requests
from tavily import TavilyClient
from dotenv import load_dotenv

# 加载环境变量
# 根据文件位置，env/.env 位于根目录，即 ../../../env/.env
env_path = os.path.join(os.path.dirname(__file__), "../../../env/.env")
load_dotenv(env_path)

def get_weather(city: str) -> str:
    """
    通过调用 wttr.in API 查询真实天气信息
    """

    url = f"https://wttr.in/{city}?format=j1"

    try:
        # 发起网络请求
        response = requests.get(url)
        # 检查响应状态码是否为200 (成功)
        response.raise_for_status() 
        # 解析返回的JSON数据
        data = response.json()
        
        # 提取当前天气状况
        current_condition = data['current_condition'][0]
        weather_desc = current_condition['weatherDesc'][0]['value']
        temp_c = current_condition['temp_C']
        
        # 格式化成自然语言返回
        return f"{city}当前天气:{weather_desc}，气温{temp_c}摄氏度"
        
    except requests.exceptions.RequestException as e:
        # 处理网络错误
        return f"错误:查询天气时遇到网络问题 - {e}"
    except (KeyError, IndexError) as e:
        # 处理数据解析错误
        return f"错误:解析天气数据失败，可能是城市名称无效 - {e}"

def get_attraction(city: str, weather: str) -> str:
    """
    根据城市和天气状况推荐景点
    """
    # 获取 API key
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return "错误:TAVILY_API_KEY环境变量未设置"
    
    tavily = TavilyClient(api_key=api_key)
    query = f"'{city}' 在 ‘{weather}’ 下最值得去的旅游景点及推荐理由"

    try:
        response = tavily.search(query=query, search_depth="basic", include_answer=True)
        answer = response.get("answer")
        if answer is not None:
            return answer
        
        formatted_results = []
        for result in response.get("results", []):
            formatted_results.append(f"- {result['title']}: {result['content']}")

        if len(formatted_results) == 0:
            return "没有找到相关景点"
        else:
            return "\n".join(formatted_results)
    except Exception as e:
        return f"错误:查询景点时遇到错误 - {e}"

def get_system_prompt(system_prompt_file: str=r"src\resource\prompt\travel.txt") -> str:
    with open(system_prompt_file, "r", encoding="utf-8") as f:
        system_prompt = f.read()
    return system_prompt


tools = {
    "get_weather": get_weather,
    "get_attraction": get_attraction
}

from openai import OpenAI

class OpenAIClient:

    def __init__(self, model: str, api_key: str, base_url: str) -> None:
        self.model = model
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def generate(self, prompt: str, system_prompt: str) -> str:
        """
        调用 OpenAI API 生成文本
        """
        print("正在调取大模型...")
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=False
            )

            answer = response.choices[0].message.content
            print("大模型响应成功")
            return answer
        except Exception as e:
            print(f"调用大模型失败: {e}")
            return f"错误:调用大模型失败 - {e}"

def main(city: str="Shanghai"):
    """
    主函数，用于处理用户请求
    """
    import re
    # env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), r"src\env\.env")
    API_KEY = os.getenv("API_KEY")
    BASE_URL = os.getenv("BASE_URL")
    MODEL_ID = os.getenv("MODEL_ID")

    llm = OpenAIClient(
        model=MODEL_ID,
        api_key=API_KEY,
        base_url=BASE_URL
    )

    user_prompt = f"帮我查看一下{city}的天气，根据天气推荐一个适合旅游的景点"
    prompt_history = [f"用户请求: {user_prompt}"]

    print(f"用户输入: {user_prompt}\n" + "="*40)

    for i in range(3):
        print(f"当前循环{i}")

        full_prompt = "\n".join(prompt_history)

        llm_output = llm.generate(full_prompt, get_system_prompt())
        match = re.search(r'(Thought:.*?Action:.*?)(?=\n\s*(?:Thought:|Action:|Observation:)|\Z)', llm_output, re.DOTALL)
        if match:
            truncated = match.group(1).strip()
            if truncated != llm_output.strip():
                llm_output = truncated
                print("已截断多余的 Thought-Action 对")
        print(f"模型输出:\n{llm_output}\n")
        prompt_history.append(llm_output)

        action_match = re.search(r"Action: (.*)", llm_output, re.DOTALL)
        if not action_match:
            observation = "错误: 未能解析到 Action 字段。请确保你的回复严格遵循 'Thought: ... Action: ...' 的格式。"
            observation_str = f"Observation: {observation}"
            print(f"{observation_str}\n" + "="*40)
            prompt_history.append(observation_str)
            continue
        action_str = action_match.group(1).strip()

        if action_str.startswith("Finish"):
            finish_match = re.match(r"Finish\[(.*)\]", action_str)
            if finish_match:
                final_answer = finish_match.group(1)
                print(f"任务完成，最终答案: {final_answer}")
            else:
                print(f"任务完成: {action_str}")
            break
    
        tool_name_match = re.search(r"(\w+)\(", action_str)
        if not tool_name_match:
            observation = f"错误: 无法解析工具名称 '{action_str}'"
            observation_str = f"Observation: {observation}"
            print(f"{observation_str}\n" + "="*40)
            prompt_history.append(observation_str)
            continue
            
        tool_name = tool_name_match.group(1)
        args_match = re.search(r"\((.*)\)", action_str)
        if args_match:
            args_str = args_match.group(1)
            kwargs = dict(re.findall(r'(\w+)="([^"]*)"', args_str))
        else:
            kwargs = {}

        if tool_name in tools:
            observation = tools[tool_name](**kwargs)
        else:
            observation = f"错误：未定义的工具 '{tool_name}'"

        # 3.4. 记录观察结果
        observation_str = f"Observation: {observation}"
        print(f"{observation_str}\n" + "="*40)
        prompt_history.append(observation_str)

if __name__ == "__main__":
    main("东京")

       
