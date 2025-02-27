const tg = window.Telegram.WebApp;
tg.ready();

const user = tg.initDataUnsafe.user;
const chat_id = user ? user.id : null;

if (!chat_id) {
    document.getElementById('status').innerHTML = "Ошибка: Не удалось определить chat_id";
}

function sendCommand(command, role = null) {  // Убрали tech, так как пока не добавляем технологии
    if (chat_id) {
        const body = { command: command, chat_id: chat_id };
        if (role) body.role = role;
        fetch('/api/command', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateStatus();  // Автоматически обновляем статус после успешного действия
                alert(data.message);  // Оставляем уведомление для пользователя
            } else {
                alert(data.message || "Ошибка выполнения команды");
            }
        })
        .catch(error => {
            alert("Ошибка связи с сервером: " + error.message);
        });
    }
}

function updateStatus() {
    if (chat_id) {
        fetch('/api/status', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ chat_id: chat_id })
        })
        .then(response => response.json())
        .then(data => {
            const rolesText = Object.entries(data.employee_roles)
                .map(([role, count]) => count > 0 ? `${role}: ${count}` : '')
                .filter(Boolean)
                .join(', ') || "Нет сотрудников";
            document.getElementById('status').innerHTML = `
                <p>📍 Этап: ${data.stage}</p>
                <p>💰 Баланс: ${data.balance}</p>
                <p>⭐ Репутация: ${data.reputation}</p>
                <p>👥 Сотрудники: ${data.employees} (${rolesText})</p>
                <p>📈 Проекты: ${data.projects}</p>
                <p>⚙️ P: ${data.paei.P}% | 📋 A: ${data.paei.A}%</p>
                <p>💡 E: ${data.paei.E}% | 🤝 I: ${data.paei.I}%</p>
            `;
        })
        .catch(error => {
            document.getElementById('status').innerHTML = "Ошибка загрузки статуса: " + error.message;
        });
    }
}

// Обработчики кнопок
document.getElementById('hire').addEventListener('click', () => {
    document.getElementById('hire-menu').style.display = 'block';
    document.querySelector('.actions').style.display = 'none';
});

document.getElementById('project').addEventListener('click', () => sendCommand('project'));
document.getElementById('upgrade').addEventListener('click', () => sendCommand('upgrade'));

document.querySelectorAll('.role-btn').forEach(button => {
    button.addEventListener('click', () => {
        const role = button.getAttribute('data-role');
        sendCommand('hire', role);
        document.getElementById('hire-menu').style.display = 'none';
        document.querySelector('.actions').style.display = 'block';
    });
});

// Инициализация статуса
updateStatus();

// Главная кнопка теперь необязательна для обновления, но оставим её для удобства
tg.MainButton.setText('Играть в DigitalDynasty').show();
tg.onEvent('mainButtonClicked', () => updateStatus());