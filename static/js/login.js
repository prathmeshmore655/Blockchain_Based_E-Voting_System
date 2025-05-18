document.getElementById("login-form").addEventListener("submit", function(event) {
    event.preventDefault();

    let csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute("content");  // Get CSRF Token
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;

    fetch("http://127.0.0.1:8000/user_login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken  // Send CSRF Token in Headers
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)

        alert(data.message) ; 

        window.location.href = 'home' ; 
    
    })
    .catch(error => console.error("Error:", error));
});