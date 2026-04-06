registerSlide(`
<section class="slide" data-title="skills-problem">
  <div class="slide-inner">
    <div class="section-label">Skills System</div>
    <h2 class="section-title">Skills: Load on Demand</h2>
    <p class="section-desc">How do you give the model specialized knowledge <strong>without</strong> bloating every request?</p>

    <div class="two-col mt-24" style="align-items:stretch">
      <div style="display:flex;flex-direction:column">
        <div class="ctx-vis" style="flex:1">
          <div class="ctx-col">
            <div class="ctx-bar-wrap">
              <div class="ctx-segment system" style="height:15%"><div class="ctx-segment-label">System</div></div>
              <div class="ctx-segment" style="height:55%;background:rgba(220,38,38,.15)"><div class="ctx-segment-label">All Instructions<br>in Prompt</div></div>
              <div class="ctx-segment conversation" style="height:15%"><div class="ctx-segment-label">History</div></div>
            </div>
            <div class="ctx-label">Naive Approach<br><strong style="color:var(--red)">~21K wasted</strong></div>
          </div>

          <div class="ctx-vs">vs</div>

          <div class="ctx-col">
            <div class="ctx-bar-wrap">
              <div class="ctx-segment system" style="height:15%"><div class="ctx-segment-label">System</div></div>
              <div class="ctx-segment" style="height:5%;background:rgba(5,150,105,.15)"><div class="ctx-segment-label" style="font-size:8px">Menu</div></div>
              <div class="ctx-segment conversation" style="height:15%"><div class="ctx-segment-label">History</div></div>
            </div>
            <div class="ctx-label">Our Approach<br><strong style="color:var(--accent4)">~550 tokens</strong></div>
          </div>
        </div>
      </div>
      <div style="display:flex;flex-direction:column;gap:12px;justify-content:center">
        <div class="card" style="border-left:3px solid var(--red)">
          <h3>&#x274C; The Naive Way</h3>
          <p>Stuff all skill instructions into the system prompt. Most are irrelevant per request. <strong>~21K tokens wasted</strong>, model attention diluted.</p>
        </div>
        <div class="card" style="border-left:3px solid var(--accent4)">
          <h3>&#x2705; Our Design: Lazy Loading</h3>
          <p>System prompt only has <code>name</code> + <code>description</code>. Model calls <code>activate_skill</code> to load full instructions on demand &mdash; <strong>97% savings</strong>.</p>
        </div>
        <div class="card" style="border-left:3px solid var(--accent)">
          <h3>&#x1F9E0; Zero Overhead</h3>
          <p>If no skills exist in the workspace, <code>activate_skill</code> tool isn't even registered. No wasted schema tokens.</p>
        </div>
      </div>
    </div>
  </div>
</section>
`);
