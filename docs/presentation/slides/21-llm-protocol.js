registerSlide(`
<section class="slide" data-title="llm-protocol">
  <div class="slide-inner">
    <div class="section-label">Extensibility</div>
    <h2 class="section-title">Protocol-Based LLM Abstraction</h2>
    <p class="section-desc">Swap providers without changing agent code. Python Protocols enable structural typing.</p>

    <div class="two-col mt-24">
      <div>
        <div class="code-block">
          <div class="code-header"><span class="c r"></span><span class="c y"></span><span class="c g"></span><span class="filename">llm/client.py</span></div>
          <div class="code-body">
<span class="kw">class</span> <span class="type">LLMClient</span>(<span class="type">Protocol</span>):
    <span class="cm">"""Any class with these methods works."""</span>

    <span class="kw">def</span> <span class="fn">generate_content</span>(
        <span class="var">self</span>,
        request: <span class="type">GenerateContentRequest</span>
    ) -&gt; <span class="type">TurnResult</span>: ...

    <span class="kw">def</span> <span class="fn">generate_content_stream</span>(
        <span class="var">self</span>,
        request: <span class="type">GenerateContentRequest</span>
    ) -&gt; <span class="type">Generator</span>[<span class="type">TurnResult</span>]: ...
          </div>
        </div>
      </div>
      <div>
        <div class="card-grid" style="grid-template-columns:1fr">
          <div class="card" style="border-left:3px solid var(--accent)">
            <h3>GeminiLLMClient</h3>
            <p>Production client. Uses <code>google-genai</code> SDK. Handles streaming, tool declarations, usage tracking.</p>
            <span class="tag" style="background:rgba(124,58,237,.06);color:var(--accent)">Current</span>
          </div>
          <div class="card" style="border-left:3px solid var(--accent3)">
            <h3>DebugLLMClient</h3>
            <p>Wrapper that logs all requests/responses to <code>.debug/</code> directory. Decorates any LLMClient.</p>
            <span class="tag" style="background:rgba(14,165,233,.06);color:var(--accent3)">Development</span>
          </div>
          <div class="card" style="border-left:3px solid var(--accent4)">
            <h3>FakeLLMClient</h3>
            <p>Returns canned responses for testing. No API calls needed. Fast, deterministic.</p>
            <span class="tag" style="background:rgba(5,150,105,.06);color:var(--accent4)">Testing</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
`);
