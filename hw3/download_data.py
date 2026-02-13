#!/usr/bin/env python3
"""
Скачивает ДАННЫЕ ЗА 2024 ГОД (январь-июнь) — именно они нужны для домашки урока 3
"""
import os
import requests
from tqdm import tqdm

# ВАЖНО: именно 2024 год, месяцы 01-06
months = ['01', '02', '03', '04', '05', '06']
base_url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-{}.parquet"

os.makedirs("data", exist_ok=True)

print("="*70)
print("Скачивание данных такси Нью-Йорка за ЯНВАРЬ-ИЮНЬ 2024 ГОДА")
print("Это единственные данные, для которых правильный ответ = 128,210")
print("="*70)

for month in months:
    url = base_url.format(month)
    filename = f"data/yellow_tripdata_2024-{month}.parquet"
    
    print(f"\n📥 Скачиваю 2024-{month}...")
    try:
        resp = requests.get(url, stream=True, timeout=60)
        resp.raise_for_status()
        total = int(resp.headers.get('content-length', 0))
        
        with open(filename, 'wb') as f, tqdm(
            total=total, unit='iB', unit_scale=True, unit_divisor=1024,
            ncols=80, leave=True
        ) as bar:
            for data in resp.iter_content(chunk_size=1024*1024):
                size = f.write(data)
                bar.update(size)
        
        size_mb = os.path.getsize(filename) / 1024 / 1024
        print(f"✅ Сохранено: {filename} ({size_mb:.1f} MB)")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        if os.path.exists(filename):
            os.remove(filename)

print("\n" + "="*70)
print("✅ Все 6 файлов за 2024 год скачаны успешно!")
print("="*70)