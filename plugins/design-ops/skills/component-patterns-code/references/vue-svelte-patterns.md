# Vue 3 and Svelte 5 Component Patterns

The React patterns in `component-api-and-composition.md` map onto Vue and Svelte
as follows: compound components become provide/inject (Vue) or context (Svelte),
render props and slot props become named slots (Vue) or snippets (Svelte).

## Slots (Vue/Svelte): Named Content Injection Points

```vue
<template>
  <Card>
    <template #header>Title</template>
    <template #content>Body text</template>
    <template #footer><Button>Action</Button></template>
  </Card>
</template>
```

## Vue 3: Composables (provide/inject compound components)

```ts
// tabs-context.ts — shared key, imported by parent and children
import type { InjectionKey, Ref } from "vue";

export interface TabsContext {
  activeTab: Ref<string>;
  setActive: (id: string) => void;
}

export const TabsKey: InjectionKey<TabsContext> = Symbol("tabs");
```

```vue
<!-- Tabs.vue (parent) -->
<script setup lang="ts">
import { ref, provide } from "vue";
import { TabsKey } from "./tabs-context";

const activeTab = ref("tab-1");
provide(TabsKey, {
  activeTab,
  setActive: (id: string) => {
    activeTab.value = id;
  },
});
</script>
```

```vue
<!-- Tab.vue (child) -->
<script setup lang="ts">
import { computed, inject } from "vue";
import { TabsKey } from "./tabs-context";

const props = defineProps<{ id: string }>();
const tabs = inject(TabsKey);
if (!tabs) throw new Error("Tab must be used within Tabs");
const isActive = computed(() => tabs.activeTab.value === props.id);
</script>
```

## Svelte 5: Runes

```svelte
<script lang="ts">
  interface Props {
    variant?: 'primary' | 'secondary';
    size?: 'sm' | 'md' | 'lg';
    onclick?: () => void;
    children: import('svelte').Snippet;
  }

  let { variant = 'primary', size = 'md', onclick, children }: Props = $props();

  const classes = $derived(
    `btn btn-${variant} btn-${size}`
  );
</script>

<button class={classes} {onclick}>
  {@render children()}
</button>
```
