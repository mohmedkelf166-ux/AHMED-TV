import requests
from bs4 import BeautifulSoup
import os

def get_30_movies():
    # رابط قسم الأفلام الأجنبية
    url = "https://cimanow.cc/category/movies/foreign-movies/" 
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        movies = []
        
        # جلب جميع العناصر المتاحة في الصفحة
        items = soup.find_all('div', class_='MovieBlock')
        
        # تحديد العدد المطلوب (30 فيلماً)
        for item in items[:30]: 
            try:
                name = item.find('h3').text.strip()
                link = item.find('a')['href']
                img_tag = item.find('img')
                img = img_tag.get('data-src') or img_tag.get('src')
                
                # إنشاء اسم ملف فريد للصفحة
                file_name = "".join(x for x in name if x.isalnum())[:30] + ".html"
                
                movies.append({
                    'name': name,
                    'link': link,
                    'img': img,
                    'file_name': file_name
                })
            except:
                continue
        return movies
    except:
        return []

def run_update():
    movies = get_30_movies()
    if not movies:
        print("📭 لم يتم العثور على أفلام.")
        return

    html_file = "Movies.html"
    with open(html_file, "r", encoding="utf-8") as f:
        content = f.read()

    marker = '<div class="grid" id="grid">'
    added_count = 0

    # التكرار على الأفلام المجلوبة (30 فيلماً)
    for movie in reversed(movies):
        # التحقق إذا كان الفيلم موجوداً بالفعل لتجنب التكرار
        if movie['name'] not in content:
            # 1. إنشاء صفحة المشغل Full Screen
            create_player_page(movie)
            
            # 2. إضافة الكارت لصفحة المعرض
            new_card = f"""
            <a href="{movie['file_name']}" class="card">
                <img src="{movie['img']}" class="card-img">
                <div class="card-info">
                    <span class="card-title">{movie['name']}</span>
                    <span class="card-year">2026</span>
                </div>
            </a>"""
            
            content = content.replace(marker, marker + new_card)
            added_count += 1
            print(f"✅ مضاف: {movie['name']}")

    if added_count > 0:
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"🔥 مجموع ما تم إضافته الآن: {added_count} فيلماً.")
    else:
        print("😴 لا توجد أفلام جديدة في الموقع حالياً.")

def create_player_page(movie):
    template = "player_template.html"
    if os.path.exists(template):
        with open(template, "r", encoding="utf-8") as f:
            p_code = f.read()
        # وضع رابط الفيلم داخل المشغل الخاص بك
        p_code = p_code.replace("MOVIE_URL_HERE", movie['link'])
        with open(movie['file_name'], "w", encoding="utf-8") as f:
            f.write(p_code)

if __name__ == "__main__":
    run_update()
