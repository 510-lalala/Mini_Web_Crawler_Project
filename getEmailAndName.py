import requests
from bs4 import BeautifulSoup
import re
import csv
import time

def scrape_all_pages():
    base_url = "https://www.csie.ncku.edu.tw/zh-hant/members/csie"
    output_file = "ncku_csie_all_professors.csv"
    data_list = []
    
    
   
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(base_url, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
        
    faculty_cards = soup.find_all('div', class_='card-body')
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

    for card in faculty_cards:
        name_ch = card.find('h3').get_text(strip=True) if card.find('h3') else "未知"
        name_en = card.find('h4').get_text(strip=True) if card.find('h4') else "Unknown"
            
        email = "無"
        p_tags = card.find_all('p', class_='card-text')
        for p in p_tags:
            raw_text = p.get_text()
            clean_text = raw_text.replace('nbsp', '').strip()
            found = re.findall(email_pattern, clean_text)
            if found:
                email = found[0]
                break
            
        data_list.append([name_ch, name_en, email])
        
    time.sleep(1) # 休息一秒，當個有禮貌的爬蟲

    # 儲存
    with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['中文姓名', '英文姓名', 'Email'])
        writer.writerows(data_list)
    print(f"✅ 全系資料抓取完畢！存檔為 {output_file}")

if __name__ == "__main__":
    scrape_all_pages()