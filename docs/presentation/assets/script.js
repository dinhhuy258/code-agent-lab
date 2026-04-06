// Slide registration — each slide .js file calls registerSlide()
const slideHtmls = [];
function registerSlide(html) {
  slideHtmls.push(html);
}

// Labels map (data-title → display name)
const labelMap = {
  'hero': 'Introduction',
  'what-is-agent': 'What is an Agent?',
  'motivation': 'Why Build One?',
  'react-pattern': 'The ReAct Loop',
  'loop-code': 'AgentClient.send()',
  'four-layers': 'Four-Layer Stack',
  'tool-mental-model': 'The Fundamental Primitive',
  'tool-abstraction': 'Tool Abstraction',
  'built-in-tools': 'Built-in Tool Set',
  'tool-call-approaches': 'Declaring Tools',
  'streaming-problem': 'Streaming Architecture',
  'event-dispatch': 'Event Dispatch',
  'token-snowball': 'Token Snowball',
  'request-assembly': 'Request Assembly',
  'history-growth': 'History Growth',
  'prompt-structure': 'Prompt Architecture',
  'five-components': '5 Agent Components',
  'skills-problem': 'Load on Demand',
  'skill-format': 'SKILL.md Format',
  'skill-activation-flow': 'Activation Flow',
  'subagent-problem': 'Context Isolation',
  'subagent-architecture': 'Isolated Sessions',
  'subagent-history': 'History Flow',
  'subagent-implementation': 'Implementation',
  'subagent-tradeoffs': 'Trade-offs',
  'lessons': 'What We Learned',
  'whats-missing': 'What\'s Missing'
};

// Called after all slide scripts have loaded
function renderSlides() {
  const container = document.getElementById('slideContainer');
  container.innerHTML = slideHtmls.join('\n');

  // Hide loading screen
  const loading = document.getElementById('loadingScreen');
  if (loading) loading.classList.add('hidden');

  initPresentation();
}

function initPresentation() {
  // Gather elements
  const slides = document.querySelectorAll('.slide-inner');
  const sections = document.querySelectorAll('.slide');
  const tocItems = document.querySelectorAll('.toc-item');
  const progressBar = document.getElementById('progress');
  const navLabel = document.getElementById('navLabel');
  const navCounter = document.getElementById('navCounter');
  const slideCount = document.getElementById('slideCount');

  const totalSlides = sections.length;

  // Update footer count
  if (slideCount) slideCount.textContent = '1 / ' + totalSlides;
  if (navCounter) navCounter.textContent = '1 / ' + totalSlides;

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

        // Update TOC — clear all active
        tocItems.forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.toc-branch').forEach(b => b.classList.remove('has-active'));

        // Set active item
        const match = document.querySelector('.toc-item[data-target="' + title + '"]');
        if (match) {
          match.classList.add('active');
          match.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

          // Highlight parent branch
          const parentBranch = match.closest('.toc-branch');
          if (parentBranch) {
            parentBranch.classList.add('has-active');
            parentBranch.classList.remove('collapsed');
          }
        }

        // Update nav bar
        if (navLabel) navLabel.textContent = labelMap[title] || title;
        if (navCounter) navCounter.textContent = (idx + 1) + ' / ' + totalSlides;
        if (slideCount) slideCount.textContent = (idx + 1) + ' / ' + totalSlides;
      }
    });
  }, { threshold: 0.35 });
  sections.forEach(s => secObs.observe(s));

  // Progress bar
  window.addEventListener('scroll', () => {
    const p = window.scrollY / (document.body.scrollHeight - window.innerHeight);
    if (progressBar) progressBar.style.width = (p * 100) + '%';
  });

  // Step-slide helpers
  function getStepItems(slideEl) {
    return slideEl ? Array.from(slideEl.querySelectorAll('.step-item')) : [];
  }
  function revealNextStep(slideEl) {
    const hidden = getStepItems(slideEl).filter(el => !el.classList.contains('step-visible'));
    if (hidden.length > 0) { hidden[0].classList.add('step-visible'); return true; }
    return false;
  }
  function hideLastStep(slideEl) {
    const visible = getStepItems(slideEl).filter(el => el.classList.contains('step-visible'));
    if (visible.length > 0) { visible[visible.length - 1].classList.remove('step-visible'); return true; }
    return false;
  }
  function showAllSteps(slideEl) {
    getStepItems(slideEl).forEach(el => el.classList.add('step-visible'));
  }
  function resetSteps(slideEl) {
    getStepItems(slideEl).forEach(el => el.classList.remove('step-visible'));
  }

  // Keyboard nav
  document.addEventListener('keydown', e => {
    if (e.key === 'ArrowDown' || e.key === 'PageDown') {
      e.preventDefault();
      if (revealNextStep(sections[currentIdx])) return;
      currentIdx = Math.min(currentIdx + 1, sections.length - 1);
      sections[currentIdx].scrollIntoView({ behavior: 'smooth' });
      resetSteps(sections[currentIdx]);
    }
    if (e.key === 'ArrowUp' || e.key === 'PageUp') {
      e.preventDefault();
      if (hideLastStep(sections[currentIdx])) return;
      currentIdx = Math.max(currentIdx - 1, 0);
      sections[currentIdx].scrollIntoView({ behavior: 'smooth' });
      showAllSteps(sections[currentIdx]);
    }
  });

  // Sync keyboard index on scroll
  const syncObs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) currentIdx = Array.from(sections).indexOf(e.target);
    });
  }, { threshold: 0.45 });
  sections.forEach(s => syncObs.observe(s));

  // Staggered card reveal on scroll
  const cardObs = new IntersectionObserver(entries => {
    entries.forEach(en => {
      if (en.isIntersecting) en.target.classList.add('cards-visible');
    });
  }, { threshold: 0.15 });
  document.querySelectorAll('.card-grid').forEach(el => cardObs.observe(el));

  // Tabs
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', function(e) { switchTab(e, this.dataset.tab); });
  });

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

  // Fade-up animation on scroll
  const fadeObs = new IntersectionObserver(entries => {
    entries.forEach(en => {
      if (en.isIntersecting) {
        en.target.querySelectorAll('.anim-fade').forEach(el => {
          el.style.opacity = '1';
          el.style.transform = 'translateY(0)';
        });
      }
    });
  }, { threshold: 0.15 });
  document.querySelectorAll('.slide').forEach(el => {
    if (el.querySelector('.anim-fade')) fadeObs.observe(el);
  });

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
  kbdOverlay.innerHTML = '<div class="kbd-modal">' +
    '<h3>Keyboard Shortcuts</h3>' +
    '<div class="kbd-row"><div class="key-combo"><span class="key">&darr;</span></div><div class="key-desc">Next step or next slide</div></div>' +
    '<div class="kbd-row"><div class="key-combo"><span class="key">&uarr;</span></div><div class="key-desc">Prev step or prev slide</div></div>' +
    '<div class="kbd-row"><div class="key-combo"><span class="key">t</span></div><div class="key-desc">Toggle sidebar</div></div>' +
    '<div class="kbd-row"><div class="key-combo"><span class="key">?</span></div><div class="key-desc">Toggle this help</div></div>' +
    '<div class="kbd-row"><div class="key-combo"><span class="key">Esc</span></div><div class="key-desc">Close overlay</div></div>' +
    '</div>';
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
}

// TOC click handler (global — used by inline onclick)
function jumpTo(e, targetTitle) {
  e.preventDefault();
  const target = document.querySelector('.slide[data-title="' + targetTitle + '"]');
  if (target) target.scrollIntoView({ behavior: 'smooth' });
  closeSidebar();
}

// Tree branch collapse/expand
function toggleBranch(labelEl) {
  const branch = labelEl.closest('.toc-branch');
  if (branch) branch.classList.toggle('collapsed');
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

// Mobile sidebar
function toggleSidebar() {
  document.getElementById('sidebar').classList.toggle('open');
}
function closeSidebar() {
  document.getElementById('sidebar').classList.remove('open');
}
