(() => {
	const navToggle = document.querySelector('[data-nav-toggle]');
	const navMenu = document.querySelector('[data-nav-menu]');

	if (!navToggle || !navMenu) {
		return;
	}

	navToggle.addEventListener('click', () => {
		const isOpen = navMenu.classList.toggle('is-open');
		navToggle.setAttribute('aria-expanded', String(isOpen));
	});
})();
