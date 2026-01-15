import requests
from bs4 import BeautifulSoup
import os

def get_latest_foreign_movies():
    # الرابط المباشر لقسم الأفلام الأجنبية (تأكد من تحديث الرابط إذا تغير الدومين)
    url = "https://cimanow.cc/category/movies/foreign-movies/" 
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        movies = []
        # البحث عن كتل الأفلام (هذا الكلاس MovieBlock هو المعتاد في هذه القوالب)
        items = soup.find_all('div', class_='MovieBlock') 
        
        for item in items[:15]: # فحص آخر 15 عنصر لضمان إيجاد أفلام جديدة
            try:
                name = item.find('h3').text.strip()
                link = item.find('a')['href']
                img_tag = item.find('img')
                # محاولة سحب الصورة من data-src (لأن أغلب المواقع تستخدم Lazy Load) أو src العادي
                img = img_tag.get('data-src') or img_tag.get('src')
                
                # إضافة الفيلم فقط إذا لم يكن موجوداً في القائمة (بناءً على الاسم)
                movies.append({
                    'name': name,
                    'link': link,
                    'img': img,
                    'year': "2025" # يمكنك تعديله ليسحب السنة من الاسم بـ Regex إذا أردت
                })
            except Exception as e:
                print(f"خطأ في سحب عنصر: {e}")
                continue
        return movies
    except Exception as e:
        print(f"حدث خطأ أثناء الاتصال بالموقع: {e}")
        return []

def update_html(movies):
    file_path = "Movies.html" # تأكد أن هذا اسم ملف الأفلام في الـ GitHub عندك
    
    if not os.path.exists(file_path):
        print(f"❌ الملف {file_path} غير موجود!")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # العلامة التي سيتم إضافة الأفلام تحتها (تأكد أنها موجودة في ملف HTML الخاص بك)
    marker = '<div class="grid" id="grid">'
    
    if marker not in content:
        print("❌ لم يتم العثور على منطقة الإضافة (grid) في ملف HTML!")
        return

    added_count = 0
    for movie in reversed(movies): # الترتيب من الأقدم للأحدث ليظهر الأحدث في الأعلى بعد الاستبدال
        # التأكد أن الفيلم ليس مضافاً مسبقاً (من خلال الاسم أو الرابط)
        if movie['name'] not in content and movie['link'] not in content:
            new_card = f"""
            <a href="{movie['link']}" class="card">
                <img src="{movie['img']}" class="card-img">
                <div class="card-info">
                    <span class="card-title">{movie['name']}</span>
                    <span class="card-year">{movie['year']}</span>
                </div>
            </a>"""
            # إضافة الفيلم الجديد مباشرة بعد علامة البداية للـ grid
            content = content.replace(marker, marker + new_card)
            print(f"✅ تم إضافة فيلم أجنبي جديد: {movie['name']}")
            added_count += 1

    if added_count > 0:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"🚀 تم تحديث الموقع بـ {added_count} أفلام جديدة.")
    else:
        print("😴 لا توجد أفلام أجنبية جديدة لإضافتها.")

if __name__ == "__main__":
    foreign_movies = get_latest_foreign_movies()
    if foreign_movies:
        update_html(foreign_movies)

