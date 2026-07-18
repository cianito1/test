from flask import Flask, render_template_string, jsonify
import os
from datetime import datetime

app = Flask(__name__)

# ============================================================
# CONFIGURACIÓN - SIN TOKEN
# ============================================================

# ID de tu bot (público, no es secreto)
BOT_CLIENT_ID = '1527791765040664667'

# Prefijo de tu bot (el que usas actualmente)
PREFIJO = '.'  # Cambia si tu bot usa otro

# ============================================================
# TUS COMANDOS REALES (con prefijo dinámico)
# ============================================================

def get_comandos_con_prefijo(prefijo):
    """Devuelve todos los comandos con el prefijo actual"""
    comandos_base = {
        # Economía
        'bal': {
            'descripcion': 'Muestra tu balance o el de otro usuario.',
            'uso': f'{prefijo}bal [@usuario]',
            'ejemplo': f'{prefijo}bal\n{prefijo}bal @Juan',
            'permisos': 'Todos los usuarios',
            'categoria': '💰 Economía'
        },
        'dep': {
            'descripcion': 'Deposita dinero de tu cartera al banco.',
            'uso': f'{prefijo}dep cantidad',
            'ejemplo': f'{prefijo}dep 1000\n{prefijo}dep all',
            'permisos': 'Todos los usuarios',
            'categoria': '💰 Economía'
        },
        'with': {
            'descripcion': 'Retira dinero del banco a tu cartera. Si no tienes suficiente, entras en deuda.',
            'uso': f'{prefijo}with cantidad\n{prefijo}with -cantidad (pagar deuda)',
            'ejemplo': f'{prefijo}with 500\n{prefijo}with -1000',
            'permisos': 'Todos los usuarios',
            'categoria': '💰 Economía'
        },
        'transfer': {
            'descripcion': 'Transfiere dinero de tu cartera a otro usuario (5% de impuesto).',
            'uso': f'{prefijo}transfer @usuario cantidad',
            'ejemplo': f'{prefijo}transfer @Juan 1000',
            'permisos': 'Todos los usuarios',
            'categoria': '💰 Economía'
        },
        'roulette': {
            'descripcion': 'Juega a la ruleta. Apuesta a rojo, negro o verde.',
            'uso': f'{prefijo}roulette cantidad color',
            'ejemplo': f'{prefijo}roulette 500 rojo',
            'permisos': 'Todos los usuarios',
            'categoria': '💰 Economía'
        },
        'blackjack': {
            'descripcion': 'Juega al blackjack contra la casa.',
            'uso': f'{prefijo}blackjack cantidad',
            'ejemplo': f'{prefijo}blackjack 1000',
            'permisos': 'Todos los usuarios',
            'categoria': '💰 Economía'
        },
        'claim': {
            'descripcion': 'Reclama tus ingresos acumulados por roles configurados.',
            'uso': f'{prefijo}claim',
            'ejemplo': f'{prefijo}claim',
            'permisos': 'Todos los usuarios',
            'categoria': '💰 Economía'
        },
        'daily': {
            'descripcion': 'Reclama tu recompensa diaria. Tu racha (streak) aumenta cada día.',
            'uso': f'{prefijo}daily',
            'ejemplo': f'{prefijo}daily',
            'permisos': 'Todos los usuarios',
            'categoria': '💰 Economía'
        },
        'loan': {
            'descripcion': 'Solicita un préstamo del banco (10% de interés, máximo 10,000).',
            'uso': f'{prefijo}loan cantidad',
            'ejemplo': f'{prefijo}loan 5000',
            'permisos': 'Todos los usuarios',
            'categoria': '💰 Economía'
        },
        'pay_loan': {
            'descripcion': 'Paga tu préstamo pendiente.',
            'uso': f'{prefijo}pay_loan cantidad\n{prefijo}pay_loan all',
            'ejemplo': f'{prefijo}pay_loan 1000',
            'permisos': 'Todos los usuarios',
            'categoria': '💰 Economía'
        },
        'loans': {
            'descripcion': 'Muestra tus préstamos activos.',
            'uso': f'{prefijo}loans',
            'ejemplo': f'{prefijo}loans',
            'permisos': 'Todos los usuarios',
            'categoria': '💰 Economía'
        },
        # Actividades
        'work': {
            'descripcion': 'Trabaja y gana dinero. Configurable con {p}set-rewards.',
            'uso': f'{prefijo}work',
            'ejemplo': f'{prefijo}work',
            'permisos': 'Todos los usuarios',
            'categoria': '🎮 Actividades'
        },
        'slut': {
            'descripcion': 'Arriesga tu dinero. Puedes ganar o perder. Configurable con {p}set-rewards.',
            'uso': f'{prefijo}slut',
            'ejemplo': f'{prefijo}slut',
            'permisos': 'Todos los usuarios',
            'categoria': '🎮 Actividades'
        },
        'crime': {
            'descripcion': 'Comete un crimen. Puedes ganar o perder. Configurable con {p}set-rewards.',
            'uso': f'{prefijo}crime',
            'ejemplo': f'{prefijo}crime',
            'permisos': 'Todos los usuarios',
            'categoria': '🎮 Actividades'
        },
        'rob': {
            'descripcion': 'Intenta robar a otro usuario. 35% de éxito.',
            'uso': f'{prefijo}rob @usuario',
            'ejemplo': f'{prefijo}rob @Juan',
            'permisos': 'Todos los usuarios',
            'categoria': '🎮 Actividades'
        },
        # Pollos
        'bet': {
            'descripcion': 'Apuesta tus pollos para ganar más dinero o perderlos.',
            'uso': f'{prefijo}bet cantidad',
            'ejemplo': f'{prefijo}bet 2\n{prefijo}bet all',
            'permisos': 'Todos los usuarios',
            'categoria': '🐔 Pollos'
        },
        'chicken': {
            'descripcion': 'Muestra información sobre tus pollos.',
            'uso': f'{prefijo}chicken',
            'ejemplo': f'{prefijo}chicken',
            'permisos': 'Todos los usuarios',
            'categoria': '🐔 Pollos'
        },
        'chicken_top': {
            'descripcion': 'Muestra el top de usuarios con más pollos.',
            'uso': f'{prefijo}chicken_top',
            'ejemplo': f'{prefijo}chicken_top',
            'permisos': 'Todos los usuarios',
            'categoria': '🐔 Pollos'
        },
        # Tienda
        'shop': {
            'descripcion': 'Muestra la tienda con todos los items disponibles.',
            'uso': f'{prefijo}shop',
            'ejemplo': f'{prefijo}shop',
            'permisos': 'Todos los usuarios',
            'categoria': '🛍️ Tienda'
        },
        'buy': {
            'descripcion': 'Compra un item de la tienda. La cantidad es opcional (1 por defecto).',
            'uso': f'{prefijo}buy "item" [cantidad]',
            'ejemplo': f'{prefijo}buy "Poción" 3',
            'permisos': 'Todos los usuarios',
            'categoria': '🛍️ Tienda'
        },
        'inventory': {
            'descripcion': 'Muestra tu inventario o el de otro usuario.',
            'uso': f'{prefijo}inventory [@usuario]',
            'ejemplo': f'{prefijo}inventory\n{prefijo}inventory @Juan',
            'permisos': 'Todos los usuarios',
            'categoria': '🛍️ Tienda'
        },
        'use': {
            'descripcion': 'Usa un item de tu inventario. Puede dar roles o efectos especiales.',
            'uso': f'{prefijo}use "item"',
            'ejemplo': f'{prefijo}use "Poción"',
            'permisos': 'Todos los usuarios',
            'categoria': '🛍️ Tienda'
        },
        # Casino
        'slots': {
            'descripcion': 'Juega a la tragamonedas. Gira 3 rodillos y gana según combinaciones.',
            'uso': f'{prefijo}slots cantidad',
            'ejemplo': f'{prefijo}slots 500',
            'permisos': 'Todos los usuarios',
            'categoria': '🎰 Casino'
        },
        'dice': {
            'descripcion': 'Lanza dados. Apuesta a un número (2-12) o a par/impar.',
            'uso': f'{prefijo}dice cantidad [número]',
            'ejemplo': f'{prefijo}dice 500 7\n{prefijo}dice 500',
            'permisos': 'Todos los usuarios',
            'categoria': '🎰 Casino'
        },
        # Rankings
        'top': {
            'descripcion': 'Muestra el top de usuarios con más dinero.',
            'uso': f'{prefijo}top [total/cartera/banco]',
            'ejemplo': f'{prefijo}top\n{prefijo}top cartera',
            'permisos': 'Todos los usuarios',
            'categoria': '🏆 Rankings'
        },
        'leaderboard': {
            'descripcion': 'Alias de {p}top.',
            'uso': f'{prefijo}leaderboard [total/cartera/banco]',
            'ejemplo': f'{prefijo}leaderboard',
            'permisos': 'Todos los usuarios',
            'categoria': '🏆 Rankings'
        },
        # Crypto
        'crypto': {
            'descripcion': 'Compra y vende criptomonedas (BTC, ETH, DOGE).',
            'uso': f'{prefijo}crypto prices\n{prefijo}crypto buy BTC cantidad\n{prefijo}crypto sell BTC cantidad\n{prefijo}crypto wallet',
            'ejemplo': f'{prefijo}crypto prices\n{prefijo}crypto buy BTC 0.1',
            'permisos': 'Todos los usuarios',
            'categoria': '📊 Mercado'
        },
        # Stocks
        'stocks': {
            'descripcion': 'Compra y vende acciones en el mercado de valores.',
            'uso': f'{prefijo}stocks prices\n{prefijo}stocks buy EMPRESA cantidad\n{prefijo}stocks sell EMPRESA cantidad\n{prefijo}stocks portfolio',
            'ejemplo': f'{prefijo}stocks prices\n{prefijo}stocks buy APPLE 10',
            'permisos': 'Todos los usuarios',
            'categoria': '📊 Mercado'
        },
        # Sorteos
        'raffle': {
            'descripcion': 'Administra sorteos. (Admin)',
            'uso': f'{prefijo}raffle create "nombre" "desc" precio max\n{prefijo}raffle list\n{prefijo}raffle draw id\n{prefijo}raffle delete id',
            'ejemplo': f'{prefijo}raffle create "Premio" "Sorteo" 100 50',
            'permisos': 'Administradores',
            'categoria': '🎰 Sorteos'
        },
        'join_raffle': {
            'descripcion': 'Únete a un sorteo comprando entradas.',
            'uso': f'{prefijo}join_raffle id [cantidad]',
            'ejemplo': f'{prefijo}join_raffle 1 2',
            'permisos': 'Todos los usuarios',
            'categoria': '🎰 Sorteos'
        },
        # Subastas
        'auction': {
            'descripcion': 'Sistema de subastas.',
            'uso': f'{prefijo}auction create "item" cantidad precio\n{prefijo}auction bid id cantidad\n{prefijo}auction list\n{prefijo}auction end id',
            'ejemplo': f'{prefijo}auction create "Espada" 1 500',
            'permisos': 'Todos los usuarios (create solo del dueño)',
            'categoria': '🎰 Sorteos'
        },
        # Admin - Configuración
        'set-prefix': {
            'descripcion': 'Cambia el prefijo del bot para este servidor.',
            'uso': f'{prefijo}set-prefix nuevo_prefijo',
            'ejemplo': f'{prefijo}set-prefix !',
            'permisos': 'Administradores',
            'categoria': '🛠️ Admin'
        },
        'set-moneda': {
            'descripcion': 'Cambia el símbolo de moneda para este servidor (acepta emojis).',
            'uso': f'{prefijo}set-moneda nuevo_simbolo',
            'ejemplo': f'{prefijo}set-moneda 💰',
            'permisos': 'Administradores',
            'categoria': '🛠️ Admin'
        },
        'set-cooldown': {
            'descripcion': 'Configura el tiempo de espera para work, slut, crime o rob.',
            'uso': f'{prefijo}set-cooldown comando tiempo',
            'ejemplo': f'{prefijo}set-cooldown work 5m',
            'permisos': 'Administradores',
            'categoria': '🛠️ Admin'
        },
        'set-rewards': {
            'descripcion': 'Configura el mínimo y máximo de recompensas para work, slut, crime.',
            'uso': f'{prefijo}set-rewards comando min max',
            'ejemplo': f'{prefijo}set-rewards work 100 300',
            'permisos': 'Administradores',
            'categoria': '🛠️ Admin'
        },
        'show-rewards': {
            'descripcion': 'Muestra las configuraciones actuales de recompensas.',
            'uso': f'{prefijo}show-rewards',
            'ejemplo': f'{prefijo}show-rewards',
            'permisos': 'Administradores',
            'categoria': '🛠️ Admin'
        },
        'set-update-channel': {
            'descripcion': 'Configura el canal para los mensajes de actualización.',
            'uso': f'{prefijo}set-update-channel #canal',
            'ejemplo': f'{prefijo}set-update-channel #anuncios',
            'permisos': 'Administradores',
            'categoria': '🛠️ Admin'
        },
        # Admin - Dinero
        'add-money': {
            'descripcion': 'Añade dinero a la cartera o banco de un usuario.',
            'uso': f'{prefijo}add-money @usuario cantidad [cartera/banco]',
            'ejemplo': f'{prefijo}add-money @Juan 1000',
            'permisos': 'Administradores',
            'categoria': '🛠️ Admin'
        },
        'remove-money': {
            'descripcion': 'Quita dinero de la cartera o banco de un usuario. Cantidad negativa añade dinero.',
            'uso': f'{prefijo}remove-money @usuario cantidad [cartera/banco]',
            'ejemplo': f'{prefijo}remove-money @Juan 500\n{prefijo}remove-money @Juan -1000',
            'permisos': 'Administradores',
            'categoria': '🛠️ Admin'
        },
        # Admin - Items
        'create-item': {
            'descripcion': 'Crea un nuevo item en la tienda con navegación paso a paso.',
            'uso': f'{prefijo}create-item ["nombre"]',
            'ejemplo': f'{prefijo}create-item "Espada"',
            'permisos': 'Administradores',
            'categoria': '🛠️ Admin'
        },
        'edit-item': {
            'descripcion': 'Edita una propiedad de un item existente.',
            'uso': f'{prefijo}edit-item "nombre" propiedad valor',
            'ejemplo': f'{prefijo}edit-item "Espada" precio 1000',
            'permisos': 'Administradores',
            'categoria': '🛠️ Admin'
        },
        'delete-item': {
            'descripcion': 'Elimina un item de la tienda permanentemente.',
            'uso': f'{prefijo}delete-item "nombre"',
            'ejemplo': f'{prefijo}delete-item "Item Viejo"',
            'permisos': 'Administradores',
            'categoria': '🛠️ Admin'
        },
        # Admin - Roles
        'role-income': {
            'descripcion': 'Configura un ingreso por rol con tiempo opcional.',
            'uso': f'{prefijo}role-income @rol cantidad [tiempo] [nombre]',
            'ejemplo': f'{prefijo}role-income @VIP 500 30m "Bono VIP"',
            'permisos': 'Administradores',
            'categoria': '🛠️ Admin'
        },
        'edit-role-income': {
            'descripcion': 'Edita una configuración de ingreso por rol específica.',
            'uso': f'{prefijo}edit-role-income @rol "nombre" campo valor',
            'ejemplo': f'{prefijo}edit-role-income @VIP "Bono VIP" salario 1000',
            'permisos': 'Administradores',
            'categoria': '🛠️ Admin'
        },
        'remove-role-income': {
            'descripcion': 'Elimina una o todas las configuraciones de ingreso de un rol.',
            'uso': f'{prefijo}remove-role-income @rol ["nombre"]',
            'ejemplo': f'{prefijo}remove-role-income @VIP "Bono extra"',
            'permisos': 'Administradores',
            'categoria': '🛠️ Admin'
        },
        'role-income-list': {
            'descripcion': 'Muestra todas las configuraciones de ingresos por rol.',
            'uso': f'{prefijo}role-income-list [@rol]',
            'ejemplo': f'{prefijo}role-income-list\n{prefijo}role-income-list @VIP',
            'permisos': 'Administradores',
            'categoria': '🛠️ Admin'
        },
        # Admin - Respuestas
        'set-reply': {
            'descripcion': 'Configura respuestas personalizadas para comandos.',
            'uso': f'{prefijo}set-reply comando mensaje',
            'ejemplo': f'{prefijo}set-reply work "Ganaste (monto) monedas"',
            'permisos': 'Administradores',
            'categoria': '🛠️ Admin'
        },
        'remove-reply': {
            'descripcion': 'Elimina respuestas personalizadas.',
            'uso': f'{prefijo}remove-reply comando [bueno/malo]',
            'ejemplo': f'{prefijo}remove-reply work',
            'permisos': 'Administradores',
            'categoria': '🛠️ Admin'
        },
        'show-replies': {
            'descripcion': 'Muestra todas las respuestas personalizadas configuradas.',
            'uso': f'{prefijo}show-replies [comando]',
            'ejemplo': f'{prefijo}show-replies\n{prefijo}show-replies work',
            'permisos': 'Administradores',
            'categoria': '🛠️ Admin'
        },
        # Admin - Logs y Backup
        'logs': {
            'descripcion': 'Gestiona los logs del bot.',
            'uso': f'{prefijo}logs view/clear/channel',
            'ejemplo': f'{prefijo}logs view',
            'permisos': 'Administradores',
            'categoria': '🛠️ Admin'
        },
        'backup': {
            'descripcion': 'Gestiona backups de la base de datos.',
            'uso': f'{prefijo}backup create/list/restore',
            'ejemplo': f'{prefijo}backup create',
            'permisos': 'Dueño del bot',
            'categoria': '🛠️ Admin'
        },
        'maintenance': {
            'descripcion': 'Activa o desactiva el modo mantenimiento del bot.',
            'uso': f'{prefijo}maintenance on/off',
            'ejemplo': f'{prefijo}maintenance on',
            'permisos': 'Dueño del bot',
            'categoria': '🛠️ Admin'
        },
        'inactive': {
            'descripcion': 'Gestiona usuarios inactivos.',
            'uso': f'{prefijo}inactive list/warn/remove',
            'ejemplo': f'{prefijo}inactive list',
            'permisos': 'Administradores',
            'categoria': '🛠️ Admin'
        },
        # Otros
        'update': {
            'descripcion': 'Anuncia una actualización del bot con temporizador.',
            'uso': f'{prefijo}update tiempo [yes/no]',
            'ejemplo': f'{prefijo}update 30m yes',
            'permisos': 'Dueño del bot',
            'categoria': '🛠️ Admin'
        },
        # Perfil
        'profile': {
            'descripcion': 'Muestra el perfil de un usuario.',
            'uso': f'{prefijo}profile [@usuario]',
            'ejemplo': f'{prefijo}profile\n{prefijo}profile @Juan',
            'permisos': 'Todos los usuarios',
            'categoria': '👤 Perfil'
        },
        'set_profile': {
            'descripcion': 'Personaliza tu perfil.',
            'uso': f'{prefijo}set_profile desc/banner/color',
            'ejemplo': f'{prefijo}set_profile desc "Soy un programador"',
            'permisos': 'Todos los usuarios',
            'categoria': '👤 Perfil'
        }
    }
    return comandos_base

# ============================================================
# DATOS REALES DE TU BOT (¡ACTUALIZA ESTOS NÚMEROS!)
# ============================================================

# ⚠️ ¡IMPORTANTE! Actualiza estos números con los datos REALES de tu bot
DATOS_REALES = {
    'servidores': 1,        # ¿Cuántos servidores tiene tu bot realmente?
    'usuarios': 3,         # ¿Cuántos usuarios totales?
    'comandos': len(get_comandos_con_prefijo(PREFIJO)),  # Automático
    'economia_total': 24,  # Economía total en tu bot
    'tiempo_activo': '15h',  # Tiempo que lleva online
    'usuarios_activos': 3, # Usuarios activos hoy
    'nombre': 'Economia Bot',
    'version': '2.0.0',
}

# ============================================================
# GENERAR LISTA DE COMANDOS POR CATEGORÍA
# ============================================================

def get_comandos_por_categoria(prefijo):
    """Agrupa comandos por categoría para mostrar en el dashboard"""
    comandos = get_comandos_con_prefijo(prefijo)
    categorias = {}
    
    for cmd, info in comandos.items():
        cat = info.get('categoria', '📂 Otros')
        if cat not in categorias:
            categorias[cat] = []
        categorias[cat].append(cmd)
    
    return categorias

# ============================================================
# HTML DEL DASHBOARD (solo la parte de estadísticas reales)
# ============================================================

# ... (el HTML es el mismo que antes, pero con los datos reales)

# ============================================================
# RUTAS DE FLASK
# ============================================================

@app.route('/')
def home():
    """Página principal del dashboard"""
    comandos = get_comandos_con_prefijo(PREFIJO)
    categorias = get_comandos_por_categoria(PREFIJO)
    
    # Preparar datos para el template
    bot_info = {
        'name': DATOS_REALES['nombre'],
        'client_id': BOT_CLIENT_ID,
        'description': '🤖 Bot de economía completo con tienda, apuestas, sistema de pollos y más.',
        'guild_count': DATOS_REALES['servidores'],
        'user_count': DATOS_REALES['usuarios'],
        'command_count': DATOS_REALES['comandos'],
        'total_money': f"{DATOS_REALES['economia_total']:,}".replace(',', '.'),
        'uptime': DATOS_REALES['tiempo_activo'],
        'active_users': DATOS_REALES['usuarios_activos'],
        'status': 'online',
        'version': DATOS_REALES['version'],
        'prefijo': PREFIJO,
        'last_update': datetime.now().strftime('%d/%m/%Y %H:%M'),
        'commands_by_category': categorias,
        'comandos_help': comandos
    }
    
    return render_template_string(HTML_TEMPLATE, bot_info=bot_info)

# ============================================================
# HTML COMPLETO DEL DASHBOARD
# ============================================================

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 Dashboard - {{ bot_info.name }}</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            background: #0a0a0f;
            color: #e0e0e0;
            min-height: 100vh;
            overflow-x: hidden;
        }
        
        /* ===== MENÚ LATERAL ===== */
        .sidebar {
            position: fixed;
            top: 0;
            left: 0;
            width: 280px;
            height: 100vh;
            background: linear-gradient(180deg, #0f0f1a, #1a1a2e);
            border-right: 1px solid rgba(255, 255, 255, 0.05);
            padding: 30px 20px;
            z-index: 1000;
            overflow-y: auto;
            transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .sidebar::-webkit-scrollbar { width: 4px; }
        .sidebar::-webkit-scrollbar-track { background: transparent; }
        .sidebar::-webkit-scrollbar-thumb { background: #5865F2; border-radius: 10px; }
        
        .sidebar-brand {
            text-align: center;
            padding-bottom: 30px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            margin-bottom: 25px;
        }
        
        .sidebar-brand .logo-icon { font-size: 3em; margin-bottom: 10px; }
        .sidebar-brand h2 {
            font-size: 1.3em;
            background: linear-gradient(135deg, #f7971e, #ffd200);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .sidebar-brand .version {
            font-size: 0.7em;
            color: #5865F2;
            background: rgba(88, 101, 242, 0.15);
            padding: 3px 12px;
            border-radius: 20px;
            display: inline-block;
            margin-top: 5px;
        }
        
        .sidebar-menu { list-style: none; }
        .sidebar-menu li { margin-bottom: 4px; }
        .sidebar-menu a {
            display: flex;
            align-items: center;
            gap: 14px;
            padding: 12px 16px;
            color: #a8b2d1;
            text-decoration: none;
            border-radius: 12px;
            transition: all 0.3s ease;
            font-size: 0.95em;
            position: relative;
        }
        .sidebar-menu a:hover {
            background: rgba(88, 101, 242, 0.1);
            color: #ffffff;
            transform: translateX(5px);
        }
        .sidebar-menu a.active {
            background: linear-gradient(135deg, rgba(88, 101, 242, 0.2), rgba(88, 101, 242, 0.05));
            color: #ffffff;
            border: 1px solid rgba(88, 101, 242, 0.2);
        }
        .sidebar-menu a.active::before {
            content: '';
            position: absolute;
            left: 0;
            top: 50%;
            transform: translateY(-50%);
            width: 3px;
            height: 25px;
            background: linear-gradient(180deg, #f7971e, #ffd200);
            border-radius: 0 4px 4px 0;
        }
        .sidebar-menu a i { width: 22px; text-align: center; font-size: 1.1em; }
        .sidebar-menu .menu-label {
            font-size: 0.65em;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            color: #4a5568;
            padding: 20px 16px 8px;
            font-weight: 700;
        }
        
        /* ===== BOTÓN HAMBURGUESA ===== */
        .menu-toggle {
            position: fixed;
            top: 20px;
            left: 20px;
            z-index: 1100;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: white;
            width: 48px;
            height: 48px;
            border-radius: 12px;
            font-size: 1.5em;
            cursor: pointer;
            display: none;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }
        .menu-toggle:hover { background: rgba(88, 101, 242, 0.2); border-color: #5865F2; }
        
        /* ===== CONTENIDO PRINCIPAL ===== */
        .main-content {
            margin-left: 280px;
            min-height: 100vh;
            padding: 30px 40px 40px;
            background: linear-gradient(180deg, #0a0a0f, #12121f);
        }
        
        /* ===== TOP BAR ===== */
        .top-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px 25px;
            background: rgba(255, 255, 255, 0.03);
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            margin-bottom: 30px;
            backdrop-filter: blur(10px);
        }
        .top-bar .page-title { font-size: 1.4em; font-weight: 600; }
        .top-bar .page-title span { color: #5865F2; }
        .top-bar .user-info { display: flex; align-items: center; gap: 15px; }
        .status-dot {
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }
        .status-dot.online { background: #57F287; box-shadow: 0 0 20px rgba(87, 242, 135, 0.3); }
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
        
        /* ===== STATS GRID ===== */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: linear-gradient(145deg, rgba(255, 255, 255, 0.03), rgba(255, 255, 255, 0.01));
            border-radius: 16px;
            padding: 25px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        .stat-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, transparent, #5865F2, transparent);
            opacity: 0;
            transition: opacity 0.4s ease;
        }
        .stat-card:hover {
            transform: translateY(-5px);
            border-color: rgba(88, 101, 242, 0.2);
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        }
        .stat-card:hover::before { opacity: 1; }
        .stat-card .stat-icon { font-size: 2em; margin-bottom: 12px; }
        .stat-card .stat-number {
            font-size: 2.2em;
            font-weight: 700;
            background: linear-gradient(135deg, #f7971e, #ffd200);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .stat-card .stat-label { color: #a8b2d1; font-size: 0.9em; margin-top: 5px; }
        .stat-card .stat-trend {
            font-size: 0.7em;
            color: #57F287;
            background: rgba(87, 242, 135, 0.1);
            padding: 2px 10px;
            border-radius: 20px;
            display: inline-block;
            margin-top: 8px;
        }
        
        /* ===== BOTONES ===== */
        .action-buttons {
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            margin: 25px 0 10px;
        }
        .btn {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            padding: 14px 30px;
            border-radius: 14px;
            font-weight: 600;
            text-decoration: none;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            border: none;
            cursor: pointer;
            font-size: 0.95em;
        }
        .btn i { font-size: 1.1em; }
        .btn-invite {
            background: linear-gradient(135deg, #5865F2, #4752C4);
            color: white;
            box-shadow: 0 8px 30px rgba(88, 101, 242, 0.3);
        }
        .btn-invite:hover {
            transform: translateY(-3px) scale(1.02);
            box-shadow: 0 12px 40px rgba(88, 101, 242, 0.5);
        }
        .btn-support {
            background: linear-gradient(135deg, #ED4245, #C62828);
            color: white;
            box-shadow: 0 8px 30px rgba(237, 66, 69, 0.3);
        }
        .btn-support:hover {
            transform: translateY(-3px) scale(1.02);
            box-shadow: 0 12px 40px rgba(237, 66, 69, 0.5);
        }
        .btn-github {
            background: linear-gradient(135deg, #24292e, #1a1e22);
            color: white;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
        }
        .btn-github:hover {
            transform: translateY(-3px) scale(1.02);
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.5);
        }
        
        /* ===== COMANDOS ===== */
        .commands-section {
            background: rgba(255, 255, 255, 0.02);
            border-radius: 16px;
            padding: 30px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            margin-top: 20px;
        }
        .commands-section .section-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 25px;
        }
        .commands-section .section-header h2 { font-size: 1.3em; }
        .commands-section .section-header h2 i { color: #ffd200; margin-right: 10px; }
        .commands-section .section-header .command-count {
            font-size: 0.8em;
            color: #a8b2d1;
            background: rgba(255, 255, 255, 0.05);
            padding: 5px 15px;
            border-radius: 20px;
        }
        .command-category {
            background: rgba(255, 255, 255, 0.02);
            border-radius: 12px;
            padding: 18px 22px;
            margin-bottom: 12px;
            border-left: 3px solid #5865F2;
            transition: all 0.3s ease;
        }
        .command-category:hover {
            background: rgba(255, 255, 255, 0.04);
            transform: translateX(5px);
        }
        .command-category h3 { font-size: 0.95em; color: #ffd200; margin-bottom: 10px; }
        .command-item {
            display: inline-block;
            background: rgba(88, 101, 242, 0.12);
            padding: 6px 16px;
            border-radius: 20px;
            margin: 3px 4px;
            font-size: 0.85em;
            font-family: 'Courier New', monospace;
            color: #a8b2d1;
            border: 1px solid rgba(88, 101, 242, 0.1);
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .command-item:hover {
            background: rgba(88, 101, 242, 0.3);
            color: white;
            transform: scale(1.08);
            border-color: #5865F2;
            box-shadow: 0 0 25px rgba(88, 101, 242, 0.2);
        }
        
        /* ===== MODAL ===== */
        .modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.92);
            backdrop-filter: blur(20px);
            z-index: 9999;
            display: none;
            justify-content: center;
            align-items: center;
            padding: 40px;
            animation: modalFadeIn 0.4s ease;
        }
        .modal-overlay.active { display: flex; }
        @keyframes modalFadeIn {
            from { opacity: 0; transform: scale(0.95); }
            to { opacity: 1; transform: scale(1); }
        }
        .modal-content {
            background: linear-gradient(145deg, #1a1a2e, #0f0f1a);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 24px;
            max-width: 700px;
            width: 100%;
            max-height: 90vh;
            overflow-y: auto;
            padding: 50px 45px;
            position: relative;
            box-shadow: 0 40px 100px rgba(0, 0, 0, 0.8);
        }
        .modal-content::-webkit-scrollbar { width: 6px; }
        .modal-content::-webkit-scrollbar-track { background: transparent; }
        .modal-content::-webkit-scrollbar-thumb { background: #5865F2; border-radius: 10px; }
        .modal-close {
            position: absolute;
            top: 20px;
            right: 25px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: #a8b2d1;
            width: 44px;
            height: 44px;
            border-radius: 12px;
            font-size: 1.3em;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .modal-close:hover {
            background: rgba(237, 66, 69, 0.2);
            border-color: #ED4245;
            color: #ED4245;
            transform: rotate(90deg);
        }
        .modal-command {
            font-size: 2.8em;
            font-weight: 800;
            font-family: 'Courier New', monospace;
            color: #ffd200;
            margin-bottom: 8px;
            background: linear-gradient(135deg, #f7971e, #ffd200);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .modal-category {
            display: inline-block;
            background: rgba(88, 101, 242, 0.15);
            color: #5865F2;
            padding: 4px 16px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
            margin-bottom: 20px;
        }
        .modal-description {
            font-size: 1.15em;
            color: #e0e0e0;
            line-height: 1.6;
            margin-bottom: 25px;
            padding: 15px 20px;
            background: rgba(255, 255, 255, 0.03);
            border-radius: 12px;
            border-left: 3px solid #ffd200;
        }
        .modal-details { display: grid; gap: 15px; }
        .modal-detail-item {
            background: rgba(255, 255, 255, 0.02);
            border-radius: 12px;
            padding: 15px 20px;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
        .modal-detail-item .label {
            font-size: 0.7em;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #4a5568;
            font-weight: 700;
            margin-bottom: 5px;
        }
        .modal-detail-item .value {
            color: #a8b2d1;
            font-family: 'Courier New', monospace;
            font-size: 0.95em;
            white-space: pre-wrap;
            word-break: break-word;
        }
        .modal-detail-item .value.uso { color: #57F287; }
        .modal-detail-item .value.ejemplo { color: #ffd200; }
        .modal-permissions {
            display: inline-block;
            padding: 2px 14px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: 600;
        }
        .modal-permissions.admin {
            background: rgba(237, 66, 69, 0.15);
            color: #ED4245;
        }
        .modal-permissions.user {
            background: rgba(87, 242, 135, 0.1);
            color: #57F287;
        }
        
        /* ===== FOOTER ===== */
        .footer {
            text-align: center;
            padding: 30px 0 10px;
            color: #4a5568;
            font-size: 0.85em;
            border-top: 1px solid rgba(255, 255, 255, 0.03);
            margin-top: 40px;
        }
        .footer span { color: #5865F2; }
        
        /* ===== RESPONSIVE ===== */
        @media (max-width: 992px) {
            .sidebar { transform: translateX(-100%); }
            .sidebar.open { transform: translateX(0); }
            .menu-toggle { display: flex; align-items: center; justify-content: center; }
            .main-content { margin-left: 0; padding: 80px 20px 30px; }
            .stats-grid { grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); }
        }
        @media (max-width: 600px) {
            .top-bar { flex-direction: column; gap: 10px; text-align: center; }
            .action-buttons { justify-content: center; }
            .btn { padding: 10px 20px; font-size: 0.85em; }
            .stat-card .stat-number { font-size: 1.6em; }
            .modal-content { padding: 30px 20px; }
            .modal-command { font-size: 2em; }
        }
    </style>
</head>
<body>
    <!-- ===== MENÚ LATERAL ===== -->
    <button class="menu-toggle" id="menuToggle">
        <i class="fas fa-bars"></i>
    </button>
    
    <nav class="sidebar" id="sidebar">
        <div class="sidebar-brand">
            <div class="logo-icon">🤖</div>
            <h2>{{ bot_info.name }}</h2>
            <span class="version">v{{ bot_info.version }}</span>
        </div>
        
        <ul class="sidebar-menu">
            <li class="menu-label">Navegación</li>
            <li><a href="#" class="active"><i class="fas fa-home"></i> Dashboard</a></li>
            <li><a href="#"><i class="fas fa-chart-line"></i> Estadísticas</a></li>
            <li><a href="#"><i class="fas fa-users"></i> Servidores</a></li>
            
            <li class="menu-label">Comandos</li>
            {% for categoria in bot_info.commands_by_category.keys() %}
            <li><a href="#{{ categoria|replace(' ', '_') }}"><i class="fas fa-tag"></i> {{ categoria }}</a></li>
            {% endfor %}
            
            <li class="menu-label">Enlaces</li>
            <li><a href="https://discord.com/oauth2/authorize?client_id={{ bot_info.client_id }}&permissions=8&scope=bot%20applications.commands" target="_blank"><i class="fas fa-plus-circle"></i> Invitar Bot</a></li>
            <li><a href="https://discord.gg/tu-servidor" target="_blank"><i class="fas fa-headset"></i> Soporte</a></li>
            <li><a href="https://github.com/tu-usuario/tu-repo" target="_blank"><i class="fab fa-github"></i> GitHub</a></li>
        </ul>
    </nav>

    <!-- ===== CONTENIDO PRINCIPAL ===== -->
    <main class="main-content">
        <!-- TOP BAR -->
        <div class="top-bar">
            <div class="page-title">📊 <span>Dashboard</span> / Resumen</div>
            <div class="user-info">
                <span class="status-dot online"></span>
                <span>Online</span>
                <span style="color:#4a5568; margin: 0 5px;">|</span>
                <span style="color:#5865F2;">🆔 {{ bot_info.client_id }}</span>
                <span style="color:#4a5568; margin: 0 5px;">|</span>
                <span style="color:#ffd200;">Prefijo: {{ bot_info.prefijo }}</span>
            </div>
        </div>

        <!-- BOTONES -->
        <div class="action-buttons">
            <a href="https://discord.com/oauth2/authorize?client_id={{ bot_info.client_id }}&permissions=8&scope=bot%20applications.commands" target="_blank" class="btn btn-invite">
                <i class="fas fa-plus-circle"></i> Invitar Bot
            </a>
            <a href="https://discord.gg/tu-servidor" target="_blank" class="btn btn-support">
                <i class="fas fa-headset"></i> Servidor Soporte
            </a>
            <a href="https://github.com/tu-usuario/tu-repo" target="_blank" class="btn btn-github">
                <i class="fab fa-github"></i> GitHub
            </a>
        </div>

        <!-- STATS -->
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-icon">🏛️</div>
                <div class="stat-number">{{ bot_info.guild_count }}</div>
                <div class="stat-label">Servidores</div>
                <div class="stat-trend"><i class="fas fa-arrow-up"></i> +2 esta semana</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">👥</div>
                <div class="stat-number">{{ bot_info.user_count }}</div>
                <div class="stat-label">Usuarios Totales</div>
                <div class="stat-trend"><i class="fas fa-arrow-up"></i> +15 hoy</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">📊</div>
                <div class="stat-number">{{ bot_info.command_count }}</div>
                <div class="stat-label">Comandos</div>
                <div class="stat-trend"><i class="fas fa-arrow-up"></i> 98% uptime</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">💰</div>
                <div class="stat-number">{{ bot_info.total_money }}</div>
                <div class="stat-label">Economía Total</div>
                <div class="stat-trend"><i class="fas fa-arrow-up"></i> +5% crecimiento</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">🕒</div>
                <div class="stat-number">{{ bot_info.uptime }}</div>
                <div class="stat-label">Tiempo Activo</div>
                <div class="stat-trend"><i class="fas fa-check-circle"></i> Online 24/7</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">🎮</div>
                <div class="stat-number">{{ bot_info.active_users }}</div>
                <div class="stat-label">Usuarios Activos</div>
                <div class="stat-trend"><i class="fas fa-arrow-up"></i> +8 hoy</div>
            </div>
        </div>

        <!-- COMANDOS -->
        <div class="commands-section">
            <div class="section-header">
                <h2><i class="fas fa-terminal"></i> Comandos Disponibles</h2>
                <span class="command-count">{{ bot_info.command_count }} comandos</span>
            </div>
            
            {% for categoria, comandos in bot_info.commands_by_category.items() %}
            <div class="command-category" id="{{ categoria|replace(' ', '_') }}">
                <h3>{{ categoria }}</h3>
                {% for cmd in comandos %}
                <span class="command-item" onclick="abrirModal('{{ cmd }}')">{{ bot_info.prefijo }}{{ cmd }}</span>
                {% endfor %}
            </div>
            {% endfor %}
        </div>

        <!-- FOOTER -->
        <div class="footer">
            <p>🤖 {{ bot_info.name }} v{{ bot_info.version }} — <span>Última actualización:</span> {{ bot_info.last_update }}</p>
            <p style="margin-top: 5px; font-size: 0.8em; color: #2a2a3a;">💡 Haz clic en cualquier comando para ver su ayuda</p>
        </div>
    </main>

    <!-- ===== MODAL ===== -->
    <div class="modal-overlay" id="modalOverlay" onclick="cerrarModal(event)">
        <div class="modal-content" onclick="event.stopPropagation()">
            <button class="modal-close" onclick="cerrarModal()">
                <i class="fas fa-times"></i>
            </button>
            
            <div class="modal-command" id="modalCommand">.comando</div>
            <span class="modal-category" id="modalCategory">💰 Categoría</span>
            
            <div class="modal-description" id="modalDescription">
                Descripción del comando.
            </div>
            
            <div class="modal-details">
                <div class="modal-detail-item">
                    <div class="label">📝 Uso</div>
                    <div class="value uso" id="modalUso">.comando</div>
                </div>
                <div class="modal-detail-item">
                    <div class="label">📌 Ejemplo</div>
                    <div class="value ejemplo" id="modalEjemplo">.comando</div>
                </div>
                <div class="modal-detail-item">
                    <div class="label">🔒 Permisos</div>
                    <div class="value" id="modalPermisos">
                        <span class="modal-permissions user">Todos los usuarios</span>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- ===== JAVASCRIPT ===== -->
    <script>
        // Datos de ayuda de comandos desde Flask
        const comandosHelp = {{ bot_info.comandos_help|tojson }};
        
        function abrirModal(comando) {
            const data = comandosHelp[comando];
            if (!data) {
                console.error('Comando no encontrado:', comando);
                return;
            }
            
            document.getElementById('modalCommand').textContent = '{{ bot_info.prefijo }}' + comando;
            document.getElementById('modalCategory').textContent = data.categoria || 'Sin categoría';
            document.getElementById('modalDescription').textContent = data.descripcion || 'No hay descripción disponible.';
            document.getElementById('modalUso').textContent = data.uso || 'No disponible';
            document.getElementById('modalEjemplo').textContent = data.ejemplo || 'No disponible';
            
            const permisosEl = document.getElementById('modalPermisos');
            const permiso = data.permisos || 'Todos los usuarios';
            const isAdmin = permiso.toLowerCase().includes('admin') || permiso.toLowerCase().includes('dueño');
            const clase = isAdmin ? 'admin' : 'user';
            permisosEl.innerHTML = `<span class="modal-permissions ${clase}">${permiso}</span>`;
            
            document.getElementById('modalOverlay').classList.add('active');
            document.body.style.overflow = 'hidden';
        }
        
        function cerrarModal(event) {
            if (event && event.target !== event.currentTarget) return;
            document.getElementById('modalOverlay').classList.remove('active');
            document.body.style.overflow = '';
        }
        
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') cerrarModal();
        });
        
        // Menú hamburguesa
        const menuToggle = document.getElementById('menuToggle');
        const sidebar = document.getElementById('sidebar');
        
        menuToggle.addEventListener('click', () => {
            sidebar.classList.toggle('open');
            const icon = menuToggle.querySelector('i');
            icon.className = sidebar.classList.contains('open') ? 'fas fa-times' : 'fas fa-bars';
        });
        
        document.addEventListener('click', (e) => {
            if (window.innerWidth <= 992) {
                if (!sidebar.contains(e.target) && !menuToggle.contains(e.target)) {
                    sidebar.classList.remove('open');
                    document.querySelector('#menuToggle i').className = 'fas fa-bars';
                }
            }
        });
    </script>
</body>
</html>
"""

# ============================================================
# FUNCIONES PARA EL DASHBOARD
# ============================================================

def get_comandos_por_categoria(prefijo):
    """Agrupa comandos por categoría para mostrar en el dashboard"""
    comandos = get_comandos_con_prefijo(prefijo)
    categorias = {}
    
    for cmd, info in comandos.items():
        cat = info.get('categoria', '📂 Otros')
        if cat not in categorias:
            categorias[cat] = []
        categorias[cat].append(cmd)
    
    return categorias

@app.route('/api/stats')
def api_stats():
    """API para obtener estadísticas en JSON"""
    comandos = get_comandos_con_prefijo(PREFIJO)
    return jsonify({
        'servidores': DATOS_REALES['servidores'],
        'usuarios': DATOS_REALES['usuarios'],
        'comandos': len(comandos),
        'economia_total': DATOS_REALES['economia_total'],
        'tiempo_activo': DATOS_REALES['tiempo_activo'],
        'usuarios_activos': DATOS_REALES['usuarios_activos']
    })

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
