# TSBot

Asynchronous framework to build **TeamSpeak 3 Server Query** bots

## ✅ Features

- Uses modern Python `async` and `await` syntax
- Secure connection through SSH
- Ease of use query building
- Built-in and configurable ratelimiter if no access to `whitelist.txt`
- Query caching

## ✏️ Examples

```python
import asyncio

from tsbot import TSBot
from tsbot import events
from tsbot.query import query


bot = TSBot(
    username="USERNAME",
    password="PASSWORD",
    address="ADDRESS",
)


@bot.command("hello")
async def hello_world(bot: TSBot, ctx: dict[str, str]):
    await bot.respond(ctx, "Hello World!")


@bot.on("cliententerview")
async def poke_on_enter(bot: TSBot, event: events.TSEvent):
    poke_query = query("clientpoke").params(clid=event.ctx["clid"], msg="Welcome to the server!")
    await bot.send(poke_query)


asyncio.run(bot.run())
```

**Check out [📁examples](https://github.com/0x4aK/TSBot/blob/master/examples) for more**

## 📦 Installation

**Python 3.10 or higher is required**

Installing with pip:

```shell
# Linux/macOS
python3 -m pip install tsbot

# Windows
py -3 -m pip install tsbot
```
