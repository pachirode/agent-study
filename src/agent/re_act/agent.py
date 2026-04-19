import sys
import os

# 避免文件名 agent.py 与包名 agent 冲突导致的 ModuleNotFoundError
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir in sys.path:
    sys.path.remove(current_dir)

from agent.re_act.llm_client import AgentCilent
from agent.re_act.tools import ToolExecutor, get_prompt_template
from agent.re_act.utils import search
from agent.re_act.parser import parse_output, parse_action, parse_action_input

class ReactAgent:
    def __init__(self, llm_client: AgentCilent, tool_executor: ToolExecutor):
        self.llm_client = llm_client
        self.tool_executor = tool_executor
        self.max_steps = 3
        self.history = []

    def run(self, question: str) -> str:
        """
        运行智能体
        :param question: 搜索查询
        :return: 搜索结果
        """

        self.history = []
        current_step = 0
        tools_desc = self.tool_executor.get_tools_desc()

        while current_step < self.max_steps:
            current_step += 1
            print(f"Step {current_step}")

            history = "\n".join(self.history)
            prompt = get_prompt_template().format(
                tools = tools_desc,
                history = history,
                question = question
            )

            msg = {"role" :"user", "content": prompt}
            response_text = self.llm_client.thinking(msg)
            if response_text is None:
                return "错误:调用 LLM 时遇到问题"

            thought, action = parse_output(response_text)
            if thought is None:
                print(f"解析失败，LLM 响应为: {response_text}")
                return "错误:无法解析输出"
            
            print(f"Thought: {thought}")

            if action is None:
                print("解析 Action 失败, 无法执行任何操作")
                break

            if action.startswith("Finish"):
                print("智能体完成任务")
                # 解析出最终答案
                _, final_answer = parse_action(action)
                return f"最终结果: {final_answer}"

            print(f"Action: {action}")

            tool_name, args = parse_action(action)
            if tool_name is None or args is None:
                print("Action 格式错误, 请检查")
                break

            print(f"开始执行操作: {tool_name}，参数: {args}")
            tool = self.tool_executor.get_tool(tool_name)
            if tool is None:
                print(f"工具 {tool_name} 不存在")
                break

            result = tool(args)
            if result is None:
                print(f"工具 {tool_name} 执行失败")
                break

            print(f"工具 {tool_name} 执行成功: {result}")
            self.history.append(f"Action: {action}")
            self.history.append(f"Observation: {result}")

        print("达到最大执行步数, 智能体无法完成任务")
        return None


if __name__ == "__main__":
    llm_client = AgentCilent()

    tool_executor = ToolExecutor()
    tool_executor.register_tool("search", search)

    agent = ReactAgent(llm_client, tool_executor)
    question = "华为最新的手机是哪一款？它的主要卖点是什么？"
    result = agent.run(question)
    print(result)
