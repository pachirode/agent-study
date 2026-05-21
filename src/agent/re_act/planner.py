import ast
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir in sys.path:
    sys.path.remove(current_dir)

from agent.re_act.llm_client import AgentClient
from agent.re_act.tools import get_planner_prompt_template

class Planner:
    def __init__(self, llm_client: AgentClient):
        self.llm_client = llm_client

    def plan(self, question: str) -> list[str]:
        prompt = get_planner_prompt_template().format(question=question)
        
        msg = {"role": "user", "content": prompt}

        print("开始生成计划")
        response = self.llm_client.thinking(msg) or ""

        try:
            plan_str = response.split("```python")[1].split("```")[0].strip()
            plan = ast.literal_eval(plan_str)
            return plan if isinstance(plan, list) else []
        except Exception:
            import traceback
            print(traceback.format_exc())
            return []

class Executor:
    def __init__(self, llm_client: AgentClient):
        self.llm_client = llm_client


if __name__ == '__main__':
    planer = Planner(llm_client=AgentClient())
    print(planer.plan("一个水果店周一卖了16个苹果。周二比周一多一倍。周三比周二少两个。一共卖了多少？"))