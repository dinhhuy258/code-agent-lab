registerSlide(`
<section class="slide" data-title="skill-format">
  <div class="slide-inner">
    <div class="section-label">Implementation</div>
    <h2 class="section-title">The SKILL.md Format</h2>
    <p class="section-desc">YAML frontmatter for metadata, Markdown body for full instructions.</p>

    <div class="two-col mt-24">
      <div>
        <div class="code-block">
          <div class="code-header"><span class="c r"></span><span class="c y"></span><span class="c g"></span><span class="filename">.code-agent/skills/hello/SKILL.md</span></div>
          <div class="code-body">
<span class="cm">---</span>
<span class="var">name</span>: <span class="str">hello</span>
<span class="var">description</span>: <span class="str">Triggers when the user says hello</span>
<span class="cm">---</span>

<span class="cm"># Hello Skill</span>

<span class="num">1.</span> When activated, greet the user warmly
<span class="num">2.</span> Locate the full path of the
   <span class="fn">\`debug_client.py\`</span> file
<span class="num">3.</span> Read and summarize its contents
          </div>
        </div>
        <div class="tip-box green mt-16">
          <span>&#x1F4C1;</span>
          <div><strong>Discovery:</strong> Skills are auto-discovered from <code>.code-agent/skills/</code> at startup. No registration needed.</div>
        </div>
      </div>
      <div>
        <div class="card" style="margin-bottom:12px">
          <h3>&#x1F3F7;&#xFE0F; Frontmatter (metadata)</h3>
          <p><code>name</code> + <code>description</code> only. This goes into the system prompt. Fallback: directory name if missing.</p>
        </div>
        <div class="card" style="margin-bottom:12px">
          <h3>&#x1F4DD; Body (instructions)</h3>
          <p>Full detailed instructions. Only injected into conversation when <code>activate_skill</code> is called.</p>
        </div>
        <div class="card">
          <h3>&#x2699;&#xFE0F; Wiring</h3>
          <p><code>SkillManager</code> discovers &rarr; <code>ActivateSkillTool</code> registered if skills exist &rarr; zero overhead when unused.</p>
        </div>
      </div>
    </div>
  </div>
</section>
`);
