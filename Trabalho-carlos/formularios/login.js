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
        
        const response = await fetch(`${API_BASE_URL}/usuarios/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dadosLogin) 
        });

        if (response.ok) {

            const data = await response.json(); 
            
            alert('🤞 Autenticadeh! Bem-vinde !');
            

            localStorage.setItem('currentUser', data.username); 
            

            window.location.href = 'dashboard.html'; 
            
        } else {

            const errorData = await response.json();
            
            alert(`❌ Falha no Login: ${errorData.detail || 'Credenciais inválidas.'}`);
        }

    } catch (error) {
        console.error('Erro de conexão com a API:', error);
        alert('🚫 Não foi possível conectar ao servidor. Verifique se a API está rodando.');
    }
});
