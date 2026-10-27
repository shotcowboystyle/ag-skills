# Extended Easing and Spring Catalog

The base tokens (`--ease-out`, `--ease-in`, `--ease-in-out`, `--ease-spring`,
`--duration-*`, and the `spring-snappy` / `spring-default` / `spring-gentle` /
`spring-bouncy` presets) are owned by `interaction-motion-design`
(`animation-timing-curves.md`) and repeated in this skill's
SKILL.md. This file is the extended catalog on top of them. Reach for an
extended curve only when a base token measurably reads wrong for the recipe.

Removed as duplicates of a base token: `--ease-out-expo` (= `--ease-out`),
`--ease-in-cubic` (= `--ease-in`), `--ease-out-back` and `--bounce`
(= `--ease-spring`), `--bounce-heavy` (= `--spring-bouncy`).

```css
:root {
  /* === Decelerate variants (entrances) === */
  --ease-out-soft:     cubic-bezier(0.33, 1, 0.68, 1);        /* Gentle decelerate */
  --ease-out-quad:     cubic-bezier(0.25, 0.46, 0.45, 0.94);  /* Quadratic decelerate */
  --ease-out-cubic:    cubic-bezier(0.22, 0.61, 0.36, 1);     /* Cubic decelerate */
  --ease-out-quart:    cubic-bezier(0.17, 0.84, 0.44, 1);     /* Quartic decelerate */
  --ease-out-quint:    cubic-bezier(0.23, 1, 0.32, 1);        /* Quintic decelerate */
  --ease-out-circ:     cubic-bezier(0.08, 0.82, 0.17, 1);     /* Circular decelerate */

  /* === Accelerate variants (exits) === */
  --ease-in-soft:      cubic-bezier(0.32, 0, 0.67, 0);        /* Gentle accelerate */
  --ease-in-quad:      cubic-bezier(0.55, 0.085, 0.68, 0.53); /* Quadratic accelerate */
  --ease-in-quart:     cubic-bezier(0.9, 0.03, 0.69, 0.22);   /* Quartic accelerate */
  --ease-in-expo:      cubic-bezier(0.7, 0, 0.84, 0);         /* Exponential accelerate */
  --ease-in-back:      cubic-bezier(0.36, 0, 0.66, -0.56);    /* Pull-back accelerate */

  /* === Symmetric variants (movement) === */
  --ease-in-out-soft:  cubic-bezier(0.45, 0, 0.55, 1);        /* Gentle symmetric */
  --ease-in-out-quad:  cubic-bezier(0.46, 0.03, 0.52, 0.96);  /* Quadratic symmetric */
  --ease-in-out-cubic: cubic-bezier(0.65, 0, 0.35, 1);        /* Cubic symmetric */
  --ease-in-out-back:  cubic-bezier(0.68, -0.6, 0.32, 1.6);   /* Overshoot symmetric */

  /* === Elastic (requires @keyframes for true elastic) === */
  --elastic-out:       cubic-bezier(0.36, 1.7, 0.5, 0.85);    /* Approximation of elastic */

  /* === Emphasis === */
  --emphasis-dramatic:  cubic-bezier(0.04, 0.62, 0.23, 0.98);
  --emphasis-energetic: cubic-bezier(0.22, 0.68, 0, 1.71);

  /* === Platform approximations (canonical platform specs: platform-visual-standards) === */
  --ios-spring:        cubic-bezier(0.25, 0.8, 0.25, 1);      /* iOS default animation */
  --material-standard: cubic-bezier(0.2, 0, 0, 1);            /* M3 standard / emphasized fallback */
  --material-decel:    cubic-bezier(0, 0, 0, 1);              /* M3 decelerate */
  --material-accel:    cubic-bezier(0.3, 0, 1, 1);            /* M3 accelerate */
}
```

## Extended Framer Motion Springs

Beyond the four base presets. Use only when the recipe says why.

```tsx
// Wobbly — emphasis, attention-grab (more oscillation than spring-bouncy)
const springWobbly = { type: "spring", stiffness: 150, damping: 8, mass: 1 };

// Slow — large-area reveals where spring-gentle still feels quick
const springSlow = { type: "spring", stiffness: 80, damping: 20, mass: 1.2 };
```

Platform-matching springs (iOS, Material 3 Expressive) are owned by
`platform-visual-standards`; do not approximate them here.
