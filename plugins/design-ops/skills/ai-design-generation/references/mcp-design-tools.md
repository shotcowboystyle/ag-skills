# MCP Design Tools — Catalog

This reference lists the MCP servers that are useful for AI-powered design generation: who
publishes each one, how to connect it, and what it is good for. Tool names change between
server versions, so list the connected server's tools at runtime before calling one. Never
call a tool name from memory.

Checked against each publisher's docs in October 2026. Re-check the linked docs before
relying on an endpoint or package name.

---

## 1. Stitch (Google)

Generates UI screens and multi-screen flows from text or an image, and exports HTML/CSS or
Figma. Google documents an MCP route at <https://stitch.withgoogle.com/docs/mcp/setup>; the
remote endpoint authenticates with Google credentials, which not every MCP client supports.
There is no official npm package. If the client can't authenticate, use Stitch in the
browser and paste the exported HTML/CSS back in.

**Best for:** fast first drafts of whole screens and wireframes.
**Limits:** output needs a token pass before it matches a design system.

## 2. fal (fal.ai)

One server in front of fal's model catalogue: FLUX, Imagen, Recraft, Veo and others.
Official remote server, OAuth sign-in (docs: <https://fal.ai/docs/documentation/setting-up/mcp>):

```bash
claude mcp add --transport http --scope user fal https://mcp.fal.ai/mcp-relay
```

Its tools cover model discovery (`search_models`, `get_model_schema`, `get_pricing`,
`recommend_model`), execution (`run_model`, `submit_job`, `check_job`, `get_job_result`,
`cancel_job`) and `upload_file`. Read `get_model_schema` before `run_model`, since every
model takes different inputs.

**Best for:** hero images, product shots, vector icons (Recraft models), short video.
**Limits:** per-generation cost; check `get_pricing` before batch runs.

## 3. Replicate

Runs public and custom fine-tuned models. Official server (npm `replicate-mcp`, from
Replicate), keyed by `REPLICATE_API_TOKEN`:

```json
{
  "mcpServers": {
    "replicate": {
      "command": "npx",
      "args": ["-y", "replicate-mcp"],
      "env": { "REPLICATE_API_TOKEN": "<token>" }
    }
  }
}
```

**Best for:** custom fine-tuned styles, utility models (background removal, upscaling).

## 4. Recraft

Raster and vector (SVG) generation, background removal, vectorizing. Official server from
Recraft (npm `@recraft-ai/mcp-recraft-server`), keyed by `RECRAFT_API_KEY`:

```json
{
  "mcpServers": {
    "recraft": {
      "command": "npx",
      "args": ["-y", "@recraft-ai/mcp-recraft-server"],
      "env": { "RECRAFT_API_KEY": "<key>" }
    }
  }
}
```

**Best for:** icon sets and illustrations that must ship as SVG.

## 5. OpenAI image models (no official MCP)

OpenAI doesn't publish an image-generation MCP server. Call the Images API directly
(`gpt-image-1`), or hand the user the prompt. Strong at following prompts, rendering text
and editing an existing image.

## 6. Figma (official)

Figma runs two servers (docs: <https://developers.figma.com/docs/figma-mcp-server/>):

```bash
claude mcp add --transport http figma https://mcp.figma.com/mcp              # remote, OAuth
claude mcp add --transport http figma-desktop http://127.0.0.1:3845/mcp      # desktop app, Dev Mode
```

Core read tools on both: `get_design_context`, `get_variable_defs`, `get_metadata`,
`get_screenshot`, `get_code_connect_map`, `search_design_system`. The remote server also
writes to files (for example `use_figma`, `generate_figma_design`, `upload_assets`). It
exposes the `create_design_system_rules` prompt.

**Best for:** pulling real specs, variables and screenshots out of a Figma file before
building; pushing a built page back into Figma for review.

Community servers such as Framelink (`figma-developer-mcp`) read files through the REST API
with a personal access token. They work, but they aren't Figma's.

---

## Tool Selection Matrix

Use this matrix to route generation tasks to the best available MCP tool.

| Task                      | Best Tool                       | Fallback                 | Notes                                            |
| ------------------------- | ------------------------------- | ------------------------ | ------------------------------------------------ |
| Full UI screen from text  | Stitch                          | FLUX Pro (as screenshot) | Stitch outputs HTML/CSS; FLUX outputs image only |
| Multi-page site           | Stitch                          | Manual                   | Keeps one style across screens                   |
| App icon (SVG)            | Recraft (own MCP or via fal)    | Manual SVG               | Native SVG output                                |
| Icon set (batch SVG)      | Recraft (own MCP or via fal)    | Manual SVG               | Generate with consistent style prompt            |
| UI illustrations          | FLUX Pro (fal)                  | OpenAI Images API        | No OpenAI MCP; call the API or hand off a prompt |
| Product photographs       | Imagen 4 (via Fal.ai)           | FLUX Pro (Fal.ai)        | Strong photorealism                              |
| Hero images               | FLUX Pro (via Fal.ai)           | Imagen 4 (Fal.ai)        | FLUX Pro best general-purpose                    |
| Images with text          | Imagen (fal) or OpenAI Images   | —                        | Both handle text well                            |
| Video/motion concepts     | Veo (via fal)                   | Kie.ai (`/scroll`)       | Short clips for motion concepts                  |
| Design system extraction  | Figma MCP                       | Manual                   | Reads Figma files directly                       |
| Design context extraction | Figma (`get_design_context`)    | Stitch                   | Figma reads real specs; Stitch infers from image |
| Wireframes                | Stitch                          | Manual                   | Fast low-fidelity generation                     |
| Background removal        | Replicate (RemBG)               | Manual                   | Utility model on Replicate                       |
| Image upscaling           | Replicate (Real-ESRGAN)         | —                        | Utility model on Replicate                       |
| Custom fine-tuned style   | Replicate                       | Fal.ai                   | Replicate supports custom models                 |
| Image editing/inpainting  | OpenAI Images API (edit)        | fal (inpainting models)  | Masked edits of an existing image                |

## MCP Detection Protocol

When Design Ops runs a generation command, follow this protocol:

### Step 1: Detect Available MCP Servers

Check which MCP servers are connected in the current session. The available tools will indicate which servers are active.

### Step 2: Route to Best Available Tool

Using the Tool Selection Matrix above, identify the best tool for the task. If the best tool is not available, use the fallback.

### Step 3: Handle No-MCP Gracefully

If no generation MCP servers are available, Design Ops should:

1. Acknowledge that no generation tools are connected
2. Provide a complete, detailed specification that the user can use manually
3. Include the exact prompt they would use with each tool
4. Suggest which MCP server(s) to install for their use case
5. Offer to proceed with design guidance using Design Ops' other skills

### Step 4: Never Fail Silently

Always tell the user:

- Which MCP tool was selected and why
- What model is being used (for fal)
- What the generation will cost (from the server's pricing tool, or say it is unknown)
- What the expected output quality is
- How to iterate if the result is not satisfactory

## Multi-MCP Coordination

When multiple MCP servers are available, coordinate them for richer output:

### Screen + Assets Pipeline

1. Use Stitch to generate the screen layout
2. Use Recraft to generate icons referenced in the screen
3. Use FLUX Pro or Imagen (fal) to generate hero images
4. Use Figma MCP to export existing brand assets if available

### Design Extraction + Generation Pipeline

1. Use Figma `get_design_context` and `get_variable_defs` on the existing file
2. Turn the variables into a token summary
3. Paste that summary into the Stitch prompt for style-consistent generation
4. Score the generated screen against the Figma original

### Iterative Refinement Pipeline

1. Generate v1 with any tool
2. Score against `visual-design-mastery/references/visual-scoring-framework.md`
3. Identify weakest dimensions
4. Adjust prompt to target weak dimensions
5. Regenerate v2
6. Repeat until quality gate is passed (max 3 iterations)
