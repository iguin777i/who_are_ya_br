# Guia de Deploy - Who Are Ya? Brasileirão

Este guia te ajudará a fazer o deploy da aplicação em diferentes plataformas.

## 📋 Pré-requisitos

- Conta GitHub (para conectar o repositório)
- Python 3.11+ instalado localmente (para testes)

## 🚀 Opções de Deploy

### 1. Render (Recomendado - Gratuito)

**Vantagens:**
- Plano gratuito generoso
- Deploy automático
- SSL gratuito
- Fácil configuração

**Passos:**

1. **Criar conta no Render:**
   - Acesse [render.com](https://render.com)
   - Faça login com sua conta GitHub

2. **Criar novo Web Service:**
   - Clique em "New +" → "Web Service"
   - Conecte seu repositório GitHub
   - Selecione o repositório `who_are_ya_br`

3. **Configurar o serviço:**
   - **Name:** `who-are-ya-br` (ou outro nome)
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn wsgi:app`
   - **Root Directory:** `app` (importante!)

4. **Variáveis de Ambiente (opcional):**
   - `FLASK_ENV=production`
   - `PORT=10000`

5. **Deploy:**
   - Clique em "Create Web Service"
   - Aguarde o build e deploy (2-3 minutos)

### 2. Railway

**Vantagens:**
- Deploy muito rápido
- Interface simples
- Bom para projetos pequenos

**Passos:**

1. **Criar conta no Railway:**
   - Acesse [railway.app](https://railway.app)
   - Faça login com GitHub

2. **Criar projeto:**
   - Clique em "New Project"
   - Selecione "Deploy from GitHub repo"
   - Escolha seu repositório

3. **Configurar:**
   - Railway detectará automaticamente que é Python
   - Certifique-se que o diretório raiz seja `app`
   - O comando de start será: `gunicorn wsgi:app`

### 3. Heroku

**Vantagens:**
- Muito popular
- Boa documentação
- Muitos add-ons

**Passos:**

1. **Instalar Heroku CLI:**
   ```bash
   # Windows
   winget install --id=Heroku.HerokuCLI
   
   # macOS
   brew tap heroku/brew && brew install heroku
   ```

2. **Login no Heroku:**
   ```bash
   heroku login
   ```

3. **Criar app:**
   ```bash
   cd app
   heroku create who-are-ya-br
   ```

4. **Deploy:**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

### 4. Vercel

**Vantagens:**
- Deploy muito rápido
- Interface excelente
- Boa para frontend

**Passos:**

1. **Criar conta no Vercel:**
   - Acesse [vercel.com](https://vercel.com)
   - Faça login com GitHub

2. **Importar projeto:**
   - Clique em "New Project"
   - Importe do GitHub
   - Selecione o repositório

3. **Configurar:**
   - **Framework Preset:** Other
   - **Root Directory:** `app`
   - **Build Command:** `pip install -r requirements.txt`
   - **Output Directory:** `src/static`
   - **Install Command:** `pip install -r requirements.txt`

### 5. DigitalOcean App Platform

**Vantagens:**
- Muito estável
- Boa performance
- Suporte técnico

**Passos:**

1. **Criar conta no DigitalOcean:**
   - Acesse [digitalocean.com](https://digitalocean.com)
   - Crie uma conta

2. **Criar App:**
   - Vá para "Apps" → "Create App"
   - Conecte seu repositório GitHub

3. **Configurar:**
   - **Source Directory:** `app`
   - **Build Command:** `pip install -r requirements.txt`
   - **Run Command:** `gunicorn wsgi:app`

## 🔧 Configurações Importantes

### Estrutura de Arquivos
```
app/
├── requirements.txt
├── Procfile
├── runtime.txt
├── wsgi.py
├── src/
│   ├── main.py
│   └── static/
└── data/
    ├── players.json
    └── teams.json
```

### Variáveis de Ambiente (Opcional)
- `FLASK_ENV=production`
- `PORT=10000`
- `DEBUG=False`

## 🧪 Teste Local

Antes do deploy, teste localmente:

```bash
cd app
pip install -r requirements.txt
python src/main.py
```

Acesse: http://localhost:5000

## 🚨 Troubleshooting

### Erro: "Module not found"
- Verifique se o `requirements.txt` está correto
- Certifique-se que o diretório raiz é `app`

### Erro: "Port already in use"
- A aplicação usa variável de ambiente `PORT`
- Plataformas de deploy definem automaticamente

### Erro: "Static files not found"
- Verifique se o `static_folder` está configurado corretamente
- Certifique-se que os arquivos estão na pasta `src/static`

## 📞 Suporte

Se encontrar problemas:
1. Verifique os logs da plataforma de deploy
2. Teste localmente primeiro
3. Verifique se todos os arquivos estão no lugar correto

## 🎯 Recomendação Final

**Para começar:** Use **Render** - é gratuito, fácil e confiável para projetos pequenos.

**Para produção:** Use **DigitalOcean** ou **Heroku** - mais estáveis e escaláveis. 