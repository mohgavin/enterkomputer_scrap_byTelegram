#!/home/nivag/.WebScrapping/bin/python

from initialization import loading_website, regex1, regex2, table_process1, table_process2
from telethon import TelegramClient

# Remember to use your own values from my.telegram.org!
api_id = #Di isi dengan API ID sendiri
api_hash = #Di isi dnegan API ID sendiri
client = TelegramClient('/home/nivag/enterkomputer_scrap/nivagad', api_id, api_hash)

async def main():

    print("Loading Website......")
    element1 = loading_website("https://www.enterkomputer.com/turun-harga/")

    print("Regex Processing.....")
    list1 = regex2(element1)

    print("Table Processing.....")
    table_process2(list1, '/home/nivag/enterkomputer_scrap/mytable2.png', '/home/nivag/enterkomputer_scrap/result2.csv')

    me = await client.get_me()
    
    await client.send_file('+621927836', '/home/nivag/enterkomputer_scrap/mytable2.png') #Di isi dengan no Handphone yang ingin dikirmkan

if __name__ == "__main__":

    with client:
        client.loop.run_until_complete(main())  

else:
    pass
