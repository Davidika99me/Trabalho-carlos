// dashboard.js

const API_BASE_URL = 'http://127.0.0.1:8000';
const userInfoDiv = document.getElementById('userInfo');
const logoutBtn = document.getElementById('logoutBtn');


const username = localStorage.getItem('currentUser');

if (!username) {
    alert('Você precisa estar logado para acessar esta página.');
    window.location.href = 'login.html'; 
} else {
 
    fetchUserInfo(username);
}


async function fetchUserInfo(username) {
    try {

        const response = await fetch(`${API_BASE_URL}/usuarios/${username}`);

        if (response.ok) {
            
           
            userInfoDiv.innerHTML = `Bem-vindo(a), ${username}! 😘`; 

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
   
    localStorage.removeItem('currentUser');  
    
    fetch(`${API_BASE_URL}/usuarios/logout`, { method: 'POST' });
    
    alert('Você foi desconectado.');
    window.location.href = 'login.html';
});