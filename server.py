# server.py
import json
import requests
from fastmcp import FastMCP

mcp = FastMCP("Real Estate MCP")  # Remove host/port from constructor
#mcp.run()
mcp.run(transport="streamable-http",
            host="localhost", port=9000, path="/mcp")

@mcp.tool  # 定義一個工具
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b
'''
@mcp.tool  # 另一個範例工具
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b
'''

@mcp.tool()  # 另一個範例工具
def get_ebugcodes_by_key_word(keyword:str) :
    url = "<url>"
    """query ebugs by key word"""

    headers = {
        "Authorization": "Bearer " + "<token>",
        "Content-Type": "application/json",
    }

    payload = {"queryModel":"TSR.EbugSearch","pageSize":25,"pageIndex":1,"isDesc":True,"sortBy":"CreateTime","conditions":
        [{"field":"CreateTime","range":{"gte":"2025-03-30","lte":"2025-09-09"}},
         {"field":"IsValid","termNot":{"query":"false"}},
         {"field":"Status","termNot":{"querys":["Close","NAB","Postpone","Wont Fix","Won't Fix","NotReproducible","Cancelled"]}},
         {"field":"ShortDescription","match":{"query":keyword}}]}
    response = requests.post(url, headers=headers, json=payload)

    #if response.status_code == 200:
    #    print("Success:" + response.text)
    #else:
    #    print(f"Failed with status code: {response.status_code}")
    #    print("Error:" + response.text)
    return response.text

'''
if __name__ == "__main__":
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    # mcp.run()
    mcp.run(transport="streamable-http",
            host="localhost", port=9000, path="/mcp")
'''