# Public-site layout and typography system

This reference preserves the Warm Touch visual identity while making public pages predictable.

## Layout

- **Outer container:** `--max-width: 1200px`, applied with `.site-container` and `.page-layout`.
- Container width is `min(100% - 2 * gutter, 1200px)`, with automatic inline margins and no horizontal padding. The gutters are outside the container; 1200px is the content width, not a padded shell.
- **Gutters:** `--page-gutter: clamp(1.25rem, 4vw, 2rem)` at every viewport width.
- **Reading column:** `--reading-width: 70ch`, applied with `.page-prose`.
- Use `.page-layout` for page-level sections and grids. Use `.page-prose` for an article or a text-heavy introduction inside that layout. Do not constrain card grids to the reading column unless the content itself requires it.
- The home `.hero` is intentionally distinct, but uses the same outer width and gutters.

## Typography

- Cormorant Garamond (`--serif`) is used for `section-title`, `section-heading`, and `card-title`.
- Inter (`--sans`) is used for body copy, metadata, controls, and `card-title--compact`.
- Use one `h1` with `.section-title` for each public page.
- Use `.section-heading` for major `h2` sections and `.card-title` for headings inside cards. Do not combine heading component classes with conflicting Tailwind font-size or line-height utilities.
- Use `.page-intro` with `.page-prose` for long introductory copy.

## Cards and controls

- Add `.card` to reusable cards. It provides the shared border, background, radius, and hover behavior.
- Use `.card-title` and `.card-description` for the standard card text hierarchy.
- Component classes may only supply layout or intentional variants (for example, a portfolio image or compact resource-card title).
- Keep pagination outside a card grid; related-post pagination uses `.related-posts__pagination`.
- Related posts use the full outer width below the narrower article. Their enclosing panel deliberately has a warm background, larger radius, and internal padding; individual cards use the shared card surface and title size. The decorative hover stripe and metadata eyebrow are intentional related-card variants.
- Article title and metadata remain inside the reading column. Images and code stay within it; code scrolls internally. No wide-content exception is currently provided. Tables still require browser overflow verification.
- Lead paragraphs intentionally use 1.05rem; article body uses 1rem. Hero typography and compact resource titles are intentional exceptions.

## Verification status

- Django response tests cover page shells and embedded versus standalone related-post markup.
- `tests/e2e/test_related_posts.py` covers full-width related panels, long titles, shared title sizing, overflow, and first/middle/last pagination states in both contexts across eight viewport widths.
- Verified 2026-09-19: all 16 related-post Chromium cases passed, along with 11 response/layout tests (22 subtests). Browser tests require `uv run playwright install chromium` and the same `DJANGO_ALLOW_ASYNC_UNSAFE=true` test-only environment used by CI.
- Font loading/fallback shifts, screenshots, all-language coverage, and the full public-page matrix remain manual verification tasks.

## Regression checklist

Review these at 320px, 768px, and 1440px after layout changes:

1. Navbar, main content, and footer start on the same horizontal line.
2. Long-form text remains within the 70ch reading column; grids retain the full outer width.
3. Long post titles, links, code blocks, and translated text do not overflow.
4. Related posts use one/two-or-more predictable grid columns as space permits, and their pager remains below the grid.
5. Direct requests and HTMX responses render the same page-level layout; test this with `blog/tests/views/test_layout_consistency.py`.
6. Confirm Cormorant Garamond and Inter load in the browser and inspect computed type sizes when changing font delivery.
