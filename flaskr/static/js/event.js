document.addEventListener('DOMContentLoaded', () => {
  const likeBtn = document.getElementById('likeBtn');
  if (!likeBtn) return;

  likeBtn.addEventListener('click', async () => {
    const eventId = likeBtn.dataset.eventId;
    if (!eventId) return;

    const data = await apiToggleLike(eventId);
    if (!data) return;

    if (data.liked) {
      likeBtn.classList.remove('bg-violet-600/20', 'text-violet-400', 'border-violet-500/30');
      likeBtn.classList.add('bg-rose-600/20', 'text-rose-400', 'border-rose-500/30');
      likeBtn.textContent = '❤ В коллекции';
    } else {
      likeBtn.classList.remove('bg-rose-600/20', 'text-rose-400', 'border-rose-500/30');
      likeBtn.classList.add('bg-violet-600/20', 'text-violet-400', 'border-violet-500/30');
      likeBtn.textContent = '🤍 Сохранить';
    }
  });
});
