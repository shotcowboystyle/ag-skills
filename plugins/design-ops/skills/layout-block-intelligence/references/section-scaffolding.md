# Section Scaffolding

Shared wrapper, header and custom-property code every block in this skill builds on.

## Section Wrapper (React/TSX + Tailwind)
```tsx
interface SectionProps {
  children: React.ReactNode;
  background?: 'white' | 'gray' | 'dark' | 'brand' | 'gradient';
  padding?: 'sm' | 'md' | 'lg' | 'xl';
  maxWidth?: 'narrow' | 'standard' | 'wide' | 'full';
  id?: string;
}

const paddingMap = { sm: 'py-8 md:py-12 lg:py-16', md: 'py-12 md:py-16 lg:py-20', lg: 'py-16 md:py-20 lg:py-24', xl: 'py-20 md:py-28 lg:py-32' };
const maxWidthMap = { narrow: 'max-w-3xl', standard: 'max-w-6xl', wide: 'max-w-7xl', full: 'max-w-full' };
const bgMap = { white: 'bg-white text-gray-900', gray: 'bg-gray-50 text-gray-900', dark: 'bg-gray-900 text-white', brand: 'bg-primary text-primary-foreground', gradient: 'bg-gradient-to-br from-primary to-primary/80 text-primary-foreground' }; // brand tokens from /style, never a stock blue→purple

export function Section({ children, background = 'white', padding = 'lg', maxWidth = 'standard', id }: SectionProps) {
  return (
    <section id={id} className={bgMap[background]}>
      <div className={`mx-auto px-4 sm:px-6 lg:px-8 ${maxWidthMap[maxWidth]} ${paddingMap[padding]}`}>{children}</div>
    </section>
  );
}
```

## Section Header
```tsx
export function SectionHeader({ label, title, description, align = 'center' }: { label?: string; title: string; description?: string; align?: 'left' | 'center' }) {
  const cls = align === 'center' ? 'text-center mx-auto' : 'text-left';
  return (
    <div className={`max-w-2xl mb-12 lg:mb-16 ${cls}`}>
      {label && <p className="text-sm font-semibold uppercase tracking-wider text-blue-600 mb-3">{label}</p>}
      <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold tracking-tight">{title}</h2>
      {description && <p className="mt-4 text-lg text-gray-600 leading-relaxed">{description}</p>}
    </div>
  );
}
```

## CSS Custom Properties
```css
:root {
  --section-py: clamp(3rem, 8vw, 7.5rem);
  --section-px: clamp(1rem, 5vw, 5rem);
  --section-max-width: 72rem;
  --section-title-size: clamp(1.875rem, 4vw, 3rem);
  --section-header-gap: clamp(2rem, 4vw, 4rem);
}
.section { padding: var(--section-py) var(--section-px); }
.section__inner { max-width: var(--section-max-width); margin-inline: auto; }
```

---
