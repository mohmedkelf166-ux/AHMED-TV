name: Auto Update Movies
on:
  schedule:
    - cron: '0 * * * *' # يعمل كل ساعة
  workflow_dispatch: # للتشغيل اليدوي

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install requests beautifulsoup4
      - name: Run Scrapper
        run: python scrapper.py
      - name: Save Changes
        run: |
          git config --local user.email "bot@github.com"
          git config --local user.name "MovieBot"
          git add .
          git commit -m "تحديث تلقائي للأفلام" || exit 0
          git push

