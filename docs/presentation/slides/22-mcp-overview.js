registerSlide(`
<section class="slide" data-title="mcp-overview">
  <div class="slide-inner">
    <div class="section-label">Extensibility</div>
    <h2 class="section-title">MCP: USB for AI Tools</h2>
    <p class="section-desc">Model Context Protocol &mdash; plug in external tools at runtime without code changes.</p>

    <div class="lifecycle mt-24">
      <div class="lc-step">
        <div class="step-num">1</div>
        <div class="step-icon">&#x1F4CB;</div>
        <div class="step-label">Config</div>
        <div class="step-desc">Define servers in <code>mcp.json</code> with command + args</div>
      </div>
      <div class="lc-arrow">&#x2192;</div>
      <div class="lc-step">
        <div class="step-num">2</div>
        <div class="step-icon">&#x1F680;</div>
        <div class="step-label">Launch</div>
        <div class="step-desc">MCPClient spawns subprocess, establishes stdio pipes</div>
      </div>
      <div class="lc-arrow">&#x2192;</div>
      <div class="lc-step">
        <div class="step-num">3</div>
        <div class="step-icon">&#x1F50D;</div>
        <div class="step-label">Discover</div>
        <div class="step-desc"><code>session.list_tools()</code> finds available tools dynamically</div>
      </div>
      <div class="lc-arrow">&#x2192;</div>
      <div class="lc-step">
        <div class="step-num">4</div>
        <div class="step-icon">&#x1F50C;</div>
        <div class="step-label">Adapt</div>
        <div class="step-desc">McpTool wraps MCP tools to look like BaseTool &mdash; agent doesn't care</div>
      </div>
    </div>

    <div class="two-col mt-24">
      <div>
        <div class="code-block">
          <div class="code-header"><span class="c r"></span><span class="c y"></span><span class="c g"></span><span class="filename">mcp.json</span></div>
          <div class="code-body">
{
  <span class="var">"mcpServers"</span>: {
    <span class="var">"weather"</span>: {
      <span class="var">"type"</span>: <span class="str">"stdio"</span>,
      <span class="var">"command"</span>: <span class="str">"/usr/bin/python"</span>,
      <span class="var">"args"</span>: [<span class="str">"weather.py"</span>]
    }
  }
}
          </div>
        </div>
      </div>
      <div>
        <div class="card">
          <h3>&#x1F3D7;&#xFE0F; Adapter Pattern</h3>
          <p>The <code>McpTool</code> wrapper makes MCP tools indistinguishable from local tools. The ToolRegistry, agent loop, and LLM don't know the difference.</p>
        </div>
        <div class="tip-box purple mt-16">
          <span>&#x1F4A1;</span>
          <div><strong>Same structure as Claude Code.</strong> The <code>mcp.json</code> format is identical to Claude Code's MCP config in <code>~/.claude/settings.json</code>.</div>
        </div>
      </div>
    </div>
  </div>
</section>
`);
