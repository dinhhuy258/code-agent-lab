registerSlide(`
<section class="slide" data-title="motivation">
  <div class="slide-inner" style="overflow-y:hidden">
    <div class="section-label">Motivation</div>
    <h2 class="section-title">Why Build One?</h2>
    <p class="section-desc">Understanding agent internals transforms how you use and build AI-powered tools. Not about reinventing the wheel &mdash; it&rsquo;s about knowing the engine so you can drive better.</p>

    <!-- The Problem Space -->
    <div style="display:flex;align-items:center;gap:12px;margin:20px 0 14px">
      <span style="font-family:var(--mono);font-size:11px;font-weight:600;color:var(--text3);letter-spacing:2px;text-transform:uppercase">The Problem Space</span>
      <div style="flex:1;height:1px;background:var(--border)"></div>
      <span style="font-family:var(--mono);font-size:10px;color:var(--text3);background:var(--surface2);border:1px solid var(--border);border-radius:5px;padding:2px 8px">&#x2193; step through</span>
    </div>

    <!-- Problem cards — revealed one by one via keyboard -->
    <div style="display:flex;flex-direction:column;gap:10px">

      <div class="step-item" style="display:flex;align-items:stretch;gap:0;border-radius:14px;overflow:hidden;border:1px solid rgba(14,165,233,.2);background:var(--surface);box-shadow:var(--shadow-sm)">
        <div style="width:4px;background:var(--accent3);flex-shrink:0"></div>
        <div style="display:flex;align-items:center;gap:16px;padding:14px 18px;flex:1">
          <div style="width:44px;height:44px;border-radius:10px;background:rgba(14,165,233,.08);border:1px solid rgba(14,165,233,.15);display:flex;align-items:center;justify-content:center;font-size:22px;flex-shrink:0">&#x1F50D;</div>
          <div style="flex:1">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px">
              <span style="font-family:var(--mono);font-size:10px;font-weight:600;color:var(--accent3);letter-spacing:1px;text-transform:uppercase">Problem 01</span>
            </div>
            <div style="font-size:15.5px;font-weight:700;color:var(--text);margin-bottom:3px">LLMs are stateless</div>
            <div style="font-size:14px;color:var(--text2);line-height:1.55">They lose context between calls; we must manage conversation history</div>
          </div>
        </div>
      </div>

      <div class="step-item" style="display:flex;align-items:stretch;gap:0;border-radius:14px;overflow:hidden;border:1px solid rgba(234,88,12,.2);background:var(--surface);box-shadow:var(--shadow-sm)">
        <div style="width:4px;background:var(--orange);flex-shrink:0"></div>
        <div style="display:flex;align-items:center;gap:16px;padding:14px 18px;flex:1">
          <div style="width:44px;height:44px;border-radius:10px;background:rgba(234,88,12,.08);border:1px solid rgba(234,88,12,.15);display:flex;align-items:center;justify-content:center;font-size:22px;flex-shrink:0">&#x1F504;</div>
          <div style="flex:1">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px">
              <span style="font-family:var(--mono);font-size:10px;font-weight:600;color:var(--orange);letter-spacing:1px;text-transform:uppercase">Problem 02</span>
            </div>
            <div style="font-size:15.5px;font-weight:700;color:var(--text);margin-bottom:3px">ReAct pattern</div>
            <div style="font-size:14px;color:var(--text2);line-height:1.55">LLMs need a reason-then-act loop to solve multi-step problems</div>
          </div>
        </div>
      </div>

      <div class="step-item" style="display:flex;align-items:stretch;gap:0;border-radius:14px;overflow:hidden;border:1px solid rgba(124,58,237,.2);background:var(--surface);box-shadow:var(--shadow-sm)">
        <div style="width:4px;background:var(--accent);flex-shrink:0"></div>
        <div style="display:flex;align-items:center;gap:16px;padding:14px 18px;flex:1">
          <div style="width:44px;height:44px;border-radius:10px;background:rgba(124,58,237,.08);border:1px solid rgba(124,58,237,.15);display:flex;align-items:center;justify-content:center;font-size:22px;flex-shrink:0">&#x1FA9B;</div>
          <div style="flex:1">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px">
              <span style="font-family:var(--mono);font-size:10px;font-weight:600;color:var(--accent);letter-spacing:1px;text-transform:uppercase">Problem 03</span>
            </div>
            <div style="font-size:15.5px;font-weight:700;color:var(--text);margin-bottom:3px">Tool use</div>
            <div style="font-size:14px;color:var(--text2);line-height:1.55">LLMs can&rsquo;t read files or run commands alone; they need tool integrations</div>
          </div>
        </div>
      </div>

      <div class="step-item" style="display:flex;align-items:stretch;gap:0;border-radius:14px;overflow:hidden;border:1px solid rgba(219,39,119,.2);background:var(--surface);box-shadow:var(--shadow-sm)">
        <div style="width:4px;background:var(--pink);flex-shrink:0"></div>
        <div style="display:flex;align-items:center;gap:16px;padding:14px 18px;flex:1">
          <div style="width:44px;height:44px;border-radius:10px;background:rgba(219,39,119,.08);border:1px solid rgba(219,39,119,.15);display:flex;align-items:center;justify-content:center;font-size:22px;flex-shrink:0">&#x1F4E6;</div>
          <div style="flex:1">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px">
              <span style="font-family:var(--mono);font-size:10px;font-weight:600;color:var(--pink);letter-spacing:1px;text-transform:uppercase">Problem 04</span>
            </div>
            <div style="font-size:15.5px;font-weight:700;color:var(--text);margin-bottom:3px">Context management</div>
            <div style="font-size:14px;color:var(--text2);line-height:1.55">System prompts, history, and dynamic context shape agent behavior</div>
          </div>
        </div>
      </div>

    </div>
  </div>
</section>
`);
