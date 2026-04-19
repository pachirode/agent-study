from agent.re_act.llm_client import AgentCilent
from agent.re_act.tools import ToolExecutor, get_prompt_template
from agent.re_act.utils import search
from agent.re_act.parser import parse_output, parse_action, parse_action_input

class ReactAgent:
    def __init__(self, llm_client: AgentCilent, tool_executor: ToolExecutor):
        self.llm_client = llm_client
        self.tool_executor = tool_executor
        self.max_steps = 10
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
            
            # TODO: 这里需要继续实现后续逻辑，比如解析 LLM 输出并执行工具
            # 目前只是演示修复导入和格式问题
            break # 暂时中断循环，因为逻辑还不完整

if __name__ == "__main__":
    llm_client = AgentCilent()

    tool_executor = ToolExecutor()
    tool_executor.register_tool("search", search)

    agent = ReactAgent(llm_client, tool_executor)
    question = "华为最新的手机是哪一款？它的主要卖点是什么？"
    result = agent.run(question)
    print(result)
