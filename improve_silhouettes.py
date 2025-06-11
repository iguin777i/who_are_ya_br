import os
import requests
from PIL import Image, ImageFilter, ImageOps, ImageEnhance
import json
from io import BytesIO

def create_better_silhouette(image):
    """
    Cria uma silhueta melhorada usando técnicas mais avançadas
    """
    # Converter para RGBA
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    # Redimensionar mantendo proporção
    image.thumbnail((300, 400), Image.Resampling.LANCZOS)
    
    # Criar nova imagem com fundo transparente
    width, height = image.size
    silhouette = Image.new('RGBA', (300, 400), (0, 0, 0, 0))
    
    # Centralizar a imagem redimensionada
    x_offset = (300 - width) // 2
    y_offset = (400 - height) // 2
    
    # Processar pixel por pixel para criar silhueta
    for x in range(width):
        for y in range(height):
            r, g, b, a = image.getpixel((x, y))
            
            # Calcular luminância
            luminance = 0.299 * r + 0.587 * g + 0.114 * b
            
            # Se o pixel não é muito claro (não é fundo), torná-lo preto
            if luminance < 240 and a > 128:  # Threshold ajustado
                silhouette.putpixel((x + x_offset, y + y_offset), (0, 0, 0, 255))
    
    # Aplicar filtros para melhorar a silhueta
    # Filtro de mediana para remover ruído
    silhouette = silhouette.filter(ImageFilter.MedianFilter(size=3))
    
    # Leve desfoque para suavizar bordas
    silhouette = silhouette.filter(ImageFilter.GaussianBlur(radius=0.5))
    
    return silhouette

def create_edge_based_silhouette(image):
    """
    Método alternativo baseado em detecção de bordas
    """
    # Converter para escala de cinza
    gray = image.convert('L')
    
    # Redimensionar
    gray.thumbnail((300, 400), Image.Resampling.LANCZOS)
    
    # Aumentar contraste
    enhancer = ImageEnhance.Contrast(gray)
    gray = enhancer.enhance(2.0)
    
    # Aplicar threshold adaptativo
    pixels = list(gray.getdata())
    # Usar percentil para threshold mais robusto
    sorted_pixels = sorted(pixels)
    threshold = sorted_pixels[int(len(sorted_pixels) * 0.7)]  # 70º percentil
    
    # Criar máscara
    mask = gray.point(lambda x: 255 if x < threshold else 0, mode='1')
    
    # Aplicar operações morfológicas para limpar a máscara
    # Erosão seguida de dilatação (abertura)
    mask = mask.filter(ImageFilter.MinFilter(3))  # Erosão
    mask = mask.filter(ImageFilter.MaxFilter(3))  # Dilatação
    
    # Criar silhueta final
    width, height = gray.size
    silhouette = Image.new('RGBA', (300, 400), (0, 0, 0, 0))
    
    # Centralizar
    x_offset = (300 - width) // 2
    y_offset = (400 - height) // 2
    
    # Aplicar máscara
    for x in range(width):
        for y in range(height):
            if mask.getpixel((x, y)) == 255:
                silhouette.putpixel((x + x_offset, y + y_offset), (0, 0, 0, 255))
    
    return silhouette

def create_silhouette_from_url_improved(image_url, output_path):
    """
    Versão melhorada para criar silhueta a partir de URL
    """
    try:
        # Baixar a imagem
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        
        # Abrir a imagem
        image = Image.open(BytesIO(response.content))
        
        # Tentar método baseado em bordas primeiro
        silhouette = create_edge_based_silhouette(image)
        
        # Salvar
        silhouette.save(output_path, 'PNG')
        return True
        
    except Exception as e:
        print(f"Erro ao processar {image_url}: {e}")
        return False

def regenerate_silhouettes():
    """
    Regenera as silhuetas com qualidade melhorada
    """
    # Carregar dados dos jogadores
    players_file = '/home/ubuntu/who_are_ya_br/data/players.json'
    with open(players_file, 'r', encoding='utf-8') as f:
        players = json.load(f)
    
    # Diretório de silhuetas
    silhouettes_dir = '/home/ubuntu/who_are_ya_br/app/src/static/images/silhouettes'
    
    processed = 0
    errors = 0
    
    for player in players[:10]:  # Processar os primeiros 10
        player_id = player['ID']
        image_url = player['ImageURL']
        silhouette_path = os.path.join(silhouettes_dir, f"{player_id}.png")
        
        print(f"Regenerando silhueta para {player['Nome']} (ID: {player_id})...")
        
        if create_silhouette_from_url_improved(image_url, silhouette_path):
            processed += 1
            print(f"✓ Silhueta melhorada criada para {player['Nome']}")
        else:
            errors += 1
            print(f"✗ Erro ao criar silhueta para {player['Nome']}")
    
    print(f"\nRegeneração concluída:")
    print(f"Sucessos: {processed}")
    print(f"Erros: {errors}")

if __name__ == "__main__":
    regenerate_silhouettes()

