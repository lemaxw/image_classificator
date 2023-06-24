import os
from aiogram import Bot, types
from image_manipulation import resize_image
from io import BytesIO
from aiogram.utils.exceptions import CantParseEntities

token=os.getenv('ADMIN_TELEGRAM_TOKEN') 
channel_id = os.getenv('TELEGRAM_CHANNEL_ID')
print (f'token={token}, channel_id={channel_id}')

bot = Bot(token=token)

async def send_telegram_message(poet,poem,location,photo_path_or_url,url):    

    img = resize_image(photo_path_or_url, 10000)
    photo_data = BytesIO()
    img.save(photo_data, format='JPEG')
    photo_data.seek(0)
    found_caption=False
    while(found_caption == False):
        caption = f'<i>{poem}</i>\n\n'  # Add line break for the next line
        caption += f'<a href="{url}">{poet}</a>\n\n'
        caption += location
        if(len(caption) > 1076):
            poem = poem[:(int(len(poem)/2))] + "\n..."
        else:
            found_caption=True
    
    try:
        await bot.send_photo(chat_id=channel_id, photo=photo_data, caption=caption, parse_mode=types.ParseMode.HTML)
    except CantParseEntities as e:
        print(f"Error while sending message: {str(e)}")
    
    await bot.close()


