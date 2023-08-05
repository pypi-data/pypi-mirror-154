# AioJikan

An asynchronous api wrapper for the [Jikan API](https://jikan.moe/).

Features
- Simple and Easy to use
- 100% API Coverage
- Fully typehinted models (I tried my best at least)
- Usage of datetime objects where applicable for easy conversions

## Examples

All projects should create a single instance of AioJikan, provide it with an aiohttp.ClientSession if you want to, and you're good to go.

```python
import asyncio
import aiojikan

async def main():

    client = aiojikan.AioJikan()

    love_is_war = await client.get_anime(37999)

    print(f"Love is war has {love_is_war.favorites} favorites!")

    await client.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

## License

This library is licensed under the MIT license, please review it [here](https://github.com/Leg3ndary/aiojikan/blob/main/LICENSE)