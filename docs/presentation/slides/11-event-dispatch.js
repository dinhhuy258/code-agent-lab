registerSlide(`
<section class="slide" data-title="event-dispatch">
  <div class="slide-inner">
    <div class="section-label">Implementation</div>
    <h2 class="section-title">Event Dispatch Pattern</h2>
    <p class="section-desc">Background thread yields events; UI thread renders them via <code>call_from_thread</code>.</p>

    <div class="two-col mt-24">
      <div>
        <div class="code-block">
          <div class="code-header"><span class="c r"></span><span class="c y"></span><span class="c g"></span><span class="filename">app.py</span></div>
          <div class="code-body">
<span class="cm"># Background thread</span>
<span class="kw">@work</span>(thread=<span class="num">True</span>)
<span class="kw">def</span> <span class="fn">_run_llm</span>(<span class="var">self</span>, user_text):
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
      <div>
        <div class="card" style="margin-bottom:12px">
          <h3>&#x1F3A8; Textual TUI</h3>
          <p>Uses the <strong>Textual</strong> framework for rich terminal UI. Widgets for chat messages, tool calls, status bar, and thinking indicators.</p>
        </div>
        <div class="card" style="margin-bottom:12px">
          <h3>&#x1F9F5; Thread Safety</h3>
          <p><code>call_from_thread()</code> bridges the background worker thread to the main UI thread safely. Events are posted, not pushed.</p>
        </div>
        <div class="card">
          <h3>&#x1F4E1; Progressive Rendering</h3>
          <p>Each <code>TextChunk</code> accumulates text in the widget. Textual diffs efficiently &mdash; only changed parts re-render.</p>
        </div>
      </div>
    </div>
  </div>
</section>
`);
