/* ============================================================
   TaskFlow — app.js
   Vanilla JS | localStorage persistence | No dependencies
   ============================================================ */

// ─── DB helpers ───────────────────────────────────────────────
const DB_KEY = 'taskflow_db';

function getDB() {
  const raw = localStorage.getItem(DB_KEY);
  if (raw) return JSON.parse(raw);
  const initial = { users: [], todos: [] };
  localStorage.setItem(DB_KEY, JSON.stringify(initial));
  return initial;
}

function saveDB(db) {
  localStorage.setItem(DB_KEY, JSON.stringify(db));
}

// ─── Session helpers ──────────────────────────────────────────
function getCurrentUser() {
  const raw = localStorage.getItem('currentUser');
  return raw ? JSON.parse(raw) : null;
}

function setCurrentUser(user) {
  localStorage.setItem('currentUser', JSON.stringify(user));
}

function clearCurrentUser() {
  localStorage.removeItem('currentUser');
}

// ─── Screen router ────────────────────────────────────────────
function showScreen(id) {
  document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
  const target = document.getElementById(id);
  if (target) {
    target.classList.add('active');
    // Re-trigger slide-up animation
    target.querySelectorAll('.slide-up').forEach(el => {
      el.style.animation = 'none';
      el.offsetHeight; // reflow
      el.style.animation = '';
    });
  }
}

// ─── Error / success display ──────────────────────────────────
function showError(elId, msg) {
  const el = document.getElementById(elId);
  if (!el) return;
  el.textContent = msg;
  el.classList.add('show');
}

function clearError(elId) {
  const el = document.getElementById(elId);
  if (!el) return;
  el.textContent = '';
  el.classList.remove('show');
}

// ─── AUTH: Register ───────────────────────────────────────────
document.getElementById('form-register').addEventListener('submit', e => {
  e.preventDefault();
  clearError('register-error');
  clearError('register-success');

  const name     = document.getElementById('reg-name').value.trim();
  const email    = document.getElementById('reg-email').value.trim().toLowerCase();
  const password = document.getElementById('reg-password').value;

  if (!name || !email || !password) {
    showError('register-error', 'Preencha todos os campos obrigatórios.');
    return;
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    showError('register-error', 'Informe um e-mail válido.');
    return;
  }
  if (password.length < 6) {
    showError('register-error', 'A senha deve ter pelo menos 6 caracteres.');
    return;
  }

  const db = getDB();
  if (db.users.find(u => u.email === email)) {
    showError('register-error', 'Este e-mail já está cadastrado.');
    return;
  }

  db.users.push({ name, email, password });
  saveDB(db);

  document.getElementById('register-success').textContent = 'Conta criada! Redirecionando para o login…';
  document.getElementById('register-success').classList.add('show');

  // Reset form
  document.getElementById('form-register').reset();

  setTimeout(() => {
    clearError('register-success');
    showScreen('screen-login');
  }, 1500);
});

// ─── AUTH: Login ──────────────────────────────────────────────
document.getElementById('form-login').addEventListener('submit', e => {
  e.preventDefault();
  clearError('login-error');

  const email    = document.getElementById('login-email').value.trim().toLowerCase();
  const password = document.getElementById('login-password').value;

  if (!email || !password) {
    showError('login-error', 'Preencha o e-mail e a senha.');
    return;
  }

  const db = getDB();
  const user = db.users.find(u => u.email === email);

  if (!user) {
    showError('login-error', 'E-mail não encontrado. Verifique ou crie uma conta.');
    return;
  }
  if (user.password !== password) {
    showError('login-error', 'Senha incorreta. Tente novamente.');
    return;
  }

  setCurrentUser({ name: user.name, email: user.email });
  document.getElementById('form-login').reset();
  initDashboard();
});

// ─── AUTH: Logout ─────────────────────────────────────────────
document.getElementById('btn-logout').addEventListener('click', () => {
  clearCurrentUser();
  currentFilter = 'all';
  showScreen('screen-login');
});

// ─── Navigation links ─────────────────────────────────────────
document.getElementById('go-register').addEventListener('click', () => {
  clearError('login-error');
  showScreen('screen-register');
});
document.getElementById('go-login').addEventListener('click', () => {
  clearError('register-error');
  clearError('register-success');
  showScreen('screen-login');
});

// ─── DASHBOARD: Init ──────────────────────────────────────────
let currentFilter = 'all';

function initDashboard() {
  const user = getCurrentUser();
  if (!user) { showScreen('screen-login'); return; }

  document.getElementById('header-username').textContent = user.name;
  renderStats();
  renderTasks();
  showScreen('screen-dashboard');
}

// ─── DASHBOARD: Stats ─────────────────────────────────────────
function renderStats() {
  const user  = getCurrentUser();
  const db    = getDB();
  const todos = db.todos.filter(t => t.userId === user.email);
  const done  = todos.filter(t => t.done).length;
  const pending = todos.length - done;

  const stats = [
    { label: 'Total',      value: todos.length, color: 'from-indigo-500 to-violet-600', icon: '📋' },
    { label: 'Pendentes',  value: pending,       color: 'from-amber-500 to-orange-500', icon: '⏳' },
    { label: 'Concluídas', value: done,          color: 'from-emerald-500 to-teal-500', icon: '✅' },
  ];

  document.getElementById('stats-row').innerHTML = stats.map(s => `
    <div class="glass rounded-2xl p-4 flex flex-col gap-2 fade-in">
      <span class="text-xl">${s.icon}</span>
      <span class="text-2xl font-bold bg-gradient-to-br ${s.color} bg-clip-text text-transparent">${s.value}</span>
      <span class="text-xs text-slate-400 font-medium">${s.label}</span>
    </div>
  `).join('');
}

// ─── DASHBOARD: Add Task ──────────────────────────────────────
document.getElementById('form-add-task').addEventListener('submit', e => {
  e.preventDefault();
  clearError('task-error');

  const title = document.getElementById('task-title').value.trim();
  const type  = document.getElementById('task-type').value;
  const desc  = document.getElementById('task-desc').value.trim();

  if (!title) {
    showError('task-error', 'O título da tarefa é obrigatório.');
    return;
  }

  const user = getCurrentUser();
  const db   = getDB();

  db.todos.push({
    id:          Date.now(),
    userId:      user.email,
    title,
    type,
    description: desc,
    done:        false,
    createdAt:   new Date().toISOString(),
  });

  saveDB(db);
  document.getElementById('form-add-task').reset();
  renderStats();
  renderTasks();
});

// ─── DASHBOARD: Filter buttons ────────────────────────────────
document.getElementById('filter-btns').addEventListener('click', e => {
  const btn = e.target.closest('[data-filter]');
  if (!btn) return;

  currentFilter = btn.dataset.filter;

  document.querySelectorAll('.filter-btn').forEach(b => {
    b.classList.remove('active-filter');
    b.style.cssText = '';
  });

  btn.classList.add('active-filter');
  renderTasks();
});

// Style active filter button
function styleFilterBtns() {
  document.querySelectorAll('.filter-btn').forEach(btn => {
    const isActive = btn.classList.contains('active-filter');
    btn.style.background     = isActive ? 'rgba(99,102,241,0.25)' : 'rgba(255,255,255,0.05)';
    btn.style.border         = isActive ? '1px solid rgba(99,102,241,0.4)' : '1px solid rgba(255,255,255,0.08)';
    btn.style.color          = isActive ? '#a5b4fc' : '#94a3b8';
  });
}

// ─── DASHBOARD: Render Tasks ──────────────────────────────────
const TYPE_META = {
  work:     { label: 'Trabalho', badgeClass: 'badge-work',     emoji: '💼' },
  personal: { label: 'Pessoal',  badgeClass: 'badge-personal', emoji: '🙂' },
  study:    { label: 'Estudos',  badgeClass: 'badge-study',    emoji: '📚' },
};

function renderTasks() {
  styleFilterBtns();

  const user  = getCurrentUser();
  const db    = getDB();
  let todos   = db.todos.filter(t => t.userId === user.email);

  // Sort: pending first, then done
  todos.sort((a, b) => {
    if (a.done === b.done) return b.id - a.id;
    return a.done ? 1 : -1;
  });

  // Filter
  if (currentFilter === 'pending') todos = todos.filter(t => !t.done);
  if (currentFilter === 'done')    todos = todos.filter(t =>  t.done);

  const container = document.getElementById('task-list');

  if (!todos.length) {
    container.innerHTML = `
      <div class="glass rounded-2xl p-10 text-center fade-in">
        <div class="text-4xl mb-3">🗂️</div>
        <p class="text-slate-400 text-sm font-medium">
          ${currentFilter === 'done'    ? 'Nenhuma tarefa concluída ainda.'    :
            currentFilter === 'pending' ? 'Nenhuma tarefa pendente. Bom trabalho! 🎉' :
                                          'Nenhuma tarefa cadastrada ainda.'}
        </p>
      </div>`;
    return;
  }

  container.innerHTML = todos.map(todo => {
    const meta = TYPE_META[todo.type] || TYPE_META.work;
    const doneClass = todo.done ? 'done' : '';
    const dateStr = new Date(todo.createdAt).toLocaleDateString('pt-BR', { day:'2-digit', month:'short' });

    return `
      <div class="task-card ${doneClass} rounded-2xl p-5 fade-in" data-id="${todo.id}">
        <div class="flex items-start justify-between gap-4">
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2 flex-wrap mb-2">
              <span class="badge ${meta.badgeClass} text-xs font-semibold px-2.5 py-0.5 rounded-full">
                ${meta.emoji} ${meta.label}
              </span>
              <span class="text-slate-500 text-xs">${dateStr}</span>
              ${todo.done ? '<span class="text-emerald-400 text-xs font-medium">✓ Concluída</span>' : ''}
            </div>
            <h4 class="task-title text-sm font-semibold text-white mb-1 truncate">${escapeHtml(todo.title)}</h4>
            ${todo.description
              ? `<p class="text-slate-400 text-xs leading-relaxed line-clamp-2">${escapeHtml(todo.description)}</p>`
              : ''}
          </div>
          <div class="flex flex-col gap-2 flex-shrink-0">
            ${!todo.done ? `
              <button class="btn-complete px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap"
                      onclick="completeTask(${todo.id})">
                ✓ Concluir
              </button>
            ` : ''}
            <button class="btn-delete px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap"
                    onclick="deleteTask(${todo.id})">
              🗑 Excluir
            </button>
          </div>
        </div>
      </div>`;
  }).join('');
}

// ─── DASHBOARD: Complete Task ─────────────────────────────────
function completeTask(id) {
  const db   = getDB();
  const todo = db.todos.find(t => t.id === id);
  if (todo) { todo.done = true; saveDB(db); }
  renderStats();
  renderTasks();
}

// ─── DASHBOARD: Delete Task ───────────────────────────────────
function deleteTask(id) {
  const db = getDB();
  db.todos = db.todos.filter(t => t.id !== id);
  saveDB(db);
  renderStats();
  renderTasks();
}

// ─── Utils ────────────────────────────────────────────────────
function escapeHtml(str) {
  const div = document.createElement('div');
  div.appendChild(document.createTextNode(str));
  return div.innerHTML;
}

// ─── Boot ─────────────────────────────────────────────────────
(function boot() {
  const user = getCurrentUser();
  if (user) {
    initDashboard();
  } else {
    showScreen('screen-login');
  }
})();
