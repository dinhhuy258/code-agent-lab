registerSlide(`
<section class="slide" data-title="subagent-implementation">
  <div class="slide-inner">
    <div class="section-label">Sub-Agents</div>
    <h2 class="section-title">Implementation</h2>
    <p class="section-desc">Three components wire together to create isolated sub-agents.</p>

    <div style="display:flex;align-items:center;gap:12px;margin:20px 0 14px">
      <div style="flex:1;height:1px;background:var(--border)"></div>
      <span style="font-family:var(--mono);font-size:10px;color:var(--text3);background:var(--surface2);border:1px solid var(--border);border-radius:5px;padding:2px 8px">&#x2193; step through</span>
    </div>

    <div class="arch-diagram" style="padding:24px;margin:0">
      <div style="display:flex;flex-direction:column;gap:0">

        <!-- Row 1: Three components -->
        <div class="step-item" style="padding-bottom:16px;border-bottom:1px solid var(--border)">
          <div style="display:flex;gap:16px;flex-wrap:wrap">
            <!-- TaskTool -->
            <div style="flex:1;min-width:200px;background:rgba(124,58,237,.04);border:1.5px solid rgba(124,58,237,.15);border-radius:12px;padding:14px 16px">
              <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px">
                <div class="node lead" style="font-size:12px;padding:4px 10px"><span class="dot-indicator"></span> TaskTool</div>
                <span style="font-family:var(--mono);font-size:11px;color:var(--text3)">tools/task.py</span>
              </div>
              <div style="font-size:13px;color:var(--text2);line-height:1.5">
                The <strong>tool</strong> the LLM calls. Receives <code style="font-size:12px">prompt</code> + <code style="font-size:12px">subagent_type</code>, orchestrates everything, returns <code style="font-size:12px">ToolResult</code>.
              </div>
            </div>
            <!-- SubagentRunner -->
            <div style="flex:1;min-width:200px;background:rgba(14,165,233,.04);border:1.5px solid rgba(14,165,233,.15);border-radius:12px;padding:14px 16px">
              <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px">
                <div class="node worker" style="font-size:12px;padding:4px 10px"><span class="dot-indicator"></span> SubagentRunner</div>
                <span style="font-family:var(--mono);font-size:11px;color:var(--text3)">agents/subagent_runner.py</span>
              </div>
              <div style="font-size:13px;color:var(--text2);line-height:1.5">
                The isolated <strong>ReAct loop</strong>. Sends prompt to LLM, executes tool calls, loops until text response. Returns a <code style="font-size:12px">string</code>.
              </div>
            </div>
            <!-- SubagentManager -->
            <div style="flex:1;min-width:200px;background:rgba(5,150,105,.04);border:1.5px solid rgba(5,150,105,.15);border-radius:12px;padding:14px 16px">
              <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px">
                <div class="node sub" style="font-size:12px;padding:4px 10px"><span class="dot-indicator"></span> SubagentManager</div>
                <span style="font-family:var(--mono);font-size:11px;color:var(--text3)">agents/subagent_manager.py</span>
              </div>
              <div style="font-size:13px;color:var(--text2);line-height:1.5">
                <strong>Prompt registry</strong>. Maps <code style="font-size:12px">subagent_type</code> &rarr; system prompt. Each type gets specialized instructions.
              </div>
            </div>
          </div>
        </div>

        <!-- Row 2: Wiring flow -->
        <div class="step-item" style="padding:16px 0;border-bottom:1px solid var(--border)">
          <div style="font-family:var(--mono);font-size:11px;font-weight:700;color:var(--text2);letter-spacing:1px;text-transform:uppercase;margin-bottom:12px">How they wire together</div>
          <div style="display:flex;align-items:stretch;gap:0">

            <!-- Step A -->
            <div style="flex:1;padding:10px 14px;background:rgba(124,58,237,.03);border:1px solid rgba(124,58,237,.1);border-radius:10px 0 0 10px">
              <div style="font-family:var(--mono);font-size:11px;font-weight:700;color:var(--accent);margin-bottom:6px">A. Guard</div>
              <div style="font-size:13px;color:var(--text2)">Check <code style="font-size:12px">_depth == 0</code><br>Prevents nesting</div>
            </div>

            <div style="display:flex;align-items:center;color:var(--text3);font-size:18px;padding:0 2px">&rarr;</div>

            <!-- Step B -->
            <div style="flex:1;padding:10px 14px;background:rgba(5,150,105,.03);border:1px solid rgba(5,150,105,.1)">
              <div style="font-family:var(--mono);font-size:11px;font-weight:700;color:var(--accent4);margin-bottom:6px">B. Prompt</div>
              <div style="font-size:13px;color:var(--text2)"><code style="font-size:12px">SubagentManager</code><br><code style="font-size:12px">.get_prompt(type)</code></div>
            </div>

            <div style="display:flex;align-items:center;color:var(--text3);font-size:18px;padding:0 2px">&rarr;</div>

            <!-- Step C -->
            <div style="flex:1.3;padding:10px 14px;background:rgba(14,165,233,.03);border:1px solid rgba(14,165,233,.1)">
              <div style="font-family:var(--mono);font-size:11px;font-weight:700;color:var(--accent3);margin-bottom:6px">C. Isolate</div>
              <div style="font-size:13px;color:var(--text2)">New <code style="font-size:12px">ChatSession</code><br><span style="color:var(--accent4)">shared</span> client + tools, <span style="color:var(--orange)">unique</span> prompt</div>
            </div>

            <div style="display:flex;align-items:center;color:var(--text3);font-size:18px;padding:0 2px">&rarr;</div>

            <!-- Step D -->
            <div style="flex:1.3;padding:10px 14px;background:rgba(14,165,233,.03);border:1px solid rgba(14,165,233,.1)">
              <div style="font-family:var(--mono);font-size:11px;font-weight:700;color:var(--accent3);margin-bottom:6px">D. Run</div>
              <div style="font-size:13px;color:var(--text2)"><code style="font-size:12px">SubagentRunner.run()</code><br>ReAct loop, max 15 turns</div>
            </div>

            <div style="display:flex;align-items:center;color:var(--text3);font-size:18px;padding:0 2px">&rarr;</div>

            <!-- Step E -->
            <div style="flex:1;padding:10px 14px;background:rgba(124,58,237,.03);border:1px solid rgba(124,58,237,.1);border-radius:0 10px 10px 0">
              <div style="font-family:var(--mono);font-size:11px;font-weight:700;color:var(--accent);margin-bottom:6px">E. Return</div>
              <div style="font-size:13px;color:var(--text2)">Wrap in <code style="font-size:12px">ToolResult</code><br>Reset <code style="font-size:12px">_depth</code></div>
            </div>

          </div>
        </div>

        <!-- Row 3: ReAct loop detail -->
        <div class="step-item" style="padding-top:16px">
          <div style="font-family:var(--mono);font-size:11px;font-weight:700;color:var(--text2);letter-spacing:1px;text-transform:uppercase;margin-bottom:12px">SubagentRunner ReAct Loop</div>
          <div style="display:flex;align-items:center;gap:0;flex-wrap:wrap">

            <div style="background:rgba(14,165,233,.04);border:1px solid rgba(14,165,233,.12);border-radius:8px;padding:10px 14px;text-align:center">
              <div style="font-family:var(--mono);font-size:12px;font-weight:600;color:var(--accent3)">append_user_message</div>
              <div style="font-size:12px;color:var(--text3);margin-top:2px">prompt &rarr; session</div>
            </div>

            <div style="color:var(--text3);font-size:18px;padding:0 8px">&rarr;</div>

            <!-- Loop block -->
            <div style="flex:1;min-width:300px;border:1.5px dashed rgba(14,165,233,.2);border-radius:10px;padding:12px 14px;position:relative">
              <div style="position:absolute;top:-10px;left:14px;background:var(--surface);padding:0 6px;font-family:var(--mono);font-size:10px;color:var(--accent3);font-weight:600">LOOP (up to 15 turns)</div>
              <div style="display:flex;align-items:center;gap:0;flex-wrap:wrap;margin-top:4px">

                <div style="background:rgba(234,88,12,.04);border:1px solid rgba(234,88,12,.12);border-radius:8px;padding:8px 12px;text-align:center">
                  <div style="font-family:var(--mono);font-size:12px;font-weight:600;color:var(--orange)">send_message_stream</div>
                  <div style="font-size:11px;color:var(--text3);margin-top:2px">session &rarr; LLM</div>
                </div>

                <div style="color:var(--text3);font-size:18px;padding:0 6px">&rarr;</div>

                <div style="background:rgba(124,58,237,.04);border:1px solid rgba(124,58,237,.12);border-radius:8px;padding:8px 12px;text-align:center">
                  <div style="font-family:var(--mono);font-size:12px;font-weight:600;color:var(--accent)">text only?</div>
                  <div style="font-size:11px;color:var(--accent4);margin-top:2px;font-weight:600">return result</div>
                </div>

                <div style="color:var(--text3);font-size:11px;padding:0 6px;font-family:var(--mono)">else</div>

                <div style="background:rgba(14,165,233,.04);border:1px solid rgba(14,165,233,.12);border-radius:8px;padding:8px 12px;text-align:center">
                  <div style="font-family:var(--mono);font-size:12px;font-weight:600;color:var(--accent3)">execute tools</div>
                  <div style="font-size:11px;color:var(--text3);margin-top:2px">append responses</div>
                </div>

                <div style="color:var(--text3);font-size:18px;padding:0 6px">&#x21BA;</div>

              </div>
            </div>

          </div>
        </div>

      </div>
    </div>

    <div class="step-item">
      <div class="tip-box purple mt-16">
        <span>&#x1F4A1;</span>
        <div style="font-size:14px">Same <code>send_message_stream()</code> loop as the main agent &mdash; but the history is <strong>isolated</strong> and the result is a <strong>string</strong>, not streamed events.</div>
      </div>
    </div>
  </div>
</section>
`);
