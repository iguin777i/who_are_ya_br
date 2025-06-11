// Estado do jogo
const gameState = {
    sessionId: null,
    attempts: 0,
    hints: 0,
    maxAttempts: 8,
    maxHints: 2
};

// Elementos DOM
const elements = {
    // Header elements
    headerSearch: document.getElementById('header-search'),
    navToggle: document.getElementById('nav-toggle'),
    navDropdown: document.getElementById('nav-dropdown'),
    instructionsLink: document.getElementById('instructions-link'),
    newGameLink: document.getElementById('new-game-link'),

    // Game elements
    playerSearch: document.getElementById('playerSearch'),
    searchSuggestions: document.getElementById('search-suggestions'),
    hintBtn: document.getElementById('hint-btn'),
    currentAttempt: document.getElementById('current-attempt'),
    viewPhotoButton: document.getElementById('viewPhotoButton'),

    // Sidebar and attempts
    hintsSidebar: document.getElementById('hints-sidebar'),
    hintsList: document.getElementById('hints-list'),
    attemptsList: document.getElementById('attemptsList'),

    // Game state
    sessionId: document.getElementById('session-id'),
    attemptsLeft: document.getElementById('attempts-left'),
    hintsLeft: document.getElementById('hints-left'),
    loadingOverlay: document.getElementById('loadingOverlay'),
    guessedPlayerName: document.getElementById('guessed-player-name'),
    attemptCounter: document.getElementById('attempt-counter'),
    hintButton: document.getElementById('hintButton'),
    mysteryPlayer: document.getElementById('mysteryPlayer'),
    suggestionsDropdown: document.getElementById('suggestionsDropdown'),
    countryFlag: document.getElementById('country-flag'),
    playerPosition: document.getElementById('player-position'),
    submitButton: document.querySelector('.submit-button'),
    teamLogo: document.getElementById('team-logo')
};

// Verificar se todos os elementos necessários foram encontrados
function validateElements() {
    const requiredElements = [
        'playerSearch',
        'hintButton',
        'attemptsList',
        'mysteryPlayer'
    ];

    const missingElements = [];
    for (const elementId of requiredElements) {
        if (!elements[elementId]) {
            missingElements.push(elementId);
        }
    }

    if (missingElements.length > 0) {
        console.error('Elementos não encontrados:', missingElements);
        return false;
    }
    return true;
}

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    if (validateElements()) {
        startNewGame();
    } else {
        showError('Erro ao inicializar o jogo. Por favor, recarregue a página.');
    }

    // Event listeners
    elements.playerSearch.addEventListener('input', handlePlayerSearch);
    elements.hintButton.addEventListener('click', handleHint);
    elements.viewPhotoButton.addEventListener('click', handleViewPhoto);

    // Adicionar event listeners para a navegação
    elements.navToggle.addEventListener('click', toggleNavDropdown);
    document.addEventListener('click', (event) => {
        if (!elements.navDropdown.contains(event.target) && !elements.navToggle.contains(event.target)) {
            hideNavDropdown();
        }
    });

    // Adicionar evento de Enter no input
    elements.playerSearch.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            handleSubmit();
        }
    });
});

// Função para lidar com a pesquisa de jogadores
async function handlePlayerSearch(event) {
    const query = event.target.value.trim();

    if (query.length < 2) {
        elements.suggestionsDropdown.innerHTML = '';
        elements.suggestionsDropdown.classList.remove('show');
        return;
    }

    try {
        const response = await fetch(`/api/players/search?q=${encodeURIComponent(query)}`);
        const data = await response.json();

        elements.suggestionsDropdown.innerHTML = '';

        if (data.length > 0) {
            data.forEach(player => {
                const suggestionItem = document.createElement('div');
                suggestionItem.className = 'suggestion-item';
                suggestionItem.innerHTML = `
                    <div class="suggestion-content">
                        <span class="suggestion-name">${player.name}</span>
                        <span class="suggestion-team">${player.team}</span>
                    </div>
                `;

                suggestionItem.addEventListener('click', () => {
                    elements.playerSearch.value = player.name;
                    elements.suggestionsDropdown.classList.remove('show');
                    handleSubmit(); // Enviar automaticamente ao clicar
                });

                elements.suggestionsDropdown.appendChild(suggestionItem);
            });

            elements.suggestionsDropdown.classList.add('show');
        } else {
            elements.suggestionsDropdown.classList.remove('show');
        }
    } catch (error) {
        console.error('Erro ao buscar jogadores:', error);
    }
}

// Fechar dropdown ao clicar fora
document.addEventListener('click', (event) => {
    if (!elements.playerSearch.contains(event.target) && !elements.suggestionsDropdown.contains(event.target)) {
        elements.suggestionsDropdown.classList.remove('show');
    }
});

// Função para criar o item de tentativa
function createAttemptItem(comparison, attemptNumber) {
    const attemptItem = document.createElement('div');
    attemptItem.className = 'attempt-item';

    // Cabeçalho com nome do jogador
    const attemptHeader = document.createElement('div');
    attemptHeader.className = 'attempt-header';

    const playerName = document.createElement('div');
    playerName.className = 'attempt-player-name';
    playerName.textContent = comparison.name;

    attemptHeader.appendChild(playerName);
    attemptItem.appendChild(attemptHeader);

    // Detalhes da tentativa
    const attemptDetails = document.createElement('div');
    attemptDetails.className = 'attempt-details';

    // Função para determinar o ícone da posição
    function getPositionIcon(position) {
        const firstPosition = position.split(',')[0].trim();
        if (firstPosition.includes('D')) return 'Zagueiro.svg';
        if (firstPosition.includes('M')) return 'Meia.svg';
        if (firstPosition.includes('A')) return 'Atacante.svg';
        if (firstPosition.includes('G')) return 'Goleiro.svg';
        return 'Meia.svg'; // fallback
    }

    // Adicionar atributos
    const attributes = [
        {
            key: 'team',
            label: 'Time',
            value: comparison.team,
            type: 'image',
            imageUrl: comparison.team_logo
        },
        {
            key: 'nationality',
            label: 'Nacionalidade',
            value: comparison.nationality,
            type: 'image',
            imageUrl: comparison.nationality_flag
        },
        {
            key: 'position',
            label: 'Posição',
            value: comparison.position,
            type: 'image',
            imageUrl: `/static/images/icon-posicao/${getPositionIcon(comparison.position)}`
        },
        {
            key: 'age',
            label: 'Idade',
            value: comparison.age,
            type: 'number',
            arrow: comparison.arrows.age
        },
        {
            key: 'shirt_number',
            label: 'Número',
            value: comparison.shirt_number,
            type: 'number',
            arrow: comparison.arrows.shirt_number
        }
    ];

    attributes.forEach(attr => {
        const attributeDiv = document.createElement('div');
        attributeDiv.className = 'attempt-attribute';

        const label = document.createElement('div');
        label.className = 'attribute-label';
        label.textContent = attr.label;

        const value = document.createElement('div');
        value.className = `attribute-value ${comparison.correct[attr.key] ? 'correct' : 'wrong'}`;

        if (attr.type === 'image' && attr.imageUrl) {
            const img = document.createElement('img');
            img.src = attr.imageUrl;
            img.alt = attr.value;

            // Definir a classe da imagem com base no tipo de atributo
            if (attr.key === 'team') {
                img.className = 'team-logo';
            } else if (attr.key === 'nationality') {
                img.className = 'flag-icon';
            } else if (attr.key === 'position') {
                img.className = 'position-icon'; // Nova classe para ícones de posição
            }

            value.appendChild(img);
        } else {
            value.textContent = attr.value;

            if (attr.type === 'number' && attr.arrow && attr.arrow !== 'equal') {
                const arrow = document.createElement('span');
                arrow.className = 'arrow';
                arrow.textContent = attr.arrow === 'up' ? '↑' : '↓';
                value.appendChild(arrow);
            }
        }

        attributeDiv.appendChild(label);
        attributeDiv.appendChild(value);
        attemptDetails.appendChild(attributeDiv);
    });

    attemptItem.appendChild(attemptDetails);
    return attemptItem;
}

// Função para lidar com o envio da tentativa
async function handleSubmit() {
    const guessName = elements.playerSearch.value.trim();

    if (!guessName) {
        return;
    }

    try {
        const response = await fetch('/api/guess', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                session_id: gameState.sessionId,
                guess_name: guessName
            })
        });

        const data = await response.json();

        if (response.ok) {
            // Limpar o input após enviar
            elements.playerSearch.value = '';
            elements.suggestionsDropdown.innerHTML = '';
            elements.suggestionsDropdown.classList.remove('show');

            // Adicionar a tentativa à lista
            const attemptItem = createAttemptItem(data.comparison, gameState.attempts + 1);
            elements.attemptsList.appendChild(attemptItem);

            // Atualizar contador de tentativas
            gameState.attempts = data.attempts_left;

            // Verificar se o jogo acabou
            if (data.game_over) {
                if (data.won) {
                    showGameOver(true, data.correct_player);
                } else {
                    showGameOver(false, data.correct_player);
                }
                // Desabilitar o input e o botão de submit
                elements.playerSearch.disabled = true;
                elements.hintButton.disabled = true;
            }
        } else {
            console.error('Erro ao fazer tentativa:', data.error);
        }
    } catch (error) {
        console.error('Erro ao fazer tentativa:', error);
    }
}

// Função para lidar com o botão "Ver Foto"
async function handleViewPhoto() {
    if (!gameState.sessionId) {
        showError('Jogo não iniciado.');
        return;
    }

    try {
        const response = await fetch(`/api/photo/${gameState.sessionId}`);
        const data = await response.json();

        if (response.ok) {
            const imageUrl = data.image_url;
            if (imageUrl) {
                const mysteryPlayerDiv = elements.mysteryPlayer;
                mysteryPlayerDiv.innerHTML = '<img src="' + imageUrl + '" alt="Jogador" class="silhouette-image" />';
                mysteryPlayerDiv.classList.add('hint-active'); // Apply hint animation
                elements.viewPhotoButton.disabled = true;
                showSuccess('Foto do jogador revelada!');
            } else {
                showError('Foto do jogador não disponível.');
            }
        } else {
            showError(`Erro ao obter foto: ${data.error}`);
        }
    } catch (error) {
        console.error('Erro ao obter foto:', error);
        showError('Erro de conexão ao obter foto.');
    }
}

// Navigation functions
function toggleNavDropdown() {
    elements.navDropdown.classList.toggle('show');
}

function hideNavDropdown() {
    elements.navDropdown.classList.remove('show');
}

function showInstructions() {
    alert('Como Jogar:\\n\\n1. Você tem 8 tentativas para adivinhar o jogador\\n2. Use até 2 dicas para te ajudar\\n3. Digite o nome do jogador e veja as comparações\\n4. Verde = Correto, Vermelho = Incorreto\\n5. Setas indicam se o valor é maior ou menor');
}

// Mostrar/esconder loading
function toggleLoading(show) {
    if (elements.loadingOverlay) {
        elements.loadingOverlay.classList.toggle('hidden', !show);
    }
}

// Função para limpar tentativas
function clearAttempts() {
    if (elements.attemptsList) {
        elements.attemptsList.innerHTML = '';
    }
}

// Função para mostrar erro
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    
    document.body.appendChild(errorDiv);
    
    setTimeout(() => {
        errorDiv.remove();
    }, 3000);
}

// Função para limpar dicas
function clearHints() {
    if (elements.hintsList) {
        elements.hintsList.innerHTML = '';
    }
}

// Função para atualizar contador de tentativas
function updateAttemptsCounter() {
    const currentAttempt = document.getElementById('current-attempt');
    if (currentAttempt) {
        currentAttempt.textContent = gameState.attemptsLeft;
    }
}

// Função para atualizar contador de dicas
function updateHintsCounter() {
    const hintsLeft = document.getElementById('hints-left');
    if (hintsLeft) {
        hintsLeft.textContent = gameState.hintsLeft;
    }
}

// Função para iniciar novo jogo
async function startNewGame() {
    try {
        // Mostrar loading
        toggleLoading(true);

        const response = await fetch('/api/start-game', {
            method: 'POST'
        });

        const data = await response.json();

        if (response.ok) {
            // Atualizar estado do jogo
            gameState.sessionId = data.session_id;
            gameState.attempts = 0;
            gameState.hints = data.max_hints;
            gameState.maxAttempts = data.max_attempts;
            gameState.maxHints = data.max_hints;

            // Limpar tentativas anteriores
            elements.attemptsList.innerHTML = '';

            // Resetar elementos
            elements.playerSearch.value = '';
            elements.playerSearch.disabled = false;
            elements.hintButton.disabled = false;
            elements.viewPhotoButton.disabled = false;

            // Resetar dicas
            const countryFlag = elements.countryFlag;
            const playerPosition = elements.playerPosition;
            const teamLogo = elements.teamLogo;

            if (countryFlag) {
                countryFlag.classList.remove('hint-active', 'text-hint');
                countryFlag.innerHTML = '';
            }
            if (playerPosition) {
                playerPosition.classList.remove('hint-active', 'text-hint');
                playerPosition.innerHTML = '';
            }
            if (teamLogo) {
                teamLogo.classList.remove('hint-active', 'text-hint');
                teamLogo.innerHTML = '';
            }

            // Reset mystery player image to question mark
            const mysteryPlayerDiv = elements.mysteryPlayer;
            if (mysteryPlayerDiv) {
                mysteryPlayerDiv.innerHTML = '<div class="question-mark">?</div>';
                mysteryPlayerDiv.classList.remove('hint-active');
            }
        } else {
            console.error('Erro ao iniciar jogo:', data.error);
        }
    } catch (error) {
        console.error('Erro ao iniciar jogo:', error);
    } finally {
        // Esconder loading
        toggleLoading(false);
    }
}

// Função para lidar com as dicas
async function handleHint() {
    if (gameState.hints <= 0) {
        console.warn('No more hints available.');
        elements.hintButton.disabled = true;
        return;
    }

    try {
        const response = await fetch('/api/hint', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                session_id: gameState.sessionId
            })
        });

        const data = await response.json();

        if (response.ok) {
            const hint = data.hint;
            gameState.hints = data.hints_left;

            let targetElement;
            if (hint.type === 'nationality') {
                targetElement = elements.countryFlag;
            } else if (hint.type === 'position') {
                targetElement = elements.playerPosition;
            } else if (hint.type === 'team') {
                targetElement = elements.teamLogo;
            }

            if (targetElement) {
                console.log('Elemento alvo encontrado:', hint.type); // Debug

                // Limpar o elemento antes de adicionar a nova dica
                targetElement.innerHTML = '';
                targetElement.classList.remove('hint-active', 'text-hint');

                targetElement.classList.add('hint-active');

                // Criar o conteúdo da dica
                const hintContent = document.createElement('div');
                hintContent.className = 'hint-content';

                if (hint.type === 'position') {
                    // Para posição, mostrar o ícone
                    const img = document.createElement('img');
                    img.src = `/static/images/icon-posicao/${getPositionIcon(hint.display)}`;
                    img.alt = hint.display;
                    img.className = 'position-icon';
                    hintContent.appendChild(img);
                } else if (hint.type === 'team') {
                    // Para time, mostrar apenas o logo
                    if (hint.image_url) {
                        const img = document.createElement('img');
                        img.src = hint.image_url;
                        img.alt = hint.display;
                        img.className = 'team-icon';
                        hintContent.appendChild(img);
                    }
                } else if (hint.type === 'nationality') {
                    // Para nacionalidade, mostrar apenas a bandeira
                    if (hint.image_url) {
                        const img = document.createElement('img');
                        img.src = hint.image_url;
                        img.alt = hint.display;
                        img.className = 'flag-icon';
                        hintContent.appendChild(img);
                    }
                }

                targetElement.appendChild(hintContent);

                // Desabilitar o botão se não houver mais dicas
                if (data.hints_left === 0) {
                    elements.hintButton.disabled = true;
                }
                showSuccess(`Dica obtida: ${hint.display}`);
            } else {
                console.error('Elemento alvo não encontrado:', hint.type); // Debug
            }
        } else {
            console.error('Erro ao obter dica:', data.error);
            showError('Erro ao obter dica. Tente novamente.');
            elements.hintButton.disabled = true;
        }
    } catch (error) {
        console.error('Erro ao obter dica:', error);
        showError('Erro de conexão ao obter dica.');
        elements.hintButton.disabled = true;
    }
}

// Função para determinar o ícone da posição
function getPositionIcon(position) {
    const firstPosition = position.split(',')[0].trim();
    if (firstPosition.includes('D')) return 'Zagueiro.svg';
    if (firstPosition.includes('M')) return 'Meia.svg';
    if (firstPosition.includes('A')) return 'Atacante.svg';
    if (firstPosition.includes('G')) return 'Goleiro.svg';
    return 'Meia.svg'; // fallback
}

// Função para mostrar resultado (antiga, substituída por showGameOver)
function showResult(won, correctPlayer) {
    const message = won ?
        `🎉 Parabéns! Você acertou em ${gameState.currentAttempt - 1} tentativa${gameState.currentAttempt - 1 !== 1 ? 's' : ''}!` :
        `😔 Que pena! O jogador era: ${correctPlayer.Nome}`;

    alert(message);

    // Opção de jogar novamente
    if (confirm('Deseja jogar novamente?')) {
        startNewGame();
    }
}

// Debounce function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Função para tentar carregar silhueta (descontinuada)
async function tryLoadSilhouette() {
    // Esta função não é mais necessária pois a silhueta foi removida do HTML
    // E o ? é exibido por padrão.
}

// Função para criar um badge de dica (usado na sidebar)
function createHintBadge(hint) {
    const badge = document.createElement('div');
    badge.className = 'hint-badge';

    // Criar o tooltip
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';

    // Definir o texto do tooltip baseado no tipo de dica
    let tooltipText = '';
    switch (hint.type) {
        case 'nationality':
            tooltipText = `Nacionalidade: ${hint.display}`;
            badge.classList.add('nationality-hint');
            break;
        case 'position':
            tooltipText = `Posição: ${hint.display}`;
            badge.classList.add('position-hint');
            break;
        case 'team':
            tooltipText = `Time: ${hint.display}`;
            badge.classList.add('team-hint');
            break;
    }

    tooltip.textContent = tooltipText;

    const content = document.createElement('div');
    content.className = 'hint-content';

    if (hint.image_url) {
        const img = document.createElement('img');
        img.src = hint.image_url;
        img.alt = hint.display;
        content.appendChild(img);
    }

    const text = document.createElement('span');
    text.className = 'hint-text';
    text.textContent = hint.display;
    content.appendChild(text);

    badge.appendChild(tooltip);
    badge.appendChild(content);
    return badge;
}

function showGameOver(won, correctPlayer) {
    // Remover qualquer overlay existente
    const existingOverlay = document.querySelector('.game-overlay');
    if (existingOverlay) {
        existingOverlay.remove();
    }

    const gameOverDiv = document.createElement('div');
    gameOverDiv.className = 'game-over';

    const message = document.createElement('h2');
    message.textContent = won ? 'Parabéns! Você acertou!' : 'Fim de jogo!';
    message.className = won ? 'win-message' : 'lose-message';

    const playerInfo = document.createElement('div');
    playerInfo.className = 'correct-player-info';
    playerInfo.innerHTML = `
        <h3>O jogador era:</h3>
        <p>${correctPlayer.Nome}</p>
        <p>${correctPlayer.Time}</p>
        <p>${correctPlayer.Posição}</p>
        <p>${correctPlayer.Nacionalidade}</p>
    `;

    const statsDiv = document.createElement('div');
    statsDiv.className = 'game-stats';
    statsDiv.innerHTML = `
        <p>Tentativas utilizadas: ${gameState.currentAttempt - 1} de ${gameState.maxAttempts}</p>
        <p>Dicas utilizadas: ${gameState.maxHints - gameState.hints} de ${gameState.maxHints}</p>
    `;

    const newGameButton = document.createElement('button');
    newGameButton.textContent = 'Novo Jogo';
    newGameButton.className = 'new-game-button';
    newGameButton.onclick = () => {
        startNewGame();
        const overlay = document.querySelector('.game-overlay');
        if (overlay) {
            overlay.remove();
        }
    };

    gameOverDiv.appendChild(message);
    gameOverDiv.appendChild(playerInfo);
    gameOverDiv.appendChild(statsDiv);
    gameOverDiv.appendChild(newGameButton);

    // Adicionar o overlay de fim de jogo
    const overlay = document.createElement('div');
    overlay.className = 'game-overlay';
    overlay.appendChild(gameOverDiv);

    document.body.appendChild(overlay);

    // Desabilitar interações com o jogo
    const playerSearch = document.getElementById('playerSearch');
    const hintButton = document.getElementById('hintButton');
    const submitButton = document.querySelector('.submit-button');

    if (playerSearch) playerSearch.disabled = true;
    if (hintButton) hintButton.disabled = true;
    if (submitButton) submitButton.disabled = true;
}

// Função para desabilitar interações com o jogo
function disableGameInteractions() {
    const playerSearch = document.getElementById('playerSearch');
    const hintButton = document.getElementById('hintButton');
    const submitButton = document.querySelector('.submit-button');

    if (playerSearch) playerSearch.disabled = true;
    if (hintButton) hintButton.disabled = true;
    if (submitButton) submitButton.disabled = true;
}

// Utilitários
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Função para carregar a silhueta
async function tryLoadSilhouette() {
    const silhouetteImg = document.getElementById('player-silhouette');
    const questionMark = document.querySelector('.question-mark');

    if (!gameState || !gameState.silhouetteUrl) {
        console.error('URL da silhueta não disponível');
        return;
    }

    try {
        console.log('Tentando carregar silhueta:', gameState.silhouetteUrl);
        silhouetteImg.src = gameState.silhouetteUrl;

        silhouetteImg.onload = function () {
            console.log('Silhueta carregada com sucesso');
            silhouetteImg.style.display = 'block';
            questionMark.style.display = 'none';
        };

        silhouetteImg.onerror = function () {
            console.error('Erro ao carregar silhueta');
            silhouetteImg.style.display = 'none';
            questionMark.style.display = 'block';
        };
    } catch (error) {
        console.error('Erro ao tentar carregar silhueta:', error);
        silhouetteImg.style.display = 'none';
        questionMark.style.display = 'block';
    }
}

function createHintBadge(hint) {
    const badge = document.createElement('div');
    badge.className = 'hint-badge';

    // Criar o tooltip
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';

    // Definir o texto do tooltip baseado no tipo de dica
    let tooltipText = '';
    switch (hint.type) {
        case 'nationality':
            tooltipText = `Nacionalidade: ${hint.display}`;
            badge.classList.add('nationality-hint');
            break;
        case 'position':
            tooltipText = `Posição: ${hint.display}`;
            badge.classList.add('position-hint');
            break;
        case 'team':
            tooltipText = `Time: ${hint.display}`;
            badge.classList.add('team-hint');
            break;
    }

    tooltip.textContent = tooltipText;

    const content = document.createElement('div');
    content.className = 'hint-content';

    if (hint.image_url) {
        const img = document.createElement('img');
        img.src = hint.image_url;
        img.alt = hint.display;
        content.appendChild(img);
    }

    const text = document.createElement('span');
    text.className = 'hint-text';
    text.textContent = hint.display;
    content.appendChild(text);

    badge.appendChild(tooltip);
    badge.appendChild(content);
    return badge;
}

// Função para inicializar elementos DOM
function initializeDOMElements() {
    // Verificar se todos os elementos necessários existem
    const requiredElements = [
        'playerSearch',
        'hintButton',
        'submitButton',
        'attemptsList',
        'hintsList',
        'currentAttempt',
        'loadingOverlay',
        'country-flag',
        'player-position',
        'team-logo'
    ];

    const missingElements = requiredElements.filter(id => !document.getElementById(id));
    if (missingElements.length > 0) {
        console.error('Elementos DOM necessários não encontrados:', missingElements);
        return false;
    }

    // Inicializar elementos
    elements.playerSearch = document.getElementById('playerSearch');
    elements.hintButton = document.getElementById('hintButton');
    elements.submitButton = document.querySelector('.submit-button');
    elements.attemptsList = document.getElementById('attemptsList');
    elements.hintsList = document.getElementById('hintsList');
    elements.currentAttempt = document.getElementById('current-attempt');
    elements.loadingOverlay = document.getElementById('loadingOverlay');
    elements.countryFlag = document.getElementById('country-flag');
    elements.playerPosition = document.getElementById('player-position');
    elements.teamLogo = document.getElementById('team-logo');

    // Adicionar event listeners
    elements.playerSearch.addEventListener('input', handlePlayerSearch);
    elements.hintButton.addEventListener('click', handleHint);
    elements.submitButton.addEventListener('click', handleSubmit);

    return true;
}

// Função para atualizar contadores
function updateCounters() {
    if (elements.currentAttempt) {
        elements.currentAttempt.textContent = `Tentativa ${gameState.currentAttempt} de ${gameState.maxAttempts}`;
    }
}

// Função para mostrar mensagem de sucesso
function showSuccess(message) {
    const successDiv = document.createElement('div');
    successDiv.className = 'success-message';
    successDiv.textContent = message;
    
    document.body.appendChild(successDiv);
    
    setTimeout(() => {
        successDiv.remove();
    }, 3000);
}

// Função para habilitar/desabilitar interações
function toggleGameInteractions(enable) {
    if (elements.playerSearch) elements.playerSearch.disabled = !enable;
    if (elements.hintButton) elements.hintButton.disabled = !enable;
    if (elements.submitButton) elements.submitButton.disabled = !enable;
}