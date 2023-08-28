document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const response = await fetch('/login', {
        method: 'POST',
        body: new URLSearchParams({ username, password }) // Enviar os dados de autenticação como formulário
    });

    if (response.ok) {
        const data = await response.json();
        const token = data.token; // Extrair o token da resposta JSON

        window.location.href = '/notes';
    } else {
        alert('Usuário ou senha incorretos');
    }
});
