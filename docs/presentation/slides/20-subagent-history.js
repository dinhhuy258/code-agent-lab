registerSlide(`
<section class="slide" data-title="subagent-history">
  <div class="slide-inner">
    <div class="section-label">Data Flow</div>
    <h2 class="section-title">History Isolation</h2>
    <p class="section-desc">The sub-agent's entire history is created, used, and garbage-collected.</p>

    <div class="two-col mt-24">
      <div>
        <div class="code-block">
          <div class="code-header"><span class="c r"></span><span class="c y"></span><span class="c g"></span><span class="filename">Main conversation history</span></div>
          <div class="code-body">
<span class="cm">[user]</span> <span class="str">"find auth validation"</span>

<span class="cm">[model]</span> call <span class="fn">task</span>(
    prompt=<span class="str">"Search for token validation"</span>
)

<span class="cm">[user]</span> tool_result: <span class="str">"Task Finished:
  Tokens validated at auth.py:42"</span>

<span class="cm">[model]</span> <span class="str">"Found it at auth.py:42"</span>
          </div>
        </div>
        <div class="tip-box green mt-16">
          <span>&#x2728;</span>
          <div>Main context stays clean. Only the <strong>summary</strong> comes back &mdash; not the 5 file reads and 3 greps the sub-agent did.</div>
        </div>
      </div>
      <div>
        <div class="code-block">
          <div class="code-header"><span class="c r"></span><span class="c y"></span><span class="c g"></span><span class="filename">Sub-agent history (discarded)</span></div>
          <div class="code-body">
<span class="cm">[user]</span> <span class="str">"Search for token validation"</span>

<span class="cm">[model]</span> call <span class="fn">grep_search</span>(...)
<span class="cm">[user]</span> function_response: <span class="str">"auth.py:42"</span>

<span class="cm">[model]</span> call <span class="fn">read_file</span>(...)
<span class="cm">[user]</span> function_response: <span class="str">"def validate..."</span>

<span class="cm">[model]</span> <span class="str">"Tokens validated in
  src/auth.py:42 via validate_token()"</span>

<span class="op">^ entire history discarded</span>
          </div>
        </div>
        <div class="card mt-16" style="border-left:3px solid var(--accent3)">
          <h3>&#x1F4CA; Impact</h3>
          <p>Same work in main context: <strong>+70K tokens</strong>. Via sub-agent: <strong>35K main + isolated 20K</strong>. Context shrinks 52%.</p>
        </div>
      </div>
    </div>
  </div>
</section>
`);
