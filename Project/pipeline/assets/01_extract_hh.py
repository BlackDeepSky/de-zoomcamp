"""@bruin
name: public.raw_vacancies
type: python
connection: pg_local
materialization:
  type: table
  strategy: create+replace
@bruin"""

import requests
import pandas as pd
import time

def materialize():
    roles = {"Data Engineer": "Data Engineer",
             "Data Analyst": "Data Analyst",
             "Data Science": "Data Scientist"}

    # 16 - это ID Беларуси в API HH
    base_url = "https://api.hh.ru/vacancies"
    all_jobs = []

    for role_name, search_text in roles.items():
        # Собираем список вакансий (поиск)
        params = {"text": search_text, "area": 16, "per_page": 50, "page": 0}
        response = requests.get(base_url, params=params).json()

        if 'items' not in response:
            continue

        # Проходим по каждой вакансии, чтобы вытащить детальную информацию (навыки и опыт)
        for item in response['items']:
            job_id = item['id']
            # Запрос детальной информации по конкретной вакансии
            detail_resp = requests.get(f"{base_url}/{job_id}").json()

            # Извлекаем навыки в виде списка строк
            skills = [skill['name'] for skill in detail_resp.get('key_skills', [])]

            job_data = {
                "id": job_id,
                "role_category": role_name,
                "title": detail_resp.get("name"),
                "published_at": detail_resp.get("published_at"),
                "experience": detail_resp.get("experience", {}).get("name"),
                "employer": detail_resp.get("employer", {}).get("name"),
                "skills": ", ".join(skills), # Сохраняем как строку для простоты SQL парсинга
                "url": detail_resp.get("alternate_url")
            }
            all_jobs.append(job_data)
            time.sleep(0.1) # Пауза, чтобы API не заблокировал за спам запросами

    df = pd.DataFrame(all_jobs)
    return df
