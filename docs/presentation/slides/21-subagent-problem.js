registerSlide(`
<section class="slide" data-title="subagent-problem">
  <div class="slide-inner">
    <div class="section-label">Sub-Agents</div>
    <h2 class="section-title">Context Isolation</h2>
    <p class="section-desc">A single conversation with one system prompt can't handle everything. Sub-agents solve three problems.</p>

    <div class="three-col mt-24">
      <div class="card" style="border-top:3px solid var(--red)">
        <h3>&#x1F4A5; Context Pollution</h3>
        <p>Intermediate tool results (file reads, greps) stay in history forever, bloating every subsequent API call.</p>
      </div>
      <div class="card" style="border-top:3px solid var(--orange)">
        <h3>&#x1F3AD; No Specialization</h3>
        <p>One system prompt can't optimize for all personas. A code reviewer needs different instructions than a debugger.</p>
      </div>
      <div class="card" style="border-top:3px solid var(--yellow)">
        <h3>&#x23F3; Sequential Only</h3>
        <p>With a single ReAct loop, tasks execute one at a time. No parallel investigation possible.</p>
      </div>
    </div>

    <div class="tip-box blue mt-24">
      <span>&#x1F4A1;</span>
      <div><strong>The solution:</strong> A sub-agent is a <strong>tool that runs its own ReAct loop</strong> in an isolated ChatSession with its own system prompt. Results return to the parent; intermediate work is discarded.</div>
    </div>
  </div>
</section>
`);
