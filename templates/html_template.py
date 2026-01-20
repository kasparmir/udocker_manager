"""HTML šablona - Moderní design"""

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="cs">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UDocker Manager</title>
    <style>
        :root {
            --primary: #6366f1;
            --primary-dark: #4f46e5;
            --success: #10b981;
            --danger: #ef4444;
            --warning: #f59e0b;
            --info: #3b82f6;
            --bg: #0f172a;
            --bg-secondary: #1e293b;
            --bg-card: #1e293b;
            --text: #e2e8f0;
            --text-muted: #94a3b8;
            --border: #334155;
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
        }
        
        .header {
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
            padding: 2rem;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.3);
            position: sticky;
            top: 0;
            z-index: 100;
        }
        
        .header h1 {
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }
        
        .header p {
            opacity: 0.9;
            font-size: 1rem;
        }
        
        .container {
            max-width: 1400px;
            margin: 2rem auto;
            padding: 0 2rem;
        }
        
        .tabs {
            display: flex;
            gap: 0.5rem;
            margin-bottom: 2rem;
            border-bottom: 2px solid var(--border);
            overflow-x: auto;
        }
        
        .tab {
            padding: 1rem 2rem;
            background: transparent;
            border: none;
            cursor: pointer;
            font-size: 1rem;
            font-weight: 500;
            color: var(--text-muted);
            border-radius: 8px 8px 0 0;
            transition: all 0.2s;
            white-space: nowrap;
        }
        
        .tab:hover {
            background: rgba(99, 102, 241, 0.1);
            color: var(--text);
        }
        
        .tab.active {
            background: var(--primary);
            color: white;
        }
        
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        
        .card {
            background: var(--bg-card);
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.3);
            border: 1px solid var(--border);
        }
        
        .card h2 {
            font-size: 1.5rem;
            margin-bottom: 1.5rem;
            color: var(--primary);
            font-weight: 600;
        }
        
        .form-group {
            margin-bottom: 1.5rem;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 500;
            color: var(--text);
        }
        
        .form-group input,
        .form-group textarea {
            width: 100%;
            padding: 0.875rem;
            background: var(--bg-secondary);
            border: 2px solid var(--border);
            border-radius: 8px;
            font-size: 1rem;
            color: var(--text);
            transition: all 0.2s;
        }
        
        .form-group input:focus,
        .form-group textarea:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        }
        
        .form-group textarea {
            resize: vertical;
            min-height: 100px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.9rem;
        }
        
        .btn {
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 0.95rem;
            font-weight: 500;
            transition: all 0.2s;
            margin: 0.25rem;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .btn:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }
        
        .btn:active {
            transform: translateY(0);
        }
        
        .btn-primary { background: var(--primary); color: white; }
        .btn-primary:hover { background: var(--primary-dark); }
        
        .btn-success { background: var(--success); color: white; }
        .btn-success:hover { background: #059669; }
        
        .btn-danger { background: var(--danger); color: white; }
        .btn-danger:hover { background: #dc2626; }
        
        .btn-warning { background: var(--warning); color: white; }
        .btn-warning:hover { background: #d97706; }
        
        .btn-info { background: var(--info); color: white; }
        .btn-info:hover { background: #2563eb; }
        
        .btn-sm {
            padding: 0.5rem 1rem;
            font-size: 0.875rem;
        }
        
        .container-item {
            background: var(--bg-secondary);
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 1rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-left: 4px solid var(--border);
            transition: all 0.2s;
            gap: 1rem;
        }
        
        .container-item:hover {
            transform: translateX(4px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }
        
        .container-item.managed { border-left-color: var(--primary); }
        .container-item.running { border-left-color: var(--success); }
        
        .container-info { flex: 1; min-width: 0; }
        
        .container-info h3 {
            font-size: 1.25rem;
            margin-bottom: 0.5rem;
            font-weight: 600;
        }
        
        .container-info p {
            color: var(--text-muted);
            font-size: 0.9rem;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        
        .container-actions {
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
        }
        
        .status {
            display: inline-flex;
            align-items: center;
            padding: 0.375rem 0.875rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            margin-right: 0.5rem;
            gap: 0.375rem;
        }
        
        .status.running {
            background: rgba(16, 185, 129, 0.2);
            color: #10b981;
        }
        
        .status.stopped {
            background: rgba(239, 68, 68, 0.2);
            color: #ef4444;
        }
        
        .status.managed {
            background: rgba(99, 102, 241, 0.2);
            color: #6366f1;
        }
        
        .status.unmanaged {
            background: rgba(245, 158, 11, 0.2);
            color: #f59e0b;
        }
        
        .status::before {
            content: '';
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: currentColor;
        }
        
        .help-text {
            font-size: 0.875rem;
            color: var(--text-muted);
            margin-top: 0.375rem;
        }
        
        .checkbox-group {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-top: 1rem;
        }
        
        .checkbox-group input[type="checkbox"] {
            width: 20px;
            height: 20px;
            cursor: pointer;
        }
        
        /* Modal styles */
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            z-index: 1000;
            align-items: center;
            justify-content: center;
        }
        
        .modal.active {
            display: flex;
        }
        
        .modal-content {
            background: var(--bg-card);
            border-radius: 16px;
            padding: 2rem;
            max-width: 500px;
            width: 90%;
            border: 1px solid var(--border);
        }
        
        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
        }
        
        .modal-header h3 {
            font-size: 1.5rem;
            color: var(--primary);
        }
        
        .modal-close {
            background: none;
            border: none;
            color: var(--text-muted);
            font-size: 1.5rem;
            cursor: pointer;
            padding: 0.25rem;
        }
        
        .progress-bar {
            width: 100%;
            height: 8px;
            background: var(--bg-secondary);
            border-radius: 4px;
            overflow: hidden;
            margin: 1rem 0;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--primary), var(--info));
            border-radius: 4px;
            transition: width 0.3s ease;
            animation: shimmer 2s infinite;
        }
        
        @keyframes shimmer {
            0% { background-position: -200% 0; }
            100% { background-position: 200% 0; }
        }
        
        .progress-fill {
            background: linear-gradient(
                90deg,
                var(--primary) 0%,
                var(--info) 50%,
                var(--primary) 100%
            );
            background-size: 200% 100%;
        }
        
        .progress-text {
            text-align: center;
            color: var(--text-muted);
            font-size: 0.9rem;
            margin-top: 0.5rem;
        }
        
        .spinner {
            border: 3px solid var(--border);
            border-top: 3px solid var(--primary);
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 1rem auto;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .empty-state {
            text-align: center;
            padding: 3rem 1rem;
            color: var(--text-muted);
        }
        
        .empty-state-icon {
            font-size: 4rem;
            margin-bottom: 1rem;
            opacity: 0.5;
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 0 1rem;
            }
            
            .container-item {
                flex-direction: column;
                align-items: stretch;
            }
            
            .container-actions {
                margin-top: 1rem;
            }
            
            .header h1 {
                font-size: 1.5rem;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🐋 UDocker Manager</h1>
        <p>Moderní webové rozhraní pro správu udocker kontejnerů</p>
    </div>

    <div class="container">
        <div class="tabs">
            <button class="tab active" onclick="switchTab('containers')">📦 Kontejnery</button>
            <button class="tab" onclick="switchTab('create')">➕ Vytvořit</button>
            <button class="tab" onclick="switchTab('images')">💿 Images</button>
        </div>

        <div id="containers" class="tab-content active">
            <div class="card">
                <h2>Kontejnery</h2>
                {% if containers %}
                {% for id, c in containers.items() %}
                <div class="container-item {% if c.running %}running{% endif %} {% if c.managed %}managed{% endif %}">
                    <div class="container-info">
                        <h3>{{ c.name }}</h3>
                        <p>📦 {{ c.image }} • 🆔 {{ id }}</p>
                        <div style="margin-top: 0.5rem;">
                            <span class="status {% if c.running %}running{% else %}stopped{% endif %}">
                                {% if c.running %}Běží{% else %}Zastaven{% endif %}
                            </span>
                            <span class="status {% if c.managed %}managed{% else %}unmanaged{% endif %}">
                                {% if c.managed %}Spravován{% else %}Externí{% endif %}
                            </span>
                            {% if c.autostart %}<span class="status running">🚀 Autostart</span>{% endif %}
                        </div>
                    </div>
                    <div class="container-actions">
                        <button class="btn btn-success btn-sm" onclick="start('{{ id }}')">▶ Start</button>
                        <button class="btn btn-warning btn-sm" onclick="stop('{{ id }}')">⏸ Stop</button>
                        {% if c.managed %}
                        <button class="btn btn-info btn-sm" onclick="edit('{{ id }}')">✏️ Editovat</button>
                        {% else %}
                        <button class="btn btn-info btn-sm" onclick="save('{{ id }}')">💾 Uložit</button>
                        {% endif %}
                        <button class="btn btn-danger btn-sm" onclick="del('{{ id }}')">🗑 Smazat</button>
                    </div>
                </div>
                {% endfor %}
                {% else %}
                <div class="empty-state">
                    <div class="empty-state-icon">📦</div>
                    <h3>Žádné kontejnery</h3>
                    <p>Vytvořte první kontejner pomocí záložky "Vytvořit"</p>
                </div>
                {% endif %}
            </div>
        </div>

        <div id="create" class="tab-content">
            <div class="card">
                <h2>Vytvořit nový kontejner</h2>
                <form id="createForm" onsubmit="createContainer(event)">
                    <div class="form-group">
                        <label>Název kontejneru *</label>
                        <input type="text" name="name" required placeholder="např. webserver">
                    </div>
                    <div class="form-group">
                        <label>Docker image *</label>
                        <input type="text" name="image" required placeholder="např. nginx:latest">
                        <p class="help-text">💡 Image bude automaticky stažen, pokud neexistuje</p>
                    </div>
                    <div class="form-group">
                        <label>Mapování portů</label>
                        <textarea name="ports" placeholder="8080:80
8443:443"></textarea>
                        <p class="help-text">Jeden port na řádek ve formátu HOST:CONTAINER</p>
                    </div>
                    <div class="form-group">
                        <label>Volumes</label>
                        <textarea name="volumes" placeholder="/host/path:/container/path
/data:/app/data"></textarea>
                        <p class="help-text">Jeden volume na řádek ve formátu HOST:CONTAINER</p>
                    </div>
                    <div class="form-group">
                        <label>Proměnné prostředí</label>
                        <textarea name="env" placeholder="DB_HOST=localhost
DB_PORT=5432"></textarea>
                        <p class="help-text">Jedna proměnná na řádek ve formátu KEY=VALUE</p>
                    </div>
                    <div class="form-group">
                        <label>Příkaz (volitelné)</label>
                        <input type="text" name="command" placeholder="/bin/bash">
                    </div>
                    <div class="checkbox-group">
                        <input type="checkbox" name="autostart" value="1" id="auto">
                        <label for="auto" style="margin: 0;">🚀 Spustit automaticky při startu manageru</label>
                    </div>
                    <button type="submit" class="btn btn-primary" style="margin-top: 1rem;">
                        ➕ Vytvořit a spustit kontejner
                    </button>
                </form>
            </div>
        </div>

        <div id="images" class="tab-content">
            <div class="card">
                <h2>Stáhnout image</h2>
                <form onsubmit="pullImage(event)" style="margin-bottom: 2rem;">
                    <div class="form-group">
                        <label>Docker image</label>
                        <input type="text" id="pullImageInput" required placeholder="např. alpine:latest">
                    </div>
                    <button type="submit" class="btn btn-primary">⬇ Stáhnout</button>
                    <button type="button" class="btn btn-danger" onclick="pruneImages()">🗑 Prune nepoužívané</button>
                </form>

                <h2>Dostupné images</h2>
                {% if images %}
                {% for img in images %}
                <div class="container-item">
                    <div class="container-info">
                        <h3>{{ img.full_name }}</h3>
                        <p>📦 {{ img.repository }} • 🏷️ {{ img.tag }}</p>
                    </div>
                    <button class="btn btn-danger btn-sm" onclick="delImage('{{ img.full_name }}')">🗑 Smazat</button>
                </div>
                {% endfor %}
                {% else %}
                <div class="empty-state">
                    <div class="empty-state-icon">💿</div>
                    <h3>Žádné images</h3>
                    <p>Stáhněte první image pomocí formuláře výše</p>
                </div>
                {% endif %}
            </div>
        </div>
    </div>

    <!-- Progress Modal -->
    <div id="progressModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h3 id="modalTitle">Stahuji image...</h3>
            </div>
            <div class="spinner"></div>
            <div class="progress-bar">
                <div class="progress-fill" id="progressFill" style="width: 0%"></div>
            </div>
            <div class="progress-text" id="progressText">Prosím čekejte...</div>
        </div>
    </div>

    <!-- Edit Container Modal -->
    <div id="editModal" class="modal">
        <div class="modal-content" style="max-width: 700px;">
            <div class="modal-header">
                <h3>✏️ Editovat kontejner</h3>
                <button class="modal-close" onclick="closeEditModal()">×</button>
            </div>
            <form id="editForm" onsubmit="updateContainer(event)">
                <input type="hidden" id="editContainerId" name="container_id">
                
                <div class="form-group">
                    <label>Název kontejneru *</label>
                    <input type="text" id="editName" name="name" required>
                </div>
                
                <div class="form-group">
                    <label>Docker image *</label>
                    <input type="text" id="editImage" name="image" required>
                    <p class="help-text">💡 Změna image automaticky stáhne novou verzi</p>
                </div>
                
                <div class="form-group">
                    <label>Mapování portů</label>
                    <textarea id="editPorts" name="ports"></textarea>
                </div>
                
                <div class="form-group">
                    <label>Volumes</label>
                    <textarea id="editVolumes" name="volumes"></textarea>
                </div>
                
                <div class="form-group">
                    <label>Proměnné prostředí</label>
                    <textarea id="editEnv" name="env"></textarea>
                </div>
                
                <div class="form-group">
                    <label>Příkaz</label>
                    <input type="text" id="editCommand" name="command">
                </div>
                
                <div class="checkbox-group">
                    <input type="checkbox" id="editAutostart" name="autostart" value="1">
                    <label for="editAutostart" style="margin: 0;">🚀 Autostart</label>
                </div>
                
                <div style="margin-top: 1.5rem;">
                    <button type="submit" class="btn btn-primary">💾 Uložit změny</button>
                    <button type="button" class="btn btn-danger" onclick="closeEditModal()">Zrušit</button>
                </div>
                
                <p class="help-text" style="margin-top: 1rem; color: #f59e0b;">
                    ⚠️ Upozornění: Starý kontejner bude smazán a nahrazen novým s aktualizovanou konfigurací.
                </p>
            </form>
        </div>
    </div>

    <script>
        function switchTab(name) {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            event.target.classList.add('active');
            document.getElementById(name).classList.add('active');
        }
        
        function showProgress(title, message) {
            const modal = document.getElementById('progressModal');
            document.getElementById('modalTitle').textContent = title;
            document.getElementById('progressText').textContent = message;
            document.getElementById('progressFill').style.width = '50%';
            modal.classList.add('active');
        }
        
        function hideProgress() {
            document.getElementById('progressModal').classList.remove('active');
        }
        
        async function createContainer(e) {
            e.preventDefault();
            const form = e.target;
            const formData = new FormData(form);
            
            showProgress('Vytváření kontejneru', 'Kontroluji image...');
            
            try {
                // Nejprve zkontrolujeme, zda potřebujeme stáhnout image
                const image = formData.get('image');
                const checkRes = await fetch(`/check-image/${encodeURIComponent(image)}`);
                const checkData = await checkRes.json();
                
                if (!checkData.exists) {
                    // Potřebujeme stáhnout image
                    document.getElementById('progressText').textContent = 'Stahuji image...';
                    
                    await new Promise((resolve, reject) => {
                        const eventSource = new EventSource(`/pull-progress/${encodeURIComponent(image)}`);
                        
                        eventSource.onmessage = function(event) {
                            try {
                                const data = JSON.parse(event.data);
                                
                                if (data.error) {
                                    eventSource.close();
                                    reject(new Error(data.error));
                                    return;
                                }
                                
                                if (data.progress) {
                                    document.getElementById('progressFill').style.width = data.progress + '%';
                                    document.getElementById('progressText').textContent = data.message || 'Stahuji...';
                                }
                                
                                if (data.success) {
                                    eventSource.close();
                                    resolve();
                                }
                            } catch (err) {
                                eventSource.close();
                                reject(err);
                            }
                        };
                        
                        eventSource.onerror = function() {
                            eventSource.close();
                            reject(new Error('Chyba při stahování image'));
                        };
                    });
                }
                
                // Nyní vytvoříme kontejner
                document.getElementById('progressText').textContent = 'Vytvářím kontejner...';
                document.getElementById('progressFill').style.width = '70%';
                
                const res = await fetch('/create', {
                    method: 'POST',
                    body: formData
                });
                const data = await res.json();
                
                document.getElementById('progressFill').style.width = '100%';
                
                hideProgress();
                
                if (data.success) {
                    alert('✅ ' + data.message);
                    location.reload();
                } else {
                    alert('❌ ' + data.message);
                }
            } catch (err) {
                hideProgress();
                alert('❌ Chyba: ' + err.message);
            }
        }
        
        async function pullImage(e) {
            e.preventDefault();
            const image = document.getElementById('pullImageInput').value;
            
            showProgress('Stahuji image', `Připojuji se k registru...`);
            
            try {
                const eventSource = new EventSource(`/pull-progress/${encodeURIComponent(image)}`);
                
                eventSource.onmessage = function(event) {
                    try {
                        const data = JSON.parse(event.data);
                        
                        if (data.error) {
                            eventSource.close();
                            hideProgress();
                            alert('❌ Chyba: ' + data.error);
                            return;
                        }
                        
                        if (data.progress) {
                            document.getElementById('progressFill').style.width = data.progress + '%';
                            document.getElementById('progressText').textContent = data.message || 'Stahuji...';
                        }
                        
                        if (data.success) {
                            eventSource.close();
                            hideProgress();
                            alert('✅ Image úspěšně stažen!');
                            location.reload();
                        }
                    } catch (err) {
                        console.error('Parse error:', err);
                    }
                };
                
                eventSource.onerror = function() {
                    eventSource.close();
                    hideProgress();
                    alert('❌ Chyba při stahování');
                };
                
            } catch (err) {
                hideProgress();
                alert('❌ Chyba: ' + err.message);
            }
        }
        
        async function start(id) {
            const res = await fetch(`/start/${id}`, {method: 'POST'});
            const data = await res.json();
            alert((data.success ? '✅ ' : '❌ ') + data.message);
            if (data.success) location.reload();
        }
        
        async function stop(id) {
            const res = await fetch(`/stop/${id}`, {method: 'POST'});
            const data = await res.json();
            alert((data.success ? '✅ ' : '❌ ') + data.message);
            if (data.success) location.reload();
        }
        
        async function del(id) {
            if (confirm('🗑️ Opravdu smazat tento kontejner?')) {
                const res = await fetch(`/delete/${id}`, {method: 'POST'});
                const data = await res.json();
                alert((data.success ? '✅ ' : '❌ ') + data.message);
                if (data.success) location.reload();
            }
        }
        
        async function save(id) {
            const res = await fetch(`/save/${id}`, {method: 'POST'});
            const data = await res.json();
            alert((data.success ? '✅ ' : '❌ ') + data.message);
            if (data.success) location.reload();
        }
        
        async function edit(id) {
            try {
                const res = await fetch(`/get-config/${id}`);
                const data = await res.json();
                
                if (data.success) {
                    document.getElementById('editContainerId').value = id;
                    document.getElementById('editName').value = data.config.name;
                    document.getElementById('editImage').value = data.config.image;
                    document.getElementById('editPorts').value = data.config.ports;
                    document.getElementById('editVolumes').value = data.config.volumes;
                    document.getElementById('editEnv').value = data.config.env;
                    document.getElementById('editCommand').value = data.config.command;
                    document.getElementById('editAutostart').checked = data.config.autostart;
                    
                    document.getElementById('editModal').classList.add('active');
                } else {
                    alert('❌ ' + data.message);
                }
            } catch (err) {
                alert('❌ Chyba: ' + err.message);
            }
        }
        
        function closeEditModal() {
            document.getElementById('editModal').classList.remove('active');
        }
        
        async function updateContainer(e) {
            e.preventDefault();
            
            if (!confirm('⚠️ Starý kontejner bude smazán a nahrazen novým. Pokračovat?')) {
                return;
            }
            
            const form = e.target;
            const formData = new FormData(form);
            const containerId = formData.get('container_id');
            
            showProgress('Aktualizuji kontejner', 'Mažu starý kontejner a vytvářím nový...');
            
            try {
                const res = await fetch(`/update/${containerId}`, {
                    method: 'POST',
                    body: formData
                });
                const data = await res.json();
                
                hideProgress();
                closeEditModal();
                
                if (data.success) {
                    alert('✅ ' + data.message);
                    location.reload();
                } else {
                    alert('❌ ' + data.message);
                }
            } catch (err) {
                hideProgress();
                alert('❌ Chyba: ' + err.message);
            }
        }
        
        async function pruneImages() {
            if (confirm('🗑️ Smazat nepoužívané images?')) {
                showProgress('Mazání images', 'Kontroluji nepoužívané images...');
                const res = await fetch('/prune-images', {method: 'POST'});
                const data = await res.json();
                hideProgress();
                alert((data.success ? '✅ ' : '❌ ') + data.message);
                location.reload();
            }
        }
        
        async function delImage(name) {
            if (confirm(`🗑️ Smazat image ${name}?`)) {
                const res = await fetch('/delete-image', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                    body: `image=${encodeURIComponent(name)}`
                });
                const data = await res.json();
                alert((data.success ? '✅ ' : '❌ ') + data.message);
                if (data.success) location.reload();
            }
        }
    </script>
</body>
</html>
"""