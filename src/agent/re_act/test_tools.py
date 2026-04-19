from tools import ToolExecutor
from utils import search

if __name__ == "__main__":
    tool_executor = ToolExecutor()

    search_description = "网页搜索引擎。当你回答知识库中找不到信息，使用此工具。"
    tool_executor.register_tool("search", search)

    print("\n--- 执行 Action: Search['最新款的华为手机'] ---")
    tool_name = "search"
    tool_input = "最新款的华为手机"

    tool_function = tool_executor.get_tool(tool_name)
    if tool_function:
        observation = tool_function(tool_input)
        print("--- 观察 (Observation) ---")
        print(observation)
    else:
        print(f"错误：未找到名为 '{tool_name}' 的工具。")

