# server.py
import json
import requests
from fastmcp import FastMCP
import os
from dotenv import load_dotenv
from datetime import datetime
from dateutil.relativedelta import relativedelta

mcp = FastMCP("Real Estate MCP")  # Remove host/port from constructor
#mcp.run()
load_dotenv()

@mcp.tool("add")  # 定義一個工具
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b


@mcp.tool("ebugcode")  # 另一個範例工具
def get_ebugcodes_by_key_word(keyword:str, page_index: int, months_ago: int):
    url = os.getenv("EPF_URL")
    """query ebugs by key word"""
    token = os.getenv("TOKEN")
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json",
    }

    format_string = "%Y-%m-%d %H:%M:%S"
    current_dt = datetime.now()
    past_dt = current_dt - relativedelta(months=months_ago)

    payload = {"queryModel":"TSR.EbugSearch","pageSize":25,"pageIndex":page_index,"isDesc":True,"sortBy":"CreateTime","conditions":
        [{"field":"CreateTime","range":{"gte":past_dt.strftime(format_string),"lte":current_dt.strftime(format_string)}},
         {"field":"IsValid","termNot":{"query":"false"}},
         {"field":"Status","termNot":{"querys":["Close","NAB","Postpone","Wont Fix","Won't Fix","NotReproducible","Cancelled"]}},
         {"field":"ShortDescription","match":{"query":keyword}}]}
    response = requests.post(url, headers=headers, json=payload)

    return response.text


mcp.run(transport="streamable-http",host="0.0.0.0", port=9000, path="/mcp")
#transport="streamable-http",host="0.0.0.0", port=9000, path="/mcp"
'''
if __name__ == "__main__":
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    # mcp.run()
    mcp.run(transport="streamable-http",
            host="0.0.0.0", port=9000, path="/mcp")
'''