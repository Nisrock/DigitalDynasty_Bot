# game.py
import random
import json
import os
from config import *
from player import Player

class Game:
    def __init__(self):
        self.players = {}
        self.save_file = SAVE_FILE
        self.stage_emoji = STAGE_EMOJI

    def load_players(self):
        if os.path.exists(self.save_file):
            with open(self.save_file, 'r', encoding='utf-8') as f:
                loaded = json.load(f)
                for chat_id, data in loaded.items():
                    self.players[int(chat_id)] = Player.from_dict(data)

    def save_players(self):
        with open(self.save_file, 'w', encoding='utf-8') as f:
            json.dump({chat_id: player.to_dict() for chat_id, player in self.players.items()}, f)

    def get_player(self, chat_id):
        if chat_id not in self.players:
            self.players[chat_id] = Player()
        return self.players[chat_id]

    def check_stage(self, player):
        current_stage = player.stage
        if current_stage in STAGE_TRANSITIONS:
            conditions = STAGE_TRANSITIONS[current_stage]
            if (player.reputation >= conditions["reputation"] and
                ("employees" not in conditions or player.employees >= conditions["employees"]) and
                ("paei_A" not in conditions or player.paei["A"] >= conditions["paei_A"]) and
                ("paei_P" not in conditions or player.paei["P"] >= conditions["paei_P"])):
                player.stage = conditions["next"]
                return f"{self.stage_emoji[player.stage]} Переход в *{player.stage}*!", True
        return None, False

    def random_event(self):
        if random.random() < RANDOM_EVENT_CHANCE:
            return random.choice([
                ("Клиент недоволен багом в проекте! Что делать?", 
                 [(f"💰 Исправить (-{FIX_BUG_COST})", 'fix_bug'), 
                  (f"❌ Игнорировать (-{IGNORE_BUG_REP_PENALTY} репутации)", 'ignore_bug')]),
                ("Сотрудник хочет уйти. Убедить его остаться?", 
                 [(f"💸 Дать бонус (-{BONUS_COST})", 'bonus'), 
                  ("🚪 Пусть уходит (-1 сотрудник)", 'let_go')])
            ])
        return None

    def handle_event(self, player, action):
        if action == 'fix_bug':
            if player.balance >= FIX_BUG_COST:
                player.balance -= FIX_BUG_COST
                return f"💰 Баг исправлен! Баланс: {player.balance}"
            return "💸 Недостаточно монет для исправления!"
        elif action == 'ignore_bug':
            player.reputation -= IGNORE_BUG_REP_PENALTY
            return f"❌ Клиент ушёл недовольным. Репутация: {player.reputation}"
        elif action == 'bonus':
            if player.balance >= BONUS_COST:
                player.balance -= BONUS_COST
                player.paei["I"] += BONUS_PAEI_I
                return f"💸 Сотрудник остался! Баланс: {player.balance}"
            return "💸 Недостаточно монет для бонуса!"
        elif action == 'let_go':
            if player.employees > 1:
                player.employees -= 1
                return f"🚪 Сотрудник ушёл. Сотрудники: {player.employees}"
        return None