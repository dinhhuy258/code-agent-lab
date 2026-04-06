registerSlide(`
<section class="slide" data-title="skills-vs-agents">
  <div class="slide-inner">
    <div class="section-label">Comparison</div>
    <h2 class="section-title">Skills vs Sub-Agents</h2>
    <p class="section-desc">Both are tool calls underneath, but they solve different problems.</p>

    <table class="cmp-table mt-24">
      <thead>
        <tr><th>Aspect</th><th>Skill</th><th>Sub-Agent</th></tr>
      </thead>
      <tbody>
        <tr><td>Provides</td><td>Instructions (context)</td><td>Execution (worker)</td></tr>
        <tr><td>Runs in</td><td>Same conversation</td><td>Isolated session</td></tr>
        <tr><td>Context effect</td><td style="color:var(--orange)">Adds tokens to main</td><td style="color:var(--accent4)">Keeps tokens out of main</td></tr>
        <tr><td>Changes</td><td>How the model works</td><td>What the model does</td></tr>
        <tr><td>Persistence</td><td>Active for rest of conversation</td><td>Gone after task completes</td></tr>
        <tr><td>Best for</td><td>Specialized knowledge &amp; workflows</td><td>Heavy multi-step operations</td></tr>
      </tbody>
    </table>

    <div class="tip-box purple mt-16">
      <span>&#x1F91D;</span>
      <div><strong>They compose well:</strong> Activate a code-reviewer skill, then spawn a sub-agent to search for changed files before reviewing. Context stays clean.</div>
    </div>
  </div>
</section>
`);
