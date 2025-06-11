# Who Are Ya? Brasileirão

## Descrição do Projeto

O "Who Are Ya? Brasileirão" é um jogo web interativo onde o jogador deve adivinhar um jogador de futebol do Brasileirão através de sua silhueta e pistas. O jogo foi desenvolvido em Python/Flask com frontend em HTML, CSS e JavaScript.

## Funcionalidades Implementadas

### ✅ Funcionalidades Principais
- **Sistema de Jogo**: 8 tentativas para adivinhar o jogador
- **Sistema de Dicas**: 2 dicas disponíveis por partida
- **Busca com Autocomplete**: Busca inteligente de jogadores com sugestões
- **Feedback Visual**: Sistema de cores e setas para comparação de atributos
- **Interface Responsiva**: Design moderno e adaptável para diferentes dispositivos
- **Silhuetas**: Geração automática de silhuetas a partir das fotos dos jogadores
- **Sistema de Mensagens**: Feedback visual com mensagens de erro e sucesso
- **Animações**: Transições suaves e efeitos visuais
- **Gerenciamento de Estado**: Controle robusto do estado do jogo

### 🎮 Mecânicas do Jogo
- **Tentativas**: 8 chances para acertar
- **Dicas**: Até 2 dicas por partida (posição, nacionalidade, time, idade)
- **Comparação de Atributos**:
  - Nome, Nacionalidade, Time, Posição (Verde = Correto, Vermelho = Incorreto)
  - Idade e Número da Camisa (com setas indicativas ↑↓)
- **Sem Limite de Tempo**: Jogo focado na estratégia, não na velocidade
- **Feedback Imediato**: Mensagens visuais para cada ação
- **Estatísticas**: Contagem de tentativas e dicas utilizadas

### 🎨 Interface e Design
- **Tela Inicial**: Logo, botões de início e instruções
- **Tela de Instruções**: Explicação completa das regras
- **Tela de Jogo**: 
  - Silhueta do jogador
  - Campo de busca com autocomplete
  - Contadores de tentativas e dicas
  - Histórico de tentativas
  - Sistema de dicas interativo
- **Tela de Resultado**: 
  - Mensagem de vitória/derrota
  - Informações do jogador correto
  - Estatísticas da partida
  - Botão para novo jogo
- **Animações**: 
  - Transições suaves entre telas
  - Efeitos de hover e click
  - Mensagens flutuantes
  - Loading spinner

## Estrutura do Projeto

```
who_are_ya_br/
├── app/
│   ├── src/
│   │   ├── static/
│   │   │   ├── index.html          # Interface principal
│   │   │   ├── styles.css          # Estilos CSS
│   │   │   ├── script.js           # Lógica JavaScript
│   │   │   └── images/
│   │   │       ├── players/        # Fotos originais dos jogadores
│   │   │       └── silhouettes/    # Silhuetas geradas
│   │   ├── main.py                 # Servidor Flask principal
│   │   └── database/
│   ├── venv/                       # Ambiente virtual Python
│   └── requirements.txt            # Dependências
├── data/
│   └── players.json               # Base de dados dos jogadores
├── silhouette_generator.py        # Script para gerar silhuetas
├── improve_silhouettes.py         # Script melhorado de silhuetas
└── teste_relatorio.md            # Relatório de testes
```

## Tecnologias Utilizadas

### Backend
- **Python 3.11**: Linguagem principal
- **Flask**: Framework web
- **Flask-CORS**: Suporte a requisições cross-origin
- **Pillow (PIL)**: Processamento de imagens
- **Requests**: Requisições HTTP

### Frontend
- **HTML5**: Estrutura das páginas
- **CSS3**: 
  - Flexbox e Grid para layout
  - Animações e transições
  - Media queries para responsividade
  - Variáveis CSS para temas
- **JavaScript (ES6+)**: 
  - Manipulação do DOM
  - Gerenciamento de estado
  - Eventos e listeners
  - Animações e transições
  - Sistema de mensagens
- **Google Fonts**: Tipografia (Poppins)

### Dados
- **JSON**: Base de dados dos jogadores do Brasileirão
- **PNG**: Formato das imagens e silhuetas

## Como Executar

### Pré-requisitos
- Python 3.11+
- pip (gerenciador de pacotes Python)
- Navegador moderno (Chrome, Firefox, Safari, Edge)

### Instalação e Execução

1. **Navegar para o diretório do projeto**:
   ```bash
   cd who_are_ya_br/app
   ```

2. **Ativar o ambiente virtual**:
   ```bash
   # Linux/macOS
   source venv/bin/activate
   
   # Windows
   venv\Scripts\activate
   ```

3. **Instalar dependências** (se necessário):
   ```bash
   pip install -r requirements.txt
   ```

4. **Executar o servidor**:
   ```bash
   python src/main.py
   ```

5. **Acessar o jogo**:
   Abrir o navegador em `http://localhost:5000`

[Instruções de Instalação](INSTALACAO.md)

## API Endpoints

### Jogo
- `POST /api/start-game`: Iniciar nova partida
- `POST /api/guess`: Fazer um palpite
- `POST /api/hint`: Obter uma dica
- `GET /api/silhouette/<session_id>`: Obter silhueta do jogador

### Busca
- `GET /api/players/search?q=<query>`: Buscar jogadores

## Características Técnicas

### Performance
- **Carregamento Rápido**: Assets otimizados
- **Responsividade**: Interface adaptável
- **Debounce**: Busca otimizada com delay
- **Lazy Loading**: Carregamento sob demanda
- **Cache**: Armazenamento local de dados

### Segurança
- **CORS Configurado**: Permite requisições cross-origin
- **Validação de Dados**: Verificação de entradas
- **Tratamento de Erros**: Mensagens de erro amigáveis
- **Sanitização**: Limpeza de inputs

### Acessibilidade
- **Cores Contrastantes**: Boa legibilidade
- **Feedback Visual**: Indicações claras de estado
- **Responsividade**: Suporte a diferentes dispositivos
- **Semântica**: HTML estruturado
- **ARIA**: Atributos de acessibilidade

## Melhorias Futuras

### Check List
- [ ] No JSON colocar 'nome na camisa' para facilitar o nome de busca
- [ ] Melhorar layout e design
- [ ] Deixa o botão de instruções funcional
- [ ] Melhorar modal de fim de jogo 
- [ ] Fazer Slides
- [ ] Colocar jogadores como: Calleri (SPFC), Memphis (Corinthans), Garro (Corinthans), e outros vocês perceberem que não tem

### Futuras
- [ ] Deploy da aplicação 

## Suporte e Manutenção

### Solução de Problemas
- Verificar logs do servidor
- Inspecionar console do navegador
- Limpar cache do navegador
- Verificar conexão com internet
- Reiniciar o servidor

### Atualizações
- Manter dependências atualizadas
- Verificar compatibilidade do navegador
- Testar em diferentes dispositivos
- Manter documentação atualizada

## Créditos

- **Dados**: Brasileirão Série A
- **Imagens**: Soccer Wiki
- **Design**: Interface moderna e responsiva

## Licença

Este projeto foi desenvolvido para fins educacionais e demonstrativos.

---

**Versão**: 1.1  
**Data**: Junho 2025  
**Status**: Funcional e Testado

