document.getElementById('fetchBtn').addEventListener('click', pobierzDane);

async function pobierzDane() {
    const payload = {
        variationsNumber: 2,
        locations: ["Moria", "Głębie", "Pieczary Thryma Ostrobrodego"],
        circumstances: [],
        characters: ["Veig - dowódca krasnoludzkiej kompanii"]
    };

    const wynikDiv = document.getElementById('wynik');
    wynikDiv.innerHTML = `<div class="loader"></div>`; // pokazujemy pierścień

    try {
        const response = await fetch('http://127.0.0.1:8000/api/table/enhanced/tor_event', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error('Błąd połączenia: ' + response.status);
        }

        const data = await response.json();

        wynikDiv.innerHTML = `
        <div class="section">
            <div class="title">Wydarzenie:</div>
            <div class="text">${data.event.event}</div>
        </div>
        <div class="section">
            <div class="title">Konsekwencje testu:</div>
            <div class="text">${data.event.testConsequences}</div>
        </div>
        <div class="section">
            <div class="title">Szczegóły wydarzenia:</div>
            <div class="text">${data.event.detailedEvent}</div>
        </div>
        <div class="section">
            <div class="title">Wymagane działanie:</div>
            <div class="text">${data.event.outcome}</div>
        </div>
        <div class="section">
            <div class="title">Rozwinięcia fabularne:</div>
            <div class="text">
            ${data.enhances.map(item => `
                <div style="margin-bottom: 15px;">
                <strong>${item.event_name}</strong><br/>
                ${item.creative_extension}
                </div>
            `).join('')}
            </div>
        </div>
        `;
    } catch (error) {
        wynikDiv.innerHTML = `<p style="color:red;">${error.message}</p>`;
    }
}
