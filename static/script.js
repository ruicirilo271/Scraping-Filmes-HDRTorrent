document.addEventListener("DOMContentLoaded", () => {
    const favButtons = document.querySelectorAll(".fav-btn");
    const favStorage = JSON.parse(localStorage.getItem("favorites")) || [];

    favButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            const movie = {
                title: btn.dataset.title,
                link: btn.dataset.link,
                image: btn.dataset.image
            };

            // verificar se já está nos favoritos
            const exists = favStorage.find(f => f.link === movie.link);

            if (!exists) {
                favStorage.push(movie);
                alert("Adicionado aos favoritos!");
            } else {
                const index = favStorage.findIndex(f => f.link === movie.link);
                favStorage.splice(index, 1);
                alert("Removido dos favoritos!");
            }

            localStorage.setItem("favorites", JSON.stringify(favStorage));
        });
    });

    document.getElementById("show-favorites").addEventListener("click", () => {
        const favs = JSON.parse(localStorage.getItem("favorites")) || [];
        const container = document.getElementById("movies");
        container.innerHTML = "";

        favs.forEach(movie => {
            const card = document.createElement("div");
            card.classList.add("movie-card");
            card.innerHTML = `
                <img src="${movie.image}" alt="${movie.title}">
                <h2>${movie.title}</h2>
                <div class="buttons">
                    <a href="${movie.link}" target="_blank" class="watch">🔗 Ver</a>
                </div>
            `;
            container.appendChild(card);
        });
    });
});
