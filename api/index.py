from flask import Flask, request, jsonify, send_from_directory
from config import EMPLOYEE_ROLES
from game import Game
import os

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
        
        player = game_instance.get_player(chat_id)
        if command == 'hire' and role in EMPLOYEE_ROLES:
            success, message = player.hire_employee(role)
        elif command == 'project':
            success, message = player.take_project()
        elif command == 'upgrade':
            success, message = player.upgrade_office()
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))