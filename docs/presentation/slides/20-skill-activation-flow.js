registerSlide(`
<section class="slide" data-title="skill-activation-flow">
  <div class="slide-inner">
    <div class="section-label">Skills System</div>
    <h2 class="section-title">Activation Flow</h2>
    <p class="section-desc">From file on disk to instructions in conversation &mdash; 4 phases, fully automatic.</p>

    <div style="display:flex;align-items:center;gap:12px;margin:20px 0 14px">
      <div style="flex:1;height:1px;background:var(--border)"></div>
      <span style="font-family:var(--mono);font-size:10px;color:var(--text3);background:var(--surface2);border:1px solid var(--border);border-radius:5px;padding:2px 8px">&#x2193; step through</span>
    </div>

    <div style="display:flex;flex-direction:column;gap:0;padding:0 8px">

      <!-- Phase 1: Discovery -->
      <div class="step-item" style="display:flex;gap:16px;padding:14px 0;border-bottom:1px solid var(--border)">
        <div style="display:flex;flex-direction:column;align-items:center;min-width:80px;padding-top:2px">
          <span style="font-family:var(--mono);font-size:10px;font-weight:700;color:var(--accent);letter-spacing:1px;text-transform:uppercase">Phase 1</span>
          <span style="font-size:11px;color:var(--text3);margin-top:2px">Startup</span>
        </div>
        <div style="flex:1">
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">
            <div class="node lead" style="font-size:13px;padding:6px 14px"><span class="dot-indicator"></span> SkillManager</div>
            <span style="color:var(--text3);font-size:18px">&rarr;</span>
            <span style="font-family:var(--mono);font-size:12px;color:var(--text2);background:var(--surface2);padding:4px 10px;border-radius:6px;border:1px solid var(--border)">.code-agent/skills/**/SKILL.md</span>
          </div>
          <span style="font-size:14px;color:var(--text2)">Scans workspace for SKILL.md files. Parses frontmatter &rarr; <code>SkillDefinition(name, description, body)</code></span>
        </div>
      </div>

      <!-- Phase 2: System Prompt -->
      <div class="step-item" style="display:flex;gap:16px;padding:14px 0;border-bottom:1px solid var(--border)">
        <div style="display:flex;flex-direction:column;align-items:center;min-width:80px;padding-top:2px">
          <span style="font-family:var(--mono);font-size:10px;font-weight:700;color:var(--accent3);letter-spacing:1px;text-transform:uppercase">Phase 2</span>
          <span style="font-size:11px;color:var(--text3);margin-top:2px">Prompt Build</span>
        </div>
        <div style="flex:1">
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">
            <div class="node worker" style="font-size:13px;padding:6px 14px"><span class="dot-indicator"></span> PromptProvider</div>
            <span style="color:var(--text3);font-size:18px">&rarr;</span>
            <span style="font-family:var(--mono);font-size:11px;color:var(--accent3);background:rgba(14,165,233,.06);padding:4px 10px;border-radius:6px;border:1px solid rgba(14,165,233,.12)">&lt;skill name="hello" description="..." /&gt;</span>
          </div>
          <span style="font-size:14px;color:var(--text2)">Appends lightweight XML to system instruction. Only <code>name</code> + <code>description</code> &mdash; body stays on disk.</span>
        </div>
      </div>

      <!-- Phase 3: LLM Decides -->
      <div class="step-item" style="display:flex;gap:16px;padding:14px 0;border-bottom:1px solid var(--border)">
        <div style="display:flex;flex-direction:column;align-items:center;min-width:80px;padding-top:2px">
          <span style="font-family:var(--mono);font-size:10px;font-weight:700;color:var(--accent4);letter-spacing:1px;text-transform:uppercase">Phase 3</span>
          <span style="font-size:11px;color:var(--text3);margin-top:2px">Tool Call</span>
        </div>
        <div style="flex:1">
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">
            <div class="node" style="font-size:13px;padding:6px 14px;background:rgba(234,88,12,.06);border-color:rgba(234,88,12,.2);color:var(--orange)"><span class="dot-indicator" style="background:var(--orange)"></span> LLM</div>
            <span style="color:var(--text3);font-size:18px">&rarr;</span>
            <span style="font-family:var(--mono);font-size:12px;color:var(--text2);background:var(--surface2);padding:4px 10px;border-radius:6px;border:1px solid var(--border)">activate_skill("hello")</span>
          </div>
          <span style="font-size:14px;color:var(--text2)">Model sees the menu, decides it needs this skill, and calls the tool. <strong>The model decides when</strong> &mdash; not us.</span>
        </div>
      </div>

      <!-- Phase 4: Injection -->
      <div class="step-item" style="display:flex;gap:16px;padding:14px 0;border-bottom:1px solid var(--border)">
        <div style="display:flex;flex-direction:column;align-items:center;min-width:80px;padding-top:2px">
          <span style="font-family:var(--mono);font-size:10px;font-weight:700;color:var(--pink);letter-spacing:1px;text-transform:uppercase">Phase 4</span>
          <span style="font-size:11px;color:var(--text3);margin-top:2px">Injection</span>
        </div>
        <div style="flex:1">
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">
            <div class="node sub" style="font-size:13px;padding:6px 14px"><span class="dot-indicator"></span> ActivateSkillTool</div>
            <span style="color:var(--text3);font-size:18px">&rarr;</span>
            <span style="font-family:var(--mono);font-size:11px;color:var(--accent4);background:rgba(5,150,105,.06);padding:4px 10px;border-radius:6px;border:1px solid rgba(5,150,105,.12)">&lt;activated_skill&gt; full body &lt;/&gt;</span>
          </div>
          <span style="font-size:14px;color:var(--text2)">Full instructions returned as <code>function_response</code>. Now in conversation history &mdash; active for the rest of the session.</span>
        </div>
      </div>

      <!-- Summary -->
      <div class="step-item" style="padding:14px 0">
        <div class="card" style="border-left:3px solid var(--accent);margin:0">
          <h3>&#x1F3AF; Result: ~550 tokens until needed, ~2K when activated</h3>
          <p>The model sees what's available (cheap), loads what it needs (on demand), and keeps it for the rest of the conversation (persistent). No eager waste.</p>
        </div>
      </div>

    </div>
  </div>
</section>
`);
