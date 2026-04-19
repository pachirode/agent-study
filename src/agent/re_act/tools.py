class ToolExecutor:
    def __init__(self) -> None:
        self.tools = {}

    def register_tool(self, name: str, func: callable) -> None:
        self.tools[name] = func

    def get_tool(self, name: str) -> callable:
        return self.tools.get(name, {})
    
    def get_tools_desc(self) -> str:
        return "\n".join([f"{name}: {func}" for name, func in self.tools.items()])

def get_prompt_template():
    with open(r"src\resource\prompt\react.txt", "r", encoding="utf-8") as f:
        return f.read()
