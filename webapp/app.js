const tg = window.Telegram.WebApp;
tg.ready();

const user = tg.initDataUnsafe.user;
const chat_id = user ? user.id : null;

if (!chat_id) {
    document.getElementById('status').innerHTML = "Ошибка: Не удалось определить chat_id";
}

function sendCommand(command, role = null, action = null) {
    if (!chat_id) {
        showNotification("Ошибка: Не удалось определить chat_id", true);
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
                showEvent(data.event);
            } else {
                showNotification(data.message || "Действие выполнено");
            }
        } else {
            showNotification(data.message || "Ошибка выполнения команды", true);
        }
    })
    .catch(error => {
        showNotification("Ошибка связи с сервером: " + error.message, true);
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
        hideEvent();
    })
    .catch(error => {
        statusElement.innerHTML = "Ошибка загрузки статуса: " + error.message;
    });
}

function showNotification(message, isError = false) {
    const messageBox = document.getElementById('message');
    if (!messageBox) return;
    messageBox.textContent = message;
    messageBox.className = 'message-box' + (isError ? ' error' : ''); // Устанавливаем класс
}

function showEvent(event) {
    const eventContainer = document.getElementById('event');
    const eventMessage = document.getElementById('event-message');
    const eventOptions = document.getElementById('event-options');
    if (!eventContainer || !eventMessage || !eventOptions) return;
    
    eventMessage.textContent = event.message;
    eventOptions.innerHTML = '';
    event.options.forEach(option => {
        const button = document.createElement('button');
        button.textContent = option.text;
        button.addEventListener('click', () => {
            sendCommand('event', null, option.action);
        });
        eventOptions.appendChild(button);
    });
    
    eventContainer.style.display = 'block';
}

function hideEvent() {
    const eventContainer = document.getElementById('event');
    if (eventContainer) eventContainer.style.display = 'none';
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