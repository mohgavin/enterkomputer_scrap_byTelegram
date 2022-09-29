#!/home/nivag/.WebScrapping/bin/python

from initialization import loading_website, regex1, regex2, table_process1
from telethon import TelegramClient

# Remember to use your own values from my.telegram.org!
api_id = 8712378 #Disi dengan API ID Sendiri
api_hash = 'sdlfiuhsoy789123' #Diisi dengan APi Hash Bot Sendiri
client = TelegramClient('/home/nivag/enterkomputer_scrap/nivagad', api_id, api_hash)

async def main():

    print("Loading Website......")
    element1 = loading_website("https://www.enterkomputer.com/category/24/vga")

    print("Regex Processing.....")
    list1 = regex1(element1)

    print("Table Processing.....")
    table_process1(list1, '/home/nivag/enterkomputer_scrap/mytable1.png', '/home/nivag/enterkomputer_scrap/result1.csv')

    me = await client.get_me()
    
    await client.send_file('No. Handphone', '/home/nivag/enterkomputer_scrap/mytable.png') # Di isi dengan no. handpphone yang dikirimkan
    
if __name__ == "__main__":

    with client:
        client.loop.run_until_complete(main())  

else:
    pass
