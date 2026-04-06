registerSlide(`
<section class="slide" data-title="architecture-summary">
  <div class="slide-inner">
    <div class="section-label">Summary</div>
    <h2 class="section-title">The Complete Picture</h2>
    <p class="section-desc">From chat to autonomous agent &mdash; every layer we covered.</p>

    <div class="arch-diagram mt-24" style="padding:28px">
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px">
        <div>
          <div class="layer-label">User Interface</div>
          <div class="node lead" style="width:100%;justify-content:center;margin-bottom:16px"><span class="dot-indicator"></span> Textual TUI &mdash; Streaming Events</div>

          <div class="layer-label">Orchestration</div>
          <div class="node lead" style="width:100%;justify-content:center;margin-bottom:16px"><span class="dot-indicator"></span> AgentClient &mdash; ReAct Loop (25 turns)</div>

          <div class="layer-label">History</div>
          <div class="node worker" style="width:100%;justify-content:center;margin-bottom:16px"><span class="dot-indicator"></span> ChatSession &mdash; Conversation Memory</div>

          <div class="layer-label">LLM</div>
          <div class="node sub" style="width:100%;justify-content:center"><span class="dot-indicator"></span> GeminiLLMClient &mdash; Protocol-based</div>
        </div>
        <div>
          <div class="layer-label">Tools (10+)</div>
          <div style="display:flex;flex-wrap:wrap;gap:6px;margin-bottom:16px">
            <code style="font-size:11px">glob</code>
            <code style="font-size:11px">read_file</code>
            <code style="font-size:11px">write_file</code>
            <code style="font-size:11px">replace</code>
            <code style="font-size:11px">grep_search</code>
            <code style="font-size:11px">run_shell</code>
            <code style="font-size:11px">web_fetch</code>
            <code style="font-size:11px">task</code>
            <code style="font-size:11px">activate_skill</code>
            <code style="font-size:11px">list_dir</code>
          </div>

          <div class="layer-label">Skills</div>
          <div class="card" style="padding:12px;margin-bottom:16px">
            <p style="font-size:13px">YAML frontmatter &rarr; deferred loading &rarr; context injection on demand</p>
          </div>

          <div class="layer-label">Sub-Agents</div>
          <div class="card" style="padding:12px;margin-bottom:16px">
            <p style="font-size:13px">Isolated ChatSession &rarr; own ReAct loop (15 turns) &rarr; summary returns</p>
          </div>

          <div class="layer-label">MCP (Extensible)</div>
          <div class="card" style="padding:12px">
            <p style="font-size:13px">Stdio pipes &rarr; dynamic discovery &rarr; adapter pattern &rarr; pluggable tools</p>
          </div>
        </div>
      </div>
    </div>

    <div class="tip-box purple mt-16">
      <span>&#x1F680;</span>
      <div><strong>Source code:</strong> <code>github.com/dinhhuy258/code-agent-cli</code> &mdash; a complete, working implementation of everything discussed today.</div>
    </div>
  </div>
</section>
`);
