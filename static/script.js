document.getElementById('registrationForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const name = document.getElementById('name').value;
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const email = document.getElementById('email').value;

    const data = {
        name: name,
        username: username,
        password: password,
        email: email
    };

    try {
        const response = await fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        const result = await response.json();
        document.getElementById('result').innerText = result.message;

        if (result.redirect) {
            document.getElementById('registrationSection').style.display = 'none';
            document.getElementById('alzheimerSection').style.display = 'block';
        }
    } catch (error) {
        document.getElementById('result').innerText = 'An error occurred. Please try again.';
    }
});

document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(this);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('resultAlzheimer').innerText = data.message || 'Error uploading image';
    })
    .catch(error => {
        document.getElementById('resultAlzheimer').innerText = 'An error occurred. Please try again.';
    });a
});
