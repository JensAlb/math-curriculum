/**
 * app.js
 * ----------------------------------------------
 * Lädt Jahrgänge, Themen und aktiviert Drag & Drop.
 * ----------------------------------------------
 */

// Wird geladen, sobald das HTML fertig ist
document.addEventListener("DOMContentLoaded", () => {
    loadJahrgaenge();
    loadThemen();

    const searchInput = document.getElementById("searchInput");
    searchInput.addEventListener("input", loadThemen);
});


// -------------------------------------------------
// Jahrgänge laden und Spalten erzeugen
// -------------------------------------------------
async function loadJahrgaenge() {
    const res = await fetch("/api/jahrgaenge");
    const jahrgaenge = await res.json();

    const container = document.getElementById("jahrgaengeRow");
    container.innerHTML = ""; // leeren

    jahrgaenge.forEach(jg => {
        // Bootstrap-Spalte erstellen
        const col = document.createElement("div");
        col.classList.add("col-4");

        col.innerHTML = `
            <div class="card mb-3">
                <div class="card-header fw-bold">${jg.name}</div>
                <ul class="list-group list-group-flush thema-list"
                    data-jahrgang-id="${jg.id}">
                </ul>
            </div>
        `;

        container.appendChild(col);

        // Drag & Drop aktivieren
        const list = col.querySelector(".thema-list");
        enableDragDrop(list);
    });
}


// -------------------------------------------------
// Themen laden und in die jeweiligen Jahrgänge verteilen
// -------------------------------------------------
async function loadThemen() {
    const query = document.getElementById("searchInput").value;

    const res = await fetch(`/api/themen?q=${encodeURIComponent(query)}`);
    const themen = await res.json();

    // Listen leeren
    document.querySelectorAll(".thema-list").forEach(list => {
        list.innerHTML = "";
    });

    // Themen in die passenden Listen einsetzen
    themen.forEach(t => {
        t.jahrgaenge.forEach(jg => {
            const list = document.querySelector(
                `.thema-list[data-jahrgang-id="${jg.id}"]`
            );
            if (!list) return;

            const li = document.createElement("li");
            li.classList.add("list-group-item");
            li.textContent = t.titel;
            li.dataset.themaId = t.id;

            list.appendChild(li);
        });
    });
}


// -------------------------------------------------
// Drag & Drop mit SortableJS
// -------------------------------------------------
function enableDragDrop(listElement) {
    Sortable.create(listElement, {
        group: "themen",
        animation: 150,

        onAdd: evt => {
            const themaId = evt.item.dataset.themaId;
            const jahrgangId = evt.to.dataset.jahrgangId;
            const position = evt.newIndex;

            moveThema(themaId, jahrgangId, position);
        }
    });
}


// -------------------------------------------------
// API-Aufruf: Thema verschieben
// -------------------------------------------------
async function moveThema(themaId, jahrgangId, position) {
    await fetch("/api/move_thema", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            thema_id: Number(themaId),
            target_jahrgang_id: Number(jahrgangId),
            position: Number(position)
        })
    });
}
