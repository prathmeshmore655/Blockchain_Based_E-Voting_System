// Get CSRF Token from cookies
const getCSRFToken = () => {
    const cookies = document.cookie.split("; ");
    const csrfCookie = cookies.find(row => row.startsWith("csrftoken="));
    return csrfCookie ? csrfCookie.split("=")[1] : "";
};






async function fetch_candidates() {

    try {
        const csrfToken = getCSRFToken(); // Get CSRF token from cookies
        console.log("CSRF Token:", csrfToken); // Debugging

        const response = await fetch("http://localhost:8000/Blockchain/fetch-candidates", {
            method: "GET",
            credentials: "include",
            headers: { 
                "Content-Type": "application/json", 
                "X-CSRFToken": csrfToken  // ✅ Correct CSRF header name
            },
        });

        const data = await response.json();
        console.log("Response:", data); 

        if (!response.ok) throw new Error(data.error || "Failed to Vote.");

        alert(data);

    } catch (error) {
        console.error("Error voting:", error);
    }
}


fetch_candidates(0) ; 


 





document.addEventListener("DOMContentLoaded", function () {
    // Data
    const candidates = ["Candidate A", "Candidate B", "Candidate C"];
    const votes = [450, 300, 250];
    const colors = ["#007bff", "#28a745", "#ffc107"];

    // Line Chart
    new Chart(document.getElementById("lineChart"), {
        type: "line",
        data: {
            labels: candidates,
            datasets: [{
                label: "Votes Over Time",
                data: votes,
                borderColor: "#007bff",
                fill: false,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });

    // Bar Chart
    new Chart(document.getElementById("barChart"), {
        type: "bar",
        data: {
            labels: candidates,
            datasets: [{
                label: "Vote Count",
                data: votes,
                backgroundColor: colors
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });

    // Pie Chart
    new Chart(document.getElementById("pieChart"), {
        type: "pie",
        data: {
            labels: candidates,
            datasets: [{
                data: votes,
                backgroundColor: colors
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
});
