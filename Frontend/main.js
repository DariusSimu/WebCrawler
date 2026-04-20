let currentUser     = null;
let currentListings = [];

async function checkAuth() {
    const res  = await fetch('/me');
    const data = await res.json();
    currentUser = data.logged_in ? data : null;
    updateAuthButton();
}

function updateAuthButton() {
    const btn = document.getElementById('auth-btn');
    if (currentUser) {
        btn.textContent = 'Account';
        btn.onclick = () => window.location.href = '/favorites';
    } else {
        btn.textContent = 'Sign In';
        btn.onclick = () => window.location.href = '/login';
    }
}

document.getElementById('search-form').addEventListener('submit', async e => {
    e.preventDefault();
    const query     = document.getElementById('search-input').value.trim();
    const list      = document.getElementById('results-list');
    const meta      = document.getElementById('results-meta');
    const countEl   = document.getElementById('results-count');
    const placeholder = document.getElementById('results-placeholder');

    if (!query) return;

    countEl.textContent = 'Searching...';
    meta.style.display  = 'flex';
    list.innerHTML      = '';
    placeholder.style.display = 'none';

    const response = await fetch(`/search?q=${encodeURIComponent(query)}`);
    const results  = await response.json();
    renderResults(query, results);
});

function renderResults(query, results) {
    const list      = document.getElementById('results-list');
    const meta      = document.getElementById('results-meta');
    const countEl   = document.getElementById('results-count');
    const queryEl   = document.getElementById('results-query');

    currentListings = results;
    buildPlatformCheckboxes(results);
    document.getElementById('filter-sidebar').style.display = results.length > 0 ? 'block' : 'none';

    list.innerHTML      = '';
    meta.style.display  = 'flex';
    countEl.textContent = `${results.length} result${results.length !== 1 ? 's' : ''}`;

    if (results.length === 0) {
        list.innerHTML = '<p class="results-placeholder">No results found.</p>';
        return;
    }

    renderListings(applyFilters(results));
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
                <button class="card-btn" data-saved="false" onclick="addToFavorites(this, ${JSON.stringify(r).replace(/"/g, '&quot;')})">
                    Add to Favorites
                </button>
            </div>
        `;
        list.appendChild(card);
    });
}

async function addToFavorites(btn, listing) {
    if (!currentUser) {
        alert('Please sign in to save favorites.');
        return;
    }

    const isSaved = btn.dataset.saved === 'true';

    if (isSaved) {
        const res  = await fetch('/favorites/remove', {
            method:  'POST',
            headers: { 'Content-Type': 'application/json' },
            body:    JSON.stringify({ listing_id: listing.listing_id })
        });
        const data = await res.json();
        if (data.success) {
            btn.textContent   = 'Add to Favorites';
            btn.dataset.saved = 'false';
            btn.classList.remove('saved');
        } else {
            alert(data.error);
        }
    } else {
        const res  = await fetch('/favorites/add', {
            method:  'POST',
            headers: { 'Content-Type': 'application/json' },
            body:    JSON.stringify(listing)
        });
        const data = await res.json();
        if (data.success) {
            btn.textContent   = '✓ Saved';
            btn.dataset.saved = 'true';
            btn.classList.add('saved');
        } else {
            alert(data.error);
        }
    }
}

fetchExchangeRates();
checkAuth();