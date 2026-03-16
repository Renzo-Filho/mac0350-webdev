document.addEventListener('DOMContentLoaded', () => {
    const sections = document.querySelectorAll("main > section");
    const navLinks = document.querySelectorAll('.nav-link');
    const themeBtn = document.getElementById('theme-toggle');

    // 1. Lógica de Navegação (SPA)
    function showSection(hash) {
        const targetId = hash || '#biography'; // Secão Padrão
        
        // Esconde todas e mostra o alvo
        sections.forEach(sec => sec.classList.add('hidden'));
        const targetSec = document.querySelector(targetId);
        
        if (targetSec) {
            targetSec.classList.remove('hidden');
        } else {
            document.querySelector('#biography').classList.remove('hidden');
        }

        // Atualiza a classe ativa no Menu
        navLinks.forEach(link => {
            link.classList.remove("active");
            if (link.getAttribute("href") === targetId) {
                link.classList.add("active");
            }
        });

        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    // Eventos de clique nos links
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const hash = link.getAttribute('href');
            history.pushState(null, null, hash);
            showSection(hash);
        });
    });

    // Suporte ao botão "Voltar" do navegador
    window.addEventListener('popstate', () => showSection(window.location.hash));

    // Inicialização
    showSection(window.location.hash);

    // 2. Lógica de Tema (Modo Escuro / Claro)
    const fapespLogo = document.getElementById('fapesp-logo'); // Pegamos a imagem da FAPESP

    themeBtn.addEventListener('click', () => {
        document.body.classList.toggle('light-mode');
        const isLight = document.body.classList.contains('light-mode');
        
        // Alterna o ícone do botão
        themeBtn.textContent = isLight ? '🌙' : '🌓';

        // Alterna a imagem da FAPESP
        if (fapespLogo) {
            fapespLogo.src = isLight ? 'img/fapesp-claro.png' : 'img/fapesp.png';
        }
    });
});
