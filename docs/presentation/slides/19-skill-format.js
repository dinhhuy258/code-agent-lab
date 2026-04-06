registerSlide(`
<section class="slide" data-title="skill-format">
  <div class="slide-inner">
    <div class="section-label">Skills System</div>
    <h2 class="section-title">The SKILL.md Format</h2>
    <p class="section-desc">One file, two sections: YAML frontmatter for the menu, Markdown body for full instructions.</p>

    <div style="display:grid;grid-template-columns:1fr 1fr;gap:24px;align-items:stretch;margin-top:24px">
      <div style="display:flex;flex-direction:column">
        <div class="code-block" style="flex:1;display:flex;flex-direction:column;margin:0">
          <div class="code-header"><span class="c r"></span><span class="c y"></span><span class="c g"></span><span class="filename">.code-agent/skills/hello/SKILL.md</span></div>
          <div class="code-body" style="flex:1">
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
      </div>
      <div style="display:flex;flex-direction:column;gap:12px;justify-content:center">
        <div class="card" style="border-left:3px solid var(--accent)">
          <h3>&#x1F3F7;&#xFE0F; Frontmatter &rarr; System Prompt</h3>
          <p><code>name</code> + <code>description</code> only. Goes into every request as an <code>&lt;available_skills&gt;</code> XML block. Fallback: directory name.</p>
        </div>
        <div class="card" style="border-left:3px solid var(--accent3)">
          <h3>&#x1F4DD; Body &rarr; On Activation</h3>
          <p>Full Markdown instructions. Only injected into conversation history when the model calls <code>activate_skill</code>.</p>
        </div>
        <div class="card" style="border-left:3px solid var(--accent4)">
          <h3>&#x1F4C1; Auto-Discovery</h3>
          <p><code>SkillManager</code> scans <code>.code-agent/skills/</code> at startup. Drop in a folder with SKILL.md &mdash; no registration needed.</p>
        </div>
      </div>
    </div>
  </div>
</section>
`);
