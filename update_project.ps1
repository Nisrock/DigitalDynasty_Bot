# update_files.ps1

# Путь к проекту
$projectPath = "C:\Users\Nikita\source\repos\DigitalDynasty_Bot\DigitalDynasty_Bot"

# Переход в директорию проекта
Set-Location -Path $projectPath
Write-Host "Changed directory to $projectPath"

# Новый код для файлов
$indexHtmlContent = @"
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DigitalDynasty</title>
    <link rel="stylesheet" href="/webapp/styles.css">
    <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
</head>
<body>
    <div class="container">
        <h1>🏢 DigitalDynasty</h1>
        <div id="balance-display" class="balance-display">$00000</div>
        <div id="status" class="status-grid">
            <div class="status-card"><span class="animated-icon">📍</span><span id="stage">Этап: Загрузка...</span></div>
            <div class="status-card"><span class="animated-icon">⭐</span><span id="reputation">Репутация: 0</span></div>
            <div class="status-card"><span class="animated-icon">👥</span><span id="employees">Сотрудники: 0</span></div>
            <div class="status-card"><span class="animated-icon">📈</span><span id="projects">Проекты: 0</span></div>
            <div class="status-card"><span class="animated-icon">⚙️</span><span id="paei-p">P: 0%</span></div>
            <div class="status-card"><span class="animated-icon">📋</span><span id="paei-a">A: 0%</span></div>
            <div class="status-card"><span class="animated-icon">💡</span><span id="paei-ei">E: 0% | I: 0%</span></div>
        </div>
        <div id="message" class="message-box"></div>
        <div class="actions">
            <button id="hire">👥 Нанять</button>
            <button id="project">📈 Проект</button>
            <button id="upgrade">🏢 Улучшить</button>
            <button id="small_project">🔧 Мелкий</button>
        </div>
        <div id="hire-menu" class="hire-menu" style="display: none;">
            <h2>Выбери роль!</h2>
            <button class="role-btn" data-role="Developer">👨‍💻 Разработчик</button>
            <button class="role-btn" data-role="Manager">👩‍💼 Менеджер</button>
            <button class="role-btn" data-role="Marketer">📢 Маркетолог</button>
        </div>
    </div>
    <script src="/webapp/app.js"></script>
</body>
</html>
"@

$stylesCssContent = @"
body {
    font-family: 'Press Start 2P', cursive;
    background-color: #0A0F14;
    margin: 0;
    padding: 20px 20px 100px 20px;
    color: #E0E0E0;
}
.container {
    max-width: 600px;
    margin: 0 auto;
    text-align: center;
}
h1 {
    color: #00FF00;
    font-size: 20px;
    text-shadow: 0 0 10px #00FF00;
}
.balance-display {
    background: linear-gradient(45deg, #00FF00, #00CC00);
    color: #000000;
    padding: 12px;
    border: 3px solid #00FF00;
    border-radius: 8px;
    margin-bottom: 20px;
    font-size: 14px;
    box-shadow: 0 0 20px rgba(0, 255, 0, 0.8);
    text-align: center;
    text-transform: uppercase;
}
.status-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
    margin-bottom: 20px;
}
.status-card {
    background: linear-gradient(135deg, #1B263B, #0F1A2A);
    padding: 12px;
    border: 3px solid #00FF00;
    border-radius: 8px;
    font-size: 14px;
    color: #FFD700;
    text-align: left;
    box-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
    display: flex;
    align-items: center;
    min-height: 50px;
}
.animated-icon {
    animation: pulse 1.5s infinite;
}
@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.2); }
    100% { transform: scale(1); }
}
.status-card span:first-child {
    color: #00FF00;
    margin-right: 10px;
    font-size: 18px;
}
.status-card span:last-child {
    margin-left: 10px;
    text-shadow: 0 0 5px #FFD700;
}
.message-box {
    background: linear-gradient(135deg, #1B263B, #0F1A2A);
    color: #00FF00;
    padding: 12px;
    border: 2px solid #00FF00;
    border-radius: 8px;
    margin-bottom: 15px;
    min-height: 50px;
    font-size: 12px;
    box-shadow: 0 0 15px rgba(0, 255, 0, 0.6);
}
.message-box.error {
    color: #FF0000;
    border-color: #FF0000;
    box-shadow: 0 0 15px rgba(255, 0, 0, 0.6);
}
.message-box.event {
    color: #FFFF00;
    border-color: #FFFF00;
    box-shadow: 0 0 15px rgba(255, 255, 0, 0.6);
}
.message-box button {
    background-color: #00FF00;
    color: #0F1A2A;
    border: none;
    padding: 10px 20px;
    margin: 5px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 12px;
    box-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
}
.message-box button:hover {
    background-color: #00CC00;
    box-shadow: 0 0 15px rgba(0, 255, 0, 0.7);
}
.actions {
    position: fixed;
    bottom: 10px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    justify-content: center;
    gap: 10px;
    width: 100%;
    max-width: 600px;
    padding: 0 20px;
    box-sizing: border-box;
}
.actions button {
    background-color: #1E3A5F;
    color: #00FF00;
    border: 2px solid #00FF00;
    padding: 12px 20px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 14px;
    box-shadow: 0 0 15px rgba(0, 255, 0, 0.5);
    text-transform: uppercase;
    width: 120px;
}
.actions button:hover {
    background-color: #14375A;
    box-shadow: 0 0 20px rgba(0, 255, 0, 0.7);
}
.hire-menu {
    position: fixed;
    bottom: 10px;
    left: 50%;
    transform: translateX(-50%);
    background-color: #0F1A2A;
    padding: 10px;
    border: 2px solid #00FF00;
    border-radius: 8px;
    width: 100%;
    max-width: 600px;
    box-sizing: border-box;
    display: none;
}
.hire-menu h2 {
    color: #00FF00;
    font-size: 16px;
}
.hire-menu button {
    background-color: #1E3A5F;
    color: #00FF00;
    border: 2px solid #00FF00;
    padding: 12px 20px;
    margin: 5px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 14px;
    box-shadow: 0 0 15px rgba(0, 255, 0, 0.5);
    width: 140px;
}
.hire-menu button:hover {
    background-color: #14375A;
    box-shadow: 0 0 20px rgba(0, 255, 0, 0.7);
}
"@

$apiIndexPyContent = @"
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
        action = data.get('action')
        
        player = game_instance.get_player(chat_id)
        if command == 'hire' and role in EMPLOYEE_ROLES:
            success, message = player.hire_employee(role)
            if success:
                event = trigger_random_event(chat_id)
                game_instance.save_players()
                if event:
                    return jsonify({"success": success, "message": message, "event": event})
        elif command == 'project':
            success, message = player.take_project()
            if success:
                event = trigger_random_event(chat_id)
                game_instance.save_players()
                if event:
                    return jsonify({"success": success, "message": message, "event": event})
        elif command == 'upgrade':
            success, message = player.upgrade_office()
            if success:
                event = trigger_random_event(chat_id)
                game_instance.save_players()
                if event:
                    return jsonify({"success": success, "message": message, "event": event})
        elif command == 'small_project':
            success, message = player.take_small_project()
            if success:
                event = trigger_random_event(chat_id)
                game_instance.save_players()
                if event:
                    return jsonify({"success": success, "message": message, "event": event})
        elif command == 'event' and action:
            success, message = handle_event(chat_id, action)
        else:
            return jsonify({"error": f"Unknown command: {command}"}), 400
        
        game_instance.save_players()
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

def trigger_random_event(chat_id):
    player = game_instance.get_player(chat_id)
    if random.random() < 0.3:  # 30% шанс
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

def handle_event(chat_id, action):
    player = game_instance.get_player(chat_id)
    if action == 'fix_bug':
        if player.balance >= FIX_BUG_COST:
            player.balance -= FIX_BUG_COST
            game_instance.save_players()
            return True, f"💰 Баг исправлен! Баланс: {player.balance}"
        return False, "💸 Недостаточно монет для исправления!"
    elif action == 'ignore_bug':
        player.reputation -= IGNORE_BUG_REP_PENALTY
        game_instance.save_players()
        return True, f"❌ Клиент ушёл недовольным. Репутация: {player.reputation}"
    elif action == 'bonus':
        if player.balance >= BONUS_COST:
            player.balance -= BONUS_COST
            player.paei["I"] += 5
            game_instance.save_players()
            return True, f"💸 Сотрудник остался! Баланс: {player.balance}"
        return False, "💸 Недостаточно монет для бонуса!"
    elif action == 'let_go':
        if player.employees > 1:
            player.employees -= 1
            game_instance.save_players()
            return True, f"🚪 Сотрудник ушёл. Сотрудники: {player.employees}"
        return False, "👥 Нельзя уволить последнего сотрудника!"
    return False, "Неизвестное действие"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
"@

# Чтение содержимого app.js.template (обязательно)
if (Test-Path "app.js.template") {
    $appJsContent = Get-Content -Path "app.js.template" -Raw
} else {
    Write-Host "Error: app.js.template not found. Please create it in the project root with the JavaScript code."
    exit
}

# Запись нового кода в файлы
Write-Host "Writing to webapp/index.html"
$indexHtmlContent | Out-File -FilePath "webapp/index.html" -Encoding UTF8
Write-Host "Writing to webapp/styles.css"
$stylesCssContent | Out-File -FilePath "webapp/styles.css" -Encoding UTF8
Write-Host "Writing to webapp/app.js"
$appJsContent | Out-File -FilePath "webapp/app.js" -Encoding UTF8
Write-Host "Writing to api/index.py"
$apiIndexPyContent | Out-File -FilePath "api/index.py" -Encoding UTF8

# Вывод успешного завершения
Write-Host "Files updated successfully! Please manually run 'git add .', 'git commit -m ""Your message""', and 'vercel --prod' to deploy."