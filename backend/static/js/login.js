document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("login-form");
    const errorMessage = document.getElementById("error-message");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        errorMessage.classList.add("d-none");

        const username = document.getElementById("username").value;
        const voter_id = document.getElementById("voter_id").value;
        const password = document.getElementById("password").value;

        // Get CSRF Token from cookies
        const getCSRFToken = () => {
            const cookies = document.cookie.split("; ");
            const csrfCookie = cookies.find(row => row.startsWith("csrftoken="));
            return csrfCookie ? csrfCookie.split("=")[1] : "";
        };

        const csrfToken = getCSRFToken();
        console.log("CSRF Token:", csrfToken);

        if (!csrfToken) {
            errorMessage.textContent = "CSRF Token missing. Refresh and try again.";
            errorMessage.classList.remove("d-none");
            return;
        }

        try {
            const response = await fetch("http://127.0.0.1:8000/API/user-login", {
                method: "POST",
                credentials: "include", // Required to send cookies with request
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken,
                },
                body: JSON.stringify({ username, password, voter_id }),
            });

            const data = await response.json();

            if (response.ok) {
                localStorage.setItem("user", JSON.stringify({ username, voter_id }));
                alert("Login successful!");

                // Redirect to home page
                window.location.href = "home"; 
            } else {
                errorMessage.textContent = data.message || "Login failed.";
                errorMessage.classList.remove("d-none");
            }
        } catch (error) {
            errorMessage.textContent = "Something went wrong. Try again.";
            errorMessage.classList.remove("d-none");
            console.error("Login Error:", error);
        }
    });
});
