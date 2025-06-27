#!/bin/bash

# Script de Deploy - Who Are Ya? Brasileirão
# Este script automatiza o processo de deploy

echo "🚀 Iniciando deploy do Who Are Ya? Brasileirão"
echo "================================================"

# Verificar se estamos no diretório correto
if [ ! -f "requirements.txt" ]; then
    echo "❌ Erro: Execute este script dentro da pasta 'app'"
    exit 1
fi

# Verificar se o Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Erro: Python 3 não está instalado"
    exit 1
fi

# Verificar se o pip está instalado
if ! command -v pip &> /dev/null; then
    echo "❌ Erro: pip não está instalado"
    exit 1
fi

echo "✅ Verificações básicas concluídas"

# Instalar dependências
echo "📦 Instalando dependências..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Erro ao instalar dependências"
    exit 1
fi

echo "✅ Dependências instaladas com sucesso"

# Testar a aplicação localmente
echo "🧪 Testando aplicação localmente..."
python3 src/main.py &
APP_PID=$!

# Aguardar um pouco para a aplicação iniciar
sleep 3

# Verificar se a aplicação está rodando
if curl -s http://localhost:5000 > /dev/null; then
    echo "✅ Aplicação funcionando localmente"
else
    echo "❌ Erro: Aplicação não está respondendo"
    kill $APP_PID 2>/dev/null
    exit 1
fi

# Parar a aplicação
kill $APP_PID 2>/dev/null

echo ""
echo "🎉 Aplicação pronta para deploy!"
echo ""
echo "📋 Próximos passos:"
echo "1. Faça commit das alterações:"
echo "   git add ."
echo "   git commit -m 'Preparar para deploy'"
echo "   git push origin main"
echo ""
echo "2. Escolha uma plataforma de deploy:"
echo "   - Render (recomendado): https://render.com"
echo "   - Railway: https://railway.app"
echo "   - Heroku: https://heroku.com"
echo "   - Vercel: https://vercel.com"
echo ""
echo "3. Siga as instruções no arquivo DEPLOY.md"
echo ""
echo "🔗 URL da aplicação local: http://localhost:5000" 