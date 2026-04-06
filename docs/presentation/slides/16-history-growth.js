registerSlide(`
<section class="slide" data-title="history-growth">
  <div class="slide-inner">
    <div class="section-label">Context Management</div>
    <h2 class="section-title">History Growth</h2>
    <p class="section-desc">Watch <code>self._history</code> grow through a single user request. Every entry is <strong>permanent</strong>.</p>

    <div style="display:flex;align-items:center;gap:12px;margin:20px 0 14px">
      <div style="flex:1;height:1px;background:var(--border)"></div>
      <span style="font-family:var(--mono);font-size:10px;color:var(--text3);background:var(--surface2);border:1px solid var(--border);border-radius:5px;padding:2px 8px">&#x2193; step through</span>
    </div>

    <div style="display:flex;flex-direction:column;gap:0;padding:0 20px">

      <div class="step-item" style="display:flex;align-items:center;gap:14px;padding:10px 0;border-bottom:1px solid var(--border)">
        <span style="font-family:var(--mono);font-size:10px;font-weight:600;color:var(--accent);letter-spacing:1px;min-width:24px;text-align:right">#1</span>
        <div class="node lead" style="flex-shrink:0;min-width:56px"><span class="dot-indicator"></span> user</div>
        <code style="font-size:12px;color:var(--text2);flex:1">Content(role="user", parts=[Part(text="fix the bug in auth.py")])</code>
        <span style="font-family:var(--mono);font-size:10px;color:var(--accent4);white-space:nowrap">~20 tokens</span>
      </div>

      <div class="step-item" style="display:flex;align-items:center;gap:14px;padding:10px 0;border-bottom:1px solid var(--border)">
        <span style="font-family:var(--mono);font-size:10px;font-weight:600;color:var(--accent3);letter-spacing:1px;min-width:24px;text-align:right">#2</span>
        <div class="node worker" style="flex-shrink:0;min-width:56px"><span class="dot-indicator"></span> model</div>
        <code style="font-size:12px;color:var(--text2);flex:1">Content(role="model", parts=[Part(function_call=read_file("auth.py"))])</code>
        <span style="font-family:var(--mono);font-size:10px;color:var(--accent4);white-space:nowrap">~30 tokens</span>
      </div>

      <div class="step-item" style="display:flex;align-items:center;gap:14px;padding:10px 0;border-bottom:1px solid var(--border)">
        <span style="font-family:var(--mono);font-size:10px;font-weight:600;color:var(--orange);letter-spacing:1px;min-width:24px;text-align:right">#3</span>
        <div class="node" style="flex-shrink:0;min-width:56px;background:rgba(234,88,12,.06);border-color:rgba(234,88,12,.2)"><span class="dot-indicator" style="background:var(--orange)"></span> tool</div>
        <code style="font-size:12px;color:var(--text2);flex:1">Content(role="user", parts=[Part(function_response={content: "...5K chars..."})])</code>
        <span style="font-family:var(--mono);font-size:10px;color:var(--red);font-weight:600;white-space:nowrap">~5,000 tokens</span>
      </div>

      <div class="step-item" style="display:flex;align-items:center;gap:14px;padding:10px 0;border-bottom:1px solid var(--border)">
        <span style="font-family:var(--mono);font-size:10px;font-weight:600;color:var(--accent3);letter-spacing:1px;min-width:24px;text-align:right">#4</span>
        <div class="node worker" style="flex-shrink:0;min-width:56px"><span class="dot-indicator"></span> model</div>
        <code style="font-size:12px;color:var(--text2);flex:1">Content(role="model", parts=[Part(function_call=write_file("auth.py", ...))])</code>
        <span style="font-family:var(--mono);font-size:10px;color:var(--red);font-weight:600;white-space:nowrap">~5,000 tokens</span>
      </div>

      <div class="step-item" style="display:flex;align-items:center;gap:14px;padding:10px 0;border-bottom:1px solid var(--border)">
        <span style="font-family:var(--mono);font-size:10px;font-weight:600;color:var(--orange);letter-spacing:1px;min-width:24px;text-align:right">#5</span>
        <div class="node" style="flex-shrink:0;min-width:56px;background:rgba(234,88,12,.06);border-color:rgba(234,88,12,.2)"><span class="dot-indicator" style="background:var(--orange)"></span> tool</div>
        <code style="font-size:12px;color:var(--text2);flex:1">Content(role="user", parts=[Part(function_response={status: "ok"})])</code>
        <span style="font-family:var(--mono);font-size:10px;color:var(--accent4);white-space:nowrap">~15 tokens</span>
      </div>

      <div class="step-item" style="display:flex;align-items:center;gap:14px;padding:10px 0;border-bottom:1px solid var(--border)">
        <span style="font-family:var(--mono);font-size:10px;font-weight:600;color:var(--accent3);letter-spacing:1px;min-width:24px;text-align:right">#6</span>
        <div class="node worker" style="flex-shrink:0;min-width:56px"><span class="dot-indicator"></span> model</div>
        <code style="font-size:12px;color:var(--text2);flex:1">Content(role="model", parts=[Part(text="Fixed the auth bug.")])</code>
        <span style="font-family:var(--mono);font-size:10px;color:var(--accent4);white-space:nowrap">~10 tokens</span>
      </div>

      <div class="step-item" style="padding:14px 0">
        <div class="card" style="border-left:3px solid var(--red);margin:0">
          <h3>&#x1F4E6; Next turn: ALL 6 entries resent + new user message</h3>
          <p>One simple "fix the bug" request produced <strong>~10,075 tokens</strong> of history. The two file operations (read + write) account for 99% of it &mdash; and they're stuck in history <strong>forever</strong>.</p>
        </div>
      </div>

    </div>
  </div>
</section>
`);
