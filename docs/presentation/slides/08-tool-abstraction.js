registerSlide(`
<section class="slide" data-title="tool-abstraction">
  <div class="slide-inner">
    <div class="section-label">Implementation</div>
    <h2 class="section-title">Tool Abstraction</h2>
    <p class="section-desc">Every tool implements the same interface. The registry dispatches by name.</p>

    <div class="two-col mt-24">
      <div>
        <div class="code-block">
          <div class="code-header"><span class="c r"></span><span class="c y"></span><span class="c g"></span><span class="filename">tools/base.py</span></div>
          <div class="code-body">
<span class="kw">class</span> <span class="type">BaseTool</span>(<span class="type">ABC</span>):

    <span class="kw">def</span> <span class="fn">get_name</span>() -&gt; <span class="type">str</span>:
        <span class="cm"># Unique tool identifier</span>
        ...

    <span class="kw">def</span> <span class="fn">get_declaration</span>() -&gt; <span class="type">ToolDeclaration</span>:
        <span class="cm"># JSON Schema for the LLM</span>
        ...

    <span class="kw">def</span> <span class="fn">execute</span>(**kwargs) -&gt; <span class="type">ToolResult</span>:
        <span class="cm"># Do the thing</span>
        ...

    <span class="kw">def</span> <span class="fn">needs_confirmation</span>() -&gt; <span class="type">bool</span>:
        <span class="cm"># Safety flag</span>
        <span class="kw">return</span> <span class="num">False</span>
          </div>
        </div>
      </div>
      <div>
        <div class="code-block">
          <div class="code-header"><span class="c r"></span><span class="c y"></span><span class="c g"></span><span class="filename">tools/registry.py</span></div>
          <div class="code-body">
<span class="kw">class</span> <span class="type">ToolRegistry</span>:

    <span class="kw">def</span> <span class="fn">get_declarations</span>():
        <span class="cm"># Collect all schemas for API</span>
        <span class="kw">return</span> [t.get_declaration()
                <span class="kw">for</span> t <span class="kw">in</span> <span class="var">self</span>._tools]

    <span class="kw">def</span> <span class="fn">execute</span>(name, **kwargs):
        <span class="cm"># Dispatch to the right tool</span>
        tool = <span class="var">self</span>._tools[name]
        <span class="kw">return</span> tool.execute(**kwargs)
          </div>
        </div>
        <div class="tip-box purple mt-16">
          <span>&#x1F50C;</span>
          <div><strong>Pluggable:</strong> New tools just register into the same dictionary. The agent loop and LLM don't care how many tools exist.</div>
        </div>
      </div>
    </div>
  </div>
</section>
`);
