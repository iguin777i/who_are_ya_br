# Instruções de Instalação e Execução

## Requisitos do Sistema

- **Sistema Operacional**: Linux, macOS ou Windows
- **Python**: Versão 3.11 ou superior
- **Navegador**: Chrome, Firefox, Safari ou Edge (versões recentes)
- **Memória RAM**: Mínimo 2GB
- **Espaço em Disco**: 500MB livres

## Instalação Passo a Passo

### 1. Preparação do Ambiente

```bash
# Verificar versão do Python
python3 --version

# Se necessário, instalar Python 3.11+
# Ubuntu/Debian:
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip

# macOS (com Homebrew):
brew install python@3.11

# Windows: Baixar do site oficial python.org
```

### 2. Configuração do Projeto

```bash
# Navegar para o diretório do projeto
cd who_are_ya_br/app

# O ambiente virtual já está configurado, apenas ative-o:
source venv/bin/activate

# No Windows:
# venv\Scripts\activate

# Verificar se as dependências estão instaladas
pip list
```

### 3. Execução do Servidor

```bash
# Executar o servidor Flask
python src/main.py

# Você verá uma saída similar a:
# * Running on http://127.0.0.1:5000
# * Running on http://0.0.0.0:5000
```

### 4. Acessar o Jogo

1. Abrir o navegador
2. Navegar para: `http://localhost:5000`
3. O jogo deve carregar automaticamente

## Solução de Problemas

### Erro: "ModuleNotFoundError"

```bash
# Ativar o ambiente virtual
source venv/bin/activate

# Instalar dependências manualmente
pip install flask flask-cors requests pillow
```

### Erro: "Port 5000 is in use"

```bash
# Verificar processos usando a porta
lsof -i :5000

# Matar processo se necessário
kill -9 <PID>

# Ou alterar a porta no arquivo main.py:
# app.run(host='0.0.0.0', port=5001, debug=True)
```

### Erro: "Permission denied"

```bash
# Dar permissões de execução
chmod +x src/main.py

# Ou executar com sudo (não recomendado)
sudo python src/main.py
```

### Silhuetas não carregam

```bash
# Verificar se as silhuetas existem
ls -la src/static/images/silhouettes/

# Se não existirem, gerar novamente
cd ..
python silhouette_generator.py
```

## Configurações Avançadas

### Alterar Porta do Servidor

Editar `src/main.py`, linha final:
```python
app.run(host='0.0.0.0', port=5001, debug=True)  # Alterar 5000 para 5001
```

### Modo de Produção

Para uso em produção, alterar:
```python
app.run(host='0.0.0.0', port=5000, debug=False)
```

### Adicionar Novos Jogadores

1. Editar `data/players.json`
2. Adicionar entrada com formato:
```json
{
  "ID": 99999,
  "Nome": "Nome do Jogador",
  "Time": "Nome do Time",
  "Nacionalidade": "País",
  "Posição": "Posição",
  "Idade": 25,
  "Camisa": "10",
  "ImageURL": "https://exemplo.com/imagem.png"
}
```
3. Executar gerador de silhuetas:
```bash
python silhouette_generator.py
```

## Estrutura de Arquivos Importantes

```
who_are_ya_br/
├── app/src/main.py              # Servidor principal - NÃO ALTERAR
├── app/src/static/index.html    # Interface - Pode personalizar
├── app/src/static/styles.css    # Estilos - Pode personalizar
├── app/src/static/script.js     # Lógica - Cuidado ao alterar
├── data/players.json            # Dados - Pode adicionar jogadores
└── README.md                    # Documentação
```

## Comandos Úteis

```bash
# Verificar status do servidor
ps aux | grep python

# Ver logs em tempo real
tail -f nohup.out

# Parar servidor
Ctrl+C (no terminal onde está rodando)

# Limpar cache do navegador
Ctrl+Shift+R (ou Cmd+Shift+R no Mac)

# Verificar conectividade
curl http://localhost:5000/api/players/search?q=test
```

## Suporte

Em caso de problemas:

1. **Verificar logs**: Observar mensagens de erro no terminal
2. **Console do navegador**: F12 → Console para erros JavaScript
3. **Reiniciar**: Parar servidor (Ctrl+C) e iniciar novamente
4. **Limpar cache**: Ctrl+Shift+R no navegador
5. **Verificar dependências**: `pip list` no ambiente virtual

## Performance

Para melhor performance:

- **Usar navegador atualizado**
- **Fechar outras abas pesadas**
- **Verificar conexão com internet** (para carregar fontes)
- **Usar modo incógnito** se houver problemas de cache

---

**Nota**: Este jogo foi testado em Ubuntu 22.04 com Python 3.11. Outras configurações podem requerer ajustes menores.

