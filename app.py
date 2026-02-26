import streamlit as st
import requests
from collections import defaultdict
import time

# Вставь сюда свой hero_roles (весь словарь)
hero_roles = { ... }  # ← весь твой словарь ролей

name_to_id = {}
id_to_name = {}

@st.cache_data
def load_heroes():
    url = "https://api.opendota.com/api/heroes"
    resp = requests.get(url)
    if resp.status_code != 200:
        st.error("Ошибка загрузки героев")
        st.stop()
    heroes = resp.json()
    global name_to_id, id_to_name
    name_to_id = {h['localized_name']: h['id'] for h in heroes}
    id_to_name = {h['id']: h['localized_name'] for h in heroes}
    return len(heroes)

@st.cache_data
def get_matchups_from_opendota(hero_id):
    url = f"https://api.opendota.com/api/heroes/{hero_id}/matchups"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            return {}
        data = resp.json()
        matchups = {}
        for m in data:
            opp_id = m['hero_id']
            games = m['games_played']
            if games > 1:  # можно поставить 1 или 0
                winrate = (m['wins'] / games) * 100
                matchups[opp_id] = {'winrate': winrate, 'games': games}
        return matchups
    except:
        return {}

def recommend_heroes(my_role, enemies_names, top_k=7, mode='average'):
    # (твоя функция полностью, без изменений)

# Интерфейс сайта (твой текущий код с selectbox и text_input)

st.set_page_config(page_title="Dota 2 Рекомендатор", layout="wide")
st.title("Dota 2 Рекомендатор героев — патч 7.40")
st.markdown("Выбери роль и укажи врагов — получи топ-7 пиков!")

load_heroes()

role = st.selectbox("Твоя роль", ["Carry", "Mid", "Offlane", "Soft Support", "Hard Support"])
role_num = {"Carry": 1, "Mid": 2, "Offlane": 3, "Soft Support": 4, "Hard Support": 5}[role]

enemies_input = st.text_input("Враги (через запятую)", "Medusa, Storm Spirit, Mars")

if st.button("Получить рекомендации"):
    enemies = [e.strip() for e in enemies_input.split(',') if e.strip()]
    if not enemies:
        st.error("Укажи хотя бы одного врага")
    else:
        with st.spinner("Загружаем данные..."):
            recs = recommend_heroes(role_num, enemies)
        st.success("Рекомендованные герои:")
        for i, rec in enumerate(recs, 1):
            st.markdown(f"**{i}.** {rec}")

st.caption("Данные: OpenDota API | Проект для школы")
