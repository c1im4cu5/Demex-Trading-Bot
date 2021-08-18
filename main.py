from tradehub.websocket_client import DemexWebsocket
import asyncio

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data_processing import ReceivingRecords
from data_processing import CleaningRecords
from data_processing import SavingRecords
from data_processing import *
from strategies import Treway


balances = []
orders = []
market_stats = []
swth_usdc = []
swth_busd = []
swth_eth = []
eth_usdc = []
cel_eth = []
cel_usdc = []
eth_wbtc = []
wbtc_usdc = []

wbtc_usdc_15_minute = []

#On successful connection
async def on_connect():
    #candlestick granularity - allowed values: 1, 5, 15, 30, 60, 360, 1440
    return await demex.subscribe("Subscription", [f"market_stats.{'market_stats'}", f"books.{'wbtc1_usdc1'}", f"books.{'eth1_wbtc1'}", f"books.{'cel_eth'}", f"books.{'cel1_usdc1'}", f"books.{'eth1_usdc1'}", f"books.{'swth_usdc1'}", f"books.{'swth_eth1'}", f"books.{'swth_busd1'}", f"candlesticks.{'swth_usdc1'}.{15}", f"balances.{''}", f"orders.{''}"])

#Receiving feed from websocket
async def on_receive(records: dict):

    #Check if "Channel" is in records (Initial response will be missing "Channel")
    if 'channel' in records:

        #Wallet Token Balances
        if 'balances' in records['channel']:
            #Send data to balance def in ReceivingRecords
            balances = ReceivingRecords.balances(records)
            SavingRecords.save_wallet_balances(balances)

        #Wallet Orders
        #Check if orders in record
        if 'orders.' in records['channel']:
            pass
            #Send data to ordes def in ReceivingRecords
            """orders.extend(ReceivingRecords.data_receiving.orders(records))
            #Send data to cleaning_orders def in CleaningRecords for accurate wallet orders (Small issues persist with clean)
            CleaningRecords.data_cleaning.cleaning_orders(orders)
            SavingRecords.saving_records.save_wallet_orders(orders)"""

        #Market Statistics
        if 'market_stats' in records['channel']:
            #Send data to market_stats def in ReceivingRecords
            market_stats = ReceivingRecords.market_stats(records)
            #Market stats is an overwriting data dump of info. There is no need to clean records
            #JSON file wil be overwritten with each new sequence update (Saves as dict of dicts) See storage file
            SavingRecords.save_market_stats(market_stats)

        #Orderbook receiving, saving and upkeep
        #Check if swth_usdc books are in the "channel"
        if 'books.swth_usdc1' in records['channel']:
            #Send data to Receiving records, return back list of dicts; which are extended with updates
            swth_usdc.extend(ReceivingRecords.swth_usdc_book(records))
            #Clean the records
            CleaningRecords.cleaning_orderbooks(swth_usdc)
            #Send to function for saving file
            SavingRecords.save_swth_usdc_orderbook(swth_usdc)
        #Check if swth_busd books are in the "channel"
        if 'books.swth_busd1' in records['channel']:
            #Send data to Receiving records, return back list of dicts; which are extended with updates
            swth_busd.extend(ReceivingRecords.swth_busd_book(records))
            #Clean the records
            CleaningRecords.cleaning_orderbooks(swth_busd)
            #Send to function for saving file
            SavingRecords.save_swth_busd_orderbook(swth_busd)
        #Check if swth_eth books are in the "channel"
        if 'books.swth_eth1' in records['channel']:
            #Send data to Receiving records, return back list of dicts; which are extended with updates
            swth_eth.extend(ReceivingRecords.swth_eth_book(records))
            #Clean the records
            CleaningRecords.cleaning_orderbooks(swth_eth)
            #Send to function for saving file
            SavingRecords.save_swth_eth_orderbook(swth_eth)
        #Check if swth_eth books are in the "channel"
        if 'books.eth1_usdc1' in records['channel']:
            #Send data to Receiving records, return back list of dicts; which are extended with updates
            eth_usdc.extend(ReceivingRecords.eth_usdc_book(records))
            #Clean the records
            CleaningRecords.cleaning_orderbooks(eth_usdc)
            #Send to function for saving file
            SavingRecords.save_eth_usdc_orderbook(eth_usdc)
        #Check if swth_eth books are in the "channel"
        if 'books.cel_eth' in records['channel']:
            #Send data to Receiving records, return back list of dicts; which are extended with updates
            cel_eth.extend(ReceivingRecords.cel_eth_book(records))
            #Clean the records
            CleaningRecords.cleaning_orderbooks(cel_eth)
            #Send to function for saving file
            SavingRecords.save_cel_eth_orderbook(cel_eth)
        #Check if swth_eth books are in the "channel"
        if 'books.cel1_usdc1' in records['channel']:
            #Send data to Receiving records, return back list of dicts; which are extended with updates
            cel_usdc.extend(ReceivingRecords.cel_usdc_book(records))
            #Clean the records
            CleaningRecords.cleaning_orderbooks(cel_usdc)
            #Send to function for saving file
            SavingRecords.save_cel_usdc_orderbook(cel_usdc)
        #Check if eth_wbtc books are in the "channel"
        if 'books.eth1_wbtc1' in records['channel']:
            #Send data to Receiving records, return back list of dicts; which are extended with updates
            eth_wbtc.extend(ReceivingRecords.eth_wbtc_book(records))
            #Clean the records
            CleaningRecords.cleaning_orderbooks(eth_wbtc)
            #Send to function for saving file
            SavingRecords.save_eth_wbtc_orderbook(eth_wbtc)
        #Check if wbtc_usdc books are in the "channel"
        if 'books.wbtc1_usdc1' in records['channel']:
            #Send data to Receiving records, return back list of dicts; which are extended with updates
            wbtc_usdc.extend(ReceivingRecords.wbtc_usdc_book(records))
            #Clean the records
            CleaningRecords.cleaning_orderbooks(wbtc_usdc)
            #Send to function for saving file
            SavingRecords.save_wbtc_usdc_orderbook(wbtc_usdc)

        #Fifteen Minute Candles
        #Check if wbtc_usdc books are in the "channel"
        if 'candlesticks.swth_usdc1' in records['channel']:
            #Send data to Receiving records, return back list of dicts; which are extended with updates
            """wbtc_usdc_15_minute.extend(ReceivingRecords.wbtc_usdc_book(records))
            #Clean the records
            CleaningRecords.cleaning_orderbooks(wbtc_usdc)
            #Send to function for saving file
            SavingRecords.save_wbtc_usdc_orderbook(wbtc_usdc)"""
            print("WBTC Candlestick was received!!!!!!!!!!!!!!!!!!!!")

async def bot_task():
    while True:
        Treway.TrewayBot().main()
        print("No trades to perform. Sleeping for two minutes.")
        await asyncio.sleep(120)

async def main():

    #Create Websocket asyncio task
    socket = asyncio.create_task(demex.connect(on_receive, on_connect))

    #Create Treway Bot task via bot_task function
    bot = asyncio.create_task(bot_task())

    #Gather and run functions concurrently
    asyncio.gather(
                    asyncio.get_event_loop().run_until_complete(await socket),
                    asyncio.get_event_loop().run_until_complete(await bot)
                    )


if __name__ == '__main__':
    demex: DemexWebsocket = DemexWebsocket('wss://ws.dem.exchange/ws')
    asyncio.run(main())
