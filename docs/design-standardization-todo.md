# Website Design Standardization TODO

## Goal

Preserve the current warm visual identity while making every public page feel part of the same website.

**Agreed direction:** use aligned outer containers with narrower text columns for comfortable reading. Not every element needs to occupy the same width.

For example, an article can have a centered reading column, followed by a wider related-post grid. Both belong inside the same outer page container.

## Implementation status (2026-09-19)

The original audit below is retained as historical context, not a description of current markup. The implemented source of truth is [Design system](design-system.md). Unchecked original items must not be interpreted as proof that implementation is absent.

- [x] Shared 1200px content-width container, fluid external gutters, and 70ch reading maximum.
- [x] Navigation, footer, hero, version, error, and contact-result outer shells standardized in templates/CSS.
- [x] Article title/metadata/text and service introductions use reading columns; About preserves its photo layout.
- [x] Shared heading/card roles; blog-list and search page titles use h1; article title inline spacing removed.
- [x] Related cards use responsive columns, shared title sizing and surfaces; panel spans the outer container.
- [x] Standalone related page has an h1 and persistent HTMX pagination target; embedded fragment omits both.
- [x] Design reference documents container arithmetic, lead text, article media, and related-card exceptions.
- [x] Response regression tests and related-post browser regression cases added.
- [x] Related-post Chromium matrix: 16 cases passed across eight widths, embedded/standalone, including pagination and overflow. Response/layout suite: 11 tests and 22 subtests passed.
- [ ] Inspect loaded fonts and fallback shifts; verify remaining browser/page coverage.
- [ ] Capture matching screenshots and verify every public page, language, navigation path, zoom, and breakpoint.
- [ ] Verify representative stored article HTML, especially tables and inline formatting beyond span/font size overrides.
- [ ] Finish the typography/spacing inventory: metadata/interface roles and a shared section-spacing scale.
- [ ] Add screenshot-based visual regression baselines and broader cross-page alignment assertions.

### Resolved layout decisions

Keep 70ch; article titles and metadata align with the reading column; related posts use the wider shell. Images/code remain inside the reading column. Shared cards are the baseline, with the related section panel and hover stripe documented as intentional variants.

The current outer container has **no horizontal padding**: its width is `min(100% - 2 * gutter, 1200px)`. Earlier discussion of a padded 1200px shell and stepped gutters below is superseded.

## Original audit and acceptance criteria

## Current foundation

- Shared CSS: `core/static/core/css/base.css`
- Tailwind configuration: `frontend/tailwind.config.js`
- Base template: `core/templates/core/utils/base.html`
- Font loading and stylesheet order: `core/templates/core/utils/head.html`
- Most public pages use `.page-layout`, with a maximum width of `1200px`.
- The homepage `.hero` uses that same maximum width.
- Heading font: **Cormorant Garamond**.
- Body and interface font: **Inter**.
- `.page-prose` already provides a centered `70ch` maximum width, but usage is limited.

Related documentation: [CSS / Tailwind Audit](css-tailwind-audit.md). That document describes CSS ownership and migration candidates; this plan focuses on visual consistency. A wholesale Tailwind migration is not required.

## 1. Define shared design rules

- [ ] Keep **1200px** as the shared maximum outer container width.
- [ ] Adopt one shared reading-width rule, approximately **65–70ch**; `70ch` is the existing starting point.
- [ ] Define one responsive horizontal-gutter scale.
- [ ] Define typography roles: page title, section heading, card title, body, metadata, and interface label.
- [ ] Keep Cormorant Garamond for headings and Inter for body/interface text.
- [ ] Define shared spacing and card-treatment rules.
- [ ] Record intentional exceptions rather than allowing page-specific values to accumulate.

### Concrete examples

- At a wide desktop viewport, the navigation content, main page container, and footer content should share the same outer boundaries.
- A portfolio grid may use the full available container width. A blog paragraph should stop at the reading-width limit.
- A page title can be larger than a card title, but related-post and portfolio-card titles should follow a common role unless there is a documented reason not to.
- Start by evaluating the existing page gutters: `2rem` on desktop, `1.5rem` at intermediate widths, and `1.25rem` on small screens. Apply the chosen scale consistently rather than creating a separate scale for navigation.

**Important:** specify whether the 1200px container includes its horizontal padding. With the current Tailwind border-box reset, it does. Matching only the `max-width` without matching padding will not align visible content edges.

`ch` is based on font metrics, not an exact count of letters per line. Use the same reading-width rule and confirm the result visually.

**Done when:** layout and typography decisions have one documented source of truth.

## 2. Standardize outer page alignment

- [ ] Align navigation content with the shared outer container.
- [ ] Replace the footer's separate container sizing with the shared layout rules.
- [ ] Verify consistent outer widths and horizontal gutters across all public pages.
- [ ] Standardize inner-page spacing below the fixed navigation.
- [ ] Preserve the homepage hero's intentional vertical layout while matching horizontal alignment.
- [ ] Bring version, error, and contact-result pages into the same outer layout system.
- [ ] Check nested containers for accidental additional padding.

### Current examples to address

| Area | Current implementation | Intended result |
| --- | --- | --- |
| Navigation | Inner wrapper has `mx-auto px-6` but no maximum width | Content aligns with the main page on wide screens |
| Footer | Uses Tailwind `container` | Uses the same outer-width rule as the page |
| Most public pages | Use `.page-layout` | Preserve this shared behavior |
| Homepage | Uses `.hero` with the shared maximum width | Preserve the special hero, align its horizontal edges |
| Version page | Uses `container mx-auto px-4 py-8` | Match the site's container and heading system |
| Article divider | `.divider` adds horizontal padding inside `.page-layout` | Decide whether the extra inset is intentional |

### Files to review

- `core/templates/core/utils/navbar.html`
- `core/templates/core/utils/footer.html`
- `core/templates/core/version.html`
- `core/templates/core/404.html`
- `core/templates/core/500.html`
- `blog/templates/blog/home.html`
- `blog/templates/blog/success.html`
- `blog/templates/blog/error.html`
- `core/static/core/css/base.css`

**Done when:** switching pages at the same viewport does not unexpectedly shift the shared outer content edges.

## 3. Apply consistent reading widths

- [ ] Constrain blog article text to the shared reading width.
- [ ] Apply the reading-width rule to text-heavy introductions on classes, consultancy, and mentoring pages.
- [ ] Harmonize the About biography with that rule while preserving its photo layout.
- [ ] Keep grids and multi-column sections free to use the wider outer container.
- [ ] Decide how article titles and metadata align with the reading column.
- [ ] Decide whether article images, tables, and code blocks stay within the reading column or may intentionally extend beyond it.
- [ ] Decide whether related posts use the reading width or the wider outer container.
- [ ] Keep contact forms and short result messages appropriately sized within the shared outer shell.

### Proposed layout examples

**Blog article**

- Shared outer page container.
- Centered reading column for the title, metadata, and article text as a starting proposal.
- Code blocks scroll internally when necessary, rather than making the whole page overflow.
- Related posts may form a wider grid below the article. This is an intentional width change, not a mismatch.

**Classes or mentoring page**

- Page heading follows the shared header treatment.
- Introductory paragraphs use the reading width.
- Resource or audience cards use the wider grid area.
- The transition between text and cards uses the shared section-spacing scale.

**About page**

- Biography remains readable beside the photo on desktop.
- On mobile, photo and biography stack without extra nested side padding.
- The biography may be narrower than the maximum reading width when the layout requires it; the limit is a maximum, not a forced width.

### Files to review

- `blog/templates/blog/posts/detail.html`
- `blog/templates/blog/about.html`
- `blog/templates/blog/classes.html`
- `blog/templates/blog/consultancy.html`
- `blog/templates/blog/mentoring.html`
- `blog/templates/blog/contact.html`
- `core/static/core/css/base.css`

**Done when:** long paragraphs have a comfortable, consistent measure while cards and other structured content can still use the available space.

## 4. Fix related-post typography and layout

- [ ] Remove overlapping typography rules from related-post card titles.
- [ ] Give card titles an explicit shared font family, size, weight, and line height.
- [ ] Separate section-heading styling from card-title styling.
- [ ] Replace percentage-based wrapping with predictable responsive columns.
- [ ] Make previous/next navigation placement consistent across pagination states.
- [ ] Harmonize backgrounds, borders, radii, padding, and hover effects with the site's card system.
- [ ] Review the directly accessible related-post page, not only the embedded fragment.

### Concrete typography issue

The current title markup combines `text-lg font-semibold section-subtitle`.

- Tailwind's `text-lg` sets an `18px` font size and `28px` line height at the default root font size.
- The later `.section-subtitle` rule changes the font size to `25.6px` but does not replace that line height.
- The result is a relatively large title with tight leading inside a narrow card.
- The related-section heading and the individual card titles both use `.section-subtitle`, weakening their hierarchy.

The configured font family is already Cormorant Garamond, so this is not evidence that a different font file is being used. Browser inspection must confirm actual font loading.

### Comparison with existing title styles

| Role | Current desktop size at default root size |
| --- | --- |
| Blog-list title (`.essay-title`) | 22.4px |
| Portfolio-card title (`.work-project__name`) | 20px |
| About-card title (`.about-card__title`) | 18.4px |
| Related-post card title (`.section-subtitle`) | 25.6px |

**Example direction, not a final approved scale:** use a shared card-title size around `1.25rem` with a line height around `1.3`, then validate with real titles. Section headings should remain visibly distinct.

### Layout examples to test

- A short title: “Python generators”.
- A long title: “What I learned while building asynchronous Django applications”.
- A grid containing one, two, or three related posts.
- First page with only Next, middle page with both controls, and last page with only Previous.
- Mobile cards should have enough width for readable titles and must not cause horizontal scrolling.

### Files to review

- `blog/templates/blog/posts/related_posts.html`
- `blog/templates/blog/posts/detail.html`
- `core/static/core/css/base.css`

**Done when:** related posts look like part of the same component family as the rest of the site, including with long titles and different pagination states.

## 5. Consolidate typography and spacing across pages

- [ ] Map existing text styles to the agreed typography roles.
- [ ] Normalize equivalent heading sizes, weights, and line heights.
- [ ] Normalize body text where differences are unintentional.
- [ ] Standardize spacing below headings and between paragraphs, sections, and cards.
- [ ] Standardize equivalent links, buttons, and calls to action.
- [ ] Remove conflicting utility/custom declarations and unnecessary inline overrides.
- [ ] Review heading semantics separately from appearance.
- [ ] Check editor-generated article HTML for inline font and size overrides.
- [ ] Document legitimate exceptions such as the hero title, code text, and compact metadata.

### Concrete examples

- Introductory paragraphs currently often use `1.05rem`, while article text uses `1rem`. Decide whether a distinct lead-paragraph role is intentional rather than automatically flattening every size.
- A “Read more” link in a related card should use the same interface typography as comparable card links.
- A card title should not inherit section-heading margins that create excessive empty space inside a small card.
- The article title has an inline bottom margin. Its spacing should belong to a documented heading or article-header role.
- The version page uses a generic bold heading and an indigo button. Review these against the existing serif heading and warm button treatments.
- Blog-list and search page titles currently use `h2`. Review whether they should be the page's `h1`; visual size should come from the role, not the HTML tag alone.
- Stored article HTML is rendered inside `.post-content`. Check representative posts for pasted inline formatting before assuming shared CSS controls every paragraph.

**Done when:** equivalent elements look equivalent, and differences can be explained by a named role or an intentional exception.

## 6. Verify fonts, responsive behavior, and navigation

- [ ] Inspect computed font family, size, weight, and line height in a browser.
- [ ] Confirm the intended web fonts actually load; check rendered fonts as well as declared font stacks.
- [ ] Check fallback-font behavior and layout shifts during loading.
- [ ] Review every public page at mobile, tablet, and desktop widths.
- [ ] Check both sides of responsive breakpoints and the exact breakpoint widths.
- [ ] Test long titles, links, code blocks, tables, and translated text.
- [ ] Verify direct loads, HTMX navigation, browser back/forward, and related-post pagination.
- [ ] Check horizontal overflow, awkward wrapping, focus visibility, and zoom behavior.
- [ ] Capture before/after screenshots at matching viewport sizes.

### Suggested viewport examples

- **375px:** small phone.
- **640px and 641px:** small-screen boundary.
- **767px, 768px, and 769px:** tablet/navigation boundary.
- **1024px:** smaller desktop or landscape tablet.
- **1440px:** wide desktop where container alignment is easy to compare.

The boundary checks matter because custom CSS uses `max-width` queries while Tailwind uses `min-width` queries. At an exact boundary, both sets of rules can apply.

### Page checklist

- [ ] Home
- [ ] About
- [ ] Blog list, including filtered and empty states
- [ ] Blog detail with short and long content
- [ ] Related posts, embedded and directly accessed
- [ ] Work / portfolio
- [ ] Classes
- [ ] Consultancy
- [ ] Mentoring
- [ ] Contact, including validation errors
- [ ] Contact success and error results
- [ ] Search
- [ ] 404 and 500 pages
- [ ] Version page

Django admin is outside this public-site standardization unless explicitly added to scope.

### Example navigation checks

1. Open a blog article directly and inspect related-post title typography.
2. Open the same article through the blog list's HTMX link and compare.
3. Paginate related posts and confirm typography, widths, and controls remain stable.
4. Navigate to About, then return with the browser Back button and check alignment.
5. Repeat representative checks in each supported language.

**Done when:** the same page has consistent layout and typography regardless of navigation path, language, or supported viewport.

## 7. Make consistency maintainable

- [ ] Publish a short reference for approved containers, reading widths, typography roles, spacing, and card treatments.
- [ ] Prefer shared layout/component rules over copied page-specific values.
- [ ] Keep Tailwind for simple utilities and custom CSS for shared brand/component styling where appropriate.
- [ ] Add suitable visual regression checks for representative pages.
- [ ] Add layout/overflow checks where practical.
- [ ] Update the CSS audit after implementation so the documentation remains accurate.

### Concrete regression examples

- Desktop screenshot of navigation, an inner-page heading, and footer alignment.
- Article screenshot covering the reading column and related-post grid.
- Mobile screenshot with a long related-post title.
- Browser assertion that document width does not exceed viewport width for representative pages.
- Direct-load and HTMX-rendered versions of a page checked for equivalent layout.

Avoid brittle tests that merely require a particular CSS class name. Prefer checks of observable layout or shared component behavior.

**Done when:** a new page can use the shared design rules without inventing its own width or typography scale.

## Recommended implementation order

1. Agree on container, reading-width, typography, and spacing rules.
2. Align the shared navigation, page shell, and footer.
3. Apply reading widths to articles and text-heavy introductions.
4. Fix related-post typography and card layout.
5. Consolidate remaining typography, spacing, and secondary pages.
6. Verify in the browser across viewports, languages, and navigation paths.
7. Document the final rules and add regression coverage.

## Decisions still to confirm before implementation

- [ ] Keep the existing `70ch` reading maximum or choose a slightly narrower measure after visual comparison?
- [ ] Align article titles and metadata to the reading column or allow a wider article header?
- [ ] Keep related posts in the wider outer container? **Recommended starting point: yes.**
- [ ] Keep images and code within the reading column, or support explicit wide-content exceptions?
- [ ] Which existing card treatment should be the baseline: About/portfolio cards or a refined shared variant?

These details are open; the overall direction of aligned outer containers with narrower reading text is already agreed.
