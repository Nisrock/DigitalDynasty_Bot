import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import telegram.error
from config import (
    TOKEN, EMPLOYEE_ROLES, PROGRESS_BAR_FULL, PROGRESS_BAR_EMPTY, 
    PAEI_EMOJI, CURRENCY_EMOJI, REPUTATION_EMOJI, EMPLOYEE_EMOJI, PROJECT_EMOJI
)
from game import Game
from flask import Flask, request, jsonify

app = Flask(__name__, static_folder='webapp', static_url_path='/webapp')
bot_instance = None

class Bot:
    def __init__(self, token, game):
        self.token = token
        self.game = game
        self.application = Application.builder().token(self.token).build()
        global bot_instance
        bot_instance = self
        self.setup_handlers()

    def get_paei_description(self, paei):
        bar_length = 10
        descriptions = []
        for key, value in paei.items():
            filled = int(value / 10)
            empty = bar_length - filled
            bar = PROGRESS_BAR_FULL * filled + PROGRESS_BAR_EMPTY * empty
            descriptions.append(f"{PAEI_EMOJI[key]} {key}: {value}% [{bar}]")
        return "\n".join(descriptions)

    def get_main_keyboard(self, player):
        keyboard = [
            [InlineKeyboardButton(f"{EMPLOYEE_EMOJI} Нанять сотрудника", callback_data='hire'),
             InlineKeyboardButton(f"{PROJECT_EMOJI} Взять проект", callback_data='project')],
            [InlineKeyboardButton("🏢 Улучшить офис", callback_data='upgrade'),
             InlineKeyboardButton("📊 Статус компании", callback_data='status')],
        ]
        if player.balance < 3000 and player.employees <= player.projects:
            keyboard.append([InlineKeyboardButton("🔧 Мелкий проект", callback_data='small_project')])
        return InlineKeyboardMarkup(keyboard)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.message.chat_id
        user = update.message.from_user.first_name
        player = self.game.get_player(chat_id)
        paei_text = self.get_paei_description(player.paei)
        message = (
            f"🎉 *Привет, {user}! Добро пожаловать в DigitalDynasty!* 🎉\n"
            "Ты начинаешь строить свою IT-империю!\n\n"
            f"📍 *Этап*: {self.game.stage_emoji[player.stage]} {player.stage}\n"
            f"{CURRENCY_EMOJI} *Баланс*: {player.balance} монет\n"
            f"{REPUTATION_EMOJI} *Репутация*: {player.reputation}\n"
            f"{EMPLOYEE_EMOJI} *Сотрудники*: {player.employees}\n"
            f"{PROJECT_EMOJI} *Проекты*: {player.projects}\n\n"
            f"🏭 *Состояние компании*:\n{paei_text}\n\n"
            "💡 Выбери действие ниже:"
        )
        await update.message.reply_text(message, reply_markup=self.get_main_keyboard(player), parse_mode='Markdown')
        self.game.save_players()

    async def status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.callback_query.message.chat_id if update.callback_query else update.message.chat_id
        player = self.game.get_player(chat_id)
        paei_text = self.get_paei_description(player.paei)
        roles_text = "\n".join(
            f"{EMPLOYEE_ROLES[role]['emoji']} {role}: {count}" for role, count in player.employee_roles.items() if count > 0
        ) or "Нет сотрудников"
        message = (
            f"🏢 *Твоя DigitalDynasty*:\n\n"
            f"📍 *Этап*: {self.game.stage_emoji[player.stage]} {player.stage}\n"
            f"{CURRENCY_EMOJI} *Баланс*: {player.balance} монет\n"
            f"{REPUTATION_EMOJI} *Репутация*: {player.reputation}\n"
            f"{EMPLOYEE_EMOJI} *Сотрудники*: {player.employees}\n"
            f"👥 *Состав команды*:\n{roles_text}\n"
            f"{PROJECT_EMOJI} *Проекты*: {player.projects}\n\n"
            f"🏭 *Состояние компании*:\n{paei_text}"
        )
        await context.bot.send_message(chat_id=chat_id, text=message, reply_markup=self.get_main_keyboard(player), parse_mode='Markdown')

    async def hire(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        try:
            await query.answer()
        except telegram.error.BadRequest:
            pass
        chat_id = query.message.chat_id
        player = self.game.get_player(chat_id)
        if "hire_" in query.data:
            role = query.data.split("_")[1]
            success, message = player.hire_employee(role)
            current_text = query.message.text
            current_markup = query.message.reply_markup
            new_markup = self.get_main_keyboard(player)
            if message != current_text or str(new_markup) != str(current_markup):
                await query.edit_message_text(f"📢 {message}", reply_markup=new_markup)
            if success:
                await self.handle_random_event(chat_id, context)
            self.game.save_players()
        else:
            keyboard = [
                [InlineKeyboardButton(f"{EMPLOYEE_ROLES['Developer']['emoji']} Разработчик ({EMPLOYEE_ROLES['Developer']['cost']} {CURRENCY_EMOJI})", callback_data='hire_Developer')],
                [InlineKeyboardButton(f"{EMPLOYEE_ROLES['Manager']['emoji']} Менеджер ({EMPLOYEE_ROLES['Manager']['cost']} {CURRENCY_EMOJI})", callback_data='hire_Manager')],
                [InlineKeyboardButton(f"{EMPLOYEE_ROLES['Marketer']['emoji']} Маркетолог ({EMPLOYEE_ROLES['Marketer']['cost']} {CURRENCY_EMOJI})", callback_data='hire_Marketer')],
                [InlineKeyboardButton("⬅ Вернуться", callback_data='status')]
            ]
            current_text = query.message.text
            current_markup = query.message.reply_markup
            new_markup = InlineKeyboardMarkup(keyboard)
            new_text = (
                "👥 *Нанять сотрудника*:\n\n"
                f"{EMPLOYEE_ROLES['Developer']['emoji']} *Разработчик*: {EMPLOYEE_ROLES['Developer']['description']}\n"
                f"{EMPLOYEE_ROLES['Manager']['emoji']} *Менеджер*: {EMPLOYEE_ROLES['Manager']['description']}\n"
                f"{EMPLOYEE_ROLES['Marketer']['emoji']} *Маркетолог*: {EMPLOYEE_ROLES['Marketer']['description']}"
            )
            if new_text != current_text or str(new_markup) != str(current_markup):
                await query.edit_message_text(new_text, reply_markup=new_markup)

    async def project(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        try:
            await query.answer()
        except telegram.error.BadRequest:
            pass
        chat_id = query.message.chat_id
        player = self.game.get_player(chat_id)
        success, message = player.take_project()
        current_text = query.message.text
        current_markup = query.message.reply_markup
        new_markup = self.get_main_keyboard(player)
        if message != current_text or str(new_markup) != str(current_markup):
            await query.edit_message_text(f"🏭 {message}", reply_markup=new_markup)
        if success:
            stage_message, changed = self.game.check_stage(player)
            if changed:
                await context.bot.send_message(chat_id=chat_id, text=f"🎉 {stage_message}", parse_mode='Markdown')
            await self.handle_random_event(chat_id, context)
        self.game.save_players()

    async def small_project(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        try:
            await query.answer()
        except telegram.error.BadRequest:
            pass
        chat_id = query.message.chat_id
        player = self.game.get_player(chat_id)
        success, message = player.take_small_project()
        current_text = query.message.text
        current_markup = query.message.reply_markup
        new_markup = self.get_main_keyboard(player)
        if message != current_text or str(new_markup) != str(current_markup):
            await query.edit_message_text(f"🔨 {message}", reply_markup=new_markup)
        self.game.save_players()

    async def upgrade(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        try:
            await query.answer()
        except telegram.error.BadRequest:
            pass
        chat_id = query.message.chat_id
        player = self.game.get_player(chat_id)
        success, message = player.upgrade_office()
        current_text = query.message.text
        current_markup = query.message.reply_markup
        new_markup = self.get_main_keyboard(player)
        if message != current_text or str(new_markup) != str(current_markup):
            await query.edit_message_text(f"🏢 {message}", reply_markup=new_markup)
        if success:
            await self.handle_random_event(chat_id, context)
        self.game.save_players()

    async def handle_random_event(self, chat_id, context):
        player = self.game.get_player(chat_id)
        event = self.game.random_event()
        if event:
            keyboard = [[InlineKeyboardButton(text, callback_data=data) for text, data in event[1]]]
            await context.bot.send_message(chat_id=chat_id, text=f"⚠ {event[0]}", reply_markup=InlineKeyboardMarkup(keyboard))

    async def handle_event(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        try:
            await query.answer()
        except telegram.error.BadRequest:
            pass
        chat_id = query.message.chat_id
        player = self.game.get_player(chat_id)
        action = query.data
        message = self.game.handle_event(player, action)
        if message:
            current_text = query.message.text
            current_markup = query.message.reply_markup
            new_markup = self.get_main_keyboard(player)
            if message != current_text or str(new_markup) != str(current_markup):
                await query.edit_message_text(f"📢 {message}", reply_markup=new_markup)
        self.game.save_players()

    def setup_handlers(self):
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CallbackQueryHandler(self.hire, pattern='^hire(_.*)?$'))
        self.application.add_handler(CallbackQueryHandler(self.project, pattern='^project$'))
        self.application.add_handler(CallbackQueryHandler(self.upgrade, pattern='^upgrade$'))
        self.application.add_handler(CallbackQueryHandler(self.status, pattern='^status$'))
        self.application.add_handler(CallbackQueryHandler(self.small_project, pattern='^small_project$'))
        self.application.add_handler(CallbackQueryHandler(self.handle_event, pattern='^(fix_bug|ignore_bug|bonus|let_go)$'))

    def run(self):
        self.game.load_players()
        print("Бот запущен!")
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

if __name__ == "__main__":
    game = Game()
    bot = Bot(TOKEN, game)
    bot.run()

@app.route('/webapp')
def serve_webapp():
    return app.send_static_file('index.html')

@app.route('/api/command', methods=['POST'])
def handle_command():
    data = request.json
    command = data.get('command')
    chat_id = data.get('chat_id')
    role = data.get('role')
    if not bot_instance or not chat_id or not command:
        return jsonify({"error": "Invalid request"}), 400
    
    player = bot_instance.game.get_player(chat_id)
    if command == 'hire' and role in EMPLOYEE_ROLES:
        success, message = player.hire_employee(role)
    elif command == 'project':
        success, message = player.take_project()
    elif command == 'upgrade':
        success, message = player.upgrade_office()
    else:
        return jsonify({"error": "Unknown command"}), 400
    
    bot_instance.game.save_players()
    return jsonify({"success": success, "message": message})

@app.route('/api/status', methods=['POST'])
def get_status():
    data = request.json
    chat_id = data.get('chat_id')
    if not bot_instance or not chat_id:
        return jsonify({"error": "Invalid request"}), 400
    
    player = bot_instance.game.get_player(chat_id)
    status = {
        "balance": player.balance,
        "reputation": player.reputation,
        "employees": player.employees,
        "projects": player.projects,
        "paei": player.paei,
        "stage": f"{bot_instance.game.stage_emoji[player.stage]} {player.stage}",
        "employee_roles": player.employee_roles
    }
    return jsonify(status)