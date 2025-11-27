function submitForm(even){
    even.preventDefault();
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const message = document.getElementById('message').value;

    const reponseDiv = document.getElementsByClassName('reponse');
    reponseDiv.innerHTML = '<strong>Nom:</strong> ${name} <br>
    <strong>Email:</strong> ${email}
    <strong>Message:</strong> ${message}';
}