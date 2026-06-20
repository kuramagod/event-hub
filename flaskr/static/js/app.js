function showToast(message, type = 'success') {
  const toast = document.createElement('div');
  const bg = type === 'success' ? 'bg-violet-600' : 'bg-rose-600';
  toast.className = `fixed bottom-6 right-6 ${bg} text-white px-6 py-3 rounded-xl shadow-2xl z-50 transition-all duration-300 transform translate-y-8 opacity-0 font-medium border border-white/10`;
  toast.textContent = message;
  document.body.appendChild(toast);

  setTimeout(() => {
    toast.classList.remove('translate-y-8', 'opacity-0');
    toast.classList.add('translate-y-0', 'opacity-100');
  }, 10);

  setTimeout(() => {
    toast.classList.replace('translate-y-0', 'translate-y-8');
    toast.classList.replace('opacity-100', 'opacity-0');
    setTimeout(() => toast.remove(), 300);
  }, 2500);
}

async function apiToggleLike(eventId) {
  const response = await fetch(`event/api/toggle-like/${eventId}`, {
    method: 'POST',
    headers: {
      'X-Requested-With': 'XMLHttpRequest'
    },
    credentials: 'same-origin'
  });

  if (response.redirected) {
    window.location.href = response.url;
    return null;
  }

  const data = await response.json();
  if (!response.ok) {
    showToast(data.error || 'Ошибка запроса', 'error');
    return null;
  }

  return data;
}
