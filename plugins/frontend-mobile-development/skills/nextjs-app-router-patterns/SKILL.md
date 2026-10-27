---
name: nextjs-app-router-patterns
description: Master the Next.js 16 App Router with Server Components, Cache Components, streaming, parallel routes, and Server Actions. Use when building Next.js applications, implementing SSR/SSG, or optimizing React Server Components.
last_verified: 2026-10-27
---

# Next.js App Router Patterns

Comprehensive patterns for Next.js 16 App Router architecture, Cache Components, Server Components, and modern full-stack React development.

## When to Use This Skill

- Building new Next.js applications with App Router
- Migrating from Pages Router to App Router
- Implementing Server Components and streaming
- Setting up parallel and intercepting routes
- Optimizing data fetching and caching
- Building full-stack features with Server Actions

## Core Concepts

### 1. Rendering Modes

| Mode                  | Where        | When to Use                               |
| --------------------- | ------------ | ----------------------------------------- |
| **Server Components** | Server only  | Data fetching, heavy computation, secrets |
| **Client Components** | Browser      | Interactivity, hooks, browser APIs        |
| **Static shell**      | Build time   | Sync markup, imports, pure computation    |
| **Cached**            | Server cache | Shared data that tolerates staleness      |
| **Dynamic**           | Request time | `cookies()`/`headers()`, per-user data    |
| **Streaming**         | Progressive  | Large pages, slow data sources            |

### 2. File Conventions

```
app/
├── layout.tsx       # Shared UI wrapper
├── page.tsx         # Route UI
├── loading.tsx      # Loading UI (Suspense)
├── error.tsx        # Error boundary
├── not-found.tsx    # 404 UI
├── route.ts         # API endpoint
├── template.tsx     # Re-mounted layout
├── default.tsx      # Parallel route fallback
└── opengraph-image.tsx  # OG image generation
```

## Quick Start

```typescript
// app/layout.tsx
import { Inter } from 'next/font/google'
import { Providers } from './providers'

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: { default: 'My App', template: '%s | My App' },
  description: 'Built with Next.js App Router',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <Providers>{children}</Providers>
      </body>
    </html>
  )
}

// next.config.ts - opt in to Cache Components (Next.js 16+)
import type { NextConfig } from 'next'

const nextConfig: NextConfig = { cacheComponents: true }
export default nextConfig

// app/page.tsx - Server Component by default
import { cacheLife, cacheTag } from 'next/cache'

async function getProducts() {
  'use cache'
  cacheLife('hours') // fetch() is uncached by default since Next.js 15
  cacheTag('products')
  const res = await fetch('https://api.example.com/products')
  return res.json()
}

export default async function HomePage() {
  const products = await getProducts()

  return (
    <main>
      <h1>Products</h1>
      <ProductGrid products={products} />
    </main>
  )
}
```

## Detailed patterns and worked examples

Detailed pattern documentation lives in `references/details.md`. Read that file when the navigation tier above is insufficient.

## Best Practices

### Do's

- **Start with Server Components** - Add 'use client' only when needed
- **Colocate data fetching** - Fetch data where it's used
- **Use Suspense boundaries** - Enable streaming for slow data
- **Leverage parallel routes** - Independent loading states
- **Use Server Actions** - For mutations with progressive enhancement; call `updateTag()` for read-your-writes
- **Cache explicitly** - Mark shared data with `'use cache'` + `cacheLife()`/`cacheTag()`; nothing is cached implicitly

### Don'ts

- **Don't pass non-serializable props to Client Components** - functions, class instances and Symbols cannot cross the Server → Client boundary (Server Actions are the exception)
- **Don't use hooks in Server Components** - No useState, useEffect
- **Don't fetch initial data in Client Components** - Fetch in Server Components; use TanStack Query only for client-driven refetching
- **Don't over-nest layouts** - Each layout adds to the component tree
- **Don't ignore loading states** - Always provide loading.tsx or Suspense
