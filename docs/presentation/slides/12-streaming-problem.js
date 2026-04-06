registerSlide(`
<section class="slide" data-title="streaming-problem">
  <div class="slide-inner">
    <div class="section-label">Real-Time UX</div>
    <h2 class="section-title">Streaming Architecture</h2>
    <p class="section-desc">Without streaming, users stare at a blank screen. The event system solves this.</p>

    <div class="two-col mt-24" style="align-items:stretch">
      <!-- BEFORE: Blocking -->
      <div style="display:flex;flex-direction:column">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px">
          <h3 style="font-size:18px;font-weight:700;color:var(--red);margin:0">&#x274C; Before: Blocking</h3>
          <button onclick="sdReplayBlocking()" class="sd-ctrl-btn" title="Replay">&#x25B6; Replay</button>
        </div>
        <div id="streamDemoBlocking" class="stream-demo stream-demo-playing" style="flex:1;background:var(--surface);border:1px solid var(--border);border-radius:14px;overflow:hidden;box-shadow:var(--shadow);display:flex;flex-direction:column">
          <div style="padding:10px 16px;background:var(--surface2);border-bottom:1px solid var(--border);display:flex;align-items:center;gap:8px;flex-shrink:0">
            <span style="width:8px;height:8px;border-radius:50%;background:var(--red)"></span>
            <span style="font-family:var(--mono);font-size:11px;color:var(--text3)">terminal</span>
          </div>
          <div style="padding:16px 18px;flex:1;font-family:var(--mono);font-size:13px;line-height:1.7;display:flex;flex-direction:column">
            <div style="color:var(--accent);margin-bottom:8px"><span style="color:var(--accent4)">&#x276F;</span> How do I fix this bug?</div>
            <div class="sd-blocking-wait" style="display:flex;align-items:center;gap:8px;color:var(--text3);margin-bottom:8px">
              <span class="sd-blocking-spinner" style="display:inline-block;width:14px;height:14px;border:2px solid var(--border2);border-top-color:var(--text3);border-radius:50%"></span>
              <span>Waiting for response...</span>
            </div>
            <div class="sd-blocking-elapsed" style="font-size:11px;color:var(--text3);margin-bottom:12px;font-style:italic">
              <span class="sd-elapsed-counter">0</span>s elapsed &mdash; no feedback
            </div>
            <div class="sd-blocking-response" style="opacity:0;color:var(--text2);border-left:2px solid var(--red);padding-left:12px;line-height:1.6;flex:1">
              The bug is in your auth middleware. The session token expires before the refresh logic runs. Move the refresh check to run before validation...<br><span style="color:var(--text3);font-size:11px;margin-top:4px;display:inline-block">(entire response dumps at once)</span>
            </div>
          </div>
        </div>
      </div>

      <!-- AFTER: Streaming -->
      <div style="display:flex;flex-direction:column">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px">
          <h3 style="font-size:18px;font-weight:700;color:var(--accent4);margin:0">&#x2705; After: Streaming Events</h3>
          <button onclick="sdReplayStreaming()" class="sd-ctrl-btn" title="Replay">&#x25B6; Replay</button>
        </div>
        <div id="streamDemoStreaming" class="stream-demo stream-demo-playing" style="flex:1;background:var(--surface);border:1px solid var(--border);border-radius:14px;overflow:hidden;box-shadow:var(--shadow);display:flex;flex-direction:column">
          <div style="padding:10px 16px;background:var(--surface2);border-bottom:1px solid var(--border);display:flex;align-items:center;gap:8px;flex-shrink:0">
            <span style="width:8px;height:8px;border-radius:50%;background:var(--accent4)"></span>
            <span style="font-family:var(--mono);font-size:11px;color:var(--text3)">terminal</span>
          </div>
          <div style="padding:16px 18px;flex:1;font-family:var(--mono);font-size:13px;line-height:1.7;display:flex;flex-direction:column">
            <div style="color:var(--accent);margin-bottom:8px"><span style="color:var(--accent4)">&#x276F;</span> How do I fix this bug?</div>
            <div style="color:var(--text2);border-left:2px solid var(--accent4);padding-left:12px">
              <span class="sd-stream-token">The </span><span class="sd-stream-token">bug </span><span class="sd-stream-token">is </span><span class="sd-stream-token">in </span><span class="sd-stream-token">your </span><span class="sd-stream-token">auth </span><span class="sd-stream-token">middleware. </span><span class="sd-stream-token">The </span><span class="sd-stream-token">session </span><span class="sd-stream-token">token </span><span class="sd-stream-token">expires </span><span class="sd-stream-token">before </span><span class="sd-stream-token">the </span><span class="sd-stream-token">refresh </span><span class="sd-stream-token">logic </span><span class="sd-stream-token">runs. </span><span class="sd-stream-token">Move </span><span class="sd-stream-token">the </span><span class="sd-stream-token">refresh </span><span class="sd-stream-token">check </span><span class="sd-stream-token">to </span><span class="sd-stream-token">run </span><span class="sd-stream-token">before </span><span class="sd-stream-token">validation...</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- API call comparison -->
    <div class="two-col mt-16" style="align-items:stretch">
      <div class="code-block" style="margin:0">
        <div class="code-header"><span class="c r"></span><span class="c y"></span><span class="c g"></span><span class="filename">gemini_client.py &mdash; Blocking</span></div>
        <div class="code-body">
<span class="cm"># Waits until entire response is ready</span>
response = <span class="var">self</span>._client.models.<span class="fn">generate_content</span>(
    model=<span class="var">self</span>._model,
    contents=sdk_contents,
    config=config,
)
<span class="cm"># Nothing happens until here ^</span>
<span class="kw">return</span> <span class="var">self</span>.<span class="fn">_parse_response</span>(response)
        </div>
      </div>
      <div class="code-block" style="margin:0">
        <div class="code-header"><span class="c r"></span><span class="c y"></span><span class="c g"></span><span class="filename">gemini_client.py &mdash; Streaming</span></div>
        <div class="code-body">
<span class="cm"># Yields chunks as they arrive</span>
stream = <span class="var">self</span>._client.models.<span class="fn">generate_content_stream</span>(
    model=<span class="var">self</span>._model,
    contents=sdk_contents,
    config=config,
)
<span class="kw">for</span> chunk <span class="kw">in</span> stream:
    <span class="kw">if</span> part.text <span class="kw">is not</span> <span class="num">None</span>:
        <span class="kw">yield</span> <span class="type">TurnResult</span>(text=part.text)
        </div>
      </div>
    </div>
  </div>

  <style>
    /* Control buttons */
    .sd-ctrl-btn {
      display: inline-flex; align-items: center; gap: 5px;
      padding: 4px 12px; border-radius: 7px;
      border: 1px solid var(--border); background: var(--surface);
      font-family: var(--mono); font-size: 11px; font-weight: 500;
      color: var(--text3); cursor: pointer; transition: all .2s;
    }
    .sd-ctrl-btn:hover { border-color: rgba(124,58,237,.4); color: var(--accent); background: rgba(124,58,237,.04); }

    /* Blocking demo */
    .stream-demo-playing .sd-blocking-spinner {
      animation: sdBlockSpin 1s linear infinite;
    }
    .stream-demo-playing .sd-blocking-response {
      animation: sdBlockReveal 0.3s ease 6s forwards;
    }
    .stream-demo-playing .sd-blocking-wait {
      animation: sdFadeOut 0.3s ease 5.9s forwards;
    }
    .stream-demo-playing .sd-blocking-elapsed {
      animation: sdFadeOut 0.3s ease 5.9s forwards;
    }
    /* Streaming demo */
    .sd-stream-token { opacity: 0; transition: none; }
    .stream-demo-playing .sd-stream-token { animation: sdTokenFade .3s ease both; }
    .stream-demo-playing .sd-stream-token:nth-child(1)  { animation-delay: .3s }
    .stream-demo-playing .sd-stream-token:nth-child(2)  { animation-delay: .5s }
    .stream-demo-playing .sd-stream-token:nth-child(3)  { animation-delay: .7s }
    .stream-demo-playing .sd-stream-token:nth-child(4)  { animation-delay: .9s }
    .stream-demo-playing .sd-stream-token:nth-child(5)  { animation-delay: 1.1s }
    .stream-demo-playing .sd-stream-token:nth-child(6)  { animation-delay: 1.3s }
    .stream-demo-playing .sd-stream-token:nth-child(7)  { animation-delay: 1.5s }
    .stream-demo-playing .sd-stream-token:nth-child(8)  { animation-delay: 1.7s }
    .stream-demo-playing .sd-stream-token:nth-child(9)  { animation-delay: 1.9s }
    .stream-demo-playing .sd-stream-token:nth-child(10) { animation-delay: 2.1s }
    .stream-demo-playing .sd-stream-token:nth-child(11) { animation-delay: 2.3s }
    .stream-demo-playing .sd-stream-token:nth-child(12) { animation-delay: 2.5s }
    .stream-demo-playing .sd-stream-token:nth-child(13) { animation-delay: 2.7s }
    .stream-demo-playing .sd-stream-token:nth-child(14) { animation-delay: 2.9s }
    .stream-demo-playing .sd-stream-token:nth-child(15) { animation-delay: 3.1s }
    .stream-demo-playing .sd-stream-token:nth-child(16) { animation-delay: 3.3s }
    .stream-demo-playing .sd-stream-token:nth-child(17) { animation-delay: 3.5s }
    .stream-demo-playing .sd-stream-token:nth-child(18) { animation-delay: 3.7s }
    .stream-demo-playing .sd-stream-token:nth-child(19) { animation-delay: 3.9s }
    .stream-demo-playing .sd-stream-token:nth-child(20) { animation-delay: 4.1s }
    .stream-demo-playing .sd-stream-token:nth-child(21) { animation-delay: 4.3s }
    .stream-demo-playing .sd-stream-token:nth-child(22) { animation-delay: 4.5s }
    .stream-demo-playing .sd-stream-token:nth-child(23) { animation-delay: 4.7s }
    .stream-demo-playing .sd-stream-token:nth-child(24) { animation-delay: 4.9s }
    /* Keyframes */
    @keyframes sdBlockSpin { to { transform: rotate(360deg) } }
    @keyframes sdBlockReveal { to { opacity: 1 } }
    @keyframes sdFadeOut { to { opacity: 0; height: 0; margin: 0; padding: 0; overflow: hidden } }
    @keyframes sdTokenFade { from { opacity: 0 } to { opacity: 1 } }
  </style>
</section>
`);

// --- Blocking demo replay ---
function sdReplayBlocking() {
  var el = document.getElementById('streamDemoBlocking');
  if (!el) return;

  // Stop elapsed timer
  if (window._sdElapsedTimer) clearInterval(window._sdElapsedTimer);

  // Remove playing class
  el.classList.remove('stream-demo-playing');

  // Reset animated elements
  var response = el.querySelector('.sd-blocking-response');
  if (response) response.style.opacity = '0';
  var wait = el.querySelector('.sd-blocking-wait');
  if (wait) { wait.style.opacity = '1'; wait.style.height = ''; wait.style.margin = ''; wait.style.overflow = ''; }
  var elapsed = el.querySelector('.sd-blocking-elapsed');
  if (elapsed) { elapsed.style.opacity = '1'; elapsed.style.height = ''; elapsed.style.margin = ''; elapsed.style.overflow = ''; }

  // Force reflow
  void el.offsetWidth;

  // Re-add playing class
  el.classList.add('stream-demo-playing');

  // Restart elapsed counter
  var counter = el.querySelector('.sd-elapsed-counter');
  if (counter) {
    var sec = 0;
    counter.textContent = '0';
    window._sdElapsedTimer = setInterval(function() {
      sec++;
      counter.textContent = sec;
      if (sec >= 8) clearInterval(window._sdElapsedTimer);
    }, 1000);
  }
}

// --- Streaming demo replay ---
function sdReplayStreaming() {
  var el = document.getElementById('streamDemoStreaming');
  if (!el) return;

  // Remove playing class
  el.classList.remove('stream-demo-playing');

  // Reset all animated elements
  el.querySelectorAll('.sd-stream-token').forEach(function(t) { t.style.opacity = '0'; });

  // Force reflow
  void el.offsetWidth;

  // Re-add playing class
  el.classList.add('stream-demo-playing');
}

// Auto-start elapsed counter after slides render
document.addEventListener('DOMContentLoaded', function() {
  var obs = new MutationObserver(function(_, o) {
    var counter = document.querySelector('.sd-elapsed-counter');
    if (counter) {
      o.disconnect();
      var sec = 0;
      window._sdElapsedTimer = setInterval(function() {
        sec++;
        counter.textContent = sec;
        if (sec >= 8) clearInterval(window._sdElapsedTimer);
      }, 1000);
    }
  });
  obs.observe(document.body, { childList: true, subtree: true });
});
