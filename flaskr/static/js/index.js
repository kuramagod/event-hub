document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.getElementById('searchInput');
  const searchButton = document.getElementById('searchButton');
  const citySelect = document.getElementById('citySelect');
  const priceSelect = document.getElementById('priceSelect');
  const categoryFilters = document.getElementById('categoryFilters');
  const eventCards = Array.from(document.querySelectorAll('.event-card'));
  const emptyState = document.getElementById('emptyState');
  let currentCategory = 'Все';

  function updateCategoryButtons(category) {
    currentCategory = category;
    document.querySelectorAll('.filter-cat').forEach(btn => {
      if (btn.dataset.cat === category) {
        btn.classList.remove('bg-gray-900', 'text-gray-400', 'hover:bg-gray-800');
        btn.classList.add('bg-violet-600', 'text-white', 'ring-2', 'ring-violet-600', 'ring-offset-2', 'ring-offset-slate-950');
      } else {
        btn.classList.remove('bg-violet-600', 'text-white', 'ring-2', 'ring-violet-600', 'ring-offset-2', 'ring-offset-slate-950');
        btn.classList.add('bg-gray-900', 'text-gray-400', 'hover:bg-gray-800');
      }
    });
  }

  function applyFilters() {
    const query = searchInput.value.trim().toLowerCase();
    const selectedCity = citySelect.value;
    const selectedPrice = priceSelect.value;
    let visibleCount = 0;

    eventCards.forEach(card => {
      const title = (card.dataset.title || '').toLowerCase();
      const category = card.dataset.category || '';
      const cityName = card.dataset.city || '';
      const priceValue = Number(card.dataset.price || 0);

      const matchTitle = query === '' || title.includes(query);
      const matchCategory = currentCategory === 'Все' || category === currentCategory;

      const matchCity = selectedCity === '' || cityName === selectedCity;
      const matchPrice = selectedPrice === '' || (selectedPrice === 'free' && priceValue === 0) || (selectedPrice === 'paid' && priceValue > 0);

      const visible = matchTitle && matchCategory && matchCity && matchPrice;
      if (!visible) {
        card.classList.add('hidden');
      } else {
        card.classList.remove('hidden');
      }
      if (visible) visibleCount += 1;
    });

    emptyState.classList.toggle('hidden', visibleCount > 0);
  }

  function attachCardNavigation() {
    eventCards.forEach(card => {
      const eventId = card.dataset.id;
      if (!eventId) return;

      const likeButton = card.querySelector('.like-btn');
      if (likeButton) {
        likeButton.addEventListener('click', (event) => {
          event.stopPropagation();
          toggleLike(eventId, likeButton);
        });
      }
    });
  }

  categoryFilters.addEventListener('click', (event) => {
    const button = event.target.closest('.filter-cat');
    if (!button) return;
    const category = button.dataset.cat;
    updateCategoryButtons(category);
    applyFilters();
  });

  searchButton.addEventListener('click', applyFilters);
  searchInput.addEventListener('keyup', (event) => {
    if (event.key === 'Enter') applyFilters();
  });
  searchInput.addEventListener('input', applyFilters);
  citySelect.addEventListener('change', applyFilters);
  priceSelect.addEventListener('change', applyFilters);

  attachCardNavigation();
});

const heartFilledSvg = `<svg class="w-5 h-5 text-rose-500" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd"></path></svg>`;
const heartOutlineSvg = `<svg class="w-5 h-5 text-white/70" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path></svg>`;

async function toggleLike(eventId, button) {
  const data = await apiToggleLike(eventId);
  if (!data) return;

  const isLiked = data.liked;
  button.dataset.liked = isLiked;
  button.innerHTML = isLiked ? heartFilledSvg : heartOutlineSvg;
  button.classList.toggle('text-rose-500', isLiked);
  button.classList.toggle('text-white/70', !isLiked);
}
