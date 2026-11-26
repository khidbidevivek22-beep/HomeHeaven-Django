(function () {
  'use strict';

  document.addEventListener('click', async function (event) {
    const saveButton = event.target.closest('.save-btn');
    if (saveButton) {
      event.preventDefault();
      if (saveButton.dataset.loading === '1') return;
      saveButton.dataset.loading = '1';
      try {
        const response = await fetch(saveButton.dataset.url, {
          method: 'POST',
          headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCookie('csrftoken')
          }
        });
        const data = await response.json();
        const icon = saveButton.querySelector('i');
        if (data.saved) {
          saveButton.classList.add('is-saved');
          icon.className = 'fa-solid fa-heart';
        } else {
          saveButton.classList.remove('is-saved');
          icon.className = 'fa-regular fa-heart';
        }
        showToast(data.message);
      } catch (error) {
        showToast('Please log in to save homes.');
      } finally {
        delete saveButton.dataset.loading;
      }
      return;
    }

    const viewButton = event.target.closest('.view-toggle button');
    if (viewButton) {
      const wrapper = document.getElementById('results-wrapper');
      if (!wrapper) return;
      document.querySelectorAll('.view-toggle button').forEach(function (button) {
        button.classList.toggle('active', button === viewButton);
      });
      wrapper.classList.toggle('list-view', viewButton.dataset.view === 'list');
      return;
    }

    const chip = event.target.closest('.chip[data-filter]');
    if (chip) {
      const input = document.getElementById(chip.dataset.filter);
      if (input) {
        input.checked = !input.checked;
        chip.classList.toggle('active', input.checked);
      }
    }
  });

  document.querySelectorAll('.chip[data-filter]').forEach(function (chip) {
    const input = document.getElementById(chip.dataset.filter);
    if (input) chip.classList.toggle('active', input.checked);
  });

  function getCookie(name) {
    const parts = document.cookie.split(';');
    for (const part of parts) {
      const item = part.trim();
      if (item.startsWith(name + '=')) return decodeURIComponent(item.slice(name.length + 1));
    }
    return '';
  }

  function showToast(message) {
    let toast = document.getElementById('hh-toast');
    if (!toast) {
      toast = document.createElement('div');
      toast.id = 'hh-toast';
      toast.style.cssText = 'position:fixed;right:22px;bottom:22px;z-index:9999;background:#17202a;color:#fff;padding:12px 18px;border-radius:10px;font-size:14px;box-shadow:0 10px 30px rgba(0,0,0,.2);opacity:0;transition:opacity .2s;';
      document.body.appendChild(toast);
    }
    toast.textContent = message;
    toast.style.opacity = '1';
    clearTimeout(window.__hhToastTimer);
    window.__hhToastTimer = setTimeout(function () { toast.style.opacity = '0'; }, 2600);
  }
})();
