#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
from datetime import datetime
import os
import time
import sys

class MovieBot:
    def __init__(self, github_token, repo_name, tmdb_access_token):
        self.github_token = github_token
        self.repo_name = repo_name  # مثال: "username/repo"
        self.tmdb_access_token = tmdb_access_token  # Bearer Token من TMDB
        self.base_url = "https://api.themoviedb.org/3"
        self.headers = {
            'Authorization': f'Bearer {tmdb_access_token}',
            'accept': 'application/json'
        }
        
    def get_existing_movies(self):
        """جلب قائمة الأفلام الموجودة في المستودع"""
        url = f"https://api.github.com/repos/{self.repo_name}/contents/movies.json"
        headers = {"Authorization": f"token {self.github_token}"}
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                content = response.json()
                import base64
                decoded = base64.b64decode(content['content']).decode('utf-8')
                return json.loads(decoded)
            else:
                return {"movies": [], "series": []}
        except Exception as e:
            print(f"خطأ في جلب الأفلام الموجودة: {e}")
            return {"movies": [], "series": []}
    
    def search_movie(self, query):
        """البحث عن فيلم معين"""
        url = f"{self.base_url}/search/movie"
        params = {
            'query': query,
            'language': 'ar',
            'include_adult': 'false'
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            if response.status_code == 200:
                return response.json()['results']
            return []
        except Exception as e:
            print(f"خطأ في البحث عن {query}: {e}")
            return []
    
    def get_popular_movies(self, page=1):
        """جلب الأفلام الشائعة"""
        url = f"{self.base_url}/movie/popular"
        params = {
            'language': 'ar',
            'page': page
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            if response.status_code == 200:
                return response.json()['results']
            return []
        except Exception as e:
            print(f"خطأ في جلب الأفلام الشائعة: {e}")
            return []
    
    def get_trending_movies(self, time_window='week'):
        """جلب الأفلام الرائجة (يومياً أو أسبوعياً)"""
        url = f"{self.base_url}/trending/movie/{time_window}"
        params = {'language': 'ar'}
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            if response.status_code == 200:
                return response.json()['results']
            return []
        except Exception as e:
            print(f"خطأ في جلب الأفلام الرائجة: {e}")
            return []
    
    def get_now_playing(self):
        """جلب الأفلام المعروضة حالياً في السينما"""
        url = f"{self.base_url}/movie/now_playing"
        params = {'language': 'ar'}
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            if response.status_code == 200:
                return response.json()['results']
            return []
        except Exception as e:
            print(f"خطأ في جلب الأفلام المعروضة: {e}")
            return []
    
    def get_upcoming_movies(self):
        """جلب الأفلام القادمة"""
        url = f"{self.base_url}/movie/upcoming"
        params = {'language': 'ar'}
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            if response.status_code == 200:
                return response.json()['results']
            return []
        except Exception as e:
            print(f"خطأ في جلب الأفلام القادمة: {e}")
            return []
    
    def get_popular_series(self, page=1):
        """جلب المسلسلات الشائعة"""
        url = f"{self.base_url}/tv/popular"
        params = {
            'language': 'ar',
            'page': page
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            if response.status_code == 200:
                return response.json()['results']
            return []
        except Exception as e:
            print(f"خطأ في جلب المسلسلات الشائعة: {e}")
            return []
    
    def get_trending_series(self):
        """جلب المسلسلات الرائجة"""
        url = f"{self.base_url}/trending/tv/week"
        params = {'language': 'ar'}
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            if response.status_code == 200:
                return response.json()['results']
            return []
        except Exception as e:
            print(f"خطأ في جلب المسلسلات الرائجة: {e}")
            return []
    
    def discover_arabic_content(self):
        """اكتشاف المحتوى العربي"""
        url = f"{self.base_url}/discover/movie"
        params = {
            'language': 'ar',
            'with_original_language': 'ar',
            'sort_by': 'popularity.desc',
            'vote_count.gte': 10
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            if response.status_code == 200:
                return response.json()['results']
            return []
        except Exception as e:
            print(f"خطأ في اكتشاف المحتوى العربي: {e}")
            return []
    
    def get_movie_details(self, movie_id):
        """جلب تفاصيل فيلم معين"""
        url = f"{self.base_url}/movie/{movie_id}"
        params = {'language': 'ar'}
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"خطأ في جلب تفاصيل الفيلم {movie_id}: {e}")
            return None
    
    def format_movie_data(self, movie):
        """تنسيق بيانات الفيلم"""
        return {
            'id': movie.get('id'),
            'title': movie.get('title', 'بدون عنوان'),
            'original_title': movie.get('original_title', ''),
            'release_date': movie.get('release_date', ''),
            'rating': round(movie.get('vote_average', 0), 1),
            'vote_count': movie.get('vote_count', 0),
            'popularity': round(movie.get('popularity', 0), 1),
            'poster': f"https://image.tmdb.org/t/p/w500{movie.get('poster_path', '')}" if movie.get('poster_path') else '',
            'backdrop': f"https://image.tmdb.org/t/p/original{movie.get('backdrop_path', '')}" if movie.get('backdrop_path') else '',
            'overview': movie.get('overview', 'لا يوجد وصف'),
            'genre_ids': movie.get('genre_ids', []),
            'original_language': movie.get('original_language', '')
        }
    
    def format_series_data(self, series):
        """تنسيق بيانات المسلسل"""
        return {
            'id': series.get('id'),
            'title': series.get('name', 'بدون عنوان'),
            'original_title': series.get('original_name', ''),
            'first_air_date': series.get('first_air_date', ''),
            'rating': round(series.get('vote_average', 0), 1),
            'vote_count': series.get('vote_count', 0),
            'popularity': round(series.get('popularity', 0), 1),
            'poster': f"https://image.tmdb.org/t/p/w500{series.get('poster_path', '')}" if series.get('poster_path') else '',
            'backdrop': f"https://image.tmdb.org/t/p/original{series.get('backdrop_path', '')}" if series.get('backdrop_path') else '',
            'overview': series.get('overview', 'لا يوجد وصف'),
            'genre_ids': series.get('genre_ids', []),
            'original_language': series.get('original_language', '')
        }
    
    def find_new_content(self):
        """العثور على المحتوى الجديد غير الموجود في المستودع"""
        print("📥 جلب المحتوى الموجود في المستودع...")
        existing = self.get_existing_movies()
        existing_ids = set(m['id'] for m in existing.get('movies', []))
        existing_series_ids = set(s['id'] for s in existing.get('series', []))
        
        new_movies = []
        new_series = []
        
        # 1. الأفلام الشائعة
        print("🔥 جلب الأفلام الشائعة...")
        for page in range(1, 4):
            movies = self.get_popular_movies(page)
            for movie in movies:
                if movie['id'] not in existing_ids:
                    new_movies.append(self.format_movie_data(movie))
            time.sleep(0.3)  # تجنب Rate Limiting
        
        # 2. الأفلام الرائجة
        print("📈 جلب الأفلام الرائجة...")
        trending = self.get_trending_movies()
        for movie in trending:
            if movie['id'] not in existing_ids:
                new_movies.append(self.format_movie_data(movie))
        time.sleep(0.3)
        
        # 3. الأفلام المعروضة حالياً
        print("🎬 جلب الأفلام المعروضة في السينما...")
        now_playing = self.get_now_playing()
        for movie in now_playing:
            if movie['id'] not in existing_ids:
                new_movies.append(self.format_movie_data(movie))
        time.sleep(0.3)
        
        # 4. الأفلام القادمة
        print("🔜 جلب الأفلام القادمة...")
        upcoming = self.get_upcoming_movies()
        for movie in upcoming:
            if movie['id'] not in existing_ids:
                new_movies.append(self.format_movie_data(movie))
        time.sleep(0.3)
        
        # 5. المحتوى العربي
        print("🇦🇪 جلب المحتوى العربي...")
        arabic_movies = self.discover_arabic_content()
        for movie in arabic_movies:
            if movie['id'] not in existing_ids:
                new_movies.append(self.format_movie_data(movie))
        time.sleep(0.3)
        
        # 6. المسلسلات الشائعة
        print("📺 جلب المسلسلات الشائعة...")
        for page in range(1, 3):
            series = self.get_popular_series(page)
            for show in series:
                if show['id'] not in existing_series_ids:
                    new_series.append(self.format_series_data(show))
            time.sleep(0.3)
        
        # 7. المسلسلات الرائجة
        print("🔥 جلب المسلسلات الرائجة...")
        trending_series = self.get_trending_series()
        for show in trending_series:
            if show['id'] not in existing_series_ids:
                new_series.append(self.format_series_data(show))
        
        # إزالة التكرارات
        new_movies = list({m['id']: m for m in new_movies}.values())
        new_series = list({s['id']: s for s in new_series}.values())
        
        # ترتيب حسب الشعبية
        new_movies.sort(key=lambda x: x['popularity'], reverse=True)
        new_series.sort(key=lambda x: x['popularity'], reverse=True)
        
        return {
            'new_movies': new_movies,
            'new_series': new_series,
            'total_movies': len(new_movies),
            'total_series': len(new_series),
            'total_count': len(new_movies) + len(new_series),
            'timestamp': datetime.now().isoformat(),
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def save_to_github(self, new_content, filename='new_content.json'):
        """حفظ المحتوى الجديد إلى GitHub"""
        url = f"https://api.github.com/repos/{self.repo_name}/contents/{filename}"
        headers = {
            "Authorization": f"token {self.github_token}",
            "Content-Type": "application/json"
        }
        
        try:
            import base64
            content_str = json.dumps(new_content, ensure_ascii=False, indent=2)
            content_bytes = content_str.encode('utf-8')
            content_base64 = base64.b64encode(content_bytes).decode('utf-8')
            
            # التحقق من وجود الملف
            check_response = requests.get(url, headers=headers)
            sha = None
            if check_response.status_code == 200:
                sha = check_response.json()['sha']
            
            data = {
                "message": f"🎬 تحديث: {new_content['total_count']} محتوى جديد - {new_content['date']}",
                "content": content_base64
            }
            
            if sha:
                data["sha"] = sha
            
            response = requests.put(url, headers=headers, json=data)
            return response.status_code in [200, 201]
        except Exception as e:
            print(f"❌ خطأ في حفظ الملف: {e}")
            return False
    
    def generate_report(self, new_content):
        """إنشاء تقرير مفصل بالمحتوى الجديد"""
        report = f"""
╔════════════════════════════════════════════════════════════╗
║          🎬 تقرير المحتوى الجديد                         ║
╚════════════════════════════════════════════════════════════╝

📅 التاريخ: {new_content['date']}
📊 إجمالي المحتوى الجديد: {new_content['total_count']}
   • أفلام: {new_content['total_movies']}
   • مسلسلات: {new_content['total_series']}

{'═' * 60}

🎥 أفضل 10 أفلام جديدة:
"""
        for i, movie in enumerate(new_content['new_movies'][:10], 1):
            report += f"\n{i}. {movie['title']}"
            if movie['original_title'] != movie['title']:
                report += f" ({movie['original_title']})"
            report += f"\n   ⭐ التقييم: {movie['rating']}/10 ({movie['vote_count']} صوت)"
            report += f"\n   📅 تاريخ الإصدار: {movie['release_date']}"
            report += f"\n   🔥 الشعبية: {movie['popularity']}"
            report += f"\n"
        
        report += f"\n{'═' * 60}\n"
        report += f"\n📺 أفضل 10 مسلسلات جديدة:\n"
        
        for i, series in enumerate(new_content['new_series'][:10], 1):
            report += f"\n{i}. {series['title']}"
            if series['original_title'] != series['title']:
                report += f" ({series['original_title']})"
            report += f"\n   ⭐ التقييم: {series['rating']}/10 ({series['vote_count']} صوت)"
            report += f"\n   📅 تاريخ البث: {series['first_air_date']}"
            report += f"\n   🔥 الشعبية: {series['popularity']}"
            report += f"\n"
        
        report += f"\n{'═' * 60}\n"
        report += f"\n✅ تم حفظ المحتوى في: new_content.json"
        
        return report


# استخدام البوت
if __name__ == "__main__":
    try:
        # إعدادات المستخدم
        GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', '')
        REPO_NAME = os.getenv('REPO_NAME', '')
        TMDB_ACCESS_TOKEN = os.getenv('TMDB_ACCESS_TOKEN', '')
        
        # التحقق من المتغيرات
        if not GITHUB_TOKEN or GITHUB_TOKEN == 'your_github_token_here':
            print("❌ خطأ: يجب تعيين GITHUB_TOKEN")
            print("💡 استخدم: export GITHUB_TOKEN='your_token'")
            sys.exit(1)
        
        if not REPO_NAME or REPO_NAME == 'username/repository-name':
            print("❌ خطأ: يجب تعيين REPO_NAME")
            print("💡 استخدم: export REPO_NAME='username/repo'")
            sys.exit(1)
        
        if not TMDB_ACCESS_TOKEN or TMDB_ACCESS_TOKEN == 'your_tmdb_bearer_token_here':
            print("❌ خطأ: يجب تعيين TMDB_ACCESS_TOKEN")
            print("💡 احصل عليه من: https://www.themoviedb.org/settings/api")
            sys.exit(1)
        
        print("🚀 بدء تشغيل Movie Scraper Bot...")
        print("=" * 60)
        
        # إنشاء البوت
        bot = MovieBot(GITHUB_TOKEN, REPO_NAME, TMDB_ACCESS_TOKEN)
        
        # جلب المحتوى الجديد
        print("\n🔍 البحث عن محتوى جديد...\n")
        new_content = bot.find_new_content()
        
        print("\n" + "=" * 60)
        print(f"\n✅ اكتمل البحث!")
        print(f"📊 النتائج:")
        print(f"   • {new_content['total_movies']} فيلم جديد")
        print(f"   • {new_content['total_series']} مسلسل جديد")
        print(f"   • {new_content['total_count']} محتوى جديد إجمالاً")
        
        # حفظ نسخة محلية أولاً
        try:
            with open('new_content.json', 'w', encoding='utf-8') as f:
                json.dump(new_content, f, ensure_ascii=False, indent=2)
            print("\n✅ تم حفظ نسخة محلية: new_content.json")
        except Exception as e:
            print(f"❌ فشل حفظ النسخة المحلية: {e}")
        
        # حفظ إلى GitHub
        print(f"\n💾 حفظ المحتوى في GitHub...")
        if bot.save_to_github(new_content):
            print("✅ تم حفظ المحتوى في GitHub بنجاح!")
        else:
            print("⚠️  فشل حفظ المحتوى في GitHub (تحقق من الصلاحيات)")
        
        # طباعة التقرير
        report = bot.generate_report(new_content)
        print(report)
        
        # حفظ التقرير
        try:
            with open('report.txt', 'w', encoding='utf-8') as f:
                f.write(report)
            print("\n📄 تم حفظ التقرير: report.txt")
        except Exception as e:
            print(f"❌ فشل حفظ التقرير: {e}")
        
        print("\n" + "=" * 60)
        print("🎉 انتهى التشغيل بنجاح!")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  تم إيقاف البوت بواسطة المستخدم")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ خطأ غير متوقع: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
