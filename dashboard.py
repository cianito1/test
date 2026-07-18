from flask import Flask, render_template_string, jsonify, request
import requests
import json
import os
from datetime import datetime

app = Flask(__name__)

# ============================================================
# CONFIGURACIÓN - ¡CAMBIAR ESTOS VALORES!
# ============================================================

# Token de tu bot de Discord (para obtener estadísticas)
BOT_TOKEN = os.environ.get('MTUyNzc5MTc2NTA0MDY2NDY2Nw.GBAip7.PXwLTJjTui2VP-udRN1Vu5ztMBSxE2ufcHoyY8', 'MTUyNzc5MTc2NTA0MDY2NDY2Nw.GBAip7.PXwLTJjTui2VP-udRN1Vu5ztMBSxE2ufcHoyY8')

# ID de tu bot (lo encuentras en Discord Developer Portal)
BOT_CLIENT_ID = '1527791765040664667'

# ============================================================
# HTML COMPLETO DEL DASHBOARD
# ============================================================

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 Dashboard - Economia Bot</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
            color: #ffffff;
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        /* HEADER */
        .header {
            text-align: center;
            padding: 40px 0;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 20px;
            margin-bottom: 30px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .header h1 {
            font-size: 3.5em;
            background: linear-gradient(45deg, #f7971e, #ffd200);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 1.2em;
            color: #a8b2d1;
        }
        
        .bot-avatar {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            border: 4px solid #ffd200;
            margin: 20px auto;
            display: block;
        }
        
        /* BOTONES DE INVITACIÓN */
        .invite-section {
            text-align: center;
            margin: 30px 0;
        }
        
        .btn {
            display: inline-block;
            padding: 15px 40px;
            border-radius: 50px;
            font-size: 1.1em;
            font-weight: bold;
            text-decoration: none;
            transition: all 0.3s ease;
            margin: 0 10px;
            border: none;
            cursor: pointer;
        }
        
        .btn-invite {
            background: linear-gradient(45deg, #5865F2, #4752C4);
            color: white;
        }
        
        .btn-invite:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(88, 101, 242, 0.4);
        }
        
        .btn-support {
            background: linear-gradient(45deg, #ED4245, #C62828);
            color: white;
        }
        
        .btn-support:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(237, 66, 69, 0.4);
        }
        
        .btn-github {
            background: linear-gradient(45deg, #24292e, #1a1e22);
            color: white;
        }
        
        .btn-github:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
        }
        
        /* ESTADÍSTICAS */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        
        .stat-card {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 25px;
            text-align: center;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: transform 0.3s ease;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
        }
        
        .stat-icon {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .stat-number {
            font-size: 2.5em;
            font-weight: bold;
            color: #ffd200;
        }
        
        .stat-label {
            color: #a8b2d1;
            margin-top: 5px;
        }
        
        /* COMANDOS */
        .commands-section {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 20px;
            padding: 30px;
            margin: 30px 0;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .commands-section h2 {
            color: #ffd200;
            margin-bottom: 20px;
            text-align: center;
        }
        
        .command-category {
            margin: 20px 0;
            padding: 15px;
            background: rgba(255, 255, 255, 0.03);
            border-radius: 10px;
            border-left: 4px solid #5865F2;
        }
        
        .command-category h3 {
            color: #a8b2d1;
            margin-bottom: 10px;
        }
        
        .command-item {
            display: inline-block;
            background: rgba(88, 101, 242, 0.2);
            padding: 5px 15px;
            border-radius: 20px;
            margin: 5px;
            font-size: 0.9em;
            font-family: 'Courier New', monospace;
        }
        
        /* FOOTER */
        .footer {
            text-align: center;
            padding: 30px;
            color: #a8b2d1;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            margin-top: 30px;
        }
        
        .status-online {
            color: #57F287;
        }
        
        .status-offline {
            color: #ED4245;
        }
        
        /* LOADING */
        .loading {
            text-align: center;
            padding: 20px;
        }
        
        .spinner {
            border: 4px solid rgba(255, 255, 255, 0.1);
            border-top: 4px solid #ffd200;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- HEADER -->
        <div class="header">
            {% if bot_info.avatar_url %}
            <img src="{{ bot_info.avatar_url }}" alt="Bot Avatar" class="bot-avatar">
            {% endif %}
            <h1>🤖 {{ bot_info.name }}</h1>
            <p>{{ bot_info.description or 'Bot de economía completo con tienda, apuestas y más.' }}</p>
            <p style="margin-top: 10px;">
                <span class="{% if bot_info.status == 'online' %}status-online{% else %}status-offline{% endif %}">
                    ● {{ bot_info.status|capitalize }}
                </span>
                &nbsp;|&nbsp; 🆔 {{ bot_info.client_id }}
            </p>
        </div>
        
        <!-- BOTONES DE INVITACIÓN -->
        <div class="invite-section">
            <a href="https://discord.com/oauth2/authorize?client_id={{ bot_info.client_id }}&permissions=8&scope=bot%20applications.commands" 
               target="_blank" class="btn btn-invite">
                ➕ Invitar Bot
            </a>
            <a href="https://discord.gg/tu-servidor-soporte" target="_blank" class="btn btn-support">
                🆘 Servidor Soporte
            </a>
            <a href="https://github.com/tu-usuario/tu-repo" target="_blank" class="btn btn-github">
                📂 GitHub
            </a>
        </div>
        
        <!-- ESTADÍSTICAS -->
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-icon">🏛️</div>
                <div class="stat-number">{{ bot_info.guild_count or 0 }}</div>
                <div class="stat-label">Servidores</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">👥</div>
                <div class="stat-number">{{ bot_info.user_count or 0 }}</div>
                <div class="stat-label">Usuarios</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">📊</div>
                <div class="stat-number">{{ bot_info.command_count or 0 }}</div>
                <div class="stat-label">Comandos</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">💰</div>
                <div class="stat-number">{{ bot_info.total_money or 0 }}</div>
                <div class="stat-label">Economía Total</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">🕒</div>
                <div class="stat-number">{{ bot_info.uptime or '0h' }}</div>
                <div class="stat-label">Tiempo Activo</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">🎮</div>
                <div class="stat-number">{{ bot_info.active_users or 0 }}</div>
                <div class="stat-label">Usuarios Activos</div>
            </div>
        </div>
        
        <!-- COMANDOS -->
        <div class="commands-section">
            <h2>📋 Comandos Disponibles</h2>
            
            {% for category, commands in bot_info.commands_by_category.items() %}
            <div class="command-category">
                <h3>{{ category }}</h3>
                {% for cmd in commands %}
                <span class="command-item">{{ cmd }}</span>
                {% endfor %}
            </div>
            {% endfor %}
        </div>
        
        <!-- FOOTER -->
        <div class="footer">
            <p>🤖 {{ bot_info.name }} v{{ bot_info.version or '2.0.0' }}</p>
            <p style="font-size: 0.8em;">Última actualización: {{ bot_info.last_update or 'N/A' }}</p>
        </div>
    </div>
</body>
</html>
"""

# ============================================================
# FUNCIONES PARA OBTENER DATOS DEL BOT
# ============================================================

def get_bot_info():
    """Obtiene información del bot desde Discord API"""
    try:
        # Obtener info básica del bot
        headers = {'Authorization': f'Bot {BOT_TOKEN}'}
        
        # Información del bot
        bot_response = requests.get(
            f'https://discord.com/api/v10/applications/{BOT_CLIENT_ID}',
            headers=headers
        )
        
        if bot_response.status_code == 200:
            bot_data = bot_response.json()
        else:
            bot_data = {}
        
        # Información de estadísticas (servidores)
        if BOT_TOKEN != 'TU_TOKEN_AQUI':
            # Si tenemos token válido, obtener info de servidores
            guilds_response = requests.get(
                'https://discord.com/api/v10/users/@me/guilds',
                headers=headers
            )
            
            if guilds_response.status_code == 200:
                guilds = guilds_response.json()
                guild_count = len(guilds)
                user_count = sum(1 for g in guilds if g.get('approximate_member_count'))
            else:
                guild_count = 0
                user_count = 0
        else:
            guild_count = 0
            user_count = 0
        
        return {
            'name': bot_data.get('name', 'Economia Bot'),
            'client_id': BOT_CLIENT_ID,
            'description': bot_data.get('description', 'Bot de economía completo con tienda, apuestas y más.'),
            'avatar_url': f"https://cdn.discordapp.com/app-icons/{BOT_CLIENT_ID}/{bot_data.get('icon', '')}.png" if bot_data.get('icon') else None,
            'guild_count': guild_count,
            'user_count': user_count * 20,  # Estimación
            'command_count': 50,  # Número total de comandos
            'total_money': 1250000,  # Economía total simulada
            'uptime': '72h',
            'active_users': 234,
            'status': 'online',
            'version': '2.0.0',
            'last_update': datetime.now().strftime('%d/%m/%Y %H:%M'),
            'commands_by_category': {
                '💰 Economía': ['.bal', '.dep', '.with', '.transfer', '.daily', '.claim'],
                '🎮 Actividades': ['.work', '.slut', '.crime', '.rob'],
                '🐔 Pollos': ['.bet', '.chicken', '.chicken_top'],
                '🛍️ Tienda': ['.shop', '.buy', '.inventory', '.use'],
                '🎰 Casino': ['.slots', '.dice', '.roulette', '.blackjack'],
                '📊 Mercado': ['.crypto', '.stocks', '.loan', '.pay_loan'],
                '🎰 Sorteos': ['.raffle', '.join_raffle', '.auction'],
                '🏆 Rankings': ['.top', '.leaderboard'],
                '🛠️ Admin': ['.set-prefix', '.set-rewards', '.add-money', '.remove-money'],
                '👤 Perfil': ['.profile', '.set_profile']
            }
        }
        
    except Exception as e:
        # Si hay error, devolver datos de muestra
        return {
            'name': 'Economia Bot',
            'client_id': BOT_CLIENT_ID,
            'description': 'Bot de economía completo con tienda, apuestas y más.',
            'avatar_url': None,
            'guild_count': 0,
            'user_count': 0,
            'command_count': 50,
            'total_money': 1250000,
            'uptime': '72h',
            'active_users': 234,
            'status': 'online',
            'version': '2.0.0',
            'last_update': datetime.now().strftime('%d/%m/%Y %H:%M'),
            'commands_by_category': {
                '💰 Economía': ['.bal', '.dep', '.with', '.transfer', '.daily', '.claim'],
                '🎮 Actividades': ['.work', '.slut', '.crime', '.rob'],
                '🐔 Pollos': ['.bet', '.chicken', '.chicken_top'],
                '🛍️ Tienda': ['.shop', '.buy', '.inventory', '.use'],
                '🎰 Casino': ['.slots', '.dice', '.roulette', '.blackjack'],
                '📊 Mercado': ['.crypto', '.stocks', '.loan', '.pay_loan'],
                '🎰 Sorteos': ['.raffle', '.join_raffle', '.auction'],
                '🏆 Rankings': ['.top', '.leaderboard'],
                '🛠️ Admin': ['.set-prefix', '.set-rewards', '.add-money', '.remove-money'],
                '👤 Perfil': ['.profile', '.set_profile']
            }
        }

# ============================================================
# RUTAS DE FLASK
# ============================================================

@app.route('/')
def home():
    """Página principal del dashboard"""
    bot_info = get_bot_info()
    return render_template_string(HTML_TEMPLATE, bot_info=bot_info)

@app.route('/api/stats')
def api_stats():
    """API para obtener estadísticas en JSON"""
    bot_info = get_bot_info()
    return jsonify(bot_info)

@app.route('/health')
def health():
    """Endpoint de salud para Render"""
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})

@app.route('/invite')
def redirect_invite():
    """Redirecciona al enlace de invitación del bot"""
    invite_url = f"https://discord.com/oauth2/authorize?client_id={BOT_CLIENT_ID}&permissions=8&scope=bot%20applications.commands"
    return f'<meta http-equiv="refresh" content="0; url={invite_url}">'

# ============================================================
# INICIAR EL SERVIDOR
# ============================================================

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
