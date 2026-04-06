registerSlide(`
<section class="slide" data-title="what-is-agent">
  <div class="slide-inner">
    <div class="section-label">Foundation</div>
    <h2 class="section-title">What is a Coding Agent?</h2>
    <p class="section-desc">A coding agent wraps an LLM in a control system that can observe, reason, act, and iterate autonomously.</p>

    <div class="card-grid mt-24">
      <div class="card">
        <h3>&#x1F4AC; Chatbot</h3>
        <p>Single turn. You ask, it answers. No memory, no tools, no persistence. Just raw text completion.</p>
        <span class="tag" style="background:var(--surface2);color:var(--text3)">Stateless</span>
      </div>
      <div class="card">
        <h3>&#x2728; Copilot</h3>
        <p>Suggests code inline as you type. Context-aware within the current file, but no autonomy or tool use.</p>
        <span class="tag" style="background:rgba(14,165,233,.06);color:var(--accent3)">Reactive</span>
      </div>
      <div class="card">
        <h3>&#x1F916; Coding Agent</h3>
        <p>Autonomous loop: reads files, executes commands, writes code, validates results. Multi-step reasoning with tool access.</p>
        <span class="tag" style="background:rgba(124,58,237,.06);color:var(--accent)">Autonomous</span>
      </div>
    </div>

    <div class="tip-box purple mt-16">
      <span>&#x1F4A1;</span>
      <div><strong>Key insight:</strong> Much of what appears to be &ldquo;model quality&rdquo; is actually <strong>context quality</strong> and surrounding system design. The harness matters as much as the model.</div>
    </div>
  </div>
</section>
`);
