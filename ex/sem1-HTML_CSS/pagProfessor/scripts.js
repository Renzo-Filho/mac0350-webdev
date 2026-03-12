
// Atualiza o ano no footer
document.getElementById('year').textContent = new Date().getFullYear();

// ---------------------------------------------------
// LÓGICA DO MODO ESCURO
// ---------------------------------------------------
const htmlElement = document.documentElement;
const desktopToggle = document.getElementById('desktopThemeToggle');
const mobileToggle = document.getElementById('mobileThemeToggle');

// Checa a preferência do usuário ou do sistema no carregamento
if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    htmlElement.classList.add('dark');
    updateThemeIcons(true);
} else {
    htmlElement.classList.remove('dark');
    updateThemeIcons(false);
}

// Função para atualizar os ícones e texto do botão
function updateThemeIcons(isDark) {
    const icons = document.querySelectorAll('.dark-icon');
    const texts = document.querySelectorAll('.theme-text');
    
    icons.forEach(icon => {
        if(isDark) {
            icon.classList.remove('fa-moon');
            icon.classList.add('fa-sun');
            icon.style.color = '#fbbf24'; // cor amarela para o sol
        } else {
            icon.classList.remove('fa-sun');
            icon.classList.add('fa-moon');
            icon.style.color = 'inherit';
        }
    });

    texts.forEach(text => {
        text.textContent = isDark ? 'Modo Claro' : 'Modo Escuro';
    });
}

// Função de alternar tema
function toggleTheme() {
    htmlElement.classList.toggle('dark');
    const isDark = htmlElement.classList.contains('dark');
    
    if (isDark) {
        localStorage.theme = 'dark';
    } else {
        localStorage.theme = 'light';
    }
    updateThemeIcons(isDark);
}

desktopToggle.addEventListener('click', toggleTheme);
mobileToggle.addEventListener('click', toggleTheme);


// ---------------------------------------------------
// LÓGICA DO MENU MOBILE
// ---------------------------------------------------
const menuBtn = document.getElementById('menuBtn');
const closeMenuBtn = document.getElementById('closeMenuBtn');
const sidebar = document.getElementById('sidebar');
const overlay = document.getElementById('overlay');
const navLinks = document.querySelectorAll('.nav-link');

function openMenu() {
    sidebar.classList.add('open');
    overlay.classList.add('active');
}

function closeMenu() {
    sidebar.classList.remove('open');
    overlay.classList.remove('active');
}

menuBtn.addEventListener('click', openMenu);
closeMenuBtn.addEventListener('click', closeMenu);
overlay.addEventListener('click', closeMenu);

// ---------------------------------------------------
// LÓGICA DE NAVEGAÇÃO EM ABAS (SPA)
// ---------------------------------------------------
const sections = document.querySelectorAll("main > section");

function showSection(hash) {
    if (!hash || hash === '#') hash = '#about';
    
    // Oculta todas as seções
    sections.forEach(sec => sec.classList.add('hidden'));
    
    // Exibe a seção alvo
    const targetSec = document.querySelector(hash);
    if (targetSec) {
        targetSec.classList.remove('hidden');
    } else {
        document.getElementById('about').classList.remove('hidden');
        hash = '#about';
    }

    // Atualiza os estilos do menu lateral
    navLinks.forEach((link) => {
        link.classList.remove("active");
        if (link.getAttribute("href") === hash) {
            link.classList.add("active");
        }
    });
    
    // Retorna ao topo
    document.querySelector('.main-content').scrollTo({ top: 0, behavior: 'smooth' });
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Evento de clique nos links do menu
navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const hash = link.getAttribute('href');
        
        // Atualiza a URL sem recarregar a página
        history.pushState(null, null, hash);
        showSection(hash);

        // Fecha o menu mobile se estiver aberto
        if (window.innerWidth < 768) {
            closeMenu();
        }
    });
});

// Evento para quando usar Voltar/Avançar do navegador
window.addEventListener('popstate', () => {
    showSection(window.location.hash);
});

// Inicia na aba correta ao carregar a página
showSection(window.location.hash);
