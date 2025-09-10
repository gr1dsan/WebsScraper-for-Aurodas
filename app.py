from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import csv
import time
import random

url = 'https://en.aruodas.lt/butu-nuoma/kaune/'

def scrape(page, url):
        page.goto(url, wait_until="networkidle")
        html = page.content()
        return html

def get_links(html):
    soup = BeautifulSoup(html, 'html.parser')

    links = []
    link_div=soup.find_all("div", class_=["list-row-v2", "object-row"])

    for div in link_div:
        ldiv = div.find('div', class_='list-adress-v2')
        if ldiv:
            h3_tags = ldiv.find_all('h3')
            for h3 in h3_tags:
                a_tags = h3.find_all('a')
                for a in a_tags:
                    links.append(a.get('href'))
    return links

def get_data(page, links):
    propertie={'names':[], 
               'total_price':[],
               'price_per_meter':[],
               'area':[],
               'rooms_number': [],
               'build_year': [],
               'building_type': [],
               'equipment': [],
               'heating_system': [],
               'avg_heating_price':[],
               'crimes': []
                   }
    
    fields = {
               'area': 'Area:',
               'rooms_number': 'Number of rooms :',
               'build_year': 'Build year:',
               'building_type': 'Building type:',
               'equipment': 'Equipment:',
               'heating_system': 'Heating system:',
            }
    
    for link in links:
        page.goto(link, wait_until="networkidle", timeout=0)
        html = page.content()

        soup = BeautifulSoup(html, 'html.parser')
        if not page.is_closed():
            for _ in range(5):  # repeat a few times
                x = random.randint(100, 800)
                y = random.randint(100, 600)
                page.mouse.move(x, y)  # move mouse to random spot
    
                page.keyboard.press("PageDown")  # scroll down
                time.sleep(random.uniform(1, 3))

        name = soup.find('h1', class_='obj-header-text')
        if name:
           propertie['names'].append(name.text.strip())
        else:
            propertie['names'].append(None) 

        div_price=soup.find('div', class_='price-left')
        if div_price:
            span = div_price.find('span', class_='price-eur')
            span2 = div_price.find('span', class_='price-per')
            propertie['total_price'].append(span.get_text(strip=True) if span else None)
            propertie['price_per_meter'].append(span2.get_text(strip=True) if span2 else None)
        else:
            propertie['total_price'].append(None)
            propertie['price_per_meter'].append(None)
        
        for key, label in fields.items():
            prs = soup.find('dt', string=lambda s: s and s.strip() == label)
            if prs:
               dd = prs.find_next_sibling('dd')
               if dd:
                  value = dd.find('span', class_='fieldValueContainer')
                  propertie[key].append(value.get_text(strip=True) if value else None)
               else:
                  propertie[key].append(None)
            else:
              propertie[key].append(None)

        heating_div=soup.find('div', class_=['arrow_line_left', 'flexBlock'])
        if heating_div:
            heating_span = heating_div.find('span', class_='cell-data cell-data-inline-block')
            if heating_span:
               propertie['avg_heating_price'].append(heating_span.get_text(strip=True))
            else:
               propertie['avg_heating_price'].append(None)
        else:
            propertie['avg_heating_price'].append(None)

        
        c =[]
        crimes_div = soup.find_all('div', attrs={'aria-label': 'A tabular representation of the data in the chart.'})
        for div in crimes_div:
            table = div.find('table')
            if table:
                tbody=table.find('tbody')
                if tbody:
                    trs = tbody.find_all('tr')
                    if trs:
                        for tr in trs:
                            td_f=tr.find_all('td')
                            for td in td_f:
                                c.append(td.get_text(strip=True))

        propertie['crimes'].append(c)
        
        time.sleep(random.uniform(5, 10))
        print(f'{link} was scanned')
    return propertie 

def save_csv(propertie, filename='anything.csv'):
    fieldnames= propertie.keys()
    rows = zip(*propertie.values())

    with open(filename, newline='', mode='w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(fieldnames) 
        writer.writerows(rows) 


with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/118.0.5993.90 Safari/537.36"
        )

        numbers=list(range(1, 33))
        random.shuffle(numbers)
        numik=1

        all_data = {
         'names': [], 'total_price': [], 'price_per_meter': [], 'area': [],
          'rooms_number': [], 'build_year': [], 'building_type': [], 'equipment': [],
         'heating_system': [], 'avg_heating_price': [], 'crimes': []
         }
        
        for n in numbers:
            print(f'Page {numik}/33')
            print(f'Page number {n} being scanned')
            if n == 1:
                url='https://en.aruodas.lt/butu-nuoma/kaune/'
            else:
                url=f'https://en.aruodas.lt/butu-nuoma/kaune/puslapis/{n}/'
            page = context.new_page()

            html=scrape(page, url)
            links = get_links(html)
            data = get_data(page, links)

            for key in all_data:
                all_data[key].extend(data[key])

            numik+=1
            print(f'Page number{n} was scanned')
            
            print('Waiting')
            time.sleep(random.uniform(1, 2)*60)
        
        print('Scapare finisned!')
        file = save_csv(all_data, filename='anything.csv')

        browser.close()