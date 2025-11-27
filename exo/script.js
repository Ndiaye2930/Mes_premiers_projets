document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('contact-form');
    
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        
        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const message = document.getElementById('message').value;
        
        if (name && email && message) {
            alert('Merci, ' + name + '! Votre message a été envoyé.');
            form.reset();
        } else {
            alert('Veuillez remplir tous les champs.');
        }
    });
});