registerSlide(`
<section class="slide" data-title="tool-call-approaches">
  <div class="slide-inner">
    <div class="section-label">Tool Use</div>
    <h2 class="section-title">Declaring Tools to the LLM</h2>
    <p class="section-desc">Two approaches for <strong>providing</strong> tool definitions to the model &mdash; each with different trade-offs.</p>

    <div class="two-col mt-24" style="align-items:stretch">
      <!-- XML Approach -->
      <div style="display:flex;flex-direction:column">
        <div class="code-block" style="flex:1;display:flex;flex-direction:column">
          <div class="code-header"><span class="c r"></span><span class="c y"></span><span class="c g"></span><span class="filename">XML Tool Call (text-based)</span></div>
          <div class="code-body" style="flex:1">
<span class="cm"># Embed tool spec in the prompt itself</span>
system_prompt = <span class="str">"""
You have these tools:

&lt;tool name="read_file"&gt;
  &lt;description&gt;Read a file&lt;/description&gt;
  &lt;param name="path" type="string"/&gt;
&lt;/tool&gt;

To call a tool, output:
&lt;tool_call&gt;
  &lt;tool_name&gt;...&lt;/tool_name&gt;
  &lt;parameters&gt;...&lt;/parameters&gt;
&lt;/tool_call&gt;
"""</span>
          </div>
        </div>
        <div class="tip-box blue mt-16">
          <span>&#x1F310;</span>
          <div><strong>Universal:</strong> Tools declared in the prompt text. Works with any model, but requires manual parsing of responses.</div>
        </div>
      </div>

      <!-- Native Function Call -->
      <div style="display:flex;flex-direction:column">
        <div class="code-block" style="flex:1;display:flex;flex-direction:column">
          <div class="code-header"><span class="c r"></span><span class="c y"></span><span class="c g"></span><span class="filename">Native Function Call (API)</span></div>
          <div class="code-body" style="flex:1">
<span class="cm"># Tool schema sent as API parameter</span>
response = client.messages.create(
    tools=[{
        <span class="str">"name"</span>: <span class="str">"read_file"</span>,
        <span class="str">"description"</span>: <span class="str">"Read a file"</span>,
        <span class="str">"input_schema"</span>: {
            <span class="str">"type"</span>: <span class="str">"object"</span>,
            <span class="str">"properties"</span>: {
                <span class="str">"path"</span>: {<span class="str">"type"</span>: <span class="str">"string"</span>}
            }
        }
    }],
    messages=conversation
)
          </div>
        </div>
        <div class="tip-box purple mt-16">
          <span>&#x2705;</span>
          <div><strong>Reliable:</strong> Tools declared via API layer with JSON Schema. Structured responses, no parsing. Used by Claude, GPT-4, Gemini.</div>
        </div>
      </div>
    </div>

    <div class="tip-box orange mt-16">
      <span>&#x1F3AF;</span>
      <div><strong>Our approach:</strong> We use <strong>native function calling</strong> via the Gemini API &mdash; the model returns structured <code>functionCall</code> parts, not free text to parse.</div>
    </div>
  </div>
</section>
`);
