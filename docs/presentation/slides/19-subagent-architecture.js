registerSlide(`
<section class="slide" data-title="subagent-architecture">
  <div class="slide-inner">
    <div class="section-label">Architecture</div>
    <h2 class="section-title">Isolated Sessions</h2>
    <p class="section-desc">Same LLM, same tools, different conversation &mdash; the key insight.</p>

    <div class="two-col mt-24">
      <div>
        <div class="arch-diagram">
          <div class="layer-label">Main Conversation</div>
          <div style="margin-bottom:16px">
            <div class="node lead"><span class="dot-indicator"></span> AgentClient + ChatSession A</div>
          </div>

          <div class="conn-row" style="margin:8px 0">
            <span style="font-size:11px;color:var(--text3);font-family:var(--mono)">calls task() tool</span>
            <div class="conn-line purple" style="flex:0.5"></div>
          </div>

          <div class="layer-label">Sub-Agent (Isolated)</div>
          <div style="margin-bottom:12px">
            <div class="node worker"><span class="dot-indicator"></span> SubagentRunner + ChatSession B</div>
          </div>

          <div class="conn-row" style="margin:8px 0">
            <span style="font-size:11px;color:var(--text3);font-family:var(--mono)">returns summary</span>
            <div class="conn-line green" style="flex:0.5"></div>
          </div>

          <div class="layer-label">Back to Main</div>
          <div>
            <div class="node lead"><span class="dot-indicator"></span> Continues with clean context</div>
          </div>
        </div>
      </div>
      <div>
        <table class="cmp-table">
          <thead><tr><th>Component</th><th>Shared?</th></tr></thead>
          <tbody>
            <tr><td>ChatSession</td><td style="color:var(--red)">&#x274C; Isolated (new instance)</td></tr>
            <tr><td>LLMClient</td><td style="color:var(--accent4)">&#x2714; Shared</td></tr>
            <tr><td>ToolRegistry</td><td style="color:var(--accent4)">&#x2714; Shared</td></tr>
            <tr><td>System Prompt</td><td style="color:var(--orange)">&#x1F504; Different per type</td></tr>
            <tr><td>Max Turns</td><td>15 (vs 25 for main)</td></tr>
            <tr><td>Nesting</td><td style="color:var(--red)">&#x274C; Depth 1 only</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</section>
`);
