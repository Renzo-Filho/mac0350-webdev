document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');

    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            // Evita que a página recarregue ao clicar em "Entrar"
            event.preventDefault(); 
            
            // Pega o valor do input de usuário
            const usuarioInput = document.getElementById('usuario').value;
            
            // Validação simples
            if(usuarioInput.trim() === '') {
                alert('Por favor, insira o seu número USP.');
                return;
            }

            // Simula uma tentativa de login
            alert(`Bem-vindo à nova interface USP!\nTentando acessar com o usuário: ${usuarioInput}`);
        });
    }
});