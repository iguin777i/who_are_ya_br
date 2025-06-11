import os
import requests
from PIL import Image, ImageOps
from io import BytesIO

def create_default_silhouette():
    # URL da silhueta padrão
    url = "https://st4.depositphotos.com/13349494/25169/i/450/depositphotos_251691910-stock-photo-silhouette-man-looking-camera-isolated.jpg"
    
    try:
        # Baixar a imagem
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Abrir a imagem
        img = Image.open(BytesIO(response.content))
        
        # Converter para RGBA se necessário
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Redimensionar para o tamanho padrão (300x400)
        img = img.resize((300, 400), Image.Resampling.LANCZOS)
        
        # Garantir que o diretório existe
        output_dir = os.path.join('app', 'src', 'static', 'images', 'silhouettes')
        os.makedirs(output_dir, exist_ok=True)
        
        # Salvar como default.png
        output_path = os.path.join(output_dir, 'default.png')
        img.save(output_path, 'PNG', optimize=True)
        print(f"Silhueta padrão criada em: {output_path}")
        
    except Exception as e:
        print(f"Erro ao criar silhueta padrão: {e}")

if __name__ == "__main__":
    create_default_silhouette() 