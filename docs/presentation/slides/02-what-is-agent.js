registerSlide(`
<section class="slide" data-title="what-is-agent">
  <div class="slide-inner" style="overflow-y:hidden">
    <div class="section-label">Foundation</div>
    <h2 class="section-title" style="margin-bottom:4px">What is an Agent?</h2>

    <div style="display:grid;grid-template-columns:1fr auto 1fr;gap:16px;align-items:stretch;margin-top:10px">
      <!-- Chatbot Card -->
      <div class="card anim-fade" style="padding:12px 16px;display:flex;flex-direction:column;opacity:0;transform:translateY(20px);transition:opacity .5s cubic-bezier(.16,1,.3,1),transform .5s cubic-bezier(.16,1,.3,1)">
        <h3>&#x1F4AC; Chatbot</h3>
        <ul style="color:var(--text2);font-size:14.5px;line-height:1.65;margin:8px 0 8px 18px;flex:1">
          <li>Text in, text out</li>
          <li>No tools, no file access</li>
          <li>Cannot take actions on its own</li>
        </ul>
        <span class="tag" style="background:var(--surface2);color:var(--text3);align-self:flex-start">Stateless</span>
      </div>

      <!-- Middle: Arrow + capabilities -->
      <div class="anim-fade" style="display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;opacity:0;transform:translateY(20px);transition:opacity .5s cubic-bezier(.16,1,.3,1) .15s,transform .5s cubic-bezier(.16,1,.3,1) .15s">
        <span style="font-size:22px;color:var(--text3)">&#x27F6;</span>
        <div style="display:flex;flex-direction:column;align-items:center;gap:8px">
          <span style="display:inline-flex;align-items:center;gap:6px;padding:6px 14px;border-radius:10px;background:rgba(14,165,233,.08);border:1px solid rgba(14,165,233,.15);color:var(--accent3);font-size:13px;font-weight:600;font-family:var(--sans)">&#x1F527; Tools</span>
          <span style="display:inline-flex;align-items:center;gap:6px;padding:6px 14px;border-radius:10px;background:rgba(234,88,12,.08);border:1px solid rgba(234,88,12,.15);color:var(--orange);font-size:13px;font-weight:600;font-family:var(--sans)">&#x1F504; ReAct Loop</span>
        </div>
        <span style="font-size:9px;font-family:var(--mono);color:var(--text3);letter-spacing:1px;text-transform:uppercase">Add Capabilities</span>
      </div>

      <!-- Agent Card -->
      <div class="card anim-fade" style="padding:12px 16px;display:flex;flex-direction:column;border-color:rgba(124,58,237,.2);background:rgba(124,58,237,.02);opacity:0;transform:translateY(20px);transition:opacity .5s cubic-bezier(.16,1,.3,1) .3s,transform .5s cubic-bezier(.16,1,.3,1) .3s">
        <h3 style="color:var(--accent)">&#x1F916; Agent</h3>
        <ul style="color:var(--text2);font-size:14.5px;line-height:1.65;margin:8px 0 8px 18px;flex:1">
          <li>Reads files, runs commands</li>
          <li>Reasons about results</li>
          <li>Iterates until task is done</li>
          <li>Multi-step autonomy</li>
        </ul>
        <span class="tag" style="background:rgba(124,58,237,.06);color:var(--accent);align-self:flex-start">Autonomous</span>
      </div>
    </div>

    <!-- Formula bar -->
    <div class="anim-fade" style="background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:10px 24px;margin-top:10px;text-align:center;font-size:15px;font-weight:600;opacity:0;transform:translateY(20px);transition:opacity .5s cubic-bezier(.16,1,.3,1) .45s,transform .5s cubic-bezier(.16,1,.3,1) .45s">
      Chatbot &nbsp;<span style="color:var(--text3)">+</span>&nbsp; <span style="color:var(--accent3)">Tools</span> &nbsp;<span style="color:var(--text3)">+</span>&nbsp; <span style="color:var(--orange)">ReAct Loop</span> &nbsp;<span style="color:var(--text3)">=</span>&nbsp; <span style="color:var(--accent)">Agent</span>
    </div>

    <!-- Key insight -->
    <div class="tip-box purple anim-fade" style="margin:8px 0 0;opacity:0;transform:translateY(20px);transition:opacity .5s cubic-bezier(.16,1,.3,1) .6s,transform .5s cubic-bezier(.16,1,.3,1) .6s">
      <span>&#x1F4A1;</span>
      <div><strong>Key insight:</strong> An agent is not a smarter model &mdash; it&rsquo;s a <strong>chatbot given tools and a loop</strong>. The ReAct pattern (Reason &rarr; Act &rarr; Observe &rarr; Repeat) is what turns a stateless LLM into an autonomous worker.</div>
    </div>
  </div>
</section>
`);
