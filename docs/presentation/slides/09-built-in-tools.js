registerSlide(`
<section class="slide" data-title="built-in-tools">
  <div class="slide-inner">
    <div class="section-label">Tools</div>
    <h2 class="section-title">Built-in Tool Set</h2>
    <p class="section-desc">10 tools covering file I/O, search, web, shell, sub-agents, and skills.</p>

    <table class="cmp-table mt-24">
      <thead>
        <tr>
          <th>Tool</th>
          <th>Purpose</th>
          <th>Confirmation</th>
        </tr>
      </thead>
      <tbody>
        <tr><td><code>glob</code></td><td>Find files by glob pattern</td><td style="color:var(--accent4)">&#x2714; Auto</td></tr>
        <tr><td><code>read_file</code></td><td>Read file contents with optional line ranges</td><td style="color:var(--accent4)">&#x2714; Auto</td></tr>
        <tr><td><code>list_directory</code></td><td>List files and subdirectories</td><td style="color:var(--accent4)">&#x2714; Auto</td></tr>
        <tr><td><code>grep_search</code></td><td>Regex search across files</td><td style="color:var(--accent4)">&#x2714; Auto</td></tr>
        <tr><td><code>web_fetch</code></td><td>Fetch and parse web content</td><td style="color:var(--accent4)">&#x2714; Auto</td></tr>
        <tr><td><code>write_file</code></td><td>Write content to files</td><td style="color:var(--orange)">&#x1F512; Required</td></tr>
        <tr><td><code>replace</code></td><td>Find-and-replace in files</td><td style="color:var(--orange)">&#x1F512; Required</td></tr>
        <tr><td><code>run_shell_command</code></td><td>Execute shell commands</td><td style="color:var(--orange)">&#x1F512; Required</td></tr>
        <tr><td><code>task</code></td><td>Launch isolated sub-agents</td><td style="color:var(--accent4)">&#x2714; Auto</td></tr>
        <tr><td><code>activate_skill</code></td><td>Load specialized skill instructions</td><td style="color:var(--accent4)">&#x2714; Auto</td></tr>
      </tbody>
    </table>

    <div class="tip-box red mt-16">
      <span>&#x1F6E1;&#xFE0F;</span>
      <div><strong>Safety is first-class.</strong> Write operations require explicit user confirmation. The model can request, but only the user can approve.</div>
    </div>
  </div>
</section>
`);
