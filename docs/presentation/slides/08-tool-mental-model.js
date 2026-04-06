registerSlide(`
<section class="slide" data-title="tool-mental-model">
  <div class="slide-inner">
    <div class="section-label">Tool Use</div>
    <h2 class="section-title">The Fundamental Primitive</h2>
    <p class="section-desc">Tool use is the <strong>only primitive</strong> an LLM actually understands for interacting with the world.</p>

    <div style="display:flex;align-items:center;gap:12px;margin:20px 0 14px">
      <div style="flex:1;height:1px;background:var(--border)"></div>
      <span style="font-family:var(--mono);font-size:10px;color:var(--text3);background:var(--surface2);border:1px solid var(--border);border-radius:5px;padding:2px 8px">&#x2193; step through</span>
    </div>

    <div class="lifecycle mt-24" style="gap:0">
      <!-- Step 1: standalone -->
      <div class="lc-step step-item">
        <div class="step-num">1</div>
        <div class="step-icon">&#x1F4CB;</div>
        <div class="step-label">Define Schema</div>
        <div class="step-desc">Declare tools with JSON Schema &mdash; name, description, parameters</div>
      </div>
      <!-- Arrow + Step 2 -->
      <div class="step-item" style="display:flex;align-items:stretch;flex:1">
        <div class="lc-arrow">&#x2192;</div>
        <div class="lc-step" style="flex:1">
          <div class="step-num">2</div>
          <div class="step-icon">&#x1F4E4;</div>
          <div class="step-label">Send to API</div>
          <div class="step-desc">Tool declarations sent alongside conversation history</div>
        </div>
      </div>
      <!-- Arrow + Step 3 -->
      <div class="step-item" style="display:flex;align-items:stretch;flex:1">
        <div class="lc-arrow">&#x2192;</div>
        <div class="lc-step" style="flex:1">
          <div class="step-num">3</div>
          <div class="step-icon">&#x1F3AF;</div>
          <div class="step-label">Parse Calls</div>
          <div class="step-desc">Model returns structured function_call objects (not free text)</div>
        </div>
      </div>
      <!-- Arrow + Step 4 -->
      <div class="step-item" style="display:flex;align-items:stretch;flex:1">
        <div class="lc-arrow">&#x2192;</div>
        <div class="lc-step" style="flex:1">
          <div class="step-num">4</div>
          <div class="step-icon">&#x1F4E5;</div>
          <div class="step-label">Return Result</div>
          <div class="step-desc">Execute locally, send result back as function_response</div>
        </div>
      </div>
    </div>

    <div class="tip-box orange mt-16 step-item">
      <span>&#x26A0;&#xFE0F;</span>
      <div><strong>The LLM never executes code.</strong> It outputs JSON describing <em>what</em> tool to call. Your code (the harness) is the executor.</div>
    </div>
  </div>
</section>
`);
