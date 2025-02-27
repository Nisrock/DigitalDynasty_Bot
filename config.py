# config.py
TOKEN = '8191066276:AAFxvTnzxd0gMljXgcxiew1FOiHRvfk0F14'

INITIAL_BALANCE = 10000
INITIAL_REPUTATION = 0
INITIAL_STAGE = "Courtship"
INITIAL_EMPLOYEES = 1
INITIAL_PROJECTS = 0
INITIAL_PAEI = {"P": 50, "A": 10, "E": 70, "I": 30}

EMPLOYEE_ROLES = {
    "Developer": {"cost": 3000, "paei": {"P": 10, "I": 5}, "description": "Повышает производительность", "emoji": "👨‍💻"},
    "Manager": {"cost": 4000, "paei": {"A": 15, "I": 5}, "description": "Улучшает организацию", "emoji": "👩‍💼"},
    "Marketer": {"cost": 3500, "paei": {"E": 10, "I": 5}, "description": "Увеличивает репутацию", "emoji": "📢"}
}

UPGRADE_COST = 5000
FIX_BUG_COST = 2000
BONUS_COST = 1000

PROJECT_REWARD_MIN = 4000
PROJECT_REWARD_MAX = 6000
PROJECT_REP_MIN = 5
PROJECT_REP_MAX = 10
SMALL_PROJECT_REWARD_MIN = 500
SMALL_PROJECT_REWARD_MAX = 1500
SMALL_PROJECT_REP_MIN = 1
SMALL_PROJECT_REP_MAX = 3
IGNORE_BUG_REP_PENALTY = 10

PROJECT_PAEI_P = 5
SMALL_PROJECT_PAEI_P = 2
UPGRADE_PAEI_A = 10
BONUS_PAEI_I = 5

STAGE_EMOJI = {"Courtship": "🌱", "Infancy": "👶", "Go-Go": "🚀", "Adolescence": "🌟", "Prime": "👑"}
STAGE_TRANSITIONS = {
    "Courtship": {"reputation": 10, "next": "Infancy"},
    "Infancy": {"reputation": 30, "employees": 3, "next": "Go-Go"},
    "Go-Go": {"reputation": 60, "paei_A": 30, "next": "Adolescence"},
    "Adolescence": {"reputation": 100, "paei_P": 70, "next": "Prime"}
}

RANDOM_EVENT_CHANCE = 0.3
SAVE_FILE = "players.json"

PROGRESS_BAR_FULL = "🟩"
PROGRESS_BAR_EMPTY = "⬜"
PAEI_EMOJI = {"P": "⚙️", "A": "📋", "E": "💡", "I": "🤝"}
CURRENCY_EMOJI = "💰"
REPUTATION_EMOJI = "⭐"
EMPLOYEE_EMOJI = "👥"
PROJECT_EMOJI = "📈"