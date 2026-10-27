# Tool Resolution

`ots`, `bagit.py` and `mat2` are installed into the plugin's virtual environment by
evidence-install-deps, which is not on `PATH`. Every skill that calls one of them
starts the same Bash command with this line, so the venv copy wins and a system-wide
install is the fallback:

```bash
export PATH="${CLAUDE_USER_DATA:-${XDG_DATA_HOME:-$HOME/.local/share}/claude-plugins}/evidence-ops/venv/bin:$PATH"
```

Then call the tool by its bare name, in the same command:

```bash
export PATH="${CLAUDE_USER_DATA:-${XDG_DATA_HOME:-$HOME/.local/share}/claude-plugins}/evidence-ops/venv/bin:$PATH" && ots info "$PROOF"
```

Rules:

- Shell state does not carry between separate commands, so the export goes into every
  command that uses a venv tool.
- Never call `"$VENV_DIR/bin/<tool>"` by full path. Bare names are what the skills'
  `allowed-tools` patterns (`Bash(ots *)`, `Bash(bagit.py *)`) match, together with
  `Bash(export PATH=*)` for the line above.
- Use the line exactly as written. Do not prepend any other directory.
- `command -v <tool>` after the export reports which location satisfied the tool.
