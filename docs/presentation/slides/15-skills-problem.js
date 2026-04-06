registerSlide(`
<section class="slide" data-title="skills-problem">
  <div class="slide-inner">
    <div class="section-label">Deferred Context</div>
    <h2 class="section-title">Skills: Load on Demand</h2>
    <p class="section-desc">Fixed system prompts waste tokens. Skills are menus the model sees but only loads when needed.</p>

    <div class="two-col mt-24">
      <div>
        <div class="card" style="border-left:3px solid var(--red);margin-bottom:12px">
          <h3>&#x274C; Eager Loading</h3>
          <p>21,000 tokens for all skills in every request. Most skills irrelevant. Dilutes model attention.</p>
          <span class="tag" style="background:rgba(220,38,38,.06);color:var(--red)">~21K tokens wasted</span>
        </div>
        <div class="card" style="border-left:3px solid var(--accent4)">
          <h3>&#x2705; Deferred Loading</h3>
          <p>~550 tokens for metadata only. Full instructions loaded on-demand via <code>activate_skill</code> tool.</p>
          <span class="tag" style="background:rgba(5,150,105,.06);color:var(--accent4)">~550 tokens (2%)</span>
        </div>
      </div>
      <div>
        <div class="arch-diagram">
          <div class="layer-label">System Prompt (~550 tokens)</div>
          <div style="margin-bottom:16px">
            <div class="node lead" style="font-size:13px;padding:8px 14px"><span class="dot-indicator"></span> code-reviewer</div>
            <div class="node lead" style="font-size:13px;padding:8px 14px;margin-left:8px"><span class="dot-indicator"></span> debugger</div>
          </div>
          <div class="layer-label">On Activation (~2,000 tokens each)</div>
          <div class="conn-row">
            <div class="node worker" style="font-size:12px;padding:8px 14px"><span class="dot-indicator"></span> activate_skill("code-reviewer")</div>
            <div class="conn-line blue" style="flex:0.3"></div>
            <div class="node sub" style="font-size:12px;padding:8px 14px"><span class="dot-indicator"></span> Full Instructions</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
`);
