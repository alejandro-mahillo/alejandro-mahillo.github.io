(() => {
  const root = document.documentElement;
  const preference = window.matchMedia('(prefers-color-scheme: dark)');
  const scheme = document.querySelector('meta[name="color-scheme"]');
  const theme = document.getElementById('theme-toggle');
  const icon = theme.querySelector('i');
  const systemTheme = () => preference.matches ? 'dark' : 'light';

  function applyTheme(override) {
    if (override === 'dark' || override === 'light') {
      root.dataset.theme = override;
      scheme.content = override;
    } else {
      delete root.dataset.theme;
      scheme.content = 'light dark';
    }

    const dark = (root.dataset.theme || systemTheme()) === 'dark';
    theme.setAttribute('aria-pressed', String(dark));
    icon.classList.toggle('fa-moon', dark);
    icon.classList.toggle('fa-sun', !dark);
  }

  applyTheme(root.dataset.theme);
  theme.hidden = false;
  theme.addEventListener('click', () => {
    const next = theme.getAttribute('aria-pressed') === 'true' ? 'light' : 'dark';
    const override = next === systemTheme() ? null : next;
    applyTheme(override);
    try {
      if (override) localStorage.setItem('theme', override);
      else localStorage.removeItem('theme');
    } catch {
      // The toggle still works for the current page when storage is blocked.
    }
  });
  preference.addEventListener('change', () => applyTheme(root.dataset.theme));
  window.addEventListener('storage', (event) => {
    if (event.key === 'theme' || event.key === null) applyTheme(event.newValue);
  });

  const nav = document.getElementById('site-nav');
  const visible = nav.querySelector('.visible-links');
  const overflow = nav.querySelector('.hidden-links');
  const more = nav.querySelector('.nav-toggle');
  const themeItem = theme.closest('li');
  const links = [...visible.querySelectorAll('[data-nav-link]')];

  function setMenuOpen(open) {
    overflow.hidden = !open;
    more.setAttribute('aria-expanded', String(open));
    more.classList.toggle('close', open);
  }

  function fitLinks() {
    const focused = document.activeElement;
    const linkHadFocus = overflow.contains(focused) || visible.contains(focused);
    for (const item of [...overflow.children]) visible.insertBefore(item, themeItem);
    more.hidden = false;

    const width = nav.clientWidth;
    let used = visible.getBoundingClientRect().width;
    if (used > width) {
      // Read all widths together before moving links into the overflow menu.
      const reserve = more.getBoundingClientRect().width + 14;
      const widths = links.map((item) => item.getBoundingClientRect().width);
      let keep = links.length;
      while (keep > 0 && used > width - reserve) used -= widths[--keep];
      overflow.append(...links.slice(keep));
    }

    more.hidden = !overflow.children.length;
    if (more.hidden) setMenuOpen(false);

    if (linkHadFocus) {
      const target = overflow.hidden && overflow.contains(focused) ? more : focused;
      if (target !== document.activeElement) target.focus({ preventScroll: true });
    } else if (focused === more && more.hidden) {
      theme.focus({ preventScroll: true });
    }
  }

  nav.classList.add('is-ready');
  fitLinks();
  if ('ResizeObserver' in window) {
    new ResizeObserver(fitLinks).observe(nav);
  } else {
    window.addEventListener('resize', fitLinks);
  }

  more.addEventListener('click', () => setMenuOpen(overflow.hidden));
  nav.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && !overflow.hidden) {
      setMenuOpen(false);
      more.focus();
    }
  });
  document.addEventListener('click', (event) => {
    if (!nav.contains(event.target) && !overflow.hidden) setMenuOpen(false);
  });
})();
