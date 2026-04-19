import os
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), "../../env/.env")
load_dotenv(env_path)

from serpapi import SerpApiClient

def search(query: str) -> str:
    """
    基于 SerpApi 搜索查询
    :param query: 搜索查询
    :return: 搜索结果
    """
    try:
        api_key = os.getenv("SERPAPI_KEY")
        if not api_key:
            return "错误:SERPAPI_KEY环境变量未设置"

        params = {
            "engine": "google",
            "q": query,
            "api_key": api_key,
            "gl": "cn",
            "hl": "zh-CN"
        }
        client = SerpApiClient(params)
        result = client.get_dict()

        if "answer_box_list" in result:
            return "\n".join(result["answer_box_list"])
        elif "answer_box" in result:
            return str(result["answer_box"].get("answer") or result["answer_box"].get("snippet"))
        elif "organic_results" in result and len(result["organic_results"]) > 0:
            snippets = [
                f"[{i+1}] {res.get('title', '')}\n{res.get('snippet', '')}"
                for i, res in enumerate(result["organic_results"][:3])
            ]
            return "\n\n".join(snippets)
        elif "knowledge_graph" in result and "description" in result["knowledge_graph"]:
            return result["knowledge_graph"]["description"]

        return f"没有查询到关于{query}的信息"
    except Exception as e:
        return f"错误:查询时遇到问题: {str(e)}"