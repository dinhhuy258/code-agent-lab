registerSlide(`
<section class="slide" data-title="lessons">
  <div class="slide-inner">
    <div class="section-label">Takeaways</div>
    <h2 class="section-title">What We Learned</h2>
    <p class="section-desc">Building a coding agent from scratch reveals truths you can't learn from using one.</p>

    <div class="pattern-grid mt-24">
      <div class="pattern-card">
        <div class="pc-header">
          <div class="pc-icon" style="background:rgba(124,58,237,.06)">&#x1F3AF;</div>
          <div>
            <div class="pc-title">Context is the Bottleneck</div>
            <span class="pc-tag" style="background:rgba(124,58,237,.06);color:var(--accent)">#1 insight</span>
          </div>
        </div>
        <p>Not raw intelligence. The quality of context you provide &mdash; and how efficiently you manage it &mdash; determines agent effectiveness.</p>
      </div>
      <div class="pattern-card">
        <div class="pc-header">
          <div class="pc-icon" style="background:rgba(14,165,233,.06)">&#x1F500;</div>
          <div>
            <div class="pc-title">Routing, Not Intelligence</div>
            <span class="pc-tag" style="background:rgba(14,165,233,.06);color:var(--accent3)">architecture</span>
          </div>
        </div>
        <p>"Agentic AI is a routing problem, not an intelligence problem." Getting the right context to the right place at the right time.</p>
      </div>
      <div class="pattern-card">
        <div class="pc-header">
          <div class="pc-icon" style="background:rgba(5,150,105,.06)">&#x1F4E6;</div>
          <div>
            <div class="pc-title">Lazy Loading is Essential</div>
            <span class="pc-tag" style="background:rgba(5,150,105,.06);color:var(--accent4)">optimization</span>
          </div>
        </div>
        <p>Deferred tools (name only at startup), deferred skills (metadata only), sub-agent isolation. Never load what you don't need.</p>
      </div>
      <div class="pattern-card">
        <div class="pc-header">
          <div class="pc-icon" style="background:rgba(234,88,12,.06)">&#x1F6E1;&#xFE0F;</div>
          <div>
            <div class="pc-title">Safety is First-Class</div>
            <span class="pc-tag" style="background:rgba(234,88,12,.06);color:var(--orange)">design</span>
          </div>
        </div>
        <p>Confirmation flags on dangerous tools, isolated sessions for sub-agents, max turn limits. Guardrails are architecture, not afterthoughts.</p>
      </div>
    </div>
  </div>
</section>
`);
