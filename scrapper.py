import requests
from bs4 import BeautifulSoup
import os

def get_latest_foreign_movies():
    url = "https://cimanow.cc/category/movies/foreign-movies/" 
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    movies = []
    items = soup.find_all('div', class_='MovieBlock')
    
    for item in items[:10]:
        try:
            name = item.find('h3').text.strip()
            link = item.find('a')['href']
            img = item.find('img').get('data-src') or item.find('img').get('src')
            # تحويل الاسم لاسم ملف صالح (بدون مسافات)
            file_name = "".join(x for x in name if x.isalnum())[:20] + ".html"
            movies.append({'name': name, 'link': link, 'img': img, 'file_name': file_name})
        except: continue
    return movies

def create_player_page(movie):
    # قراءة القالب وتغيير الرابط
    template_path = "player_template.html"
    if os.path.exists(template_path):
        with open(template_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # استبدال الرابط (هنا نضع رابط الفيلم من سيما ناو)
        new_content = content.replace("MOVIE_URL_HERE", movie['link'])
        
        with open(movie['file_name'], "w", encoding="utf-8") as f:
            f.write(new_content)

def update_html(movies):
    file_path = "Movies.html"
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    marker = '<div class="grid" id="grid">'
    for movie in reversed(movies):
        if movie['name'] not in content:
            # إنشاء صفحة المشغل للفيلم أولاً
            create_player_page(movie)
            
            # إضافة الكارت الذي يوجه لصفحة المشغل الجديدة
            new_card = f"""
            <a href="{movie['file_name']}" class="card">
                <img src="{movie['img']}" class="card-img">
                <div class="card-info">
                    <span class="card-title">{movie['name']}</span>
                    <span class="card-year">2025</span>
                </div>
            </a>"""
            content = content.replace(marker, marker + new_card)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    movies = get_latest_foreign_movies()
    update_html(movies)
