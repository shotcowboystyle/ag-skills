# protect-mcp starter Cedar policy

The starter policy referenced from `SKILL.md`. It permits read-only tools,
read-only git and a few shell built-ins, and writes inside the project, and
forbids access to the signing key, secrets, receipts, the policy itself, and
Claude Code settings.

Create `./protect.cedar` at the project root and replace `/path/to/project`
with the project's absolute path:

```cedar
// Read-only tools. Add WebFetch with your own URL rule.
permit (principal, action == Action::"MCP::Tool::call", resource) when {
    resource == Tool::"Read" || resource == Tool::"Glob" || resource == Tool::"Grep"
};

// Never read the signing key, .env files, or SSH keys. Grep and Glob take
// `path`; keep the key gitignored as well, since Grep skips gitignored files.
forbid (principal, action == Action::"MCP::Tool::call", resource) when {
    (resource == Tool::"Read" || resource == Tool::"Grep" || resource == Tool::"Glob") &&
    context has input &&
    ((context.input has file_path &&
      (context.input.file_path like "*protect-mcp.key*" ||
       context.input.file_path like "*.env*" || context.input.file_path like "*.ssh*")) ||
     (context.input has path &&
      (context.input.path like "*protect-mcp.key*" ||
       context.input.path like "*.env*" || context.input.path like "*.ssh*")))
};

// Shell: read-only git subcommands and a few harmless built-ins. No `cat`:
// use Read, which the forbid above covers. No interpreter or package-manager
// prefix (`npm`, `node`, `python`, `make`): they run arbitrary code.
permit (principal, action == Action::"MCP::Tool::call", resource == Tool::"Bash") when {
    context has input && context.input has command &&
    (context.input.command like "git status*" || context.input.command like "git diff*" ||
     context.input.command like "git log*" || context.input.command like "git show*" ||
     context.input.command like "ls*" || context.input.command like "pwd*" ||
     context.input.command like "echo *" || context.input.command like "test *")
};

// No chaining (`&` also denies `2>&1`), `$` expansion, redirection (`>` or
// `<`, which covers `<(`), file output (`git diff --output`), reads outside
// git (`git diff --no-index`), rm -rf, or naming the secrets above
forbid (principal, action == Action::"MCP::Tool::call", resource == Tool::"Bash") when {
    context has input && context.input has command &&
    (context.input.command like "*;*" || context.input.command like "*&*" ||
     context.input.command like "*|*" || context.input.command like "*$*" ||
     context.input.command like "*`*" || context.input.command like "*>*" ||
     context.input.command like "*<*" || context.input.command like "*\n*" ||
     context.input.command like "*--output*" || context.input.command like "*--no-index*" ||
     context.input.command like "*rm -rf*" || context.input.command like "*protect-mcp.key*" ||
     context.input.command like "*.env*" || context.input.command like "*.ssh*")
};

// Writes only inside the project (paths are absolute), never via `..`
permit (principal, action == Action::"MCP::Tool::call", resource) when {
    (resource == Tool::"Write" || resource == Tool::"Edit") &&
    context has input && context.input has file_path &&
    context.input.file_path like "/path/to/project/*"
};

// Never write the policy, the key, the receipts, secrets, or Claude Code
// settings (which can turn the hooks off)
forbid (principal, action == Action::"MCP::Tool::call", resource) when {
    (resource == Tool::"Write" || resource == Tool::"Edit") &&
    context has input && context.input has file_path &&
    (context.input.file_path like "*/../*" || context.input.file_path like "*/.." ||
     context.input.file_path like "*protect.cedar*" ||
     context.input.file_path like "*protect-mcp.key*" ||
     context.input.file_path like "*/receipts/*" ||
     context.input.file_path like "*.env*" || context.input.file_path like "*.ssh*" ||
     context.input.file_path like "*/.claude/*")
};
```
