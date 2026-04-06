registerSlide(`
<section class="slide" data-title="loop-code">
  <div class="slide-inner">
    <div class="section-label">Implementation</div>
    <h2 class="section-title">AgentClient.send()</h2>
    <p class="section-desc">The core loop from our codebase — surprisingly simple at its heart.</p>

    <div class="two-col mt-24">
      <div>
        <div class="code-block">
          <div class="code-header"><span class="c r"></span><span class="c y"></span><span class="c g"></span><span class="filename">core/agent_client.py</span></div>
          <div class="code-body">
<span class="kw">async def</span> <span class="fn">send</span>(<span class="var">self</span>, <span class="var">user_text</span>: <span class="type">str</span>):
    <span class="var">self</span>._session.append_user_message(user_text)

    <span class="kw">for</span> _ <span class="kw">in</span> <span class="fn">range</span>(<span class="num">MAX_TURNS</span>):
        <span class="cm"># Send history + tools to LLM</span>
        result = <span class="kw">await</span> <span class="var">self</span>._session
            .send_message_stream()

        <span class="cm"># Yield text chunks for streaming</span>
        <span class="kw">for</span> chunk <span class="kw">in</span> result.text_chunks:
            <span class="kw">yield</span> <span class="fn">TextChunk</span>(chunk)

        <span class="cm"># No tool calls? We're done</span>
        <span class="kw">if not</span> result.function_calls:
            <span class="kw">yield</span> <span class="fn">TextResponse</span>(result.text)
            <span class="kw">return</span>

        <span class="cm"># Execute tools, loop back</span>
        <span class="kw">await</span> <span class="var">self</span>._process_tool_calls(
            result.function_calls
        )
          </div>
        </div>
      </div>
      <div>
        <div class="card" style="margin-bottom:12px;border-left:3px solid var(--accent)">
          <h3>&#x1F504; The Loop</h3>
          <p>Up to 25 iterations. Each iteration: call LLM &rarr; check for tool calls &rarr; execute or return.</p>
        </div>
        <div class="card" style="margin-bottom:12px;border-left:3px solid var(--accent3)">
          <h3>&#x1F4DD; History is Memory</h3>
          <p>The conversation history <em>is</em> the agent's memory. Every message, tool call, and result stays in the list.</p>
        </div>
        <div class="card" style="border-left:3px solid var(--accent4)">
          <h3>&#x26A0;&#xFE0F; Errors are Messages</h3>
          <p>Tool failures return as <code>ToolResult.error</code> — the model sees the error and can adjust its approach.</p>
        </div>
      </div>
    </div>
  </div>
</section>
`);
