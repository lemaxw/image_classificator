import requests
import os
import asyncio
from google_translator import translate_word

cx=os.getenv('GOOGLE_CUSTOM_SEARCH_CX') 
api_key=os.getenv('GOOGLE_CUSTOM_SEARCH_API_KEY') 
print (f'cx={cx}, api_key={api_key}')



def search_bing(query, num_results):
    subscription_key = os.getenv('BING_SEARCH_V7_SUBSCRIPTION_KEY') 
    endpoint = "https://api.bing.microsoft.com/v7.0/search"
    query = f"{query} site:poemata.ru"

    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    params  = {"q": query, "textDecorations": True, "textFormat": "HTML"}

    response = requests.get(endpoint, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()

    urls = [item['url'] for item in search_results['webPages']['value']]
    
    for url in urls:
                print(url)

    return urls[:num_results]

def search_google(query):
    endpoint = "https://www.googleapis.com/customsearch/v1"
    params  = {"key": api_key, "cx": cx, "q": query}

    response = requests.get(endpoint, params=params)
    response.raise_for_status()
    search_results = response.json()
    urls = []
    if 'items' in search_results.keys() :
        urls = [item['link'] for item in search_results['items']]    
    return urls

good_poets = ["белый", "Маяковский", "Хаям", "Бродский", "Рубцов", "Бальмонт", "Брюсов", "Тряпкин", "Визбор", "Высоцкий", 
    "Асадов", "Полозкова", "Рубальская", "Турбина", "Ахмадулина", "державин", "иванов", "сапгир"
    "Вертинский", "Сологуб", "Бенедиктов", "Цветаева", "Уткин", "Блок", "Тютчев", "Бунин", "Эренбург", "Есенин",
    "Мандельштам", "Васильев", "Евтушенко", "Волошин", "Касьян", "Солоухин", "Фет", "Никитин", "Пушкин", "Шефнер", 
    "Лермонтов", "Северянин", "Карамзин", "Гарипов", "Сюоси", "Рюрик", "Хармс", "Надсон", "Мережковский", "Шаламов", 
    "Гамзатов", "Орлов", "Клычков", "Ивнев", "Гумилев", "Тарковский", "Берестов", "Жуковский", "Британишский", "Вяземский"]

def poet_is_good_one(poet):
    poet_lower = poet.lower()
    for good_poet in good_poets:
        if good_poet.lower() in poet_lower:
            return True
    print(poet_lower)
    return False


if __name__ == '__main__':
    import sys
    from get_tags import get_tags 
    from extract_poem import extract_info
    from telegram_msg import send_telegram_message

    if len(sys.argv) != 3:
        print(f'Usage: python {sys.argv[0]} <file_path> <location>', file=sys.stderr)
        sys.exit(1)

    translated = translate_word(sys.argv[2])
    if(len(translated) > 0):
        location = translated
    else:
        location = sys.argv[2]

    image_location = sys.argv[1]
    tags = get_tags(image_location)
     
    for tag in tags:
        urls = search_google(tag)
        print(f"====={tag}======")
        count=0
        for url in urls:
            if 'poets' in url:
                poet_name, poem = extract_info(url)        
                if poet_name and poem and poet_is_good_one(poet_name[0]):
                    print(url)
                    count = count + 1
                    asyncio.run(send_telegram_message(poet_name[0], poem[0], location, image_location,url))
                    if count > 5: 
                        break

