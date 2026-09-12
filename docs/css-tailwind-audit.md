# CSS / Tailwind Audit

This audit documents the current `base.css` role after replacing the Tailwind CDN with a compiled Bun/Tailwind build.

## Current split

- `core/static/core/css/tailwind.css`: generated utility CSS from Tailwind.
- `core/static/core/css/base.css`: custom brand, component, animation, and content CSS.

Target direction: keep Tailwind for simple layout/spacing/responsive utilities, and keep `base.css` for site identity and complex components.

## `base.css` size

Current size: ~2,055 lines.

Large, but still manageable. No immediate need for SCSS or CSS splitting.

## Section inventory

| Section | Lines | Decision |
| --- | ---: | --- |
| Design tokens / base document styles | 1-37 | Keep |
| Utility classes | 38-46 | Review gradually |
| Navigation | 47-116 | Keep for brand styling; layout may move to Tailwind |
| Nav dropdown | 117-197 | Keep for Alpine/dropdown component styling |
| Section utilities | 198-237 | Keep |
| Divider | 238-250 | Keep or replace later if trivial |
| Hero | 251-371 | Keep |
| Page-level waves | 372-445 | Keep |
| Floating particles | 446-496 | Keep |
| Hero photo | 497-520 | Keep |
| Page layout | 521-537 | Candidate for Tailwind/container utilities |
| Writing / essay grid | 538-589 | Keep for now |
| Contact page/layout/sidebar/result | 590-748 | Keep for now |
| About page | 749-974 | Keep for now |
| Classes page | 975-1097 | Keep for now |
| Consultancy page | 1098-1124 | Keep for now |
| Work / portfolio page | 1125-1235 | Keep for now |
| Mentoring page | 1236-1347 | Keep for now |
| Footer | 1348-1366 | Candidate for Tailwind utilities |
| Forms / crispy overrides | 1367-1437 | Keep |
| Post content / CKEditor output | 1438-1571 | Keep |
| Confirmation dialog | 1572-1679 | Keep |
| Scroll reveal | 1680-1715 | Keep |
| Pagination | 1716-1750 | Keep for now |
| Related posts | 1751-1763 | Candidate after template cleanup |
| Responsive rules | 1764-2053 | Review gradually as templates move to Tailwind |

## Keep in `base.css`

These are not good Tailwind migration targets right now:

1. **Design tokens**
   - `:root` variables
   - font families
   - brand colors
   - navbar height
   - transition token

2. **Global body theme**
   - warm gradient background
   - font smoothing
   - base text color/line-height

3. **Custom visual identity**
   - hero typography
   - waves
   - particles
   - photo treatment
   - warm links
   - section titles

4. **Complex components**
   - nav dropdown
   - confirmation dialog
   - reveal animation
   - post content rendering
   - CKEditor/code-block styling

5. **Crispy form overrides**
   - `.warm-form` should stay because it deliberately overrides crispy/Tailwind defaults.

## Good Tailwind migration candidates

Move these only when touching nearby templates:

1. **Simple layout wrappers**
   - `.page-layout`
   - `.page-prose`
   - simple `container`/padding combinations

2. **Simple footer styling**
   - footer padding
   - centered text
   - small text sizing

3. **Simple responsive layout behavior**
   - single-column mobile grid switches
   - basic flex direction changes
   - simple gaps/padding

4. **Tiny utility classes**
   - `.mobile-menu-bg`
   - `.divider` if markup can become simple Tailwind utilities

5. **Related posts layout/card sizing**
   - currently mixed Tailwind + `.related-card`; can be cleaned up page-by-page.

## Avoid migrating for now

Do not migrate these until there is a strong reason:

- `.hero*`
- `.page-waves*`
- `.hero-particle*`
- `.about-*` cards/skills/CTA
- `.classes-*` cards/books
- `.work-*` portfolio cards
- `.mentoring-*` cards/steps
- `.post-content*`
- `.confirm-dialog*`
- `.warm-form*`

These are semantic, brand-heavy, or content-generated styles. Tailwind would make the templates noisier without much benefit.

## Recommended next cleanup order

1. **Small layout templates**
   - `core/templates/core/utils/footer.html`
   - `core/templates/core/utils/personal_links.html`
   - `core/templates/core/404.html`
   - `core/templates/core/500.html`
   - `core/templates/core/version.html`

2. **Navigation shell only**
   - keep `.nav-link`, `.logo`, dropdown styles
   - move only simple spacing/layout to Tailwind where it reduces CSS

3. **Related posts**
   - simplify mixed Tailwind/custom usage
   - either make it mostly Tailwind or mostly semantic classes

4. **Page layout utilities**
   - replace `.page-layout` only if the repeated Tailwind class list remains readable

## Rule of thumb

Use Tailwind when the style is obvious from utilities:

```html
<div class="mx-auto flex max-w-6xl items-center justify-between px-6 py-3">
```

Keep semantic CSS when the class represents a designed component:

```html
<section class="hero">
```

Do not migrate everything just to migrate it. The win is removing duplicated/simple CSS while preserving the brand layer.
