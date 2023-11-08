import asyncio
import pywebio
from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import defer_call, info as session_info, run_async, run_js

bts = {
    '←': 1,
    '↑': 2,
    '◯': 3,
    '↓': 4,
    '→': 5,
}


@pywebio.config(theme="dark")
async def main():
    put_buttons(['←', '↑', '◯', '↓', '→'], onclick=lambda btn: print(btn), outline=True, position=OutputPosition.TOP)


if __name__ == "__main__":
    start_server(main, host="0.0.0.0", port=8080)