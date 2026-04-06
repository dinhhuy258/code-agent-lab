registerSlide(`
<section class="slide" data-title="four-layers">
  <div class="slide-inner">
    <div class="section-label">Architecture</div>
    <h2 class="section-title">Four-Layer Stack</h2>
    <p class="section-desc">Each layer has a single responsibility and can evolve independently.</p>

    <div class="arch-diagram mt-24">
      <div class="layer-label">Layer 4 — Orchestrator</div>
      <div style="display:flex;gap:12px;margin-bottom:20px;flex-wrap:wrap">
        <div class="node lead"><span class="dot-indicator"></span> AgentClient</div>
        <span style="color:var(--text3);font-size:13px;align-self:center">The agent loop. Decides when to stop.</span>
      </div>

      <div class="layer-label">Layer 3 — History Manager</div>
      <div style="display:flex;gap:12px;margin-bottom:20px;flex-wrap:wrap">
        <div class="node worker"><span class="dot-indicator"></span> ChatSession</div>
        <span style="color:var(--text3);font-size:13px;align-self:center">Maintains conversation history. Appends messages.</span>
      </div>

      <div class="layer-label">Layer 2 — Turn</div>
      <div style="display:flex;gap:12px;margin-bottom:20px;flex-wrap:wrap">
        <div class="node worker"><span class="dot-indicator"></span> Turn</div>
        <span style="color:var(--text3);font-size:13px;align-self:center">Single request/response cycle. Extracts tool calls.</span>
      </div>

      <div class="layer-label">Layer 1 — LLM Client</div>
      <div style="display:flex;gap:12px;flex-wrap:wrap">
        <div class="node sub"><span class="dot-indicator"></span> GeminiLLMClient</div>
        <span style="color:var(--text3);font-size:13px;align-self:center">Talks to the API. Handles auth, errors, streaming.</span>
      </div>
    </div>

    <div class="tip-box green">
      <span>&#x1F3D7;&#xFE0F;</span>
      <div><strong>Why layers?</strong> New features just "fill in" existing layers. Adding streaming didn't require rewriting the agent loop. Adding sub-agents didn't change the tool system.</div>
    </div>
  </div>
</section>
`);
