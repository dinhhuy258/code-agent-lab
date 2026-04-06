registerSlide(`
<section class="slide" data-title="subagent-architecture">
  <div class="slide-inner">
    <div class="section-label">Architecture</div>
    <h2 class="section-title">Isolated Sessions</h2>
    <p class="section-desc">A sub-agent is just a <strong>tool</strong> &mdash; same LLM, same tools, different conversation.</p>

    <div class="tip-box purple mt-24" style="margin-bottom:24px">
      <span>&#x1F527;</span>
      <div style="font-size:14px"><strong>Sub-agent = Tool.</strong> The LLM calls <code>task()</code> like any other tool. The framework spawns an isolated ReAct loop, runs it to completion, and returns the result as a <code>function_response</code>.</div>
    </div>

    <!-- Component diagram: shared vs isolated -->
    <div class="arch-diagram" style="padding:24px;margin:0">
      <div style="display:flex;gap:20px;align-items:stretch">

        <!-- Main Agent -->
        <div style="flex:1;background:rgba(124,58,237,.03);border:1.5px solid rgba(124,58,237,.15);border-radius:12px;padding:16px">
          <div style="font-family:var(--mono);font-size:12px;font-weight:700;color:var(--accent);letter-spacing:1px;text-transform:uppercase;margin-bottom:14px">Main Agent</div>
          <div style="display:flex;flex-direction:column;gap:8px">
            <div class="node lead" style="font-size:13px;padding:8px 14px;width:100%;justify-content:center"><span class="dot-indicator"></span> ChatSession A</div>
            <div style="font-size:13px;color:var(--text2);text-align:center;padding:4px 0">system prompt + full history</div>
          </div>
        </div>

        <!-- Shared center -->
        <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;min-width:140px;gap:10px">
          <div style="font-family:var(--mono);font-size:11px;font-weight:700;color:var(--accent4);letter-spacing:1px;text-transform:uppercase;margin-bottom:4px">Shared</div>
          <div style="background:rgba(5,150,105,.04);border:1.5px solid rgba(5,150,105,.15);border-radius:10px;padding:10px 16px;text-align:center;width:100%">
            <div style="font-family:var(--mono);font-size:12px;font-weight:600;color:var(--accent4)">LLMClient</div>
            <div style="font-size:11px;color:var(--text3);margin-top:2px">same API connection</div>
          </div>
          <div style="background:rgba(5,150,105,.04);border:1.5px solid rgba(5,150,105,.15);border-radius:10px;padding:10px 16px;text-align:center;width:100%">
            <div style="font-family:var(--mono);font-size:12px;font-weight:600;color:var(--accent4)">ToolRegistry</div>
            <div style="font-size:11px;color:var(--text3);margin-top:2px">same tool set</div>
          </div>
          <div style="display:flex;align-items:center;gap:6px;margin-top:4px">
            <div style="width:40px;height:2px;background:linear-gradient(90deg,var(--accent),transparent)"></div>
            <span style="font-family:var(--mono);font-size:10px;color:var(--text3)">wired to both</span>
            <div style="width:40px;height:2px;background:linear-gradient(270deg,var(--accent3),transparent)"></div>
          </div>
        </div>

        <!-- Sub-Agent -->
        <div style="flex:1;background:rgba(14,165,233,.03);border:1.5px dashed rgba(14,165,233,.2);border-radius:12px;padding:16px">
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px">
            <div style="font-family:var(--mono);font-size:12px;font-weight:700;color:var(--accent3);letter-spacing:1px;text-transform:uppercase">Sub-Agent</div>
            <div style="display:inline-flex;align-items:center;gap:4px;background:rgba(220,38,38,.06);border:1px solid rgba(220,38,38,.15);border-radius:5px;padding:2px 8px">
              <span style="font-family:var(--mono);font-size:10px;font-weight:600;color:var(--red)">ISOLATED</span>
            </div>
          </div>
          <div style="display:flex;flex-direction:column;gap:8px">
            <div class="node worker" style="font-size:13px;padding:8px 14px;width:100%;justify-content:center"><span class="dot-indicator"></span> ChatSession B</div>
            <div style="font-size:13px;color:var(--text2);text-align:center;padding:4px 0">different prompt + empty history</div>
          </div>
        </div>

      </div>

      <!-- Key differences row -->
      <div style="display:flex;gap:12px;margin-top:18px;flex-wrap:wrap">
        <div style="flex:1;min-width:140px;background:var(--surface2);border-radius:8px;padding:10px 14px;text-align:center">
          <div style="font-family:var(--mono);font-size:11px;font-weight:600;color:var(--orange)">System Prompt</div>
          <div style="font-size:13px;color:var(--text2);margin-top:4px">Different per type</div>
        </div>
        <div style="flex:1;min-width:140px;background:var(--surface2);border-radius:8px;padding:10px 14px;text-align:center">
          <div style="font-family:var(--mono);font-size:11px;font-weight:600;color:var(--orange)">History</div>
          <div style="font-size:13px;color:var(--text2);margin-top:4px">Fresh &amp; garbage-collected</div>
        </div>
        <div style="flex:1;min-width:140px;background:var(--surface2);border-radius:8px;padding:10px 14px;text-align:center">
          <div style="font-family:var(--mono);font-size:11px;font-weight:600;color:var(--orange)">Max Turns</div>
          <div style="font-size:13px;color:var(--text2);margin-top:4px">15 (vs 25 for main)</div>
        </div>
        <div style="flex:1;min-width:140px;background:var(--surface2);border-radius:8px;padding:10px 14px;text-align:center">
          <div style="font-family:var(--mono);font-size:11px;font-weight:600;color:var(--orange)">Nesting</div>
          <div style="font-size:13px;color:var(--text2);margin-top:4px">Depth 1 only</div>
        </div>
      </div>
    </div>

    <div class="tip-box green mt-16">
      <span>&#x1F4A1;</span>
      <div style="font-size:14px">From the LLM's perspective, <code>task()</code> is no different from <code>read_file()</code> &mdash; call it, get a result. The isolation is invisible to the caller.</div>
    </div>
  </div>
</section>
`);
