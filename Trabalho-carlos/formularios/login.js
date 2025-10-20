// login.js

const API_BASE_URL = 'http://127.0.0.1:8000';

const form = document.getElementById('loginForm');

form.addEventListener('submit', async (e) => {
    e.preventDefault(); 

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const dadosLogin = {
        username: username,
        password: password
    };

    try {
        // Rota que vamos criar na API: /usuarios/login
        const response = await fetch(`${API_BASE_URL}/usuarios/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dadosLogin) 
        });

        if (response.ok) {
            // Garanta que você está definindo 'data' DENTRO deste bloco
            const data = await response.json(); 
            
            alert('🤞 Autenticadeh! Bem-vinde !');
            
            // O acesso a 'data' deve estar AQUI
            localStorage.setItem('currentUser', data.username); 
            
            // Redirecionar para o dashboard
            window.location.href = 'dashboard.html'; 
            
        } else {
            // Se o status for 400 (Bad Request) ou 401 (Unauthorized)
            const errorData = await response.json();
            
            alert(`❌ Falha no Login: ${errorData.detail || 'Credenciais inválidas.'}`);
        }

    } catch (error) {
        console.error('Erro de conexão com a API:', error);
        alert('🚫 Não foi possível conectar ao servidor. Verifique se a API está rodando.');
    }
});
