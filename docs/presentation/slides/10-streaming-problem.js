registerSlide(`
<section class="slide" data-title="streaming-problem">
  <div class="slide-inner">
    <div class="section-label">Real-Time UX</div>
    <h2 class="section-title">Streaming Architecture</h2>
    <p class="section-desc">Without streaming, users stare at a blank screen. The event system solves this.</p>

    <div class="two-col mt-24">
      <div>
        <h3 style="font-size:18px;font-weight:700;margin-bottom:12px;color:var(--red)">&#x274C; Before: Blocking</h3>
        <div class="card" style="border-left:3px solid var(--red)">
          <p>User sends message &rarr; <strong>5-30 seconds of nothing</strong> &rarr; full response appears at once. No feedback, no progress.</p>
        </div>
        <h3 style="font-size:18px;font-weight:700;margin:16px 0 12px;color:var(--accent4)">&#x2705; After: Streaming Events</h3>
        <div class="card" style="border-left:3px solid var(--accent4)">
          <p>Tokens appear as they're generated. Tool calls show names and progress. Sub-agent activity visible in real-time.</p>
        </div>
      </div>
      <div>
        <div class="code-block">
          <div class="code-header"><span class="c r"></span><span class="c y"></span><span class="c g"></span><span class="filename">core/events.py</span></div>
          <div class="code-body">
<span class="cm"># Event types the UI subscribes to</span>

<span class="type">TextChunk</span>       <span class="cm"># streaming token</span>
<span class="type">TextResponse</span>    <span class="cm"># final complete text</span>
<span class="type">ToolCallStart</span>   <span class="cm"># tool name + args</span>
<span class="type">ToolCallUpdate</span>  <span class="cm"># sub-agent progress</span>
<span class="type">ToolCallEnd</span>     <span class="cm"># success or error</span>
<span class="type">UsageUpdate</span>     <span class="cm"># token metrics</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
`);
