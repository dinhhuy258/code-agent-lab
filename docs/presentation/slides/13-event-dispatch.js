registerSlide(`
<section class="slide" data-title="event-dispatch">
  <div class="slide-inner">
    <div class="section-label">Implementation</div>
    <h2 class="section-title">Event Dispatch Pattern</h2>
    <p class="section-desc">Background thread yields events; UI thread renders them via <code>call_from_thread</code>.</p>

    <div class="two-col mt-24" style="align-items:stretch">
      <!-- LEFT: Code -->
      <div style="display:flex;flex-direction:column;gap:14px">
        <div class="code-block" style="flex:1;margin:0">
          <div class="code-header"><span class="c r"></span><span class="c y"></span><span class="c g"></span><span class="filename">app.py &mdash; Background Worker Thread</span></div>
          <div class="code-body">
<span class="cm"># Runs on a background thread</span>
<span class="cm"># &rarr; cannot touch UI widgets directly</span>
<span class="kw">@work</span>(thread=<span class="num">True</span>)
<span class="kw">def</span> <span class="fn">_run_llm</span>(<span class="var">self</span>, user_text):
    <span class="cm"># agent.send() yields events as</span>
    <span class="cm"># the LLM streams its response</span>
    <span class="kw">for</span> event <span class="kw">in</span> agent.send(user_text):

        <span class="kw">if</span> <span class="fn">isinstance</span>(event, <span class="type">TextChunk</span>):
            <span class="var">self</span>.call_from_thread(
                _on_text_chunk, event
            )

        <span class="kw">elif</span> <span class="fn">isinstance</span>(event, <span class="type">ToolCallStart</span>):
            <span class="var">self</span>.call_from_thread(
                _on_tool_call_start, event
            )

        <span class="kw">elif</span> <span class="fn">isinstance</span>(event, <span class="type">ToolCallEnd</span>):
            <span class="var">self</span>.call_from_thread(
                _on_tool_call_end, event
            )
          </div>
        </div>
      </div>

      <!-- RIGHT: Thread model explanation -->
      <div style="display:flex;flex-direction:column;gap:12px">
        <!-- Thread diagram -->
        <div class="card" style="margin:0;padding:20px;background:var(--surface)">
          <h3 style="font-size:16px;margin-bottom:14px">Thread Model</h3>
          <div style="display:flex;flex-direction:column;gap:0;position:relative">
            <!-- UI Thread -->
            <div style="display:flex;align-items:center;gap:10px;padding:10px 14px;background:rgba(124,58,237,.05);border:1.5px solid rgba(124,58,237,.2);border-radius:10px">
              <span style="font-size:18px">&#x1F3A8;</span>
              <div>
                <div style="font-weight:700;font-size:14px;color:var(--accent)">UI Thread (Main)</div>
                <div style="font-size:12px;color:var(--text2);margin-top:2px">Renders widgets, handles input, updates DOM. <strong>Single-threaded</strong> &mdash; must never block.</div>
              </div>
            </div>
            <!-- Bridge arrow -->
            <div style="display:flex;align-items:center;justify-content:center;padding:4px 0">
              <div style="display:flex;flex-direction:column;align-items:center;gap:0">
                <div style="width:2px;height:16px;background:var(--border2);position:relative;overflow:hidden">
                  <div style="position:absolute;width:100%;height:60%;background:linear-gradient(180deg,transparent,var(--accent),transparent);animation:flowLine 2s linear infinite;top:-60%"></div>
                </div>
                <div style="font-family:var(--mono);font-size:10px;color:var(--text3);padding:2px 8px;background:var(--surface2);border:1px solid var(--border);border-radius:5px;white-space:nowrap">call_from_thread()</div>
                <div style="width:2px;height:16px;background:var(--border2);position:relative;overflow:hidden">
                  <div style="position:absolute;width:100%;height:60%;background:linear-gradient(180deg,transparent,var(--accent),transparent);animation:flowLine 2s linear infinite;top:-60%"></div>
                </div>
              </div>
            </div>
            <!-- Worker Thread -->
            <div style="display:flex;align-items:center;gap:10px;padding:10px 14px;background:rgba(14,165,233,.05);border:1.5px solid rgba(14,165,233,.2);border-radius:10px">
              <span style="font-size:18px">&#x2699;&#xFE0F;</span>
              <div>
                <div style="font-weight:700;font-size:14px;color:var(--accent3)">Worker Thread (Background)</div>
                <div style="font-size:12px;color:var(--text2);margin-top:2px">Runs LLM streaming, tool execution, I/O. Yields events via generator.</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Key concepts -->
        <div class="card" style="margin:0">
          <h3>&#x1F9F5; Why Two Threads?</h3>
          <p>LLM API calls take <strong>seconds to minutes</strong>. If the UI thread waited, the terminal would freeze &mdash; no scrolling, no input, no cancel. The worker thread streams in the background while the UI stays responsive.</p>
        </div>

        <div class="card" style="margin:0">
          <h3>&#x1F6E1; Thread Safety Bridge</h3>
          <p><code>call_from_thread()</code> safely posts events from the worker to the UI thread's message queue. Events are <strong>posted, not pushed</strong> &mdash; the UI processes them on its own schedule, preventing race conditions.</p>
        </div>

        <div class="card" style="margin:0">
          <h3>&#x1F4E1; Progressive Rendering</h3>
          <p>Each <code>TextChunk</code> appends to the message widget. Textual diffs efficiently &mdash; only changed regions re-render. Tool calls get their own expandable widgets with live status.</p>
        </div>
      </div>
    </div>
  </div>
</section>
`);
