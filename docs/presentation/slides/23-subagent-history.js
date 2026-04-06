registerSlide(`
<section class="slide" data-title="subagent-history">
  <div class="slide-inner">
    <div class="section-label">Data Flow</div>
    <h2 class="section-title">History Isolation</h2>
    <p class="section-desc">The sub-agent's entire history is created, used, and garbage-collected.</p>

    <div style="display:flex;align-items:center;gap:12px;margin:20px 0 14px">
      <div style="flex:1;height:1px;background:var(--border)"></div>
      <span style="font-family:var(--mono);font-size:10px;color:var(--text3);background:var(--surface2);border:1px solid var(--border);border-radius:5px;padding:2px 8px">&#x2193; step through the flow</span>
    </div>

    <!-- Sequential timeline diagram (full width) -->
    <div class="arch-diagram mt-24" style="padding:20px 24px;margin-bottom:0">
      <div style="display:flex;flex-direction:column;gap:0">

        <!-- 1. User request -->
        <div class="step-item" style="display:flex;gap:14px;align-items:flex-start;padding:10px 0;border-bottom:1px solid var(--border)">
          <div style="min-width:28px;text-align:center;font-family:var(--mono);font-size:13px;font-weight:700;color:var(--accent)">1</div>
          <div style="flex:1">
            <div style="background:rgba(124,58,237,.04);border:1px solid rgba(124,58,237,.12);border-radius:8px;padding:10px 14px;font-size:14px">
              <span style="font-family:var(--mono);font-size:12px;font-weight:600;color:var(--accent)">user</span>
              <div style="color:var(--text2);margin-top:3px">"find auth validation"</div>
            </div>
          </div>
        </div>

        <!-- 2. Model calls task -->
        <div class="step-item" style="display:flex;gap:14px;align-items:flex-start;padding:10px 0;border-bottom:1px solid var(--border)">
          <div style="min-width:28px;text-align:center;font-family:var(--mono);font-size:13px;font-weight:700;color:var(--accent)">2</div>
          <div style="flex:1">
            <div style="background:rgba(124,58,237,.04);border:1px solid rgba(124,58,237,.12);border-radius:8px;padding:10px 14px;font-size:14px">
              <span style="font-family:var(--mono);font-size:12px;font-weight:600;color:var(--accent)">model</span>
              <div style="color:var(--text2);margin-top:3px">call <span style="color:var(--accent);font-weight:600">task</span>(<span style="color:var(--text3)">"Search for token validation"</span>)</div>
            </div>
          </div>
        </div>

        <!-- 3-5. Sub-agent work (nested block) -->
        <div class="step-item" style="display:flex;gap:14px;align-items:flex-start;padding:10px 0;border-bottom:1px solid var(--border)">
          <div style="min-width:28px;text-align:center;font-family:var(--mono);font-size:13px;font-weight:700;color:var(--accent3)">3-5</div>
          <div style="flex:1">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px">
              <span style="font-family:var(--mono);font-size:12px;font-weight:700;color:var(--accent3);letter-spacing:.5px">SUB-AGENT SESSION</span>
              <div style="flex:1;height:1px;background:rgba(14,165,233,.15)"></div>
              <div style="display:inline-flex;align-items:center;gap:4px;background:rgba(220,38,38,.06);border:1px solid rgba(220,38,38,.15);border-radius:5px;padding:2px 8px">
                <span style="color:var(--red);font-size:12px">&#x1F5D1;</span>
                <span style="font-family:var(--mono);font-size:10px;font-weight:600;color:var(--red)">DISCARDED</span>
              </div>
            </div>
            <div style="border:1.5px dashed rgba(14,165,233,.2);border-radius:10px;padding:10px;display:flex;flex-direction:column;gap:5px">
              <div style="background:rgba(14,165,233,.04);border:1px solid rgba(14,165,233,.1);border-radius:6px;padding:8px 12px;font-size:13px">
                <span style="font-family:var(--mono);font-size:11px;font-weight:600;color:var(--accent3)">user</span>
                <span style="color:var(--text3);margin-left:8px">"Search for token validation"</span>
              </div>
              <div style="background:rgba(14,165,233,.04);border:1px solid rgba(14,165,233,.1);border-radius:6px;padding:8px 12px;font-size:13px">
                <span style="font-family:var(--mono);font-size:11px;font-weight:600;color:var(--accent3)">model</span>
                <span style="color:var(--text3);margin-left:8px">call grep_search(...) &rarr; <span style="opacity:.6">"auth.py:42"</span></span>
              </div>
              <div style="background:rgba(14,165,233,.04);border:1px solid rgba(14,165,233,.1);border-radius:6px;padding:8px 12px;font-size:13px">
                <span style="font-family:var(--mono);font-size:11px;font-weight:600;color:var(--accent3)">model</span>
                <span style="color:var(--text3);margin-left:8px">call read_file(...) &rarr; <span style="opacity:.6">"def validate_token..."</span></span>
              </div>
              <div style="background:rgba(14,165,233,.04);border:1px solid rgba(14,165,233,.1);border-radius:6px;padding:8px 12px;font-size:13px">
                <span style="font-family:var(--mono);font-size:11px;font-weight:600;color:var(--accent3)">model</span>
                <span style="color:var(--text3);margin-left:8px">call read_file(...) &rarr; <span style="opacity:.6">"class AuthMiddleware..."</span></span>
              </div>
              <div style="background:rgba(14,165,233,.06);border:1px solid rgba(14,165,233,.15);border-radius:6px;padding:8px 12px;font-size:13px">
                <span style="font-family:var(--mono);font-size:11px;font-weight:600;color:var(--accent3)">model</span>
                <span style="color:var(--accent3);margin-left:8px;font-weight:500">"Tokens validated at auth.py:42"</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 6. tool_result returns to main -->
        <div class="step-item" style="display:flex;gap:14px;align-items:flex-start;padding:10px 0;border-bottom:1px solid var(--border)">
          <div style="min-width:28px;text-align:center;font-family:var(--mono);font-size:13px;font-weight:700;color:var(--accent4)">6</div>
          <div style="flex:1">
            <div style="background:rgba(5,150,105,.04);border:1px solid rgba(5,150,105,.15);border-radius:8px;padding:10px 14px;font-size:14px">
              <span style="font-family:var(--mono);font-size:12px;font-weight:600;color:var(--accent4)">tool_result</span>
              <div style="color:var(--text2);margin-top:3px">"Task Finished: Tokens validated at auth.py:42"</div>
            </div>
          </div>
        </div>

        <!-- 7. Model responds -->
        <div class="step-item" style="display:flex;gap:14px;align-items:flex-start;padding:10px 0">
          <div style="min-width:28px;text-align:center;font-family:var(--mono);font-size:13px;font-weight:700;color:var(--accent)">7</div>
          <div style="flex:1">
            <div style="background:rgba(124,58,237,.04);border:1px solid rgba(124,58,237,.12);border-radius:8px;padding:10px 14px;font-size:14px">
              <span style="font-family:var(--mono);font-size:12px;font-weight:600;color:var(--accent)">model</span>
              <div style="color:var(--text2);margin-top:3px">"Found it at auth.py:42"</div>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</section>
`);
