// Elements
const slides = document.querySelectorAll('.slide-inner');
const sections = document.querySelectorAll('.slide');
const tocItems = document.querySelectorAll('.toc-item');
const progressBar = document.getElementById('progress');
const navLabel = document.getElementById('navLabel');
const navCounter = document.getElementById('navCounter');
const slideCount = document.getElementById('slideCount');
const sidebar = document.getElementById('sidebar');
const sidebarOverlay = document.getElementById('sidebarOverlay');

// Slide visibility animation
const visObs = new IntersectionObserver(entries => {
  entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
}, { threshold: 0.12 });
slides.forEach(s => visObs.observe(s));

// Active section tracking
let currentIdx = 0;
const secObs = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      const idx = Array.from(sections).indexOf(e.target);
      const title = e.target.dataset.title;
      currentIdx = idx;

      // Update TOC
      tocItems.forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.toc-branch').forEach(b => b.classList.remove('has-active'));

      const match = document.querySelector(`.toc-item[data-target="${title}"]`);
      if (match) {
        match.classList.add('active');
        match.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        const parentBranch = match.closest('.toc-branch');
        if (parentBranch) {
          parentBranch.classList.add('has-active');
          parentBranch.classList.remove('collapsed');
        }
      }

      // Update nav bar
      if (navLabel) navLabel.textContent = title.replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
      if (navCounter) navCounter.textContent = `${idx + 1} / ${sections.length}`;
      if (slideCount) slideCount.textContent = `${idx + 1} / ${sections.length}`;
    }
  });
}, { threshold: 0.35 });
sections.forEach(s => secObs.observe(s));

// Progress bar
window.addEventListener('scroll', () => {
  const p = window.scrollY / (document.body.scrollHeight - window.innerHeight);
  if (progressBar) progressBar.style.width = (p * 100) + '%';
});

// Keyboard nav
document.addEventListener('keydown', e => {
  if (e.key === 'ArrowDown' || e.key === 'PageDown') {
    e.preventDefault();
    currentIdx = Math.min(currentIdx + 1, sections.length - 1);
    sections[currentIdx].scrollIntoView({ behavior: 'smooth' });
  }
  if (e.key === 'ArrowUp' || e.key === 'PageUp') {
    e.preventDefault();
    currentIdx = Math.max(currentIdx - 1, 0);
    sections[currentIdx].scrollIntoView({ behavior: 'smooth' });
  }
});

// Sync keyboard index
const syncObs = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) currentIdx = Array.from(sections).indexOf(e.target);
  });
}, { threshold: 0.45 });
sections.forEach(s => syncObs.observe(s));

// TOC click handler
function jumpTo(e, targetTitle) {
  e.preventDefault();
  const target = document.querySelector(`.slide[data-title="${targetTitle}"]`);
  if (target) target.scrollIntoView({ behavior: 'smooth' });
  closeSidebar();
}

// Tree branch collapse/expand
function toggleBranch(labelEl) {
  const branch = labelEl.closest('.toc-branch');
  if (branch) branch.classList.toggle('collapsed');
}

// Mobile sidebar toggle
function toggleSidebar() {
  sidebar.classList.toggle('open');
}
function closeSidebar() {
  sidebar.classList.remove('open');
}

// Tabs
function switchTab(e, id) {
  const group = e.target.closest('.tab-group') || e.target.parentElement;
  group.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  e.target.classList.add('active');
  const parent = group.parentElement;
  parent.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
  document.getElementById(id).classList.add('active');
}

// Animate token bars on scroll
const barObs = new IntersectionObserver(entries => {
  entries.forEach(en => {
    if (en.isIntersecting) {
      en.target.querySelectorAll('.bar-fill').forEach(b => {
        b.style.width = b.style.width;
        b.classList.add('animate');
      });
    }
  });
}, { threshold: 0.3 });
document.querySelectorAll('.token-calc').forEach(el => barObs.observe(el));

// Context vis animation on scroll
const ctxObs = new IntersectionObserver(entries => {
  entries.forEach(en => {
    if (en.isIntersecting) en.target.classList.add('animate');
  });
}, { threshold: 0.3 });
document.querySelectorAll('.ctx-vis').forEach(el => ctxObs.observe(el));

// Staggered card reveal on scroll
const cardObs = new IntersectionObserver(entries => {
  entries.forEach(en => {
    if (en.isIntersecting) en.target.classList.add('cards-visible');
  });
}, { threshold: 0.15 });
document.querySelectorAll('.card-grid').forEach(el => cardObs.observe(el));

// Stat counter animation
const statObs = new IntersectionObserver(entries => {
  entries.forEach(en => {
    if (en.isIntersecting) {
      en.target.querySelectorAll('.stat').forEach((s, i) => {
        s.classList.add('animate-in');
        s.style.animationDelay = (i * 0.1) + 's';
      });
    }
  });
}, { threshold: 0.3 });
document.querySelectorAll('.stat-row').forEach(el => statObs.observe(el));

// Copy buttons on code blocks
document.querySelectorAll('.code-block').forEach(block => {
  const btn = document.createElement('button');
  btn.className = 'code-copy-btn';
  btn.textContent = 'Copy';
  btn.onclick = function(e) {
    e.stopPropagation();
    const codeBody = block.querySelector('.code-body') || block;
    const text = codeBody.textContent.trim();
    navigator.clipboard.writeText(text).then(() => {
      btn.textContent = 'Copied!';
      btn.classList.add('copied');
      setTimeout(() => { btn.textContent = 'Copy'; btn.classList.remove('copied'); }, 1500);
    });
  };
  block.appendChild(btn);
});

// Keyboard overlay
const kbdOverlay = document.createElement('div');
kbdOverlay.className = 'kbd-overlay';
kbdOverlay.innerHTML = `<div class="kbd-modal">
  <h3>Keyboard Shortcuts</h3>
  <div class="kbd-row"><div class="key-combo"><span class="key">&uarr;</span><span class="key">&darr;</span></div><div class="key-desc">Navigate slides</div></div>
  <div class="kbd-row"><div class="key-combo"><span class="key">t</span></div><div class="key-desc">Toggle sidebar</div></div>
  <div class="kbd-row"><div class="key-combo"><span class="key">?</span></div><div class="key-desc">Toggle this help</div></div>
  <div class="kbd-row"><div class="key-combo"><span class="key">Esc</span></div><div class="key-desc">Close overlay</div></div>
</div>`;
document.body.appendChild(kbdOverlay);
kbdOverlay.addEventListener('click', (e) => {
  if (e.target === kbdOverlay) kbdOverlay.classList.remove('visible');
});

document.addEventListener('keydown', (e) => {
  if (e.key === '?' && !e.ctrlKey && !e.metaKey) {
    e.preventDefault();
    kbdOverlay.classList.toggle('visible');
  }
  if (e.key === 'Escape') kbdOverlay.classList.remove('visible');
  if (e.key === 't' && !e.ctrlKey && !e.metaKey && !kbdOverlay.classList.contains('visible')) {
    toggleSidebar();
  }
});

// Lightbox
(function(){
  var overlay = document.createElement('div');
  overlay.className = 'lightbox-overlay';
  overlay.innerHTML = '<button class="lightbox-close" aria-label="Close preview">&times;</button><img alt="">';
  document.body.appendChild(overlay);
  var lbImg = overlay.querySelector('img');
  var closeBtn = overlay.querySelector('.lightbox-close');

  function openLightbox(src, alt){
    lbImg.src = src; lbImg.alt = alt || '';
    overlay.classList.add('open');
    document.body.style.overflow = 'hidden';
  }
  function closeLightbox(){
    overlay.classList.remove('open');
    document.body.style.overflow = '';
  }

  document.querySelectorAll('.slide-inner img').forEach(function(img){
    img.addEventListener('click', function(){ openLightbox(this.src, this.alt); });
  });
  overlay.addEventListener('click', function(e){ if(e.target===overlay) closeLightbox(); });
  closeBtn.addEventListener('click', closeLightbox);
  document.addEventListener('keydown', function(e){ if(e.key==='Escape' && overlay.classList.contains('open')) closeLightbox(); });
})();
