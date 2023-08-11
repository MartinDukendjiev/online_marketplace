function registerFormHandler() {
    document.querySelector('form').addEventListener('submit', function (event) {
        event.preventDefault();

        let searchTerm = document.querySelector('input[name="search"]').value;
        let url = window.location.origin + window.location.pathname + '?search=' + encodeURIComponent(searchTerm);

        fetch(url)
            .then(response => response.text())
            .then(html => {
                document.documentElement.innerHTML = html;
                document.getElementById('categories-section').scrollIntoView({behavior: 'smooth'});
                registerFormHandler();
            })
            .catch(error => {
                console.error('Възникна грешка при изпращане на формуляра:', error);
            });
    });
}

registerFormHandler();


