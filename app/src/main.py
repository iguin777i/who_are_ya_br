import os
import sys
import json
import random
from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
import unicodedata

# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Enable CORS for all routes
CORS(app)

def remove_accents(text):
    """Remove acentos e caracteres especiais de um texto"""
    if not text:
        return ""
    # Normaliza o texto para a forma NFD (decomposição)
    text = unicodedata.normalize('NFD', text)
    # Remove os caracteres de acentuação
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    return text.lower()

# Load players data
def load_players():
    players_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'players.json')
    with open(players_file, 'r', encoding='utf-8') as f:
        return json.load(f)

# Load teams data
def load_teams():
    teams_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'teams.json')
    with open(teams_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        # Criar um dicionário para busca rápida por nome do time
        teams_dict = {}
        for team in data['PlayerData']:
            teams_dict[team['Name']] = team
        return teams_dict

players_data = load_players()
teams_data = load_teams()

# Mapeamento de países para códigos de bandeiras
country_flags = {
    'Brasil': 'br',
    'Argentina': 'ar',
    'Uruguai': 'uy',
    'Paraguai': 'py',
    'Chile': 'cl',
    'Colômbia': 'co',
    'Venezuela': 've',
    'Peru': 'pe',
    'Equador': 'ec',
    'Bolívia': 'bo',
    'Portugal': 'pt',
    'Espanha': 'es',
    'França': 'fr',
    'Itália': 'it',
    'Alemanha': 'de',
    'Inglaterra': 'gb-eng',
    'Holanda': 'nl',
    'Bélgica': 'be',
    'Croácia': 'hr',
    'Sérvia': 'rs',
    'Dinamarca': 'dk',
    'Suécia': 'se',
    'Noruega': 'no',
    'Polônia': 'pl',
    'República Tcheca': 'cz',
    'Eslováquia': 'sk',
    'Hungria': 'hu',
    'Áustria': 'at',
    'Suíça': 'ch',
    'Ucrânia': 'ua',
    'Rússia': 'ru',
    'Japão': 'jp',
    'Coreia do Sul': 'kr',
    'Austrália': 'au',
    'Nova Zelândia': 'nz',
    'Estados Unidos': 'us',
    'México': 'mx',
    'Canadá': 'ca',
    'Costa Rica': 'cr',
    'Jamaica': 'jm',
    'Panamá': 'pa',
    'Honduras': 'hn',
    'Guatemala': 'gt',
    'El Salvador': 'sv',
    'Nigéria': 'ng',
    'Gana': 'gh',
    'Senegal': 'sn',
    'Marrocos': 'ma',
    'Tunísia': 'tn',
    'Argélia': 'dz',
    'Egito': 'eg',
    'África do Sul': 'za',
    'Camarões': 'cm',
    'Costa do Marfim': 'ci'
}

# Mapping for position icons
position_icons = {
    'MD': 'Meia.svg',
    'M(C)': 'Meia.svg',
    'MA': 'Meia.svg',
    'A(C)': 'Atacante.svg',
    'D': 'Zagueiro.svg',
    'G': 'Goleiro.svg',
    # Add more mappings as needed
}

# Game state storage (in production, use Redis or database)
game_sessions = {}

@app.route('/api/start-game', methods=['POST'])
def start_game():
    """Start a new game session"""
    try:
        session_id = str(random.randint(100000, 999999))
        
        # Select a random player
        selected_player = random.choice(players_data)
        
        game_sessions[session_id] = {
            'player': selected_player,
            'attempts': 0,
            'max_attempts': 8,
            'guesses': [],
            'hints_used': 0,
            'max_hints': 2,
            'game_over': False,
            'won': False
        }
        
        response_data = {
            'session_id': session_id,
            'max_attempts': 8,
            'max_hints': 2,
            'silhouette_url': f'/api/silhouette/{session_id}'
        }
        
        print(f"Nova sessão iniciada: {session_id}")
        print(f"Jogador selecionado: {selected_player['Nome']}")
        
        return jsonify(response_data)
    except Exception as e:
        print(f"Erro ao iniciar jogo: {str(e)}")
        return jsonify({'error': 'Erro ao iniciar jogo'}), 500

@app.route('/api/guess', methods=['POST'])
def make_guess():
    """Make a guess for the current game"""
    data = request.get_json()
    session_id = data.get('session_id')
    guess_name = data.get('guess_name')
    
    if session_id not in game_sessions:
        return jsonify({'error': 'Invalid session'}), 400
    
    session = game_sessions[session_id]
    
    if session['game_over']:
        return jsonify({'error': 'Game already over'}), 400
    
    if session['attempts'] >= session['max_attempts']:
        return jsonify({'error': 'No more attempts'}), 400
    
    # Find the guessed player
    guessed_player = None
    for player in players_data:
        if remove_accents(player['Nome']).lower() == remove_accents(guess_name).lower():
            guessed_player = player
            break
    
    if not guessed_player:
        return jsonify({'error': 'Player not found'}), 400
    
    session['attempts'] += 1
    correct_player = session['player']
    
    # Determine position icon URL
    guessed_positions = guessed_player['Posição'].split(',')
    first_position_code = guessed_positions[0].strip()
    
    position_icon_filename = position_icons.get(first_position_code, '') # Default to empty if not found
    position_icon_url = f'/static/images/icon-posicao/{position_icon_filename}' if position_icon_filename else ''

    # Compare attributes
    comparison = {
        'name': guessed_player['Nome'],
        'team': guessed_player['Time'],
        'team_logo': teams_data.get(guessed_player['Time'], {}).get('ImageURL', ''),
        'nationality': guessed_player['Nacionalidade'],
        'nationality_flag': f"https://flagcdn.com/32x24/{country_flags.get(guessed_player['Nacionalidade'], 'xx')}.png",
        'position': guessed_player['Posição'],
        'position_icon_url': position_icon_url,
        'age': guessed_player['Idade'],
        'shirt_number': guessed_player['Camisa'],
        'correct': {
            'name': guessed_player['Nome'] == correct_player['Nome'],
            'team': guessed_player['Time'] == correct_player['Time'],
            'nationality': guessed_player['Nacionalidade'] == correct_player['Nacionalidade'],
            'position': guessed_player['Posição'] == correct_player['Posição'],
            'age': guessed_player['Idade'] == correct_player['Idade'],
            'shirt_number': guessed_player['Camisa'] == correct_player['Camisa']
        },
        'arrows': {
            'age': 'equal' if guessed_player['Idade'] == correct_player['Idade'] else ('up' if guessed_player['Idade'] < correct_player['Idade'] else 'down'),
            'shirt_number': 'equal' if guessed_player['Camisa'] == correct_player['Camisa'] else ('up' if str(guessed_player['Camisa']).isdigit() and str(correct_player['Camisa']).isdigit() and int(guessed_player['Camisa']) < int(correct_player['Camisa']) else 'down')
        }
    }
    
    session['guesses'].append(comparison)
    
    # Check if won
    if guessed_player['Nome'] == correct_player['Nome']:
        session['won'] = True
        session['game_over'] = True
    elif session['attempts'] >= session['max_attempts']:
        session['game_over'] = True
    
    return jsonify({
        'comparison': comparison,
        'attempts_left': session['max_attempts'] - session['attempts'],
        'game_over': session['game_over'],
        'won': session['won'],
        'correct_player': correct_player if session['game_over'] else None
    })

@app.route('/api/hint', methods=['POST'])
def get_hint():
    """Get a hint for the current game"""
    data = request.get_json()
    session_id = data.get('session_id')
    
    if session_id not in game_sessions:
        return jsonify({'error': 'Invalid session'}), 400
    
    session = game_sessions[session_id]
    
    if session['game_over']:
        return jsonify({'error': 'Game already over'}), 400
    
    if session['hints_used'] >= session['max_hints']:
        return jsonify({'error': 'No more hints available'}), 400
    
    player = session['player']
    
    # Verificar quais atributos já foram acertados
    correct_attributes = set()
    for guess in session['guesses']:
        for attr, is_correct in guess['correct'].items():
            if is_correct:
                correct_attributes.add(attr)
    
    # Inicializar lista de dicas usadas se não existir
    if 'used_hints' not in session:
        session['used_hints'] = []
    
    # Definir todas as possíveis dicas
    all_hints = [
        {
            'type': 'nationality',
            'display': player['Nacionalidade'],
            'image_url': f"https://flagcdn.com/32x24/{country_flags.get(player['Nacionalidade'], 'xx')}.png",
            'target': 'country-flag'
        },
        {
            'type': 'position',
            'display': player['Posição'],
            'target': 'player-position'
        },
        {
            'type': 'team',
            'display': player['Time'],
            'image_url': teams_data.get(player['Time'], {}).get('ImageURL', ''),
            'target': 'country-flag'
        }
    ]
    
    # Filtrar dicas disponíveis
    available_hints = [
        hint for hint in all_hints 
        if hint['type'] not in correct_attributes  # Não dar dica de atributo já acertado
        and hint['type'] not in session['used_hints']  # Não repetir dica já usada
    ]
    
    # Se não houver dicas disponíveis
    if not available_hints:
        return jsonify({'error': 'No more hints available'}), 400
    
    # Escolher uma dica aleatória das disponíveis
    hint = random.choice(available_hints)
    
    # Registrar a dica usada
    session['used_hints'].append(hint['type'])
    session['hints_used'] += 1
    
    return jsonify({
        'hint': hint,
        'hints_left': session['max_hints'] - session['hints_used']
    })

@app.route('/api/photo/<session_id>', methods=['GET'])
def get_player_photo(session_id):
    """Get the correct player's photo for the current game"""
    if session_id not in game_sessions:
        return jsonify({'error': 'Invalid session'}), 400

    session = game_sessions[session_id]

    if session['game_over']:
        return jsonify({'error': 'Game already over'}), 400

    player = session['player']
    image_url = player.get('ImageURL', '')

    return jsonify({'image_url': image_url})

@app.route('/api/players/search')
def search_players():
    """Search players for autocomplete"""
    query = request.args.get('q', '').lower()
    query = remove_accents(query)
    
    if len(query) < 2:
        return jsonify([])
    
    matches = []
    for player in players_data:
        # Remove acentos do nome do jogador
        nome_sem_acentos = remove_accents(player['Nome'])
        nome_completo = nome_sem_acentos.lower()
        sobrenomes = nome_completo.split()[1:]  # Pega todos os nomes exceto o primeiro
        
        # Verifica se a query está no nome completo ou em algum sobrenome
        if (query in nome_completo or 
            any(query in sobrenome for sobrenome in sobrenomes)):
            matches.append({
                'name': player['Nome'],
                'team': player['Time'],
                'display': f"{player['Nome']} ({player['Time']})"
            })
    
    return jsonify(matches[:10])  # Limit to 10 results

@app.route('/api/silhouette/<session_id>')
def get_silhouette(session_id):
    """Get silhouette image for the player"""
    if session_id == 'default':
        # Servir a silhueta padrão
        default_silhouette = os.path.join(
            os.path.dirname(__file__),
            'static',
            'images',
            'silhouettes',
            'default.png'
        )
        
        if os.path.exists(default_silhouette):
            return send_from_directory(
                os.path.join(os.path.dirname(__file__), 'static', 'images', 'silhouettes'),
                'default.png'
            )
        return "Default silhouette not found", 404
    
    if session_id not in game_sessions:
        return "Session not found", 404
    
    player = game_sessions[session_id]['player']
    player_id = player['ID']
    
    # Caminho para a silhueta
    silhouette_path = os.path.join(
        os.path.dirname(__file__), 
        'static', 
        'images', 
        'silhouettes', 
        f'{player_id}.png'
    )
    
    # Verificar se a silhueta existe
    if os.path.exists(silhouette_path):
        return send_from_directory(
            os.path.join(os.path.dirname(__file__), 'static', 'images', 'silhouettes'),
            f'{player_id}.png'
        )
    else:
        # Se a silhueta não existir, usar a silhueta padrão
        default_silhouette = os.path.join(
            os.path.dirname(__file__),
            'static',
            'images',
            'silhouettes',
            'default.png'
        )
        
        if os.path.exists(default_silhouette):
            return send_from_directory(
                os.path.join(os.path.dirname(__file__), 'static', 'images', 'silhouettes'),
                'default.png'
            )
        
        # Se não houver silhueta padrão, retornar erro
        return "Silhouette not found", 404

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

