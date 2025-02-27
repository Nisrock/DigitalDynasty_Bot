# player.py
import random
from config import *

class Player:
    def __init__(self):
        self.balance = INITIAL_BALANCE
        self.reputation = INITIAL_REPUTATION
        self.stage = INITIAL_STAGE
        self.employees = INITIAL_EMPLOYEES
        self.projects = INITIAL_PROJECTS
        self.paei = INITIAL_PAEI.copy()
        self.employee_roles = {"Developer": 1, "Manager": 0, "Marketer": 0}

    def hire_employee(self, role="Developer"):
        role_data = EMPLOYEE_ROLES.get(role)
        if self.balance >= role_data["cost"]:
            self.balance -= role_data["cost"]
            self.employees += 1
            self.employee_roles[role] = self.employee_roles.get(role, 0) + 1
            for key, value in role_data["paei"].items():
                self.paei[key] += value
            return True, f"👨‍💻 Нанят {role}!\nСотрудники: {self.employees}\nБаланс: {self.balance} монет"
        return False, f"💸 Недостаточно монет для найма {role} ({role_data['cost']} монет)!"

    def take_project(self):
        if self.employees > self.projects:
            self.projects += 1
            reward = random.randint(PROJECT_REWARD_MIN, PROJECT_REWARD_MAX)
            self.balance += reward
            rep_gain = random.randint(PROJECT_REP_MIN, PROJECT_REP_MAX)
            self.reputation += rep_gain
            self.paei["P"] += PROJECT_PAEI_P
            return True, f"📈 Проект выполнен!\n+{reward} монет\n+{rep_gain} репутации\nБаланс: {self.balance}"
        return False, "👥 Нужно больше сотрудников для новых проектов!"

    def take_small_project(self):
        reward = random.randint(SMALL_PROJECT_REWARD_MIN, SMALL_PROJECT_REWARD_MAX)
        self.balance += reward
        rep_gain = random.randint(SMALL_PROJECT_REP_MIN, SMALL_PROJECT_REP_MAX)
        self.reputation += rep_gain
        self.paei["P"] += SMALL_PROJECT_PAEI_P
        return True, f"🔧 Мелкий проект выполнен!\n+{reward} монет\n+{rep_gain} репутации\nБаланс: {self.balance}"

    def upgrade_office(self):
        if self.balance >= UPGRADE_COST:
            self.balance -= UPGRADE_COST
            self.paei["A"] += UPGRADE_PAEI_A
            return True, f"🏢 Офис улучшен!\nБаланс: {self.balance} монет"
        return False, "💸 Недостаточно монет для улучшения!"

    def to_dict(self):
        return {
            "balance": self.balance,
            "reputation": self.reputation,
            "stage": self.stage,
            "employees": self.employees,
            "projects": self.projects,
            "paei": self.paei,
            "employee_roles": self.employee_roles
        }

    @classmethod
    def from_dict(cls, data):
        player = cls()
        player.balance = data["balance"]
        player.reputation = data["reputation"]
        player.stage = data["stage"]
        player.employees = data["employees"]
        player.projects = data["projects"]
        player.paei = data["paei"]
        player.employee_roles = data.get("employee_roles", {"Developer": 1, "Manager": 0, "Marketer": 0})
        return player