registerSlide(`
<section class="slide" data-title="request-assembly">
  <div class="slide-inner">
    <div class="section-label">Context Management</div>
    <h2 class="section-title">Request Assembly</h2>
    <p class="section-desc">Every API call builds the same <code>GenerateContentRequest</code> &mdash; here's exactly what gets sent.</p>

    <div style="display:grid;grid-template-columns:1fr 1fr;gap:24px;align-items:stretch;margin-top:24px">
      <div style="display:flex;flex-direction:column">
        <div class="code-block" style="flex:1;display:flex;flex-direction:column;margin:0">
          <div class="code-header"><span class="c r"></span><span class="c y"></span><span class="c g"></span><span class="filename">core/chat_session.py</span></div>
          <div class="code-body" style="flex:1">
<span class="kw">def</span> <span class="fn">send_message_stream</span>(<span class="var">self</span>):

    request = <span class="fn">GenerateContentRequest</span>(
        <span class="cm"># Full conversation history</span>
        contents=<span class="fn">list</span>(<span class="var">self</span>._history),

        <span class="cm"># System prompt + skills</span>
        system_instruction=<span class="var">self</span>._system_instruction,

        <span class="cm"># All tool schemas</span>
        tools=<span class="var">self</span>._tool_declarations,
    )

    turn = <span class="fn">Turn</span>()
    <span class="kw">for</span> result <span class="kw">in</span> turn.run_stream(
        <span class="var">self</span>._client, request
    ):
        <span class="kw">yield</span> result
          </div>
        </div>
      </div>

      <div style="display:flex;flex-direction:column;gap:0">
        <div style="display:flex;align-items:center;gap:12px;margin:20px 0 14px">
          <div style="flex:1;height:1px;background:var(--border)"></div>
          <span style="font-family:var(--mono);font-size:10px;color:var(--text3);background:var(--surface2);border:1px solid var(--border);border-radius:5px;padding:2px 8px">&#x2193; step through</span>
        </div>
        <div class="step-item card" style="border-left:3px solid var(--accent);margin-bottom:12px">
          <h3>system_instruction</h3>
          <p><strong>Stable.</strong> Core prompt + available skills. Same string every turn. Benefits from <strong>prefix caching</strong>.</p>
        </div>
        <div class="step-item card" style="border-left:3px solid var(--accent3);margin-bottom:12px">
          <h3>tools</h3>
          <p><strong>Stable.</strong> All tool schemas (read_file, grep_search, etc.). Declared once, sent every turn unchanged.</p>
        </div>
        <div class="step-item card" style="border-left:3px solid var(--orange);margin-bottom:12px">
          <h3>contents (history)</h3>
          <p><strong>Grows.</strong> <code>list(self._history)</code> &mdash; the entire conversation. No truncation, no summarization. This is the snowball.</p>
        </div>
        <div class="step-item card" style="border-left:3px solid var(--red)">
          <h3>The Key Insight</h3>
          <p>2 parts are stable and cacheable. 1 part grows unbounded. All 3 are resent on <strong>every single API call</strong>.</p>
        </div>
      </div>
    </div>
  </div>
</section>
`);
