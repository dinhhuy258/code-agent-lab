registerSlide(`
<section class="slide" data-title="four-layers">
  <div class="slide-inner">
    <div class="section-label">Architecture</div>
    <h2 class="section-title">Four-Layer Stack</h2>
    <p class="section-desc">Each layer has a single responsibility and can evolve independently.</p>

    <div style="display:flex;align-items:center;gap:12px;margin:20px 0 14px">
      <div style="flex:1;height:1px;background:var(--border)"></div>
      <span style="font-family:var(--mono);font-size:10px;color:var(--text3);background:var(--surface2);border:1px solid var(--border);border-radius:5px;padding:2px 8px">&#x2193; step through</span>
    </div>

    <div class="arch-diagram mt-24" style="display:flex;flex-direction:column;gap:0;padding:20px">

      <div class="step-item" style="display:flex;align-items:center;gap:12px;padding:12px 0;border-bottom:1px solid var(--border)">
        <span style="font-family:var(--mono);font-size:10px;font-weight:600;color:var(--accent);letter-spacing:1px;text-transform:uppercase;min-width:80px">Layer 4</span>
        <div class="node lead" style="flex-shrink:0"><span class="dot-indicator"></span> AgentClient</div>
        <span style="color:var(--text3);font-size:13px;flex:1">The agent loop. Decides when to stop.</span>
        <span style="font-family:var(--mono);font-size:10px;color:var(--text3);background:rgba(124,58,237,.06);border:1px solid rgba(124,58,237,.12);border-radius:5px;padding:2px 8px;white-space:nowrap">Orchestrator</span>
      </div>

      <div class="step-item" style="display:flex;align-items:center;gap:12px;padding:12px 0;border-bottom:1px solid var(--border)">
        <span style="font-family:var(--mono);font-size:10px;font-weight:600;color:var(--accent3);letter-spacing:1px;text-transform:uppercase;min-width:80px">Layer 3</span>
        <div class="node worker" style="flex-shrink:0"><span class="dot-indicator"></span> ChatSession</div>
        <span style="color:var(--text3);font-size:13px;flex:1">Maintains conversation history. Appends messages.</span>
        <span style="font-family:var(--mono);font-size:10px;color:var(--text3);background:rgba(14,165,233,.06);border:1px solid rgba(14,165,233,.12);border-radius:5px;padding:2px 8px;white-space:nowrap">History Manager</span>
      </div>

      <div class="step-item" style="display:flex;align-items:center;gap:12px;padding:12px 0;border-bottom:1px solid var(--border)">
        <span style="font-family:var(--mono);font-size:10px;font-weight:600;color:var(--accent3);letter-spacing:1px;text-transform:uppercase;min-width:80px">Layer 2</span>
        <div class="node worker" style="flex-shrink:0"><span class="dot-indicator"></span> Turn</div>
        <span style="color:var(--text3);font-size:13px;flex:1">Single request/response cycle. Extracts tool calls.</span>
        <span style="font-family:var(--mono);font-size:10px;color:var(--text3);background:rgba(14,165,233,.06);border:1px solid rgba(14,165,233,.12);border-radius:5px;padding:2px 8px;white-space:nowrap">Turn</span>
      </div>

      <div class="step-item" style="display:flex;align-items:center;gap:12px;padding:12px 0">
        <span style="font-family:var(--mono);font-size:10px;font-weight:600;color:var(--accent4);letter-spacing:1px;text-transform:uppercase;min-width:80px">Layer 1</span>
        <div class="node sub" style="flex-shrink:0"><span class="dot-indicator"></span> GeminiLLMClient</div>
        <span style="color:var(--text3);font-size:13px;flex:1">Talks to the API. Handles auth, errors, streaming.</span>
        <span style="font-family:var(--mono);font-size:10px;color:var(--text3);background:rgba(5,150,105,.06);border:1px solid rgba(5,150,105,.12);border-radius:5px;padding:2px 8px;white-space:nowrap">LLM Client</span>
      </div>

    </div>
  </div>
</section>
`);
