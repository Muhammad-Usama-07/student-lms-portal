// EduNest — Main JS

// Auto-dismiss alerts after 4 seconds
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.alert').forEach(alert => {
    setTimeout(() => {
      alert.style.transition = 'opacity .5s';
      alert.style.opacity = '0';
      setTimeout(() => alert.remove(), 500);
    }, 4000);
  });

  // Active nav highlight
  const currentPath = window.location.pathname;
  document.querySelectorAll('.nav-item').forEach(item => {
    if (item.getAttribute('href') === currentPath) {
      item.classList.add('active');
    }
  });

  // Quiz timer (if on quiz take page)
  const quizForm = document.getElementById('quizForm');
  if (quizForm) {
    const timeLimitEl = document.querySelector('[data-time-limit]');
    if (timeLimitEl) {
      let seconds = parseInt(timeLimitEl.dataset.timeLimit) * 60;
      const timerEl = document.getElementById('quiz-timer');
      const interval = setInterval(() => {
        seconds--;
        if (timerEl) {
          const m = Math.floor(seconds / 60);
          const s = seconds % 60;
          timerEl.textContent = `${m}:${s.toString().padStart(2, '0')}`;
          if (seconds <= 60) timerEl.style.color = '#e53935';
        }
        if (seconds <= 0) {
          clearInterval(interval);
          quizForm.submit();
        }
      }, 1000);
    }
  }
});