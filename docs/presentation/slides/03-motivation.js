registerSlide(`
<section class="slide" data-title="motivation">
  <div class="slide-inner">
    <div class="section-label">Motivation</div>
    <h2 class="section-title">Why Build One?</h2>
    <p class="section-desc">Understanding agent internals transforms how you use and build AI-powered tools.</p>

    <div class="two-col mt-24">
      <div>
        <h3 style="font-size:20px;font-weight:700;margin-bottom:12px">The Problem Space</h3>
        <div class="card" style="margin-bottom:12px">
          <p>&#x1F50D; <strong>Raw LLMs are stateless</strong> &mdash; they don't know your codebase, can't run tests, can't read files</p>
        </div>
        <div class="card" style="margin-bottom:12px">
          <p>&#x1F504; <strong>Multi-step tasks require loops</strong> &mdash; read, analyze, modify, verify, repeat</p>
        </div>
        <div class="card">
          <p>&#x1F6E1;&#xFE0F; <strong>Safety requires guardrails</strong> &mdash; confirmation for writes, isolation for sub-tasks</p>
        </div>
      </div>
      <div>
        <h3 style="font-size:20px;font-weight:700;margin-bottom:12px">Our Implementation</h3>
        <div class="code-block">
          <div class="code-header"><span class="c r"></span><span class="c y"></span><span class="c g"></span><span class="filename">code-agent-cli</span></div>
          <div class="code-body">
<span class="cm"># A real coding agent built with:</span>
<span class="var">LLM</span>      = Gemini 2.5 Flash
<span class="var">UI</span>       = Textual TUI
<span class="var">Language</span> = Python
<span class="var">Tools</span>    = 10+ built-in
<span class="var">Skills</span>   = YAML-defined, on-demand
<span class="var">Agents</span>   = Isolated sub-agents
          </div>
        </div>
        <div class="tip-box green">
          <span>&#x2705;</span>
          <div>Production patterns inspired by <strong>Claude Code</strong> and <strong>Gemini CLI</strong></div>
        </div>
      </div>
    </div>
  </div>
</section>
`);
