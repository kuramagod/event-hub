document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.event-card').forEach(card => {
    const eventId = card.dataset.id;
    if (!eventId) return;

    card.addEventListener('click', (e) => {
      if (e.target.closest('.delete-btn')) return;
      window.location.href = `/event?id=${eventId}`;
    });
  });

  document.querySelectorAll('.delete-btn').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      e.stopPropagation();

      const eventId = btn.dataset.eventId;
      const card = btn.closest('.event-card');

      try {
        const response = await fetch(`/api/toggle-like/${eventId}`, {
          method: 'POST',
          headers: {
            'X-Requested-With': 'XMLHttpRequest'
          },
          credentials: 'same-origin'
        });

        if (response.ok) {
          card.remove();

          showToast('Мероприятие удалено из коллекции', 'success');

          const remainingCards = document.querySelectorAll('.event-card');
          const emptyState = document.getElementById('emptyState');

          if (remainingCards.length === 0) {
            emptyState.classList.remove('hidden');
          }
        } else {
          const data = await response.json();
          showToast(data.error || 'Ошибка при удалении мероприятия', 'error');
        }
      } catch (error) {
        console.error('Ошибка:', error);
        showToast('Произошла ошибка при удалении мероприятия', 'error');
      }
    });
  });
});
