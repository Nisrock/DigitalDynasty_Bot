$gamePyContent = @"
import json
import os

class Game:
    def __init__(self):
        self.players = {}
        self._stage_emoji = {
            "Courtship": "🌱",
            "Infancy": "👶",
            "Adolescence": "🎓",
            "Maturity": "🏢",
            "Decline": "🍂"
        }
        self.current_stage = "Courtship"
        self.load_players()

    def get_player(self, chat_id):
        if chat_id not in self.players:
            self.players[chat_id] = {
                "balance": 5000,
                "reputation": 0,
                "employees": 1,
                "projects": 0,
                "paei": {"P": 50, "A": 10, "E": 70, "I": 30},
                "stage": self.current_stage,
                "employee_roles": {"Developer": 1, "Manager": 0, "Marketer": 0}
            }
        return self.players[chat_id]

    def load_players(self):
        try:
            if os.path.exists("players.json"):
                with open("players.json", "r") as f:
                    self.players = json.load(f)
        except Exception as e:
            print(f"Error loading players: {e}")
            self.players = {}

    def save_players(self):
        try:
            # На Vercel используем временное хранилище или игнорируем сохранение
            with open("players.json", "w") as f:
                json.dump(self.players, f)
        except Exception as e:
            print(f"Warning: Could not save players on Vercel: {e}")
            # В случае ошибки данные останутся в памяти для текущей сессии

    @property
    def stage_emoji(self):
        return self._stage_emoji
"@
Write-Host "Writing to game.py"
$gamePyContent | Out-File -FilePath "game.py" -Encoding UTF8
git add game.py