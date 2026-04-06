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
        </tr>
      </thead>
      <tbody>
        <tr><td><code>glob</code></td><td>Find files by glob pattern</td></tr>
        <tr><td><code>read_file</code></td><td>Read file contents with optional line ranges</td></tr>
        <tr><td><code>list_directory</code></td><td>List files and subdirectories</td></tr>
        <tr><td><code>grep_search</code></td><td>Regex search across files</td></tr>
        <tr><td><code>web_fetch</code></td><td>Fetch and parse web content</td></tr>
        <tr><td><code>write_file</code></td><td>Write content to files</td></tr>
        <tr><td><code>replace</code></td><td>Find-and-replace in files</td></tr>
        <tr><td><code>run_shell_command</code></td><td>Execute shell commands</td></tr>
        <tr><td><code>task</code></td><td>Launch isolated sub-agents</td></tr>
        <tr><td><code>activate_skill</code></td><td>Load specialized skill instructions</td></tr>
      </tbody>
    </table>
  </div>
</section>
`);
