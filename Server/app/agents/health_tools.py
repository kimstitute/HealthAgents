from langchain_core.tools import tool 

@tool
def test_tool():
    pass

HEALTH_TOOLS = [
    test_tool,
]