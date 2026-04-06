registerSlide(`
<section class="slide" data-title="tool-mental-model">
  <div class="slide-inner">
    <div class="section-label">Tool Use</div>
    <h2 class="section-title">The Fundamental Primitive</h2>
    <p class="section-desc">Tool use is the <strong>only primitive</strong> an LLM actually understands for interacting with the world.</p>

    <div class="lifecycle mt-24">
      <div class="lc-step">
        <div class="step-num">1</div>
        <div class="step-icon">&#x1F4CB;</div>
        <div class="step-label">Define Schema</div>
        <div class="step-desc">Declare tools with JSON Schema &mdash; name, description, parameters</div>
      </div>
      <div class="lc-arrow">&#x2192;</div>
      <div class="lc-step">
        <div class="step-num">2</div>
        <div class="step-icon">&#x1F4E4;</div>
        <div class="step-label">Send to API</div>
        <div class="step-desc">Tool declarations sent alongside conversation history</div>
      </div>
      <div class="lc-arrow">&#x2192;</div>
      <div class="lc-step">
        <div class="step-num">3</div>
        <div class="step-icon">&#x1F3AF;</div>
        <div class="step-label">Parse Calls</div>
        <div class="step-desc">Model returns structured function_call objects (not free text)</div>
      </div>
      <div class="lc-arrow">&#x2192;</div>
      <div class="lc-step">
        <div class="step-num">4</div>
        <div class="step-icon">&#x1F4E5;</div>
        <div class="step-label">Return Result</div>
        <div class="step-desc">Execute locally, send result back as function_response</div>
      </div>
    </div>

    <div class="tip-box orange mt-16">
      <span>&#x26A0;&#xFE0F;</span>
      <div><strong>The LLM never executes code.</strong> It outputs JSON describing <em>what</em> tool to call. Your code (the harness) is the executor.</div>
    </div>
  </div>
</section>
`);
