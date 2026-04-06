registerSlide(`
<section class="slide" data-title="whats-missing">
  <div class="slide-inner">
    <div class="section-label">Gaps</div>
    <h2 class="section-title">What&rsquo;s Missing</h2>
    <p class="section-desc">Features that exist but haven&rsquo;t graduated to first-class architecture yet.</p>

    <div class="two-col mt-24" style="gap:24px">

      <div class="pattern-card">
        <div class="pc-header">
          <div class="pc-icon" style="background:rgba(234,88,12,.06)">&#x1F4CB;</div>
          <div>
            <div class="pc-title">TaskManager</div>
            <span class="pc-tag" style="background:rgba(234,88,12,.06);color:var(--orange)">still a tool</span>
          </div>
        </div>
        <p>Task tracking lives inside the tool layer &mdash; the agent calls it like any other tool. There is no dedicated orchestration-level task manager that can plan, prioritize, and coordinate work across turns.</p>
      </div>

      <div class="pattern-card">
        <div class="pc-header">
          <div class="pc-icon" style="background:rgba(14,165,233,.06)">&#x1F50C;</div>
          <div>
            <div class="pc-title">MCP</div>
            <span class="pc-tag" style="background:rgba(14,165,233,.06);color:var(--accent3)">still a tool</span>
          </div>
        </div>
        <p>MCP integration is implemented as a tool adapter. Discovery, lifecycle management, and resource access are not yet promoted to a core subsystem with its own event model.</p>
      </div>

    </div>
  </div>
</section>
`);
