document.getElementById('theme-toggle').addEventListener('click', function(event) {
    event.preventDefault();
    var navbar = document.getElementById('navbar');
    var body = document.getElementById('body');
    var sidebar = document.getElementById('sidebar');
    
    if (navbar.classList.contains('navbar-dark')) {
        toggleTheme('light');
    } else {
        toggleTheme('dark');
    }
});

window.onload = function() {
    var navbar = document.getElementById('navbar');
    var body = document.getElementById('body');
    var sidebar = document.getElementById('sidebar');  
    var theme = localStorage.getItem('theme');
    toggleTheme(theme || 'light');

    setTimeout(function() {
        var messages = document.querySelectorAll('.alert');
        messages.forEach(function(message) {
            message.classList.add('hide-message');
        });
    }, 2000);  // 2 seconds
}

function toggleTheme(theme) {
    var navbar = document.getElementById('navbar');
    var body = document.getElementById('body');
    var sidebar = document.getElementById('sidebar');

    if (theme === 'light') {
        navbar.classList.remove('navbar-dark', 'bg-dark');
        navbar.classList.add('navbar-light', 'bg-light');
        body.classList.remove('bg-dark-theme');
        body.classList.add('bg-light-theme');
        sidebar.classList.remove('bg-dark');
        sidebar.classList.add('bg-light');
        localStorage.setItem('theme', 'light');
    } else {
        navbar.classList.remove('navbar-light', 'bg-light');
        navbar.classList.add('navbar-dark', 'bg-dark');
        body.classList.remove('bg-light-theme');
        body.classList.add('bg-dark-theme');
        sidebar.classList.remove('bg-light');
        sidebar.classList.add('bg-dark');
        localStorage.setItem('theme', 'dark');
    }
}
