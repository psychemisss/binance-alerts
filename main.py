import asyncio
import aiohttp


async def get_highest_hour_price(symbol: str):
    """
    Gets the highest price of a symbol in the last hour

    :param symbol: symbol
    :return: highest price in the last hour
    """

    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1h&limit=1"

    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return float(data[0][2])
            else:
                return None


async def get_price(symbol: str):
    """
    Gets the current price of a symbol

    :param symbol: symbol
    :return: current price
    """

    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"

    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return float(data["price"])
            else:
                return None


async def get_multiple_prices(symbols: list):
    tasks = []
    for symbol in symbols:
        tasks.append(get_price(symbol))
    return await asyncio.gather(*tasks)


async def get_multiple_highest_hour_prices(symbols: list):
    tasks = []
    for symbol in symbols:
        tasks.append(get_highest_hour_price(symbol))
    return await asyncio.gather(*tasks)


async def run_checkout(symbol: list) -> None:
    """
    Checks if the price of a symbol is 1 percent lower than the highest price in the last hour

    :param symbol: list of symbols
    :return: None
    """

    if symbol:
        prices = await get_multiple_prices(symbol)
        highest_prices = await get_multiple_highest_hour_prices(symbol)

        # map the highest price to current prices
        highest_prices_map = {
            highest_price_symbol: highest_price for highest_price_symbol, highest_price in zip(symbol, highest_prices)
        }

        for price_symbol, price in zip(symbol, prices):
            # write print if price is 1 percent lower than the highest price in the last hour
            if price < highest_prices_map[price_symbol] * 0.99:
                print(f"Price of {price_symbol} is 1 percent lower than highest price in the last hour!")

            # for visualizing the current price and the highest price in the last hour
            # print(# f"Current price of {price_symbol} is {price}, \
            # highest price in the last hour is {highest_prices_map[price_symbol]} ")


async def main():
    symbol = ["XRPUSDT"]
    while True:
        await run_checkout(symbol)
        await asyncio.sleep(1)


asyncio.run(main())
