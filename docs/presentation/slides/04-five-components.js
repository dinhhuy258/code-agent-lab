registerSlide(`
<section class="slide" data-title="five-components">
  <div class="slide-inner">
    <div class="section-label">Architecture</div>
    <h2 class="section-title">5 Components of a Coding Agent</h2>
    <p class="section-desc">The building blocks every coding agent needs &mdash; from prompt design to task delegation.</p>

    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:24px">

      <div class="pattern-card" style="border-left:3px solid var(--accent)">
        <div class="pc-header">
          <div class="pc-icon" style="background:rgba(124,58,237,.06)">&#x1F4DD;</div>
          <div>
            <div class="pc-title">Prompt Shape &amp; Cache</div>
            <span class="pc-tag" style="background:rgba(124,58,237,.06);color:var(--accent)">foundation</span>
          </div>
        </div>
        <p>Stable system instructions at the top, dynamic context below. Maximizes prefix caching across turns.</p>
      </div>

      <div class="pattern-card" style="border-left:3px solid var(--accent3)">
        <div class="pc-header">
          <div class="pc-icon" style="background:rgba(14,165,233,.06)">&#x1F527;</div>
          <div>
            <div class="pc-title">Tool Access &amp; Use</div>
            <span class="pc-tag" style="background:rgba(14,165,233,.06);color:var(--accent3)">capability</span>
          </div>
        </div>
        <p>Predefined, validated tool set with JSON schemas. Structured calls &mdash; not arbitrary code execution.</p>
      </div>

      <div class="pattern-card" style="border-left:3px solid var(--accent4)">
        <div class="pc-header">
          <div class="pc-icon" style="background:rgba(5,150,105,.06)">&#x2702;&#xFE0F;</div>
          <div>
            <div class="pc-title">Context Reduction</div>
            <span class="pc-tag" style="background:rgba(5,150,105,.06);color:var(--accent4)">efficiency</span>
          </div>
        </div>
        <p>Clip verbose outputs, deduplicate content, compress transcripts. Keep the context window useful.</p>
      </div>

    </div>

    <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:14px;margin-top:14px;max-width:68%;margin-left:auto;margin-right:auto">

      <div class="pattern-card" style="border-left:3px solid var(--orange)">
        <div class="pc-header">
          <div class="pc-icon" style="background:rgba(234,88,12,.06)">&#x1F9E0;</div>
          <div>
            <div class="pc-title">Session Memory</div>
            <span class="pc-tag" style="background:rgba(234,88,12,.06);color:var(--orange)">continuity</span>
          </div>
        </div>
        <p>Working memory (distilled) + full transcript. The agent remembers what happened and picks up where it left off.</p>
      </div>

      <div class="pattern-card" style="border-left:3px solid var(--pink)">
        <div class="pc-header">
          <div class="pc-icon" style="background:rgba(219,39,119,.06)">&#x1F4E4;</div>
          <div>
            <div class="pc-title">Delegation</div>
            <span class="pc-tag" style="background:rgba(219,39,119,.06);color:var(--pink)">scale</span>
          </div>
        </div>
        <p>Spawn bounded sub-tasks with inherited context but tighter restrictions. Keeps the main loop focused.</p>
      </div>

    </div>
  </div>
</section>
`);
