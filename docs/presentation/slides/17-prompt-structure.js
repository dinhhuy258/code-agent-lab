registerSlide(`
<section class="slide" data-title="prompt-structure">
  <div class="slide-inner">
    <div class="section-label">Context Management</div>
    <h2 class="section-title">Prompt Architecture</h2>
    <p class="section-desc">Every API call sends the same 3-part structure. The API reports what was cached vs reprocessed.</p>

    <div class="two-col mt-24" style="align-items:stretch">
      <div style="display:flex;flex-direction:column">
        <div class="ctx-vis" style="flex:1">
          <div class="ctx-col">
            <div class="ctx-bar-wrap">
              <div class="ctx-segment system" style="height:15%"><div class="ctx-segment-label">System<br>Instruction</div></div>
              <div class="ctx-segment tools" style="height:10%"><div class="ctx-segment-label">Tool<br>Schemas</div></div>
              <div class="ctx-segment conversation" style="height:20%"><div class="ctx-segment-label">History</div></div>
            </div>
            <div class="ctx-label">Turn 1<br><strong style="color:var(--accent4)">~36K</strong></div>
          </div>

          <div class="ctx-vs">&#x27A1;</div>

          <div class="ctx-col">
            <div class="ctx-bar-wrap">
              <div class="ctx-segment system" style="height:15%"><div class="ctx-segment-label">System<br>(cached)</div></div>
              <div class="ctx-segment tools" style="height:10%"><div class="ctx-segment-label">Tools<br>(cached)</div></div>
              <div class="ctx-segment conversation" style="height:60%"><div class="ctx-segment-label">History<br>&#x1F4C8;</div></div>
            </div>
            <div class="ctx-label">Turn 10<br><strong style="color:var(--orange)">~52K</strong></div>
          </div>
        </div>
      </div>
      <div style="display:flex;flex-direction:column;gap:12px;justify-content:center">
        <div class="card" style="border-left:3px solid var(--accent)">
          <h3>&#x1F4CC; Stable Prefix</h3>
          <p>System instruction + tool schemas. <strong>Identical every turn</strong> &mdash; the LLM can prefix-cache this portion.</p>
        </div>
        <div class="card" style="border-left:3px solid var(--orange)">
          <h3>&#x1F504; Growing History</h3>
          <p>Full <code>self._history</code> resent every call. No truncation, no summarization. This is the snowball.</p>
        </div>
        <div class="card" style="border-left:3px solid var(--accent4)">
          <h3>&#x1F4CA; Token Tracking</h3>
          <p>The API returns <code>cached_content_token_count</code> per response. We surface this via <code>UsageUpdate</code> events so the UI shows real cache hit rates.</p>
        </div>
      </div>
    </div>
  </div>
</section>
`);
