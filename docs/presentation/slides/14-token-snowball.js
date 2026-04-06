registerSlide(`
<section class="slide" data-title="token-snowball">
  <div class="slide-inner">
    <div class="section-label">The Hidden Challenge</div>
    <h2 class="section-title">The Token Snowball</h2>
    <p class="section-desc">The API is stateless. Every turn resends the <strong>entire</strong> conversation history. Cost grows quadratically.</p>

    <div class="two-col mt-24" style="align-items:stretch">
      <div style="display:flex;flex-direction:column">
        <div class="token-calc" style="flex:1;display:flex;flex-direction:column;justify-content:center">
          <h4 style="font-size:14px;font-weight:700;margin-bottom:12px">Token Growth Per Turn</h4>
          <div class="tc-bar">
            <div class="bar-label">Turn 1</div>
            <div class="bar-track"><div class="bar-fill" style="width:18%;background:var(--accent4)"></div></div>
            <div class="bar-val" style="color:var(--accent4)">36K</div>
          </div>
          <div class="tc-bar">
            <div class="bar-label">Turn 5</div>
            <div class="bar-track"><div class="bar-fill" style="width:23%;background:var(--accent3)"></div></div>
            <div class="bar-val" style="color:var(--accent3)">44K</div>
          </div>
          <div class="tc-bar">
            <div class="bar-label">Turn 10</div>
            <div class="bar-track"><div class="bar-fill" style="width:27%;background:var(--orange)"></div></div>
            <div class="bar-val" style="color:var(--orange)">52K</div>
          </div>
          <div class="tc-bar">
            <div class="bar-label">Turn 30</div>
            <div class="bar-track"><div class="bar-fill" style="width:95%;background:var(--red)"></div></div>
            <div class="bar-val" style="color:var(--red)">190K</div>
          </div>
        </div>
      </div>
      <div style="display:flex;flex-direction:column;justify-content:center">
        <div class="card" style="margin-bottom:12px;border-left:3px solid var(--red)">
          <h3>&#x1F4C8; Quadratic Cost</h3>
          <p>Total tokens &asymp; N &times; fixed + N(N+1)/2 &times; delta. 30 turns = <strong>56x</strong> the cost of turn 1.</p>
        </div>
        <div class="card" style="border-left:3px solid var(--orange)">
          <h3>&#x1F4A8; Context Pollution</h3>
          <p>1 file read = 5K tokens <strong>permanently</strong> stuck in history. 10 reads = 50K resent every turn.</p>
        </div>
      </div>
    </div>
  </div>
</section>
`);
