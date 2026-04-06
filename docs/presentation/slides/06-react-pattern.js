registerSlide(`
<section class="slide" data-title="react-pattern">
  <div class="slide-inner">
    <div class="section-label">Core Architecture</div>
    <h2 class="section-title">The ReAct Loop</h2>
    <p class="section-desc">Reasoning + Acting — the agent iterates between thinking and doing until the task is complete.</p>

    <div style="display:flex;align-items:center;gap:12px;margin:20px 0 14px">
      <div style="flex:1;height:1px;background:var(--border)"></div>
      <span style="font-family:var(--mono);font-size:10px;color:var(--text3);background:var(--surface2);border:1px solid var(--border);border-radius:5px;padding:2px 8px">&#x2193; step through</span>
    </div>

    <div class="lifecycle mt-24" style="gap:0">
      <!-- Step 1: standalone -->
      <div class="lc-step step-item">
        <div class="step-num">STEP 1</div>
        <div class="step-icon">&#x1F4E5;</div>
        <div class="step-label">Observe</div>
        <div class="step-desc">Receive user message, collect environment context</div>
      </div>
      <!-- Arrow + Step 2 together -->
      <div class="step-item" style="display:flex;align-items:stretch;flex:1">
        <div class="lc-arrow">&#x2192;</div>
        <div class="lc-step" style="flex:1">
          <div class="step-num">STEP 2</div>
          <div class="step-icon">&#x1F9E0;</div>
          <div class="step-label">Reason</div>
          <div class="step-desc">Send full history + tools to LLM, get structured response</div>
        </div>
      </div>
      <!-- Arrow + Step 3 together -->
      <div class="step-item" style="display:flex;align-items:stretch;flex:1">
        <div class="lc-arrow">&#x2192;</div>
        <div class="lc-step" style="flex:1">
          <div class="step-num">STEP 3</div>
          <div class="step-icon">&#x1F6E0;&#xFE0F;</div>
          <div class="step-label">Act</div>
          <div class="step-desc">Execute tool calls, append results to history</div>
        </div>
      </div>
      <!-- Arrow + Step 4 together -->
      <div class="step-item" style="display:flex;align-items:stretch;flex:1">
        <div class="lc-arrow">&#x2192;</div>
        <div class="lc-step" style="flex:1">
          <div class="step-num">STEP 4</div>
          <div class="step-icon">&#x1F501;</div>
          <div class="step-label">Loop</div>
          <div class="step-desc">Repeat until text-only response or max turns (25)</div>
        </div>
      </div>
    </div>

    <div class="tip-box blue mt-16 step-item">
      <span>&#x1F4A1;</span>
      <div><strong>The model controls the loop.</strong> The harness is the executor; the LLM decides when to call tools, which tools to call, and when the task is done.</div>
    </div>
  </div>
</section>
`);
