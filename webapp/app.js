const tg = window.Telegram.WebApp;
tg.ready();

const user = tg.initDataUnsafe.user;
const chat_id = user ? user.id : null;

if (!chat_id) {
    const statusElement = document.getElementById('status');
    if (statusElement) statusElement.innerHTML = "Ошибка: Не удалось определить chat_id";
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
    const balanceDisplay = document.getElementById('balance-display');
    const stage = document.getElementById('stage');
    const reputation = document.getElementById('reputation');
    const employees = document.getElementById('employees');
    const projects = document.getElementById('projects');
    const paeiP = document.getElementById('paei-p');
    const paeiA = document.getElementById('paei-a');
    const paeiEI = document.getElementById('paei-ei');

    if (!chat_id || !statusElement || !balanceDisplay || !stage || !reputation || !employees || !projects || !paeiP || !paeiA || !paeiEI) {
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
        stage.textContent = data.stage;
        reputation.textContent = `Репутация: ${data.reputation}`;
        employees.textContent = `Сотрудники: ${data.employees} (${Object.entries(data.employee_roles).filter(([_, count]) => count > 0).map(([role, count]) => `${role}: ${count}`).join(', ') || "Нет сотрудников"})`;
        projects.textContent = `Проекты: ${data.projects}`;
        paeiP.textContent = `P: ${data.paei.P}%`;
        paeiA.textContent = `A: ${data.paei.A}%`;
        paeiEI.textContent = `E: ${data.paei.E}% | I: ${data.paei.I}%`;
        balanceDisplay.textContent = `⏰ ${new Date().toLocaleTimeString()} $${data.balance.toLocaleString('en-US', { minimumIntegerDigits: 5, useGrouping: false })}`;
    })
    .catch(error => {
        statusElement.innerHTML = "Ошибка загрузки статуса: " + error.message;
    });
}

function showMessage(message, isError = false, options = null) {
    const messageBox = document.getElementById('message');
    if (!messageBox) return;
    
    messageBox.innerHTML = message;
    messageBox.className = 'message-box' + (isError ? ' error' : options ? ' event' : '');
    
    if (options) {
        const optionsDiv = document.createElement('div');
        options.forEach(option => {
            const button = document.createElement('button');
            button.innerHTML = `${option.text.split(' ')[0]} <span>${option.text.split(' ').slice(1).join(' ')}</span>`;
            button.addEventListener('click', () => {
                sendCommand('event', null, option.action);
            });
            optionsDiv.appendChild(button);
        });
        messageBox.innerHTML = ''; // Очищаем перед добавлением
        messageBox.appendChild(document.createTextNode(message));
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
document.getElementById('small_project').addEventListener('click', () => sendCommand('small_project'));

document.querySelectorAll('.role-btn').forEach(button => {
    button.addEventListener('click', () => {
        const role = button.getAttribute('data-role');
        sendCommand('hire', role);
        const hireMenu = document.getElementById('hire-menu');
        const actions = document.querySelector('.actions');
        if (hireMenu && actions) {
            hireMenu.style.display = 'none';
            actions.style.display = 'flex';
        }
    });
});

updateStatus();

tg.MainButton.setText('Играть в DigitalDynasty').show();
tg.onEvent('mainButtonClicked', () => updateStatus());