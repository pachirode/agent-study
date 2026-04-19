from pyparsing import Keyword, Word, Suppress, SkipTo, Optional, StringEnd
from pyparsing import alphanums
from pyparsing import ParseException

THOUGHT = Keyword("Thought:")
ACTION = Keyword("Action:")

action_name = Word(alphanums + "_")("name")
action_input = Suppress("[") + SkipTo("]")("input") + Suppress("]")
action_expr = Optional(Suppress("`")) + action_name + action_input + Optional(Suppress("`"))

output_parser = (
    Suppress(THOUGHT) + 
    SkipTo(ACTION)("thought") +
    Suppress(ACTION) + 
    Optional(Suppress("`")) +
    action_expr("action_part")
)

def parse_output(text: str):
    """
    解析输出字符串
    :param output: 输出字符串
    :return: 解析结果字典
    """
    try:
        res = output_parser.parse_string(text)
        thought = res.thought.strip() if "thought" in res else None
        
        action = None
        if "name" in res and "input" in res:
            action = f"{res.name}[{res.input}]"
        
        return thought, action
    except ParseException:
        return None, None

def parse_action(action_text: str):
    """解析类似 search[python] 的字符串"""
    try:
        res = action_expr.parse_string(action_text)
        return res.name, res.input
    except ParseException:
        return None, None

def parse_action_input(action_text: str):
    """仅解析方括号内的内容"""
    name, action_input = parse_action(action_text)
    return action_input if action_input is not None else ""

if __name__ == "__main__":
    test_text = """
    Thought: 我需要搜索关于 Python 的定义。
    Action: google_search[What is Python?]
    """

    thought, action = parse_output(test_text)
    print(f"Thought: {thought}") # Thought: 我需要搜索关于 Python 的定义。
    print(f"Action: {action}")   # Action: google_search[What is Python?]

    name, args = parse_action(action)
    print(f"Action Name: {name}")  # Action Name: google_search
    print(f"Action Input: {args}") # Action Input: What is Python?