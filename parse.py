from bs4 import BeautifulSoup
import requests
import pandas as pd
import os


URL = 'https://tt.sport-liga.pro/tours/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.86 YaBrowser/20.8.0.903 Yowser/2.5 Yptp/1.23 Safari/537.36', 
    'accept': '*/*'}
date, title, number, winner, ref = [], [], [], [], []

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html, newURL, col = 1):
    print(col, '\n', newURL, '\n')
    soup = BeautifulSoup(html, 'html.parser')
    spisok = soup.find("table", class_='table')

    items = spisok.find_all('tr')[1:]

    for item in items:
        item = item.find_all('td')
        date.append(item[0].text)
        title.append(item[1].text)
        number.append(item[2].a.text)
        l = 'None'
        if item[3].a:
            l = item[3].a.text
        winner.append(l)
        ref.append(URL.replace('/tours/', '/') + item[1].a.get('href'))


    if soup.find('a', class_='icon-arw-n'):
        newURL = newURL.replace('page={}'.format(str(col)), 'page=') + str(col + 1)
        html = get_html(newURL)
        get_content(html.text, newURL, col + 1)

    if col == 1:
        gd = {"Дата проведения": date, "Название турнира": title, "Количество участников": number, "Победитель": winner, 'Ссылка': ref}
        df = pd.DataFrame(gd)
        return (df.set_index("Дата проведения"))
        




def parse(year, month):
    if month < 10:
        month = '0' + str(month)
    else:
        month = str(month)

    newURL = URL + "?year={}&month={}&page=1".format(str(year), month)
    html = get_html(newURL)
    if html.status_code == 200:
        return get_content(html.text, newURL)
        
    else:
        print("Wrong format")




def main():
    year1, month1 = list(map(int, input("Введите начальный год, а потом месяц:\n").split(" ")))
    year2, month2 = list(map(int, input("Введите конечный год, а потом месяц:\n").split(" ")))
    print("Идёт парсинг...")
    while (year1 != year2 or month1 != month2):
        data = parse(year1, month1)
        data.to_excel('info.xlsx')
        month1 += 1
        if (month1 == 13):
            month1 = 0
            year1 += 1
    data = parse(year1, month1)
    data.to_excel('info.xlsx')
    print("Готово! Наслаждайтесь этой информацией!")

if __name__ == "__main__":
    try:
        os.remove('info.xlsx')
    except FileNotFoundError:
        pass
    main()