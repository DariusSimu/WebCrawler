let currentListings = [];

async function loadAccount() {
    const res  = await fetch('/me');
    const data = await res.json();
    if (!data.logged_in) {
        window.location.href = '/login';
        return;
    }
    document.getElementById('account-email').textContent = data.email;
    loadFavorites();
}

async function loadFavorites() {
    const res  = await fetch('/favorites/get');
    const favs = await res.json();
    const list        = document.getElementById('results-list');
    const meta        = document.getElementById('results-meta');
    const countEl     = document.getElementById('results-count');
    const placeholder = document.getElementById('results-placeholder');

    currentListings = favs;
    placeholder.style.display = 'none';
    meta.style.display        = 'flex';
    countEl.textContent       = `${favs.length} favorite${favs.length !== 1 ? 's' : ''}`;

    if (favs.length === 0) {
        list.innerHTML = '<p class="results-placeholder">No saved favorites yet.</p>';
        return;
    }

    buildPlatformCheckboxes(favs);
    document.getElementById('filter-sidebar').style.display = 'block';
    renderListings(applyFilters(favs));
}

function renderListings(listings) {
    const list = document.getElementById('results-list');
    list.innerHTML = '';

    if (listings.length === 0) {
        list.innerHTML = '<p class="results-placeholder">No results match the current filters.</p>';
        return;
    }

    listings.forEach((r, i) => {
        const card = document.createElement('div');
        card.className = 'result-card';
        card.style.animationDelay = `${i * 80}ms`;
        card.innerHTML = `
            <div class="card-info">
                ${r.image ? `<img src="${r.image}" class="card-image" alt="${r.title}"/>` : ''}
                <div class="card-details">
                    <a href="${r.url}" class="card-title" target="_blank">${r.title}</a>
                    <div class="card-meta">
                        <span class="card-platform">${r.platform}</span>
                    </div>
                </div>
            </div>
            <div class="card-price-col">
                <p class="card-price">${getDisplayPrice(r.price)}</p>
                <a href="${r.url}" class="card-btn" target="_blank">View</a>
                <button class="card-btn remove-btn" onclick="removeFavorite(this, '${r.listing_id}')">
                    Remove
                </button>
            </div>
        `;
        list.appendChild(card);
    });
}

async function removeFavorite(btn, listing_id) {
    const res  = await fetch('/favorites/remove', {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify({ listing_id })
    });
    const data = await res.json();
    if (data.success) {
        currentListings = currentListings.filter(l => l.listing_id !== listing_id);
        btn.closest('.result-card').remove();
        const countEl  = document.getElementById('results-count');
        const current  = parseInt(countEl.textContent);
        countEl.textContent = `${current - 1} favorite${current - 1 !== 1 ? 's' : ''}`;
        if (currentListings.length === 0) {
            document.getElementById('filter-sidebar').style.display = 'none';
            document.getElementById('results-list').innerHTML = '<p class="results-placeholder">No saved favorites yet.</p>';
        }
    } else {
        alert(data.error);
    }
}

async function handleLogout() {
    await fetch('/logout', { method: 'POST' });
    window.location.href = '/';
}

fetchExchangeRates();
loadAccount();