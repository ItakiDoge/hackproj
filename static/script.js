let jobs = [];
let currentJobIndex = 0;

document.addEventListener("DOMContentLoaded", async () => {
    await fetchJobs();
    renderJob();

    document.getElementById("like-button").addEventListener("click", () => swipe("like"));
    document.getElementById("dislike-button").addEventListener("click", () => swipe("dislike"));
});

function logOut() {
    window.location.href = "{{ url_for('login') }}";
}

async function fetchJobs() {
    const response = await fetch("/get_jobs");
    jobs = await response.json();
}

function renderJob() {
    const cardContainer = document.getElementById("card-container");
    cardContainer.innerHTML = "";

    if (currentJobIndex < jobs.length) {
        const job = jobs[currentJobIndex];

        const card = document.createElement("div");
        card.classList.add("card");
        card.innerHTML = `
            <img src="${job.image}" alt="${job.title}">
            <h2>${job.title}</h2>
            <p>${job.location}</p>
            <p>${job.salary}</p>
        `;
        cardContainer.appendChild(card);
    } else {
        cardContainer.innerHTML = "<p>No more jobs available.</p>";
    }
}


function swipe(action) {
    if (currentJobIndex < jobs.length) {
        const job = jobs[currentJobIndex];

        if (action === "like") {
            fetch("/match", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(job)
            }).then(() => console.log("Matched with job:", job.title));
        }

        currentJobIndex++;
        renderJob();
    }
}
