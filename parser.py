import requests
from bs4 import BeautifulSoup


def parser(days_count):
    """Парсим обновления с сайта с учетом количества дней.
    
    Keyword arguments:
    days_count -- Количество дней за которые надо получить обновления
    Return: список с названием и ссылкой на запись
    """
    
    
    new_recodrs = []
    request_url = f'https://www.applegamingwiki.com/wiki/Special:RecentChangesLinked?hidebots=1&target=Home&limit=50&days={days_count}&enhanced=1&urlversion=2'
    r = requests.get(request_url)
    soup = BeautifulSoup(r.text, 'lxml')
    records = soup.find_all('span', class_='mw-title')
    for record in records:
        record_title = record.text
        record_url = 'https://www.applegamingwiki.com' + record.find('a').get('href')
        new_recodrs.append({'record_title':record_title,
                            'record_url':record_url
                            })
        
    return new_recodrs