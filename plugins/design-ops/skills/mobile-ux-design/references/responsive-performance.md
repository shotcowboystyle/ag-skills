# Responsive Layout and Mobile Performance UX

## Responsive Design Framework

### Breakpoint Strategy
- **Mobile-first CSS:** base styles for mobile, enhance with min-width media queries
- **Common breakpoints:** 320px (small phone), 375px (standard phone), 428px (large phone), 768px (tablet), 1024px (small desktop), 1440px (desktop)
- **Content-driven breakpoints** are superior to device-driven — break when the layout breaks
- **Container queries** (2025 standard) enable component-level responsiveness

### Responsive Patterns
- **Reflow:** Single column on mobile, multi-column on desktop
- **Reveal:** Show more content/controls as space allows
- **Collapse:** Tabs or expanded sections become accordion or hamburger
- **Prioritize:** Show different content hierarchies based on screen size
- **Scale:** Proportionally adjust sizes while maintaining ratios

### Responsive Typography
- Base font: 16px minimum on mobile (browser default, prevents zoom on iOS)
- Use fluid typography (clamp()) for smooth scaling between breakpoints
- Line length: 45-75 characters per line for readability (mobile often shorter is fine)
- Increase line-height on small screens (1.5-1.6) for touch-scroll readability

## Performance-Conscious Mobile UX

### Critical Performance Metrics
- **LCP (Largest Contentful Paint):** < 2.5s — the primary content must load fast
- **INP (Interaction to Next Paint):** < 200ms — every tap must paint a visual response quickly (INP replaced FID as a Core Web Vital in March 2024)
- **CLS (Cumulative Layout Shift):** < 0.1 — nothing should jump after rendering

### Performance UX Patterns
- **Skeleton screens** over spinners — show content shape before data arrives
- **Optimistic UI:** show the expected result immediately, roll back on failure
- **Lazy loading** for below-fold content and images
- **Offline-first architecture** for unreliable mobile networks — cache aggressively
- **Image optimization:** WebP/AVIF format, responsive srcset, lazy loading
