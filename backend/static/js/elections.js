document.addEventListener("DOMContentLoaded", async () => {
    const newsContainer = document.getElementById("news-container");
    const apiKey = "pub_7461627311f69ab645025907a1e7fa1c13723";

    async function fetchNews() {
        try {
            const response = await fetch(
                `https://newsdata.io/api/1/news?apikey=${apiKey}&country=in&category=politics&language=en`
            );
            const data = await response.json();

            displayNews(data.results);
        } catch (error) {
            console.error("Error fetching news:", error);
            newsContainer.innerHTML = "<p class='text-danger'>Failed to load news.</p>";
        }
    }

    function displayNews(articles) {
        newsContainer.innerHTML = "";
        articles.forEach(article => {
            const card = document.createElement("div");
            card.className = "col-md-4 mb-3";
            card.innerHTML = `
                <div class="card h-100 shadow">
                    ${article.image_url ? `<img src="${article.image_url}" class="card-img-top" alt="News Image">` : ""}
                    <div class="card-body">
                        <h5 class="card-title">${article.title}</h5>
                        <p class="card-text">${article.description || "No description available."}</p>
                        <a href="${article.link}" target="_blank" rel="noopener noreferrer" class="btn btn-primary">
                            Read More
                        </a>
                    </div>
                    <div class="card-footer">
                        <small class="text-muted">Source: ${article.source_id || "Unknown"}</small>
                    </div>
                </div>
            `;
            newsContainer.appendChild(card);
        });
    }

    fetchNews();
});
