function getCSRFToken() {
    let cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        let cookie = cookies[i].trim();
        if (cookie.startsWith('csrftoken=')) {
            return cookie.split('=')[1];
        }
    }
    return '';
}


const csrfToken = getCSRFToken();
console.log("CSRF Token:", csrfToken);







document.addEventListener("DOMContentLoaded", async () => {
    const candidatesList = document.getElementById("candidates-list");
    const modal = new bootstrap.Modal(document.getElementById("candidateModal"));

    // Function to fetch candidates from API
    async function fetchCandidates() {
            try {
                const response = await fetch("http://localhost:8000/API/get-candidates", {
                    method: "GET",
                    credentials: "include",
                    headers: { "Content-Type": "application/json" , 
                        "X-CSRFToken": csrfToken
                    }
                });

            if (!response.ok) throw new Error("Failed to fetch candidates.");

            const data = await response.json();
            console.log(data); 

            displayCandidates(data);  // ✅ Fix: Pass 'data' directly
        } catch (error) {
            console.error("Error fetching candidates:", error);
        }
    }

    // Function to display candidates in the table
    function displayCandidates(candidates) {
        candidatesList.innerHTML = "";
        candidates.forEach((candidate, index) => {
            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${index + 1}</td>
                <td><img src="http://localhost:8000${candidate.photo}" class="candidate-img"></td>
                <td>${candidate.name}</td>
                <td>${candidate.party}</td>
                <td>${candidate.election_position}</td>
                <td><img src="http://localhost:8000${candidate.election_sign}" class="candidate-img"></td>
                <td>
                    <button class="btn btn-info btn-sm" onclick="showCandidateDetails(${index})">Info</button>
                </td>
                <td>
                    <button class="btn btn-primary btn-sm" onclick="Vote_candidate(${candidate.candidate_id})">Vote</button>

                </td>
            `;

            candidatesList.appendChild(row);
        });

        // Store candidates globally for modal access
        window.candidatesData = candidates;
    }

    // Function to show candidate details in modal
    window.showCandidateDetails = (index) => {
        const candidate = window.candidatesData[index];

        document.getElementById("candidate-photo").src = `http://localhost:8000/${candidate.photo}`;
        document.getElementById("candidate-name").textContent = candidate.name;
        document.getElementById("candidate-party").textContent = candidate.party;
        document.getElementById("candidate-age").textContent = candidate.age;
        document.getElementById("candidate-position").textContent = candidate.election_position;
        document.getElementById("candidate-bio").textContent = candidate.bio;
        document.getElementById("candidate-sign").src = `http://localhost:8000${candidate.election_sign}`;

        modal.show();
    };

    // Fetch candidates on page load
    fetchCandidates();
});




async function Vote_candidate(candidate_id) {

    voter_id = document.getElementById('user_id').value ; 
    try {
        const csrfToken = getCSRFToken(); // Get CSRF token from cookies
        console.log("CSRF Token:", csrfToken); // Debugging

        const response = await fetch("http://localhost:8000/Blockchain/blockchain-api", {
            method: "POST",
            credentials: "include",
            headers: { 
                "Content-Type": "application/json", 
                "X-CSRFToken": csrfToken  // ✅ Correct CSRF header name
            },
            body: JSON.stringify({ "action" : "vote" , "candidate_id": candidate_id , "voter_id" : voter_id })
        });

        const data = await response.json();
        console.log("Vote API Response:", data); 

        if (!response.ok) throw new Error(data.error || "Failed to Vote.");

        alert(data.message);

    } catch (error) {
        console.error("Error voting:", error);
    }
}
