from flask import request, jsonify
import json

@app.route('/api/players/search')
def search_players():
    query = request.args.get('q', '').strip().lower()
    if not query:
        return jsonify([])
    
    # Carregar dados dos jogadores
    with open('data/players.json', 'r', encoding='utf-8') as f:
        players = json.load(f)
    
    # Função para calcular similaridade entre strings
    def string_similarity(s1, s2):
        s1 = s1.lower()
        s2 = s2.lower()
        
        # Verifica se uma string contém a outra
        if s1 in s2 or s2 in s1:
            return True
            
        # Verifica similaridade por palavras
        s1_words = set(s1.split())
        s2_words = set(s2.split())
        
        # Se alguma palavra de s1 está em s2 ou vice-versa
        return bool(s1_words & s2_words)
    
    # Buscar jogadores
    results = []
    for player in players:
        # Verifica similaridade no nome
        if string_similarity(query, player['name']):
            results.append({
                'name': player['name'],
                'team': player['team']
            })
    
    # Ordenar resultados por relevância
    results.sort(key=lambda x: len(x['name']))
    
    # Limitar a 10 resultados
    return jsonify(results[:10]) 