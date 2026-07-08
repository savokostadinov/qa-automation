---
name: test-charter-generator
description: Use when the user wants to generate, create, or write test charters for the PrestaShop demo shop. Triggers on phrases like "create test charter", "generate test charter", "make test charter", "write charter for tablet/mobile/laptop", "SBTM charter", or any request to produce exploratory testing session charters from the reference test cases in docs/skill-test-charters/references/. Supports platform-scoped generation (tablet, mobile, laptop) and full exploratory coverage following Session-Based Test Management (SBTM).
---

# Test Charter Generator — PrestaShop Demo Shop

This skill guides the generation of **Session-Based Test Management (SBTM)** test charters for the PrestaShop demo shop at https://demo.prestashop.com/#/en/front.

The charters are derived from three platform-specific reference documents stored at:

```
docs/skill-test-charters/references/
  task-testcase-report-tablet.pdf          — Tablet test cases (TC_01–TC_34)
  test_case_and_proper_defect_report_laptop.xlsx  — Laptop test cases + defect reports
  test-cases-mobile.xlsx                   — Mobile test cases + defects + summary
```

---

## How to Trigger This Skill

When a user asks to create test charters, identify:

1. **Which platform** they want to target: `tablet`, `mobile`, `laptop`, or `all`
2. **Which scope** within the platform (optional): navigation, filters, cart, registration, search, etc.
3. **Whether they want exploratory-only**, reference-based, or both

Example user commands and how to interpret them:

| User says | What to do |
|---|---|
| "Create test charters for tablet" | Parse tablet PDF, generate SBTM charters for all TC_01–TC_34 |
| "Generate charter for mobile search" | Parse mobile XLSX, filter search-related test cases, generate charter |
| "Create all platform charters" | Parse all three files, generate separate charter sets per platform |
| "Write charter for laptop registration" | Parse laptop XLSX, filter TC_12–TC_20 (registration/auth), generate charter |
| "Make a full charter for mobile" | Parse mobile XLSX, generate charters + add exploratory coverage for untested areas |

---

## Step-by-Step Workflow

### Step 1 — Parse the Reference Document(s)

Use the Python script at `.opencode/skills/test-charter-generator/scripts/parse_references.py` to extract test cases from the chosen file(s).

**Run the parser — each platform separately (absolute path, works from anywhere):**

Tablet:
```bash
python3 /Users/skostadi/IdeaProjects/qa-automation-sk/.opencode/skills/test-charter-generator/scripts/parse_references.py --platform tablet
```

Laptop:
```bash
python3 /Users/skostadi/IdeaProjects/qa-automation-sk/.opencode/skills/test-charter-generator/scripts/parse_references.py --platform laptop
```

Mobile:
```bash
python3 /Users/skostadi/IdeaProjects/qa-automation-sk/.opencode/skills/test-charter-generator/scripts/parse_references.py --platform mobile
```

All platforms:
```bash
python3 /Users/skostadi/IdeaProjects/qa-automation-sk/.opencode/skills/test-charter-generator/scripts/parse_references.py --platform all
```

> If you are inside the project root (`qa-automation-sk/`) you can also use:
> `python3 .opencode/skills/test-charter-generator/scripts/parse_references.py --platform <platform>`
>
> If you are inside the skill folder (`test-charter-generator/`) you can use:
> `python3 scripts/parse_references.py --platform <platform>`

The script outputs structured JSON to stdout. Read it and use it as your source of truth for the charter content.

### Step 2 — Group Test Cases into Functional Areas

Group the extracted test cases into logical **mission areas** (one charter per area). Common groupings derived from the reference files:

| Mission Area | Covers (reference TCs) |
|---|---|
| Navigation & Banners | Homepage banners, back-to-top, category nav, subcategory menus |
| Product Discovery | Quick View, product details, filtering (color, price, composition, dimension), sorting |
| Shopping Cart | Add to cart, quantity management, remove items, cart totals, checkout button state |
| User Registration & Auth | Account creation, field validation, birthdate, email uniqueness, duplicate login |
| Search | Empty search, keyword search, relevance of results |
| Localization | Language switch, translation completeness |
| Responsiveness & Layout | Mobile/tablet layout adaptation, hamburger menu, footer, scroll |
| Checkout Flow | Guest checkout, password requirements, policies, payment |

Adapt the groupings based on what the parsed file actually contains.

---

### Available Commands — Generate Charters by Platform & Area

Each command below parses the relevant reference file and generates a charter for that specific area. Run them in the opencode TUI by typing `/` followed by the command name.

**Full platform (all areas at once):**

| Command | Generates |
|---|---|
| `/charter-tablet` | All tablet charters (TC_01–TC_34) |
| `/charter-laptop` | All laptop charters (TC_01–TC_20 + DEF-01–09) |
| `/charter-mobile` | All mobile charters (TC_001–TC_017 + BUG_001–015) |
| `/charter-all` | All platforms in one run |

**Tablet — by area:**

| Command | Area | Reference TCs |
|---|---|---|
| `/charter-tablet-navigation` | Navigation & Banners | TC_01–TC_08 |
| `/charter-tablet-product` | Product Discovery | TC_09–TC_12 |
| `/charter-tablet-cart` | Shopping Cart | TC_13–TC_15 |
| `/charter-tablet-localization` | Localization | TC_16–TC_17 |
| `/charter-tablet-filters` | Filters | TC_18–TC_23 |
| `/charter-tablet-registration` | Registration & Validation | TC_24–TC_34 |

**Laptop — by area:**

| Command | Area | Reference TCs / Defects |
|---|---|---|
| `/charter-laptop-localization` | Localization | TC_01, DEF-01 |
| `/charter-laptop-cart` | Shopping Cart | TC_03, TC_16–TC_19, DEF-02 |
| `/charter-laptop-auth` | Auth & Registration | TC_04, TC_12–TC_13, DEF-03, DEF-07–08 |
| `/charter-laptop-navigation` | Navigation & Banners | TC_05, TC_11, TC_18, DEF-04 |
| `/charter-laptop-search` | Search | TC_14, TC_20, DEF-09 |
| `/charter-laptop-filters` | Filters & Sorting | TC_06–TC_10, DEF-05–06 |
| `/charter-laptop-product` | Product Details | TC_15 |

**Mobile — by area:**

| Command | Area | Reference TCs / Bugs |
|---|---|---|
| `/charter-mobile-search` | Search | TC_001, TC_015, BUG_001–002 |
| `/charter-mobile-filters` | Filters | TC_002–TC_003, BUG_003–005, BUG_010, BUG_015 |
| `/charter-mobile-localization` | Localization | TC_004, BUG_011 |
| `/charter-mobile-navigation` | Navigation | TC_005, TC_009–TC_010, TC_013, BUG_013 |
| `/charter-mobile-auth` | Auth & Login | TC_006, BUG_006, BUG_014 |
| `/charter-mobile-cart` | Shopping Cart | TC_007, TC_011, TC_014, BUG_007–008 |
| `/charter-mobile-layout` | Responsiveness & Layout | TC_008, TC_016–TC_017, BUG_009, BUG_012 |

---

### Step 3 — Generate Each Test Charter

For each mission area, output a fully filled SBTM charter using the template below. Do **not** leave any field empty — use the reference test cases plus exploratory judgment to fill everything.

### Step 4 — Combine into HTML and Open in Browser

After saving the `.md` file(s), **always** run the combiner script to produce a styled HTML file and open it in the browser:

```bash
# For a single platform (laptop example):
python3 /Users/skostadi/IdeaProjects/qa-automation-sk/.opencode/skills/test-charter-generator/scripts/combine_charters.py --platform laptop --open

# Replace "laptop" with "tablet" or "mobile" as appropriate
```

The combiner reads all `CHR-[PLATFORM]-*.md` files in the output directory and produces:
- `docs/skill-test-charters/output/CHARTERS-LAPTOP.html`
- `docs/skill-test-charters/output/CHARTERS-TABLET.html`
- `docs/skill-test-charters/output/CHARTERS-MOBILE.html`

**Always tell the user:** "The HTML file has been generated and opened in the browser. It can be printed to PDF using File → Print (or Cmd+P) in the browser."

> **Important:** The combiner parses the plain-text `-----` / SECTION TITLE / `-----` format used by the charter template. Do NOT use `#` Markdown headings in charter `.md` files — they will not render correctly in the HTML output. Always follow the exact charter template format below.

---

## SBTM Test Charter Template

```
=============================================================
  TEST CHARTER
=============================================================

Charter ID    : CHR-[PLATFORM]-[AREA]-[NNN]
                  Example: CHR-TAB-NAV-001, CHR-MOB-CART-002

Platform      : [Tablet | Mobile | Laptop]
Target URL    : https://demo.prestashop.com/#/en/front
Test Session  : [leave blank — filled by tester at execution time]

-------------------------------------------------------------
MISSION
-------------------------------------------------------------
Explore [specific area] of the PrestaShop demo shop on [platform] to
[discover defects | verify behavior | assess risk | evaluate usability].

Focus Areas:
  - [Bullet list of specific sub-areas to investigate]

-------------------------------------------------------------
SCOPE — WHAT IS COVERED
-------------------------------------------------------------
[Describe what is explicitly IN scope for this session.
 Reference the specific test case IDs from the source file.]

Reference Test Cases Included:
  - TC_XX : [Title]  [PASS/FAIL from reference]
  - TC_XX : [Title]  [PASS/FAIL from reference]
  ...

-------------------------------------------------------------
SCOPE — WHAT IS NOT COVERED
-------------------------------------------------------------
[Describe what is explicitly OUT OF scope. E.g., back-end,
 payment gateway, performance, accessibility standards.]

-------------------------------------------------------------
START CONDITIONS (Preconditions)
-------------------------------------------------------------
  - Browser/Device: [Chrome/Safari/Firefox on Tablet/Mobile/Laptop]
  - URL: https://demo.prestashop.com/#/en/front
  - Account status: [logged in / logged out / guest]
  - Cart state: [empty / contains items]
  - Any other preconditions drawn from reference TCs

-------------------------------------------------------------
TEST IDEAS & EXPLORATION NOTES
-------------------------------------------------------------
[List all test ideas, both from reference TCs and from
 exploratory judgment. Use action-oriented phrases.]

From Reference Test Cases:
  1. [Test idea from TC_XX]
  2. [Test idea from TC_XX]
  ...

Exploratory Extensions (not in reference docs):
  A. [Area not covered in reference TCs — explore here]
  B. [Edge case to probe]
  C. [Cross-area interaction to investigate]
  ...

-------------------------------------------------------------
ORACLE — HOW TO DETERMINE PASS/FAIL
-------------------------------------------------------------
[Define the oracles (heuristics, standards, user expectations)
 used to judge whether behavior is correct.]

  - Expected results from reference test cases (see above)
  - PrestaShop UX conventions (consistent navigation, clear errors)
  - Platform responsiveness: no horizontal scroll, no layout overflow
  - Data integrity: prices, quantities, totals must be mathematically correct
  - Localization: language switch must propagate to ALL UI elements
  - Accessibility: interactive elements must be reachable by tap/click

-------------------------------------------------------------
KNOWN DEFECTS & RISKS (from reference docs)
-------------------------------------------------------------
[List any FAIL results from the reference TCs that are relevant
 to this charter area, so the tester is primed to re-verify or probe deeper.]

  - TC_XX FAILED: [brief description of failure]
  - DEFECT DEF-XX / BUG_XXX: [title and severity from defect report]

-------------------------------------------------------------
EXPLORATORY TESTING AREAS (beyond reference TCs)
-------------------------------------------------------------
[Aspects of the demo shop NOT covered by the reference test cases
 that should also be explored in this session.]

  Heuristics to apply:
  - GOLDFINGER: Does the interface follow established conventions?
  - HICCUPS: Consistency, correctness, usability, performance?
  - SFDIPOT: Structure, Function, Data, Interfaces, Platform, Operations, Time
  - FCC CUTS VIDS: (Familiar, Consistent, Correct, Complete, Unambiguous,
    Timely, Scalable, Versatile, Installable, Durable, Supportable)

  Specific areas to probe:
  - [List concrete exploratory ideas]

-------------------------------------------------------------
EXIT CONDITIONS (When to stop this session)
-------------------------------------------------------------
  - Time box reached (recommended: 90 minutes per charter)
  - All reference TCs in scope have been re-executed
  - All exploratory ideas have been investigated or noted as deferred
  - Critical blocker found (stop and report immediately)

-------------------------------------------------------------
OUTPUT / DELIVERABLES
-------------------------------------------------------------
  - Completed session sheet (filled during execution)
  - New defect reports for any bugs found
  - Notes on exploratory observations (unexpected behaviors)
  - Recommendation: re-test, defer, escalate, or close

-------------------------------------------------------------
REFERENCES
-------------------------------------------------------------
  Source file : [tablet PDF / laptop XLSX / mobile XLSX]
  Platform    : [Tablet / Mobile / Laptop]
  SBTM method : Bach, J. (1999). Session-Based Test Management.
  Shop URL    : https://demo.prestashop.com/#/en/front
=============================================================
```

---

## Platform-Specific Notes

### Tablet (source: `task-testcase-report-tablet.pdf`)

- **34 test cases** (TC_01–TC_34), 16 PASS / 18 FAIL
- Key failure areas: banner redirection, subcategory overlap, Quick View product mismatch, product detail image mismatch, color filter correctness, language translation completeness, birthdate validation logic, long name UI overflow, real-time validation feedback
- **Suggested charter split:**
  - CHR-TAB-NAV-001: Navigation, Banners, Scrolling (TC_01–TC_08)
  - CHR-TAB-PROD-002: Product Discovery — Quick View & Product Details (TC_09–TC_12)
  - CHR-TAB-FILTER-004: Filters & Color Filtering (TC_18–TC_23)
  - CHR-TAB-REG-005: Registration & Field Validation (TC_24–TC_34)
  - CHR-TAB-LOCALE-003: Localization / Language Switch (TC_16–TC_17)

### Laptop (source: `test_case_and_proper_defect_report_laptop.xlsx`)

- **20 test cases** (TC_01–TC_20), multiple PASS/FAIL
- **Also includes a proper defect report** (DEF-01 through DEF-04+): localization bug, cart total rounding, password requirements visibility, banner anchor redirect issue, duplicate email registration allowing duplicate accounts
- **Suggested charter split:**
  - CHR-LAP-LOCALE-001: Localization / Language Switch (TC_01)
  - CHR-LAP-CART-002: Cart Management & Pricing Accuracy (TC_03, TC_16, TC_17, TC_19)
  - CHR-LAP-AUTH-003: Account Creation, Login, Email Uniqueness (TC_04, TC_12, TC_13)
  - CHR-LAP-NAV-004: Navigation, Banners, Logo, Categories (TC_05, TC_11, TC_18)
  - CHR-LAP-SEARCH-005: Search Functionality (TC_14, TC_20)
  - CHR-LAP-FILTER-006: Filtering & Sorting (TC_06, TC_07, TC_08, TC_09, TC_10)
  - CHR-LAP-PROD-007: Product Details Page (TC_15)

### Mobile (source: `test-cases-mobile.xlsx`)

- **17 test cases** (TC_001–TC_017), 9 PASS / 8 FAIL
- **Also includes a defect sheet** (BUG_001–BUG_015) and a Summary sheet
- Key issues: search relevance, multiple filter reset, blank page on Graphic Corner filter, layout responsiveness, Contact Us error page, authentication failure, language partial update
- **Suggested charter split:**
  - CHR-MOB-SEARCH-001: Search (TC_001, TC_015, BUG_001, BUG_002)
  - CHR-MOB-FILTER-002: Filters (TC_002, TC_003, BUG_003, BUG_004, BUG_005, BUG_010, BUG_015)
  - CHR-MOB-LOCALE-003: Localization (TC_004, BUG_011)
  - CHR-MOB-NAV-004: Navigation, Logo, Homepage, Pages (TC_005, TC_009, TC_010, TC_013, BUG_013)
  - CHR-MOB-AUTH-005: Login & Registration (TC_006, BUG_006, BUG_014)
  - CHR-MOB-CART-006: Cart, Add/Remove, Totals, Checkout (TC_007, TC_011, TC_014, TC_016–TC_017, BUG_007, BUG_008)
  - CHR-MOB-LAYOUT-007: Responsiveness & Mobile Layout (TC_008, TC_016, TC_017, BUG_009, BUG_012)

---

## Exploratory Testing Areas (Not in Reference Docs)

The following areas of the demo shop are NOT covered by the reference test cases. When generating charters, include at least one exploratory section addressing these:

- **Wishlist functionality**: Can users add/remove items from a wishlist? Is it persistent?
- **Product reviews**: Can users leave reviews? Are they visible and paginated?
- **Newsletter subscription**: Does the footer newsletter field work? Is there confirmation?
- **Social sharing**: Are share buttons functional?
- **Pagination**: Do page controls on product listing pages work correctly?
- **Breadcrumb navigation**: Are breadcrumbs accurate and clickable on all pages?
- **404 handling**: What happens when navigating to nonexistent pages?
- **Keyboard navigation**: Can users tab through interactive elements?
- **Image zoom**: Does product image zoom work on all platforms?
- **Pack deals / bundles**: Are pack product pages displaying correct bundled pricing?
- **Customer service / Contact form**: Does the form submit correctly (Mobile BUG_009)?
- **Policies (terms, privacy)**: Are policy links accessible and readable on all platforms?
- **Footer links**: Do all footer links resolve correctly?
- **Order history**: For logged-in users, is order history accessible?
- **Currency display**: Are prices consistently formatted across pages?

---

## Output Format Options

When generating charters, always ask the user (or infer from context) which output format they prefer:

| Format | When to use |
|---|---|
| Markdown (.md) | Default — save to `docs/skill-test-charters/output/` |
| Plain text (.txt) | When user wants to copy-paste into a document |
| Console output | When user just wants to see the charter inline |

Default output path: `docs/skill-test-charters/output/CHR-[PLATFORM]-[AREA]-[NNN].md`

---

## Quality Checklist Before Finalizing Any Charter

Before outputting a charter, verify:

- [ ] Charter ID follows the naming convention (CHR-[PLATFORM]-[AREA]-[NNN])
- [ ] Mission statement is specific, not generic
- [ ] Every reference TC in scope is listed with its ID and title
- [ ] FAIL results from reference docs are in the Known Defects section
- [ ] Exploratory ideas go beyond what the reference TCs tested
- [ ] Oracle section states the POSITIVE expected behavior, not just "document the failure"
- [ ] Start conditions match the platform (device type, browser, screen context)
- [ ] Start conditions include specific test data to prepare (e.g., long name string, birthdate values, email address)
- [ ] Exit conditions include a time box (90 min recommended per SBTM)
- [ ] Output / Deliverables includes a debrief note (see rule below)
- [ ] Output file saved to `docs/skill-test-charters/output/` (if saving to file)

---

## Content Quality Rules — Applied to Every Charter

These rules must be followed when writing charter content. They fix the most common weaknesses found in generated charters.

### Rule 1 — Oracle must state positive expected behavior

The ORACLE section must describe what **correct behavior looks like**, not just echo "FAILED — document behavior".

**Bad:**
```
- Expected: TC_06 FAILED — document the actual destination
```

**Good:**
```
- Expected: tapping the promotional banner navigates the user to a product listing page
  filtered to the promoted category (e.g., Clothes on sale), or to a dedicated
  promotional landing page. The URL should change and the page content should be
  directly relevant to the banner's offer. Redirecting to the homepage top is incorrect.
```

Every oracle bullet must answer: "What would a correct implementation look like?"

### Rule 2 — Output / Deliverables must include a debrief note

Every charter OUTPUT section must end with:
```
  - Session debrief: report time-on-test, time-on-bugs, and time-on-other activities;
    bring all new defect reports and open questions to the debrief meeting
```

This is a core SBTM requirement. Omitting it produces charters that describe testing but not the reporting loop.

### Rule 3 — Quantity limit test ideas must name the limit

When a test case covers quantity limits (e.g., TC_13–TC_15 for physical products), the test ideas must:
1. First instruct the tester to **find and note** the stated maximum quantity on the product page
2. Then test at `max`, `max+1`, `max-1`, and `0`
3. Verify behavior at each boundary — not just "enter a high number"

**Bad:**
```
- Attempt to set quantity above the stated limit. Verify the system enforces the maximum.
```

**Good:**
```
- On the product page, locate and note the stated maximum quantity (displayed as
  "Max: X" or similar). Attempt to type max+1 directly into the quantity field.
  Verify the system either caps the value at max, shows an inline error, or prevents
  submission. Then test at max-1 (should be accepted), max (should be accepted),
  and 0 or negative (should be rejected with a clear error).
```

### Rule 4 — Exploratory extensions must be numbered when required

If the exploratory section covers areas that a tester **must** investigate (not optional ideas), use numbered items (`1.`, `2.`…), not lettered bullets (`A.`, `B.`…).

Use lettered bullets only for genuinely optional side-investigations.
Use numbered items for any exploratory idea that directly probes a known failure area or risk.

---

## SBTM Background (Reference)

Session-Based Test Management (SBTM) was introduced by James Bach (1999). Key principles:

- **Sessions** are uninterrupted blocks of test work with a defined mission (time-boxed, typically 60–120 min)
- **Charters** define what to test, not exactly how — preserving tester judgment
- **Debrief**: after each session, testers report bugs found, areas covered, and open questions
- **Metrics** tracked: coverage, bugs per session, time on test vs. setup vs. other

SBTM complements scripted test cases (like those in the reference files) by adding:
- Freedom to follow surprising findings
- Explicit mission scope to keep sessions focused
- Structured reporting without being prescriptive about steps

---

## combine_charters.py — Known Behaviour & Fixes Applied

The combiner script at `.opencode/skills/test-charter-generator/scripts/combine_charters.py`
has been updated with the following fixes. Do not revert these changes:

### 1 — Section parser uses `-----` sandwich format (not `#` headings)
Charter `.md` files use plain-text section headers formatted as:
```
-------------------------------------------------------------
SECTION TITLE
-------------------------------------------------------------
```
The parser detects lines sandwiched between two `---` separator lines as section headers.
Do NOT use `#`-style Markdown headings in charter files — they are not rendered correctly.

### 2 — `overflow: visible` on `.charter` div
The `.charter` CSS rule uses `overflow: visible` (not `overflow: hidden`).
The `border-radius` clip is applied only to `.charter-header` via `overflow: hidden` + `border-radius: 12px 12px 0 0`.
This is required so that browser anchor scrolling (`#chr-lap-nav-004` etc.) works correctly.
`overflow: hidden` on a parent element prevents the browser from scrolling to an anchor target inside it.

### 3 — `render_section_body` uses `list_type` — no `<strong>` tags in `list_buf`
Numbered items (`1. text`) are stored as plain text in `list_buf` with `list_type = "ol"`.
Bullet items (`- text`) are stored as plain text with `list_type = "ul"`.
Alpha items (`A. text`) are stored as plain text with `list_type = "ul"`.
`flush_list()` calls `escape_html()` on each item — this is safe only because items are plain text.
Never put raw HTML (`<strong>`, `<em>`, etc.) into `list_buf` — `escape_html` will escape the tags to literal text.

### 4 — `extract_charter_meta` parses mission text as title
If no `#`-style heading is found, the first substantive line of the MISSION section body
is used as the charter title in the TOC. Area labels are derived from the charter ID segment
(e.g., `LOCALE` → "Localization", `AUTH` → "Auth & Registration").

---

## Example Interaction

**User:** "Create test charters for the tablet platform, focus on registration"

**Expected behavior:**
1. Read `docs/skill-test-charters/references/task-testcase-report-tablet.pdf` (already known: TC_24–TC_34 cover registration)
2. Group those into 1–2 charters covering field validation, birthdate, name length, real-time feedback
3. Add exploratory extensions: password rules, email format validation, required field handling
4. Output CHR-TAB-REG-001 (and optionally CHR-TAB-REG-002 if scope is large) as markdown
5. Save to `docs/skill-test-charters/output/CHR-TAB-REG-001.md`

**User:** "Now do the same for mobile"

**Expected behavior:**
1. Read `docs/skill-test-charters/references/test-cases-mobile.xlsx`
2. Focus on TC_006 (login), BUG_006 (policies), BUG_014 (auth failure)
3. Generate CHR-MOB-AUTH-001
4. Save to `docs/skill-test-charters/output/CHR-MOB-AUTH-001.md`
