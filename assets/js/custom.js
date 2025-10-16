// Custom JavaScript pour les composants interactifs

document.addEventListener('DOMContentLoaded', function() {

  // ========================================
  // TABS
  // ========================================
  initializeTabs();

  // ========================================
  // COPY CODE BUTTONS
  // ========================================
  addCopyButtons();

  // ========================================
  // SMOOTH SCROLL
  // ========================================
  initializeSmoothScroll();

});

// Initialiser les tabs
function initializeTabs() {
  const tabContainers = document.querySelectorAll('.tabs-container');

  tabContainers.forEach(container => {
    const tabs = container.querySelectorAll('.tab-content');
    const buttons = container.querySelector('.tab-buttons');

    if (!buttons || tabs.length === 0) return;

    // Créer les boutons si nécessaire
    if (buttons.children.length === 0) {
      tabs.forEach((tab, index) => {
        const button = document.createElement('button');
        button.className = 'tab-button';
        button.textContent = tab.id || `Tab ${index + 1}`;
        button.dataset.tab = tab.id;

        button.addEventListener('click', () => {
          activateTab(container, tab.id);
        });

        buttons.appendChild(button);
      });
    }

    // Activer le premier onglet
    if (tabs.length > 0) {
      activateTab(container, tabs[0].id);
    }
  });
}

function activateTab(container, tabId) {
  // Désactiver tous les onglets et boutons
  const tabs = container.querySelectorAll('.tab-content');
  const buttons = container.querySelectorAll('.tab-button');

  tabs.forEach(tab => tab.classList.remove('active'));
  buttons.forEach(btn => btn.classList.remove('active'));

  // Activer l'onglet et le bouton sélectionnés
  const activeTab = container.querySelector(`#${tabId}`);
  const activeButton = container.querySelector(`[data-tab="${tabId}"]`);

  if (activeTab) activeTab.classList.add('active');
  if (activeButton) activeButton.classList.add('active');
}

// Ajouter des boutons de copie aux blocs de code
function addCopyButtons() {
  const codeBlocks = document.querySelectorAll('pre code');

  codeBlocks.forEach(codeBlock => {
    const pre = codeBlock.parentElement;
    const wrapper = document.createElement('div');
    wrapper.className = 'code-wrapper';

    const copyButton = document.createElement('button');
    copyButton.className = 'copy-button';
    copyButton.innerHTML = '📋 Copier';
    copyButton.title = 'Copier le code';

    copyButton.addEventListener('click', () => {
      const code = codeBlock.textContent;
      navigator.clipboard.writeText(code).then(() => {
        copyButton.innerHTML = '✅ Copié !';
        copyButton.classList.add('copied');

        setTimeout(() => {
          copyButton.innerHTML = '📋 Copier';
          copyButton.classList.remove('copied');
        }, 2000);
      });
    });

    pre.parentNode.insertBefore(wrapper, pre);
    wrapper.appendChild(copyButton);
    wrapper.appendChild(pre);
  });
}

// Smooth scroll pour les liens d'ancrage
function initializeSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const href = this.getAttribute('href');
      if (href === '#') return;

      const target = document.querySelector(href);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });
}

// Fonction utilitaire pour les accordéons
function initializeAccordions() {
  const accordions = document.querySelectorAll('details');

  accordions.forEach(accordion => {
    const summary = accordion.querySelector('summary');

    summary.addEventListener('click', (e) => {
      // Optionnel : fermer les autres accordéons
      // const parent = accordion.parentElement;
      // parent.querySelectorAll('details[open]').forEach(other => {
      //   if (other !== accordion) other.removeAttribute('open');
      // });
    });
  });
}