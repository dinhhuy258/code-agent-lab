registerSlide(`
<section class="slide" data-title="prompt-structure">
  <div class="slide-inner">
    <div class="section-label">Optimization</div>
    <h2 class="section-title">Prompt Architecture</h2>
    <p class="section-desc">Structure prompts into stable and dynamic sections to maximize cache reuse.</p>

    <div class="ctx-vis mt-24">
      <div class="ctx-col">
        <div class="ctx-bar-wrap">
          <div class="ctx-segment system" style="height:20%"><div class="ctx-segment-label">System<br>Prompt</div></div>
          <div class="ctx-segment tools" style="height:15%"><div class="ctx-segment-label">Tool<br>Schemas</div></div>
          <div class="ctx-segment conversation" style="height:50%"><div class="ctx-segment-label">Conversation<br>History</div></div>
        </div>
        <div class="ctx-label">Turn 10<br><strong style="color:var(--orange)">~52K tokens</strong></div>
      </div>

      <div class="ctx-vs">&#x27A1;</div>

      <div class="ctx-col">
        <div class="ctx-bar-wrap">
          <div class="ctx-segment system" style="height:20%"><div class="ctx-segment-label">System<br>(cached)</div></div>
          <div class="ctx-segment tools" style="height:15%"><div class="ctx-segment-label">Tools<br>(cached)</div></div>
          <div class="ctx-segment summary" style="height:15%"><div class="ctx-segment-label">Summary</div></div>
          <div class="ctx-segment conversation" style="height:20%"><div class="ctx-segment-label">Recent</div></div>
        </div>
        <div class="ctx-label">After Compact<br><strong style="color:var(--accent4)">~30K tokens</strong></div>
      </div>
    </div>

    <div class="card-grid mt-16">
      <div class="card">
        <h3>&#x1F4CC; Stable Section</h3>
        <p>System instructions + tool schemas. Rarely changes. <strong>Cacheable</strong> across turns for reduced cost.</p>
        <span class="tag" style="background:rgba(124,58,237,.06);color:var(--accent)">~35% of tokens</span>
      </div>
      <div class="card">
        <h3>&#x1F504; Dynamic Section</h3>
        <p>User messages + model responses + tool results. Grows every turn. <strong>This is the snowball.</strong></p>
        <span class="tag" style="background:rgba(234,88,12,.06);color:var(--orange)">~65% of tokens</span>
      </div>
      <div class="card">
        <h3>&#x2702;&#xFE0F; Compaction</h3>
        <p>Summarize old conversation into a single message. Saves 50-70% but <strong>lossy</strong> &mdash; detail is lost.</p>
        <span class="tag" style="background:rgba(5,150,105,.06);color:var(--accent4)">Production must-have</span>
      </div>
    </div>
  </div>
</section>
`);
