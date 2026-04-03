document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');

    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            event.preventDefault(); 
            
            const usuarioInput = document.getElementById('usuario').value;
            
            if(usuarioInput.trim() === '') {
                alert('Por favor, insira o seu número USP.');
                return;
            }

            alert(`Bem-vindo à nova interface USP!\nTentando acessar com o usuário: ${usuarioInput}`);
        });
    }
});