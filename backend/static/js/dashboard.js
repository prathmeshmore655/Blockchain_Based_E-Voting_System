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




document.addEventListener("DOMContentLoaded", async function () {
    const csrfToken = getCSRFToken();

    try {
        // Fetch votes data (which already includes candidate names)
        const voteResponse = await fetch("http://localhost:8000/Blockchain/fetch-votes", {
            method: "GET",
            credentials: "include",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            }
        });

        if (!voteResponse.ok) {
            throw new Error("Failed to fetch votes data");
        }

        const votesData = await voteResponse.json();

        console.log("data :", votesData);

        // Extract candidate names and votes
        const candidates = votesData.candidates.map(candidate => candidate.name);
        const votes = votesData.candidates.map(candidate => candidate.votes);
        const colors = ["#007bff", "#28a745", "#ffc107", "#dc3545", "#6f42c1"]; // Extend for more candidates


        document.getElementById('participation').value = votesData.defined.participation ; 
        document.getElementById('t_voters').value = votesData.defined.total_voters ; 
        document.getElementById('options').value = votesData.defined.options ; 

        // Function to create a chart
        function createChart(ctx, type, labels, datasetLabel, datasetData, datasetColors) {
            new Chart(ctx, {
                type: type,
                data: {
                    labels: labels,
                    datasets: [{
                        label: datasetLabel,
                        data: datasetData,
                        backgroundColor: datasetColors,
                        borderColor: type === "line" ? "#007bff" : datasetColors,
                        fill: type === "line" ? false : true,
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            ticks: {
                                precision: 0, // Ensures whole numbers only
                                stepSize: 1 // Ensures increments of 1
                            }
                        }
                    }
                }
            });
        }

        // Initialize charts
        createChart(document.getElementById("lineChart"), "line", candidates, "Votes Over Time", votes, colors);
        createChart(document.getElementById("barChart"), "bar", candidates, "Vote Count", votes, colors);
        createChart(document.getElementById("pieChart"), "pie", candidates, "Vote Share", votes, colors);

    } catch (error) {
        console.error("Error loading vote data:", error);
    }
});
