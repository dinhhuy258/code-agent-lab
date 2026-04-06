registerSlide(`
<section class="slide" data-title="six-components">
  <div class="slide-inner">
    <div class="section-label">Reference</div>
    <h2 class="section-title">6 Components of a Coding Agent</h2>
    <p class="section-desc">From Sebastian Raschka's analysis &mdash; mapped to our implementation.</p>

    <div class="card-grid mt-24">
      <div class="card">
        <h3>1. Live Repo Context</h3>
        <p>Git status, project structure, CLAUDE.md docs. Agent doesn't start from zero.</p>
        <span class="tag" style="background:rgba(124,58,237,.06);color:var(--accent)">system_prompt.py</span>
      </div>
      <div class="card">
        <h3>2. Prompt Shape &amp; Cache</h3>
        <p>Stable vs dynamic sections. Maximize prefix caching across turns.</p>
        <span class="tag" style="background:rgba(14,165,233,.06);color:var(--accent3)">prompt_provider.py</span>
      </div>
      <div class="card">
        <h3>3. Tool Access &amp; Use</h3>
        <p>Predefined, validated tool set with schemas. Not arbitrary code execution.</p>
        <span class="tag" style="background:rgba(5,150,105,.06);color:var(--accent4)">tools/registry.py</span>
      </div>
      <div class="card">
        <h3>4. Context Reduction</h3>
        <p>Clipping verbose outputs, deduplication, transcript compression.</p>
        <span class="tag" style="background:rgba(234,88,12,.06);color:var(--orange)">Future: ch4-5</span>
      </div>
      <div class="card">
        <h3>5. Session Memory</h3>
        <p>Working memory (distilled) + full transcript. Enables session continuity.</p>
        <span class="tag" style="background:rgba(202,138,4,.06);color:var(--yellow)">chat_session.py</span>
      </div>
      <div class="card">
        <h3>6. Delegation</h3>
        <p>Spawn bounded subtasks with inherited context but tighter restrictions.</p>
        <span class="tag" style="background:rgba(219,39,119,.06);color:var(--pink)">agents/subagent_runner.py</span>
      </div>
    </div>
  </div>
</section>
`);
