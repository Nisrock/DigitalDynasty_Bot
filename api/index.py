from flask import Flask, request, jsonify, send_from_directory
from config import EMPLOYEE_ROLES
from game import Game
import os

app = Flask(__name__, static_folder='../webapp', static_url_path='/webapp')
game_instance = Game()

# Загрузка данных игроков при старте
game_instance.load_players()

@app.route('/webapp')
def serve_webapp():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/command', methods=['POST'])
def handle_command():
    data = request.json
    command = data.get('command')
    chat_id = data.get('chat_id')
    role = data.get('role')
    if not chat_id or not command:
        return jsonify({"error": "Invalid request"}), 400
    
    player = game_instance.get_player(chat_id)
    if command == 'hire' and role in EMPLOYEE_ROLES:
        success, message = player.hire_employee(role)
    elif command == 'project':
        success, message = player.take_project()
    elif command == 'upgrade':
        success, message = player.upgrade_office()
    else:
        return jsonify({"error": "Unknown command"}), 400
    
    game_instance.save_players()
    return jsonify({"success": success, "message": message})

@app.route('/api/status', methods=['POST'])
def get_status():
    data = request.json
    chat_id = data.get('chat_id')
    if not chat_id:
        return jsonify({"error": "Invalid request"}), 400
    
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

# Vercel запускает Flask как Serverless-функцию
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))