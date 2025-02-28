const tg = window.Telegram.WebApp;
tg.ready();

const user = tg.initDataUnsafe.user;
const chat_id = user ? user.id : null;

if (!chat_id) {
    document.getElementById('status').innerHTML = "Ошибка: Не удалось определить chat_id";
}

function sendCommand(command, role = null, action = null) {
    if (!chat_id) {
        showMessage("Ошибка: Не удалось определить chat_id", true);
        return;
    }
    const body = { command: command, chat_id: chat_id };
    if (role) body.role = role;
    if (action) body.action = action;
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
            if (data.event) {
                showMessage(data.event.message, false, data.event.options);
            } else {
                showMessage(data.message || "Действие выполнено");
            }
        } else {
            showMessage(data.message || "Ошибка выполнения команды", true);
        }
    })
    .catch(error => {
        showMessage("Ошибка связи с сервером: " + error.message, true);
    });
}

function updateStatus() {
    const statusElement = document.getElementById('status');
    if (!chat_id || !statusElement) {
        if (statusElement) statusElement.innerHTML = "Ошибка: Не удалось загрузить статус";
        return;
    }
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
        statusElement.innerHTML = `
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
        statusElement.innerHTML = "Ошибка загрузки статуса: " + error.message;
    });
}

function showMessage(message, isError = false, options = null) {
    const messageBox = document.getElementById('message');
    if (!messageBox) return;
    
    messageBox.innerHTML = message; // Используем innerHTML для поддержки кнопок
    messageBox.className = 'message-box' + (isError ? ' error' : options ? ' event' : '');
    
    if (options) {
        const optionsDiv = document.createElement('div');
        options.forEach(option => {
            const button = document.createElement('button');
            button.textContent = option.text;
            button.addEventListener('click', () => {
                sendCommand('event', null, option.action);
            });
            optionsDiv.appendChild(button);
        });
        messageBox.appendChild(optionsDiv);
    }
}

document.getElementById('hire').addEventListener('click', () => {
    const hireMenu = document.getElementById('hire-menu');
    const actions = document.querySelector('.actions');
    if (hireMenu && actions) {
        hireMenu.style.display = 'block';
        actions.style.display = 'none';
    }
});

document.getElementById('project').addEventListener('click', () => sendCommand('project'));
document.getElementById('upgrade').addEventListener('click', () => sendCommand('upgrade'));

document.querySelectorAll('.role-btn').forEach(button => {
    button.addEventListener('click', () => {
        const role = button.getAttribute('data-role');
        sendCommand('hire', role);
        const hireMenu = document.getElementById('hire-menu');
        const actions = document.querySelector('.actions');
        if (hireMenu && actions) {
            hireMenu.style.display = 'none';
            actions.style.display = 'block';
        }
    });
});

updateStatus();

tg.MainButton.setText('Играть в DigitalDynasty').show();
tg.onEvent('mainButtonClicked', () => updateStatus());