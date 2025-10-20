// dashboard.js

const API_BASE_URL = 'http://127.0.0.1:8000';
const userInfoDiv = document.getElementById('userInfo');
const logoutBtn = document.getElementById('logoutBtn');

// 1. Verificar se o usuário está logado
const username = localStorage.getItem('currentUser');

if (!username) {
    alert('Você precisa estar logado para acessar esta página.');
    window.location.href = 'login.html'; // Redireciona para o login
} 

// 2. Função para buscar os dados do usuário
async function fetchUserInfo(username) {
    try {
        // Usa a rota GET /usuarios/{username} que criamos
        const response = await fetch(`${API_BASE_URL}/usuarios/${username}`);

        if (response.ok) {
           
           userInfoDiv.innerHTML = '<p> Você está logado!</p>'

        } else if (response.status === 404) {
            userInfoDiv.innerHTML = '<p>Erro: Usuário não encontrado na API.</p>';
            
        } else {
            const errorData = await response.json();
            userInfoDiv.innerHTML = `<p>Erro ao carregar dados: ${errorData.detail || 'Erro desconhecido.'}</p>`;
        }

    } catch (error) {
        userInfoDiv.innerHTML = '<p>🚫 Erro de conexão com a API.</p>';
        console.error('Erro de conexão:', error);
    }
}


logoutBtn.addEventListener('click', () => {
    // Limpa o username do armazenamento local
    localStorage.removeItem('currentUser');  
    alert('Você foi desconectado.');
    window.location.href = 'login.html'; // Redireciona
});