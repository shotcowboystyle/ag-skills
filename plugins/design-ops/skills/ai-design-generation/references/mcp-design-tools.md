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


---

## Appendix: MCP Integration, Stitch, Image and Video Tools

Moved verbatim from the `ai-design-generation` SKILL.md.

### 2. MCP Integration Overview

#### How the agent connects to design generation tools

The agent communicates with design generation services through MCP (Model Context Protocol) servers. Each MCP server wraps an external API and exposes it as a set of tools the agent can invoke directly within a conversation.

**The Architecture:**

```
User Request → Agent (Design Ops skill) → MCP Server → External API → Generated Asset
                      ↓                                        ↓
              Prompt Engineering                         Raw Output
              Quality Scoring                            Post-Processing
              Iteration Direction                        Final Delivery
```

**Key Benefits of MCP Integration:**

- Claude can generate designs mid-conversation without the user leaving the terminal
- Prompt construction is automated using Design Ops' design intelligence
- Results can be evaluated, iterated, and refined in a continuous loop
- Multiple tools can be chained in a single pipeline (e.g., Stitch for layout, Fal.ai for hero image, Recraft for icons)

#### MCP Server Configuration

All MCP servers are configured in your coding tool's MCP settings. Each server requires an API key for its respective service. For example: project `.mcp.json` (Claude Code, Cursor), `~/.codex/config.toml` (Codex), `opencode.json` (OpenCode).

**Example configuration** (servers checked against each publisher's docs; see `mcp-design-tools.md`):

```bash
claude mcp add --transport http figma https://mcp.figma.com/mcp           # Figma, OAuth
claude mcp add --transport http --scope user fal https://mcp.fal.ai/mcp-relay  # fal, OAuth
```

```json
{
  "mcpServers": {
    "recraft": {
      "command": "npx",
      "args": ["-y", "@recraft-ai/mcp-recraft-server"],
      "env": { "RECRAFT_API_KEY": "<key>" }
    },
    "replicate": {
      "command": "npx",
      "args": ["-y", "replicate-mcp"],
      "env": { "REPLICATE_API_TOKEN": "<token>" }
    }
  }
}
```

#### Supported MCP Servers (All Optional)

| Server    | What It Does                                         | Connect                                         | Auth              |
| --------- | ---------------------------------------------------- | ----------------------------------------------- | ----------------- |
| Stitch    | UI screens and flows from text or an image           | Google's MCP route (see Stitch docs) or the web | Google account    |
| fal       | FLUX, Imagen, Recraft, Veo and more through one API  | `https://mcp.fal.ai/mcp-relay`                  | OAuth             |
| Recraft   | Raster and SVG generation, vectorize, cut-outs       | `npx -y @recraft-ai/mcp-recraft-server`         | Recraft API key   |
| Replicate | Public and fine-tuned open models                    | `npx -y replicate-mcp`                          | Replicate token   |
| Figma     | Read specs/variables/screenshots; write to files     | `https://mcp.figma.com/mcp` or desktop `:3845`  | OAuth / Dev Mode  |

OpenAI image models have no official MCP server; call the Images API directly or hand the user the prompt.

This skill enhances Design Ops when MCP servers are available but does NOT require them. Without MCP servers, Design Ops provides detailed specifications and prompts that users can use manually with any generation tool.

---

### 3. Stitch MCP — UI Generation

#### Capabilities

Stitch is purpose-built for generating UI screens from natural language descriptions. Unlike general image models, Stitch understands UI primitives: navigation bars, cards, forms, data tables, modals, sidebars. Its output is structured, layouted, and component-aware.

**What Stitch Generates Well:**

- Full page layouts (dashboards, settings, profiles, feeds)
- Component compositions (card grids, form sections, navigation)
- Responsive variations (desktop, tablet, mobile)
- Light and dark mode variants
- Platform-specific UIs (iOS, Android, web)

**What Stitch Does NOT Do Well:**

- Photorealistic imagery (use Fal.ai or DALL-E for hero images)
- Custom illustrations (use Recraft or Midjourney)
- Animated prototypes (use Veo or Runway for motion)
- Pixel-perfect production code (use component-patterns-code skill for code)

#### Prompt Patterns for Stitch

**Layout Generation Pattern:**

```
Generate a [platform] [screen type] with:
- Navigation: [nav style + items]
- Layout: [grid/stack/split description]
- Content: [specific data to show]
- Style: [visual direction — reference product or design tokens]
- State: [default/loading/empty/error]
```

**Component Generation Pattern:**

```
Generate a [component name] component that:
- Contains: [child elements]
- Shows: [specific data]
- Supports: [interactions — hover, selected, disabled]
- Follows: [design system reference]
```

**Full Page Generation Pattern:**

```
Generate a complete [product type] [page name]:
- Header: [logo + nav items + user menu]
- Hero: [headline + subtext + CTA + visual]
- Section 1: [feature grid — 3 columns, icon + title + description]
- Section 2: [testimonials — carousel or grid]
- Section 3: [pricing — 3 tier cards with highlighted recommended]
- Footer: [links + social + newsletter signup]
Style: [reference product], [color palette], [typography]
```

#### Iteration Workflow with Stitch

**Round 1 — Broad Exploration:** Generate 3-4 variations with different layout approaches. Use general descriptions. Goal: find the right structural direction.

**Round 2 — Refinement:** Take the best layout and add specificity. Add exact content, adjust spacing descriptions, specify component variants. Goal: nail the composition.

**Round 3 — Polish:** Fine-tune typography descriptions, color references, spacing, and state variants. Generate light and dark modes. Goal: production-adjacent fidelity.

**Round 4 — Variants:** Generate the same screen for different breakpoints, different data states (empty, loading, error, populated), and edge cases (long text, missing images). Goal: completeness.

---

### 4. Image Generation Tools

#### Fal.ai — The Multi-Model Platform

fal provides access to a large model catalogue through a single API, making it the most versatile generation platform available. Key models for design work:

**FLUX Pro / FLUX.1 Dev:**

- Best for: High-fidelity UI mockup screenshots, product photography, realistic renders
- Strengths: Exceptional text rendering in images, photorealistic quality, fast generation
- Resolution: Up to 2048x2048, supports custom aspect ratios
- Prompt style: Descriptive, natural language, responds well to camera/lighting terminology
- Use case: Hero images, product shots, lifestyle imagery for landing pages

**FLUX Schnell:**

- Best for: Rapid iteration, concept exploration, batch generation
- Strengths: much faster and cheaper than FLUX Pro, good quality for drafts
- Use case: Quick visual explorations before committing to high-fidelity generation

**Imagen 4 (via Fal):**

- Best for: Photorealistic imagery with precise prompt adherence
- Strengths: Superior text rendering, excellent at following complex compositional prompts
- Use case: Marketing materials, product mockups, banner images

**Configuration for UI Asset Generation:**

```
Model: flux-pro (high fidelity) or flux-schnell (speed)
Resolution: Match target — 1440x900 for desktop hero, 390x844 for mobile, 1200x630 for OG image
Steps: 28-50 for Pro, 4 for Schnell
Guidance: 3.5-7.5 (higher = more prompt adherence, lower = more creative latitude)
```

#### Recraft V3 — Vector and Icon Generation

Recraft V3 is the only AI model capable of generating true SVG/vector output. This makes it indispensable for icon generation, logo exploration, and scalable illustrations.

**Vector Generation Capabilities:**

- SVG output — real vector paths, not rasterized images saved as SVG
- Consistent style across batch generations
- Icon sets with unified weight, style, and grid alignment
- Illustration styles: flat, line art, isometric, hand-drawn, geometric

**Icon Generation Best Practices:**

```
Prompt structure: "[icon subject] icon, [style], [weight], [grid], [color]"
Example: "Shopping cart icon, line style, 2px stroke, 24x24 grid, single color #1A1A2E"
Batch: Generate full sets by varying only the subject while keeping style tokens identical
```

**Illustration Style Presets:**

- **Corporate flat:** "flat vector illustration, geometric shapes, limited palette, no outlines, modern SaaS style"
- **Line art:** "continuous line illustration, single stroke weight, minimal detail, elegant, editorial"
- **Isometric:** "isometric 3D illustration, flat shading, consistent 30-degree angle, pastel palette"
- **Hand-drawn:** "hand-drawn sketch illustration, imperfect lines, warm, approachable, ink on paper feel"

**Brand Consistency Technique:**
To maintain brand consistency across multiple Recraft generations, anchor every prompt with the same style suffix:

```
Style anchor: ", [brand] style, [primary color] and [secondary color] palette, [illustration style], [line weight], consistent with previous generations"
```

#### Midjourney — High-Impact Visuals

Midjourney excels at generating visually striking imagery for hero sections, editorial illustrations, and marketing materials. It is not ideal for precise UI generation but unmatched for visual impact.

**Prompt Structure for UI/UX Work:**

```
[Subject description] --ar [aspect ratio] --style [raw/aesthetic] --stylize [0-1000] --v 6.1
```

**Key Parameters:**

- `--ar 16:9` — Desktop hero images
- `--ar 9:16` — Mobile hero images, app store screenshots
- `--ar 1:1` — Avatars, thumbnails, social media
- `--ar 3:2` — Blog post headers, card images
- `--style raw` — More literal prompt interpretation, better for specific UI needs
- `--stylize 50-150` — Lower values for more control, higher for more artistic flair
- `--no text, UI elements, buttons` — Negative prompts to avoid unwanted elements

**Best Use Cases in Design:**

- Hero section background imagery
- Editorial and blog illustrations
- Conceptual mood board imagery
- Abstract background patterns and textures
- Product lifestyle photography concepts
- Marketing campaign visuals

**Prompt Examples for Common Design Needs:**

```
Hero image: "Abstract gradient mesh, deep navy transitioning to electric violet, subtle grain texture, premium SaaS aesthetic --ar 16:9 --style raw --stylize 100"

Illustration: "Isometric workspace with laptop, coffee cup, and plant, soft pastel palette, minimal geometric style --ar 3:2 --stylize 200"

Background: "Subtle topographic line pattern, light grey on white, barely visible, clean minimal texture --ar 16:9 --style raw --stylize 50 --no color"
```

#### DALL-E 3 — Concept Art and Exploration

DALL-E 3 (via OpenAI) has strong prompt comprehension and excels at conceptual exploration, but produces softer, more painterly results than FLUX or Midjourney.

**Strengths:**

- Excellent text comprehension — understands complex, multi-part prompts
- Good at conceptual and metaphorical imagery
- Reliable text rendering within images
- Accessible via direct API (no Discord, no queue)
- Integrated editing capabilities (inpainting, outpainting)

**Limitations for UI Work:**

- Output tends toward illustrated/painterly rather than photorealistic
- Less control over exact style compared to Midjourney
- Resolution limited to 1024x1024, 1024x1792, or 1792x1024
- Cannot match the precision of Stitch for UI layouts
- No vector output capability

**Best Use Cases:**

- Early concept exploration (before committing to a style direction)
- Metaphorical illustrations for blog posts and marketing
- Placeholder imagery during wireframing
- Quick visual brainstorming during design workshops
- Social media graphics and promotional imagery

---

### 5. Video Generation

#### Veo 3.1 (Google, via Fal.ai)

Veo 3.1 generates high-quality video clips from text prompts, useful for prototype animations, product demos, and marketing content.

**Design Applications:**

- Animated hero sections (looping background videos)
- Product walkthrough animations
- Micro-interaction previews at scale
- Social media video ads and promotional clips
- App store preview videos (conceptual)

**Prompt Pattern:**

```
"Smooth UI animation showing [interaction]: [starting state] transitions to [ending state],
[platform] design style, [duration] seconds, [camera movement], clean background, 60fps"
```

#### Runway Gen-3 Alpha

Runway specializes in creative video generation with strong artistic control.

**Best For:**

- Stylized product videos with artistic flair
- Brand videos with specific mood and aesthetic
- Motion graphics concepts
- Cinematic product reveals

**Key Features:**

- Image-to-video (animate a static mockup)
- Motion brush (control where movement happens)
- Style reference (maintain visual consistency)

#### Pika

Pika focuses on quick, accessible video generation with simple controls.

**Best For:**

- Rapid prototype animation concepts
- Simple motion mockups for client presentations
- Social media short-form content
- Quick iteration on animation direction

**When to Use Which Video Tool:**

| Need                        | Tool         | Why                         |
| --------------------------- | ------------ | --------------------------- |
| Photorealistic product demo | Veo 3.1      | Best realism, longest clips |
| Artistic brand video        | Runway Gen-3 | Best creative control       |
| Quick motion concept        | Pika         | Fastest, simplest           |
| UI animation reference      | Veo 3.1      | Understands UI context      |
