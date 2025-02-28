from flask import Flask, request, jsonify, send_from_directory
from config import EMPLOYEE_ROLES, FIX_BUG_COST, BONUS_COST, IGNORE_BUG_REP_PENALTY
from game import Game
import os
import random

app = Flask(__name__, static_folder='../webapp', static_url_path='/webapp')
game_instance = Game()
game_instance.load_players()

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route('/webapp', methods=['GET'])
def serve_webapp():
    response = send_from_directory(app.static_folder, 'index.html')
    response.headers['Cache-Control'] = 'no-store'
    response.headers['Connection'] = 'keep-alive'
    return response

@app.route('/api/command', methods=['POST', 'OPTIONS'])
def handle_command():
    if request.method == 'OPTIONS':
        return '', 200
    try:
        data = request.get_json()
        if not data or 'chat_id' not in data or 'command' not in data:
            return jsonify({"error": "Invalid request payload"}), 400
        
        command = data['command']
        chat_id = data['chat_id']
        role = data.get('role')
        action = data.get('action')  # Для выбора действия в событиях
        
        player = game_instance.get_player(chat_id)
        if command == 'hire' and role in EMPLOYEE_ROLES:
            success, message = player.hire_employee(role)
            if success:
                event = trigger_random_event(chat_id)
                if event:
                    return jsonify({"success": success, "message": message, "event": event})
        elif command == 'project':
            success, message = player.take_project()
            if success:
                event = trigger_random_event(chat_id)
                if event:
                    return jsonify({"success": success, "message": message, "event": event})
        elif command == 'upgrade':
            success, message = player.upgrade_office()
            if success:
                event = trigger_random_event(chat_id)
                if event:
                    return jsonify({"success": success, "message": message, "event": event})
        elif command == 'event' and action:
            success, message = handle_event(chat_id, action)
        else:
            return jsonify({"error": f"Unknown command: {command}"}), 400
        
        # game_instance.save_players() # Пока в памяти
        return jsonify({"success": success, "message": message})
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/api/status', methods=['POST', 'OPTIONS'])
def get_status():
    if request.method == 'OPTIONS':
        return '', 200
    try:
        data = request.get_json()
        if not data or 'chat_id' not in data:
            return jsonify({"error": "Invalid request payload"}), 400
        
        chat_id = data['chat_id']
        player = game_instance.get_player(chat_id)
        status = {
            "balance": player.balance,
            "reputation": player.reputation,
            "employees": player.employees,
            "projects": player.projects,
            "paei": player.paei,
            "stage": f"{game_instance.stage_emoji[player.stage]} {player.stage}",
            "employee_roles": player.employee_roles
        }
        return jsonify(status)
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

# Функция для генерации случайных событий
def trigger_random_event(chat_id):
    player = game_instance.get_player(chat_id)
    if random.random() < 0.3:  # 30% шанс события
        event = random.choice([
            {
                "message": "Клиент недоволен багом в проекте! Что делать?",
                "options": [
                    {"text": f"💰 Исправить (-{FIX_BUG_COST})", "action": "fix_bug"},
                    {"text": f"❌ Игнорировать (-{IGNORE_BUG_REP_PENALTY} репутации)", "action": "ignore_bug"}
                ]
            },
            {
                "message": "Сотрудник хочет уйти. Убедить его остаться?",
                "options": [
                    {"text": f"💸 Дать бонус (-{BONUS_COST})", "action": "bonus"},
                    {"text": "🚪 Пусть уходит (-1 сотрудник)", "action": "let_go"}
                ]
            }
        ])
        return event
    return None

# Обработка выбора действия в событии
def handle_event(chat_id, action):
    player = game_instance.get_player(chat_id)
    if action == 'fix_bug':
        if player.balance >= FIX_BUG_COST:
            player.balance -= FIX_BUG_COST
            return True, f"💰 Баг исправлен! Баланс: {player.balance}"
        return False, "💸 Недостаточно монет для исправления!"
    elif action == 'ignore_bug':
        player.reputation -= IGNORE_BUG_REP_PENALTY
        return True, f"❌ Клиент ушёл недовольным. Репутация: {player.reputation}"
    elif action == 'bonus':
        if player.balance >= BONUS_COST:
            player.balance -= BONUS_COST
            player.paei["I"] += 5  # Бонус к командному духу
            return True, f"💸 Сотрудник остался! Баланс: {player.balance}"
        return False, "💸 Недостаточно монет для бонуса!"
    elif action == 'let_go':
        if player.employees > 1:
            player.employees -= 1
            return True, f"🚪 Сотрудник ушёл. Сотрудники: {player.employees}"
        return False, "👥 Нельзя уволить последнего сотрудника!"
    return False, "Неизвестное действие"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))