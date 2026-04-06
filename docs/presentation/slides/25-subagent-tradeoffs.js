registerSlide(`
<section class="slide" data-title="subagent-tradeoffs">
  <div class="slide-inner">
    <div class="section-label">Sub-Agents</div>
    <h2 class="section-title">Trade-offs</h2>
    <p class="section-desc">Sub-agents are powerful but come with costs. When to use them &mdash; and when not to.</p>

    <div class="two-col mt-24" style="gap:20px">

      <!-- Pros -->
      <div>
        <div style="font-family:var(--mono);font-size:13px;font-weight:700;color:var(--accent4);letter-spacing:1px;text-transform:uppercase;margin-bottom:14px">Pros</div>

        <div class="step-item" style="margin-bottom:10px">
          <div class="card" style="border-left:3px solid var(--accent4);margin:0">
            <h3 style="font-size:15px">&#x1F9F9; Context stays clean</h3>
            <p style="font-size:14px">Intermediate tool results (file reads, greps) are discarded. Only the summary returns to the main conversation.</p>
          </div>
        </div>

        <div class="step-item" style="margin-bottom:10px">
          <div class="card" style="border-left:3px solid var(--accent4);margin:0">
            <h3 style="font-size:15px">&#x26A1; Parallel execution</h3>
            <p style="font-size:14px">Multiple sub-agents can run concurrently. Investigate 3 files at the same time instead of sequentially.</p>
          </div>
        </div>

        <div class="step-item" style="margin-bottom:10px">
          <div class="card" style="border-left:3px solid var(--accent4);margin:0">
            <h3 style="font-size:15px">&#x1F3AD; Specialized prompts</h3>
            <p style="font-size:14px">Each sub-agent type gets its own system prompt. A code reviewer and a debugger need different instructions.</p>
          </div>
        </div>

        <div class="step-item">
          <div class="card" style="border-left:3px solid var(--accent4);margin:0">
            <h3 style="font-size:15px">&#x1F4CA; Token savings</h3>
            <p style="font-size:14px">Same work in main context: <strong style="color:var(--red)">+70K tokens</strong>. Via sub-agent: <strong style="color:var(--accent4)">35K main + isolated 20K</strong>. Context shrinks 52%.</p>
          </div>
        </div>
      </div>

      <!-- Cons -->
      <div>
        <div style="font-family:var(--mono);font-size:13px;font-weight:700;color:var(--red);letter-spacing:1px;text-transform:uppercase;margin-bottom:14px">Cons</div>

        <div class="step-item" style="margin-bottom:10px">
          <div class="card" style="border-left:3px solid var(--red);margin:0">
            <h3 style="font-size:15px">&#x1F4B8; Extra API calls</h3>
            <p style="font-size:14px">Each sub-agent is a full ReAct loop &mdash; multiple LLM round-trips. A simple grep doesn't need a sub-agent.</p>
          </div>
        </div>

        <div class="step-item" style="margin-bottom:10px">
          <div class="card" style="border-left:3px solid var(--red);margin:0">
            <h3 style="font-size:15px">&#x23F3; Latency overhead</h3>
            <p style="font-size:14px">Spawning a new session, running turns, and returning adds wall-clock time. Fast tasks are faster inline.</p>
          </div>
        </div>

        <div class="step-item" style="margin-bottom:10px">
          <div class="card" style="border-left:3px solid var(--red);margin:0">
            <h3 style="font-size:15px">&#x1F50D; Lost detail</h3>
            <p style="font-size:14px">Only the summary survives. If the main agent needs raw data later, it must re-fetch or the sub-agent must include it.</p>
          </div>
        </div>

        <div class="step-item">
          <div class="card" style="border-left:3px solid var(--red);margin:0">
            <h3 style="font-size:15px">&#x1F6AB; No nesting</h3>
            <p style="font-size:14px">Depth is limited to 1. A sub-agent cannot spawn another sub-agent &mdash; keeps complexity bounded.</p>
          </div>
        </div>
      </div>

    </div>
  </div>
</section>
`);
