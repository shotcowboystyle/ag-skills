# Desktop Interaction Patterns

Dashboards, charts and data tables (sorting, filtering, density, inline editing, grid vs. table) are owned by `data-visualization-mastery`; see its `dashboards-and-tables.md` and `data-table-mastery.md`.

---

## Master-Detail Patterns

### List-Detail (Side-by-Side)

The dominant desktop pattern for entity management. Display a scrollable list or table in the left panel (30-40% width) and the selected item's detail in the right panel (60-70% width). Update the detail panel on list selection without full page reload. Support keyboard navigation: arrow keys traverse the list, Enter opens detail. Persist the split ratio and allow resizing.

### Split View (Horizontal)

Use a top-bottom split when the list and detail have wide layouts that benefit from full horizontal width. The top panel shows the list or table; the bottom panel shows the detail. This works well for code review tools (file list on top, diff below) and email clients (inbox on top, message below). Allow collapsing either pane.

### Drawer Detail

Slide a detail panel in from the right edge of the screen as an overlay or push panel. Use drawers when the user needs to peek at detail without losing the context of the full list. Close the drawer to return to the list. Drawers work well when the detail view is secondary or temporary (previewing a record before deciding to navigate to its full page).

**Drawer sizing.** Small drawers (320-400px) suit simple metadata views. Medium drawers (480-640px) suit forms and multi-section detail. Large drawers (50-70% viewport width) suit complex detail with sub-tabs and embedded tables.

### Modal Detail

Open a modal dialog to display record detail. Use modals when the detail requires focused attention and the user should complete an action (approve, edit, configure) before returning to the list. Avoid modals for read-only browsing -- the overhead of opening and closing modals disrupts scanning workflows. Ensure modals support keyboard dismiss (Escape) and click-outside-to-close (unless data loss is a risk).

---

## Complex Form Design

### Multi-Section Forms

Organize long forms into logical sections with visible headings (General, Contact, Billing, Permissions). Use one of these layout strategies:

- **Vertical accordion.** All sections visible as collapsed headers; expand one or more at a time. Best for forms where users fill sections non-linearly.
- **Tabbed sections.** Each section in a horizontal tab. Best when sections are independent and users may skip irrelevant ones.
- **Single scrollable page.** All sections expanded in a continuous scroll with a sticky table-of-contents sidebar for jump navigation. Best for forms where users fill top to bottom.

### Nested Entities

When a form includes related sub-entities (an order with line items, a project with team members), display the sub-entities in an embedded table or repeatable section. Provide "Add item" and "Remove item" actions. Validate sub-entities independently and roll up errors to the parent form. Support reordering of sub-entities via drag-and-drop.

### Dynamic Forms

Implement conditional logic that shows, hides, or modifies fields based on other field values. When a field becomes visible due to a condition, animate it into view (slide-down, 150ms) to communicate the causal relationship. Clearly label required fields that appear conditionally -- users may not realize they exist until the condition triggers. Maintain form state for hidden fields so data is not lost if the user toggles a condition back and forth.

---

## Wizard Pattern

### Multi-Step Workflows with Branching Logic

Use the wizard pattern when a complex process must be completed in a specific order and the full form would overwhelm users if presented at once.

**Progress indicator.** Display a step indicator at the top showing all steps as numbered or named nodes connected by a line. Highlight the current step, mark completed steps with a checkmark, and dim future steps. For processes with more than 7 steps, group steps into phases.

**Navigation controls.** Provide Back and Next buttons at the bottom of each step. Disable Next until required fields are complete. Allow clicking completed steps in the progress indicator to navigate back non-linearly.

**Branching logic.** When the workflow path varies based on user input (e.g., a different set of configuration steps for different product types), update the progress indicator dynamically to reflect the actual steps for this user's path. Never show steps that the user will not reach.

**Data persistence.** Save wizard state after every step. If the user navigates away and returns, restore the wizard to the last completed step. Store state server-side for multi-session workflows (e.g., loan applications that take days to complete).

**Review step.** Include a final review step that summarizes all inputs across all steps in a read-only format. Provide "Edit" links next to each section that jump back to the relevant step. Only enable the final Submit action from the review step.

**Error recovery.** If submission fails after the review step, return the user to the review step with the error clearly displayed. Never silently reset the wizard to step 1.

---

## Command Palette Design

### Implementation

The command palette is the most transformative desktop UX pattern of the 2020s. It provides a keyboard-activated search interface for accessing any action, navigation target, or entity in the application.

**Activation.** Bind to Cmd+K (macOS) / Ctrl+K (Windows/Linux). Support alternative bindings (Cmd+P for file search, Cmd+Shift+P for commands, following VS Code conventions). Open the palette as a centered modal overlay with a prominent search input.

**Architecture.** Index three categories of items:

1. **Actions.** Application commands: "Create new project," "Export CSV," "Toggle dark mode," "Open settings." Prefix with a verb.
2. **Navigation.** Pages and views: "Go to Dashboard," "Go to User Management," "Open Billing." Prefix with "Go to" or "Open."
3. **Entities.** Searchable records: specific users, projects, orders, documents. Display the entity type as a badge.

### Action Organization

Group results by category with section headers. Display the most relevant result highlighted at the top. Show keyboard shortcut hints (if any) next to action items. Limit visible results to 8-10 with a scrollable overflow. Display "No results" with a helpful suggestion ("Try searching for a user or action").

### Fuzzy Matching

Implement fuzzy search that tolerates typos, partial matches, and abbreviations. Highlight matching characters in the result labels. Weight recent actions and frequently used commands higher in the ranking. Support scoping: allow typing a prefix to filter to a category (e.g., ">" for commands, "@" for users, "#" for projects -- following conventions established by VS Code and Slack).

---

## Keyboard Shortcut System Design

### Discovery

Users cannot use shortcuts they do not know about. Implement multiple discovery mechanisms:

- **Shortcut overlay.** Open with ? or Ctrl+/ showing all available shortcuts organized by category. Implement as a modal or panel.
- **Tooltip hints.** Display keyboard shortcuts in all tooltips for toolbar buttons and menu items.
- **Menu annotations.** Show shortcut keys right-aligned in dropdown menus and context menus.
- **Command palette.** Show shortcuts next to matching commands.
- **Onboarding prompts.** After a user performs an action with the mouse 3-5 times, display a transient hint: "Tip: Press Ctrl+S to save."

### Customization

Allow power users to remap keyboard shortcuts. Provide a settings panel listing all commands with their current bindings. Support recording a new binding by pressing the desired key combination. Detect and display conflicts immediately: "Ctrl+D is already bound to 'Delete item.' Replace?"

### Conflict Resolution

Reserve platform-standard shortcuts and never override them: Cmd/Ctrl+C (copy), Cmd/Ctrl+V (paste), Cmd/Ctrl+Z (undo), Cmd/Ctrl+W (close tab), Cmd/Ctrl+T (new tab in browser). Use modifier escalation for application-specific commands: Cmd+Shift+K instead of Cmd+K if Cmd+K conflicts with browser behavior. Document which shortcuts differ between macOS and Windows/Linux. Detect the user's platform and display the correct modifier key labels.

---

## Multi-Window and Panel Layouts

### Docking Systems

Implement a docking layout where panels can be attached to edges (left, right, top, bottom) or stacked as tabs within a dock zone. Visual indicators (highlighted zones, snap guides) show where the panel will dock when the user drags it near an edge. Store the complete dock layout as a serializable JSON structure for persistence and sharing.

### Floating Panels

Allow panels to detach from the dock and float as independent windows within the application viewport (or as separate OS windows for Electron/Tauri apps). Floating panels are essential for multi-monitor workflows: a user may float an inspector panel onto a secondary monitor while the main workspace occupies the primary monitor. Ensure floating panels maintain data synchronization with the main window.

### Snapping and Resize

Support snap-to-grid behavior when resizing panels. Define minimum and maximum panel sizes to prevent panels from becoming too small to be functional or too large to leave room for peers. Display a resize cursor on panel borders. Implement double-click on a resize handle to auto-size the panel to its content or to a predefined default width.

### Workspaces

Allow users to save and switch between named workspace layouts: "Development" (code editor + terminal + file tree), "Review" (diff viewer + comments + file list), "Debugging" (variables + call stack + breakpoints + console). Store workspaces per user. Provide quick switching via a workspace selector in the toolbar or through the command palette.

---

## Drag and Drop Design

### Visual Feedback

Provide continuous visual feedback throughout the drag lifecycle:

1. **Grab.** On mousedown + mousemove (or after a 150ms hold to distinguish from click), attach the dragged item to the cursor as a semi-transparent ghost (60-70% opacity). Apply a subtle lift shadow to the ghost to create a sense of elevation.
2. **Drag.** Highlight valid drop targets with a dashed border or color fill as the ghost passes over them. Dim or disable invalid drop targets. If the drag is for reordering within a list, show an insertion indicator (horizontal line) between items where the drop would land.
3. **Drop.** On release over a valid target, animate the item into its new position (200ms ease-out). On release over an invalid area, animate the ghost back to its origin (snap-back). Provide a brief visual confirmation (flash, checkmark) on successful drop.

### Drop Targets

Design drop targets to be large and forgiving. Expand the hit area beyond the visible boundary of the target element. For tree structures, expanding a collapsed node on hover-over-while-dragging (auto-expand after 500ms hover) allows users to drag items deep into nested hierarchies without manually expanding first.

### Accessibility Alternatives

Drag and drop is inaccessible to keyboard-only and screen reader users by default. Provide a parallel interaction: select the item, invoke a "Move" action (from context menu or keyboard shortcut), then select the destination from a list or tree dialog. Announce the operation via ARIA live regions: "Item 'Project Alpha' selected for move. Choose destination." Do not use `aria-grabbed` or `aria-dropeffect`: both are deprecated in ARIA 1.1 and poorly supported. The parallel interaction and live-region announcements carry the accessibility.

---

## Right-Click Context Menus

### Design Patterns

Right-click context menus surface the most relevant actions for the clicked element. Open the menu at the cursor position. Ensure the menu does not overflow the viewport -- flip vertically or horizontally if the cursor is near an edge.

**Anatomy.** Organize menu items into groups separated by dividers:

1. **Primary actions** at the top: Open, Edit, View Detail.
2. **Transfer actions** in the middle: Copy, Cut, Paste, Duplicate, Move.
3. **Modification actions:** Rename, Change Status, Tag, Assign.
4. **Destructive actions** at the bottom, visually separated: Delete, Archive. Display destructive items in red text.

**Display keyboard shortcuts** right-aligned on each menu item. Display disabled items as grayed-out text with an optional tooltip explaining why the action is unavailable. Limit the menu to 10-12 items -- use submenus sparingly and never nest more than one level deep.

### Keyboard Access

Support Menu key (or Shift+F10) to open the context menu for the focused element. Allow full keyboard navigation within the menu: arrow keys to traverse, Enter to select, Escape to close. First item in the menu should receive focus automatically on open.

### Adaptive Context Menus

Adjust the menu contents based on the selection context. A single-row context menu differs from a multi-row context menu (bulk actions become available). A right-click on a column header offers column-specific actions (sort, filter, hide column, freeze column). A right-click on a chart element offers chart-specific actions (drill-down, exclude, highlight).

---

## Tree View and File Browser Patterns

Implement tree views for hierarchical data: file systems, organizational structures, category taxonomies, nested configurations.

**Visual design.** Indent each level by 16-24px. Display expand/collapse chevrons for nodes with children. Use connection lines (indentation guides) to clarify parent-child relationships in deep trees. Display an icon appropriate to the node type (folder, file, user, tag).

**Interaction.** Click to select a node. Double-click or Enter to open/activate a node. Single-click the chevron or press Right Arrow to expand; Left Arrow to collapse. Left Arrow on an already-collapsed node moves focus to the parent. Support multi-select with Ctrl+Click (individual) and Shift+Click (range).

**Lazy loading.** For large trees, load children on demand when a node is expanded. Display a loading spinner in place of children during fetch. Cache expanded state so that collapsing and re-expanding a node does not trigger a new fetch if the data has not changed.

**Drag and drop.** Support dragging nodes to rearrange hierarchy (move a file to a different folder, reassign a team member to a different department). Auto-expand collapsed target nodes after 500ms of hover. Validate the move (prevent circular references, enforce depth limits) and display an error if the drop is invalid.

**Search and filter.** Provide a search input above the tree that filters to matching nodes. When filtering, display matching nodes with their ancestor chain (maintain hierarchy context) while hiding non-matching branches. Highlight the matching text within node labels.

---

## Split-Pane Interfaces

### Horizontal and Vertical Splits

Allow the user to divide the workspace into two or more panes arranged horizontally (side-by-side) or vertically (stacked). Support nested splits: a horizontal split where the right pane is itself vertically split. Common in code editors (multi-file editing), email clients (folder tree | inbox | message), and comparison tools (before | after).

### Resize Handles

Display a visible resize handle (4-8px wide/tall) between adjacent panes. Change the cursor to col-resize or row-resize on hover. Support drag to resize with real-time content reflow. Double-click the resize handle to reset panes to equal sizes or to collapse one pane.

### Collapse Behavior

Allow any pane to collapse to zero width/height, effectively maximizing the adjacent pane. Provide a collapse button (chevron) on the resize handle or pane header. When collapsed, display a thin rail (8-16px) with an expand button to restore the pane. Preserve the pane's content state during collapse so no data is lost on restore.

**Keyboard shortcuts.** Bind shortcuts to toggle pane visibility: Cmd+B for sidebar, Cmd+J for bottom panel (following VS Code conventions). Support Cmd+\ to split the current pane.

---

## Notification Center

### In-App Notification Design

Implement a notification center accessible from a bell icon in the application header. Display an unread count badge on the icon (numeric for 1-99, "99+" for higher counts). Open the notification center as a dropdown panel or slide-in drawer.

**Notification anatomy:**

1. **Icon.** Reflects notification type: info (blue circle), success (green checkmark), warning (amber triangle), error (red circle), system (gray gear).
2. **Title.** Brief summary in bold: "Deployment completed," "Review requested."
3. **Body.** One to two lines of detail: "Your deployment to staging-env succeeded in 3m 42s."
4. **Timestamp.** Relative time ("5 minutes ago," "Yesterday at 3:42 PM").
5. **Action.** An optional primary action button: "View deployment," "Review now."

### Badge Management

Clear the unread badge when the user opens the notification center. Mark individual notifications as read when the user interacts with them (click, expand, dismiss) or provide a "Mark all as read" action. Persist read/unread state server-side.

### Read/Unread States

Visually distinguish unread notifications with a bold title, a colored left border or dot, and a slightly different background color. Read notifications use normal-weight text and neutral styling. Support marking a notification as unread (for reminders). Provide filtering controls in the notification center: All, Unread, Read, by type.

### Notification Preferences

Allow users to configure which notification types they receive in-app, by email, or not at all. Provide a matrix: rows are notification types (deployment, review request, system alert), columns are channels (in-app, email, Slack, SMS). Respect "Do not disturb" modes that suppress non-critical notifications.

---

## Bulk Operation Patterns

### Selection Mechanisms

**Checkbox selection.** Place a checkbox in the first column of each row. Display a header checkbox for "Select all on this page." Provide a "Select all N items" link after the header checkbox is checked to extend selection across all pages.

**Range selection.** Click the first item, then Shift+Click the last item to select the entire range. Support Ctrl/Cmd+Click to toggle individual items in and out of the selection without deselecting others.

**Lasso/Marquee selection.** In spatial layouts (kanban boards, canvas tools), support click-drag to draw a selection rectangle around multiple items.

### Action Toolbar

Display a contextual action toolbar when one or more items are selected. Position it above the table (sticky) or as a floating bar at the bottom of the viewport. Display the selection count: "47 items selected." Provide bulk actions: Delete, Change Status, Assign, Tag, Export, Move. Highlight destructive actions in red and require confirmation.

### Progress Tracking

For bulk operations that take time (deleting 500 records, sending 200 emails, processing 1,000 imports), display a progress indicator: determinate progress bar with percentage and item count ("Processing 342 of 1,000..."). Allow cancellation mid-operation. On completion, display a summary: "Successfully processed 987 of 1,000. 13 failed. View errors."

---

## Infinite Canvas and Spatial Workspace Design

### The Infinite Canvas Mental Model

Infinite canvas interfaces (Figma, Miro, Mural, tldraw) replace linear page-based layouts with a two-dimensional spatial plane that users navigate by panning and zooming. The canvas has no fixed boundaries -- content can be placed anywhere.

**Camera controls.** Implement pan via middle-click-drag, Space+click-drag, or two-finger trackpad scroll. Implement zoom via Ctrl/Cmd+scroll, pinch gesture, or zoom controls in the toolbar. Display a zoom level indicator (e.g., "75%") with quick-access presets: Zoom to Fit, Zoom to Selection, 100%. Constrain zoom range (e.g., 10%-6400%) to prevent disorientation.

**Minimap.** Display a small overview map in the corner showing the entire canvas with a viewport indicator rectangle. Allow clicking the minimap to navigate directly to a region. The minimap is especially important for large canvases where spatial awareness would otherwise be lost.

### Object Manipulation

**Selection.** Click to select a single object. Click-drag on empty space to create a marquee selection box. Shift+Click to add/remove objects from selection. Display selection handles (resize, rotate) on the selected object's bounding box.

**Transform.** Drag to move. Drag handles to resize (hold Shift to maintain aspect ratio, hold Alt to resize from center). Drag rotation handle to rotate (hold Shift to snap to 15-degree increments). Display real-time dimension labels during transform.

**Alignment and distribution.** Provide smart guides (magenta snap lines) that appear when objects align with each other's edges or centers. Offer explicit alignment actions: align left/center/right, align top/middle/bottom, distribute horizontally/vertically with equal spacing.

**Layering.** Support z-order: bring to front, send to back, bring forward, send backward. Display layers in an optional layers panel for complex compositions.

### Performance

Render only objects within the current viewport (frustum culling). For very large canvases (10,000+ objects), implement level-of-detail rendering: show simplified representations at low zoom levels and full detail only when zoomed in. Use WebGL or Canvas 2D for rendering rather than DOM elements for canvases with more than a few hundred objects.

---

## Undo/Redo Architecture

### Single Action Undo

Implement Cmd/Ctrl+Z for undo and Cmd/Ctrl+Shift+Z (or Cmd/Ctrl+Y) for redo. Maintain an undo stack of individual actions. Each action on the stack stores sufficient information to reverse the operation (previous value, previous position, previous state). Display the action name in the Edit menu: "Undo Delete Item" rather than just "Undo."

### Grouped Undo

Group related sub-actions into a single undo unit when they form a logical operation from the user's perspective. For example, a drag-and-drop that moves an item from one list to another may involve a "remove from source" and "add to target" at the data level, but the user should undo both in a single Cmd+Z. Define grouping boundaries explicitly: begin a group before the compound operation and close it after.

Typing in a text field presents a special grouping challenge. Do not create an undo entry for every character -- group characters typed within a continuous burst (no pause longer than 500ms-1s) into a single undo unit. Start a new group after a pause, a cursor move, or a formatting change.

### Undo History Panel

For advanced applications (design tools, document editors, audio/video editors), provide an undo history panel that lists all actions chronologically. Allow clicking any entry to jump to that state (undoing all subsequent actions). Display a visual separator between saved checkpoints. Graying out actions above the current position communicates what will be lost if the user makes a new edit from a historical state (which forks the history, discarding the grayed entries).

### Architecture Considerations

**Command pattern.** Implement undo/redo using the Command pattern: each user action is an object with execute() and undo() methods. Push executed commands onto the undo stack. On undo, pop the top command and call its undo() method, pushing it onto the redo stack. On redo, pop from the redo stack, call execute(), and push back onto the undo stack.

**Stack depth.** Limit the undo stack to a reasonable depth (50-200 actions) to bound memory usage. Discard the oldest entries when the limit is reached. For document-centric applications, consider persisting the undo history to disk so it survives application restarts.

**Collaboration considerations.** In multi-user real-time environments, undo becomes significantly more complex. An undo must reverse the current user's action without affecting concurrent edits by other users. Implement operational transformation (OT) or conflict-free replicated data types (CRDTs) to manage concurrent undo. Display a notice when an undo cannot be cleanly applied due to a conflict: "Your change was modified by another user. Undo may produce unexpected results."

**Selective undo.** Some advanced applications allow undoing a specific past action without undoing subsequent actions (non-linear undo). This requires computing the inverse of the selected action and applying it as a new forward action. This is complex to implement correctly and should only be offered when the application domain demands it (e.g., version control systems, advanced audio editors).

---

## Quick Rules: Workflows, Keyboard, Panels, Enterprise UI

### Complex Workflow Design

#### Multi-Step Workflows
- **Progress indicator:** Show current step, total steps, and completion state
- **Non-linear navigation:** Allow jumping to completed steps for editing
- **Save draft at every step** — never lose user work on navigation
- **Summary/review step** before final submission
- **Clear step labels** that describe the content, not just "Step 1, Step 2"

#### Form-Heavy Interfaces
- **Section grouping** with clear headings and optional collapse
- **Contextual help** near complex fields — info icons with tooltips or inline descriptions
- **Dependent fields:** Show/hide fields based on previous selections
- **Auto-save with visual confirmation** (subtle "Saved" indicator)
- **Validation summary** at top of form linking to each error field

#### Master-Detail Pattern
- **List/grid on left, detail panel on right** — the dominant desktop productivity pattern
- Support resizable split panes
- Detail panel updates without full page reload
- Keyboard navigation: arrow keys traverse list, Enter opens detail, Escape returns to list
- Mobile adaptation: replace side-by-side with stack navigation

### Keyboard-First Interaction

#### Essential Keyboard Patterns
- **Global shortcuts:** Document common shortcuts in an overlay (? or Ctrl+/)
- **Command palette:** Cmd/Ctrl+K for quick action access — the most important desktop UX innovation of the 2020s
- **Tab order:** Logical focus progression through interactive elements
- **Focus indicators:** Always visible, high-contrast focus rings (never remove outline without replacement)
- **Escape key:** Consistently closes modals, dropdowns, and cancels operations

#### Shortcut Design Rules
- Follow platform conventions (Ctrl/Cmd+S = Save, Ctrl/Cmd+Z = Undo)
- Avoid overriding browser shortcuts
- Use modifier combinations logically: Ctrl = action, Shift = modify/extend, Alt = alternate
- Provide visual shortcut hints in menus, tooltips, and command palette

### Multi-Window and Panel Management

#### Panel Patterns
- **Sidebar navigation:** Collapsible, persistent across views, icon+label or icon-only modes
- **Inspector panels:** Right-side contextual properties panel (design tool pattern)
- **Bottom panels:** Console, log, terminal outputs — resizable with collapse
- **Floating panels:** Detachable for multi-monitor workflows

#### State Management
- Persist panel states (open/closed, sizes) across sessions
- Remember user's last-used view and filters
- Support workspace presets ("Developer layout", "Review layout")
- Handle window resize gracefully — responsive desktop is essential for varied monitor sizes

### Enterprise UI

#### Permission-Aware UI
- Hide elements users cannot access (not just disable) for cleaner interfaces
- For disabled elements that provide context, show tooltip explaining why access is restricted
- Role-based views: admin sees all controls, viewer sees read-only, etc.
- Audit trails for sensitive actions with clear attribution

#### Notification and Alert Design
- **Severity levels:** Info (blue), Success (green), Warning (amber), Error (red), Critical (red + icon)
- **Position:** Non-blocking toasts for confirmations, blocking modals for critical decisions
- **Persistence:** Success toasts auto-dismiss (3-5s), errors persist until addressed
- **Grouping:** Batch similar notifications to prevent notification fatigue

#### Empty States and Onboarding
- First-run experience should guide users to first value moment
- Empty states include illustration, explanation, and clear CTA to populate the view
- Progressive onboarding: introduce features as they become relevant, not all at once
- In-app guidance: highlight new features with subtle callouts, dismissible permanently

---

## Key Sources

- Cooper, A., Reimann, R., Cronin, D., and Noessel, C. (2014). *About Face: The Essentials of Interaction Design.* 4th ed. Wiley.
- Tidwell, J., Brewer, C., and Valencia, A. (2020). *Designing Interfaces: Patterns for Effective Interaction Design.* 3rd ed. O'Reilly.
- Microsoft Fluent 2 Design System -- Data grid, command bar, and panel patterns.
- Apple macOS Human Interface Guidelines -- Sidebars, split views, and table views.
- ARIA Authoring Practices Guide (APG) -- Treegrid, table, dialog, and drag-and-drop patterns.
- Figma engineering blog -- Canvas rendering architecture and performance.
- VS Code UX guidelines -- Command palette, keyboard shortcuts, and panel layout.
- Nielsen Norman Group -- Enterprise UX research on complex application design.
