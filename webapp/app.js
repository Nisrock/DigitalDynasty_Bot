﻿const tg = window.Telegram.WebApp;
tg.ready();

const user = tg.initDataUnsafe.user;
const chat_id = user ? user.id : null;

if (!chat_id) {
    document.getElementById('status').innerHTML = "Ошибка: Не удалось определить chat_id";
}

function sendCommand(command, role = null) {
    if (chat_id) {
        const body = { command: command, chat_id: chat_id };
        if (role) body.role = role;
        fetch('/api/command', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                updateStatus();
                showNotification(data.message || "Действие выполнено"); // Показываем сообщение в интерфейсе
            } else {
                showNotification(data.message || "Ошибка выполнения команды", true); // Красный фон для ошибок
            }
        })
        .catch(error => {
            showNotification("Ошибка связи с сервером: " + error.message, true);
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
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
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

function showNotification(message, isError = false) {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.style.display = 'block';
    notification.style.backgroundColor = isError ? '#ffe0e0' : '#e0ffe0'; // Красный для ошибок, зелёный для успеха
    setTimeout(() => {
        notification.style.display = 'none';
    }, 3000); // Скрываем через 3 секунды
}

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

updateStatus();

tg.MainButton.setText('Играть в DigitalDynasty').show();
tg.onEvent('mainButtonClicked', () => updateStatus());