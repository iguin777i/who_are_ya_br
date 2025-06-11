import os
import requests
from PIL import Image, ImageFilter, ImageOps, ImageEnhance
import json
from io import BytesIO
import numpy as np
from pathlib import Path

def create_silhouette_from_url(image_url, output_path):
    """
    Cria uma silhueta a partir de uma URL de imagem
    """
    try:
        # Baixar a imagem
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        
        # Abrir a imagem
        image = Image.open(BytesIO(response.content))
        
        # Converter para RGBA se necessário
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        
        # Redimensionar para um tamanho padrão mantendo proporção
        target_size = (300, 400)
        image = resize_with_aspect_ratio(image, target_size)
        
        # Melhorar contraste e brilho
        image = enhance_image(image)
        
        # Criar silhueta
        silhouette = create_silhouette(image)
        
        # Salvar com qualidade otimizada
        silhouette.save(output_path, 'PNG', optimize=True)
        return True
        
    except Exception as e:
        print(f"Erro ao processar {image_url}: {e}")
        return False

def resize_with_aspect_ratio(image, target_size):
    """
    Redimensiona a imagem mantendo a proporção e centralizando
    """
    target_width, target_height = target_size
    width, height = image.size
    
    # Calcular nova dimensão mantendo proporção
    ratio = min(target_width/width, target_height/height)
    new_size = (int(width * ratio), int(height * ratio))
    
    # Redimensionar
    image = image.resize(new_size, Image.Resampling.LANCZOS)
    
    # Criar nova imagem com fundo transparente
    new_image = Image.new('RGBA', target_size, (0, 0, 0, 0))
    
    # Colar a imagem redimensionada centralizada
    paste_x = (target_width - new_size[0]) // 2
    paste_y = (target_height - new_size[1]) // 2
    new_image.paste(image, (paste_x, paste_y))
    
    return new_image

def enhance_image(image):
    """
    Melhora o contraste e brilho da imagem
    """
    # Converter para RGB para processamento
    rgb_image = image.convert('RGB')
    
    # Ajustar contraste
    enhancer = ImageEnhance.Contrast(rgb_image)
    rgb_image = enhancer.enhance(1.5)
    
    # Ajustar brilho
    enhancer = ImageEnhance.Brightness(rgb_image)
    rgb_image = enhancer.enhance(1.2)
    
    # Converter de volta para RGBA
    enhanced = Image.new('RGBA', rgb_image.size)
    enhanced.paste(rgb_image)
    
    return enhanced

def create_silhouette(image):
    """
    Cria uma silhueta a partir de uma imagem PIL usando técnicas avançadas
    """
    # Converter para escala de cinza
    gray = image.convert('L')
    
    # Aplicar filtro gaussiano para reduzir ruído
    gray = gray.filter(ImageFilter.GaussianBlur(radius=1))
    
    # Converter para array numpy para processamento
    img_array = np.array(gray)
    
    # Calcular threshold adaptativo usando Otsu's method
    hist, bins = np.histogram(img_array.flatten(), 256, [0, 256])
    cdf = hist.cumsum()
    cdf_normalized = cdf * float(hist.max()) / cdf.max()
    
    # Encontrar o ponto de inflexão
    threshold = np.argmax(np.gradient(cdf_normalized))
    
    # Criar máscara binária
    mask = img_array < threshold
    
    # Aplicar operações morfológicas para limpar a máscara
    from scipy import ndimage
    mask = ndimage.binary_opening(mask, structure=np.ones((3,3)))
    mask = ndimage.binary_closing(mask, structure=np.ones((3,3)))
    
    # Converter de volta para imagem PIL
    mask_image = Image.fromarray(mask.astype(np.uint8) * 255)
    
    # Criar silhueta preta
    silhouette = Image.new('RGBA', image.size, (0, 0, 0, 0))
    
    # Aplicar a máscara
    silhouette.paste((0, 0, 0, 255), mask=mask_image)
    
    # Suavizar bordas
    silhouette = silhouette.filter(ImageFilter.GaussianBlur(radius=1))
    
    return silhouette

def create_simple_silhouette(image):
    """
    Método alternativo mais simples para criar silhueta
    """
    # Converter para escala de cinza
    gray = image.convert('L')
    
    # Criar threshold adaptativo
    # Encontrar o valor médio dos pixels
    pixels = list(gray.getdata())
    avg_brightness = sum(pixels) / len(pixels)
    
    # Usar threshold baseado na média
    threshold = max(200, avg_brightness + 50)
    
    # Criar máscara binária
    mask = gray.point(lambda x: 255 if x < threshold else 0, mode='1')
    
    # Criar silhueta
    silhouette = Image.new('RGBA', image.size, (0, 0, 0, 0))
    
    # Aplicar máscara
    silhouette.paste((0, 0, 0, 255), mask=mask)
    
    return silhouette

def process_all_players():
    """
    Processa todos os jogadores e cria suas silhuetas
    """
    # Carregar dados dos jogadores
    current_dir = Path(__file__).parent.parent
    players_file = current_dir / 'data' / 'players.json'
    
    with open(players_file, 'r', encoding='utf-8') as f:
        players = json.load(f)
    
    # Diretórios
    images_dir = current_dir / 'app' / 'src' / 'static' / 'images' / 'players'
    silhouettes_dir = current_dir / 'app' / 'src' / 'static' / 'images' / 'silhouettes'
    
    # Criar diretórios se não existirem
    images_dir.mkdir(parents=True, exist_ok=True)
    silhouettes_dir.mkdir(parents=True, exist_ok=True)
    
    processed = 0
    errors = 0
    
    for player in players:
        player_id = player['ID']
        image_url = player['ImageURL']
        
        # Caminhos dos arquivos
        original_path = images_dir / f"{player_id}.png"
        silhouette_path = silhouettes_dir / f"{player_id}.png"
        
        print(f"Processando {player['Nome']} (ID: {player_id})...")
        
        # Baixar e salvar imagem original
        try:
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()
            
            with open(original_path, 'wb') as f:
                f.write(response.content)
            
            # Criar silhueta
            if create_silhouette_from_url(image_url, silhouette_path):
                processed += 1
                print(f"✓ Silhueta criada para {player['Nome']}")
            else:
                errors += 1
                print(f"✗ Erro ao criar silhueta para {player['Nome']}")
                
        except Exception as e:
            errors += 1
            print(f"✗ Erro ao baixar imagem de {player['Nome']}: {e}")
    
    print(f"\nProcessamento concluído:")
    print(f"Sucessos: {processed}")
    print(f"Erros: {errors}")

if __name__ == "__main__":
    process_all_players()

