import os
from dotenv import load_dotenv

# 使用与 weather_agent.py 相同的相对路径逻辑
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../env/.env")
print(f"Checking env path: {env_path}")
print(f"File exists: {os.path.exists(env_path)}")

load_dotenv(env_path)

print(f"API_KEY: {os.getenv('API_KEY')}")
print(f"BASE_URL: {os.getenv('BASE_URL')}")
print(f"MODEL_ID: {os.getenv('MODEL_ID')}")
print(f"TAVILY_API_KEY: {os.getenv('TAVILY_API_KEY')}")
