# How to Generate Test Charters with AI

This guide explains how to use AI tools (such as GitHub Copilot, ChatGPT, or similar) to generate **exploratory test charters** from existing test case documents. No prior experience is required — follow the steps below.

---

## What Is a Test Charter?

A **test charter** is a structured document that guides an exploratory testing session. Unlike scripted test cases that tell you exactly what to click and type, a charter gives you:

- A **mission** — what area of the application to explore
- **Scope** — what is covered and what is not
- **Test ideas** — specific things to investigate
- **Oracles** — how to decide if something is a bug
- **Exit conditions** — when to stop testing

Test charters follow the **Session-Based Test Management (SBTM)** methodology created by James Bach (1999).

---

## Project Structure

```
docs/skill-test-charters/
├── references/                              # Input files (your test cases)
│   ├── test_case_and_proper_defect_report_laptop.xlsx
│   ├── test-cases-mobile.xlsx
│   └── task-testcase-report-tablet.pdf
├── output/                                  # Generated charters (AI output)
│   ├── CHARTERS-LAPTOP.html                 # All laptop charters (HTML overview)
│   ├── CHARTERS-TABLET.html                 # All tablet charters (HTML overview)
│   ├── CHR-LAP-AUTH-003.md                  # Individual charter (Markdown)
│   └── CHR-TAB-CART-006.md                  # Individual charter (Markdown)
└── HOW-TO-GENERATE-CHARTERS.md             # This guide
```

### Folder Descriptions

| Folder | Purpose |
|---|---|
| `references/` | Contains the **source test case documents** (Excel or PDF). These are the input that the AI reads to generate charters. |
| `output/` | Contains the **generated test charters**. HTML files contain an overview of all charters for a platform. Markdown files contain detailed individual charters. |

---

## Prerequisites

Before you start, make sure you have:

1. **An AI tool** — any of the following will work:
   - [GitHub Copilot](https://github.com/features/copilot) (recommended — can read files directly)
   - [ChatGPT](https://chat.openai.com) (upload files as attachments)
   - [Claude](https://claude.ai) (upload files as attachments)
   - Any other LLM that can process document attachments

2. **Test case documents** — Excel (`.xlsx`) or PDF files containing:
   - Test case IDs, descriptions, steps, and expected results
   - Test execution results (PASS / FAIL)
   - Defect reports (if any)

3. **Basic understanding of the application under test** — you should know:
   - What the application does (in this project: [PrestaShop Demo Shop](https://demo.prestashop.com/#/en/front))
   - What platform/device is being tested (Laptop, Tablet, Mobile)

---

## Step-by-Step Guide

### Step 1: Prepare Your Test Case Document

Place your test case file (Excel or PDF) in the `references/` folder:

```
docs/skill-test-charters/references/your-test-cases.xlsx
```

Before proceeding, review the document and identify:
- Which test cases **FAILED** (these are high-priority candidates for charters)
- Which **functional areas** are covered (e.g., Authentication, Shopping Cart, Navigation)
- Any **defect reports** linked to the failed test cases

### Step 2: Write the AI Prompt

Use the following prompt template. Copy it into your AI tool and adjust the placeholders (`[...]`) to match your context:

---

> **Prompt Template:**
>
> I have a test case document for the **[Platform: Laptop / Tablet / Mobile]** platform, testing the **[Application Name]** web application at **[URL]**.
>
> The document contains test cases with execution results (PASS/FAIL) and defect reports.
>
> Please analyze the attached document and generate **exploratory test charters** following the **Session-Based Test Management (SBTM)** format.
>
> For each charter, include the following sections:
> 1. **Charter ID** — use the format: `CHR-[PLATFORM]-[AREA]-[NUMBER]` (e.g., `CHR-LAP-AUTH-003`)
> 2. **Platform** — the device/viewport being tested
> 3. **Target URL** — the application URL
> 4. **Mission** — a clear statement of what to explore and why
> 5. **Scope — What Is Covered** — list the reference test cases included and the functional area
> 6. **Scope — What Is Not Covered** — explicitly list what is out of scope
> 7. **Start Conditions (Preconditions)** — browser, device, account state, test data needed
> 8. **Test Ideas & Exploration Notes** — detailed test ideas derived from the reference test cases, plus additional exploratory extensions
> 9. **Oracle — How to Determine Pass/Fail** — clear criteria for each test case
> 10. **Known Defects & Risks** — list any known defects from the reference document
> 11. **Exploratory Testing Areas** — heuristics to apply (GOLDFINGER, HICCUPS, SFDIPOT, FCC CUTS VIDS)
> 12. **Exit Conditions** — when to stop the testing session
> 13. **Output / Deliverables** — what to produce after the session
> 14. **References** — source file, platform, SBTM citation
>
> Group the test cases by **functional area** (e.g., Navigation, Authentication, Shopping Cart, Search & Filter, etc.) and create one charter per area.
>
> **Prioritize areas with FAILED test cases** — these charters should include more detailed test ideas and reference the specific defects found.
>
> Generate the output in **Markdown** format.

---

### Step 3: Attach the Document and Run

1. **Attach** your test case file to the AI conversation (upload the `.xlsx` or `.pdf`)
2. **Paste** the prompt from Step 2 (with your values filled in)
3. **Send** the message and wait for the AI to generate the charters

### Step 4: Review the Generated Charters

The AI will produce one or more charters. Review each one for:

- ✅ **Completeness** — all sections present?
- ✅ **Accuracy** — do the test ideas match the original test cases?
- ✅ **Defect references** — are known defects correctly cited?
- ✅ **Test data** — are realistic test values suggested (emails, passwords, quantities)?
- ✅ **Scope boundaries** — is the scope clear and reasonable?

> **Tip:** The AI may group test cases differently than you expect. You can ask it to split or merge charters by providing follow-up instructions.

### Step 5: Save the Output

Save the generated charters in the `output/` folder:

```bash
# Individual detailed charter (Markdown)
docs/skill-test-charters/output/CHR-LAP-AUTH-003.md

# Overview of all charters for a platform (HTML)
docs/skill-test-charters/output/CHARTERS-LAPTOP.html
```

#### Naming Convention

| Format | Pattern | Example |
|---|---|---|
| Individual charter | `CHR-[PLATFORM]-[AREA]-[NUMBER].md` | `CHR-TAB-CART-006.md` |
| Platform overview | `CHARTERS-[PLATFORM].html` | `CHARTERS-LAPTOP.html` |

**Platform codes:** `LAP` (Laptop), `TAB` (Tablet), `MOB` (Mobile)

**Area codes (examples):** `AUTH` (Authentication), `CART` (Shopping Cart), `NAV` (Navigation), `SRCH` (Search & Filter), `PROD` (Product Details), `CHK` (Checkout), `ERR` (Error Handling), `ACC` (User Account)

### Step 6: Commit and Push

```bash
# Force-add is needed because the output/ folder is in .gitignore
git add -f docs/skill-test-charters/output/

git commit -m "Add test charters for [Platform]"

git push origin your-branch-name
```

> **Note:** The `output/` directory is listed in `.gitignore`, so you must use `git add -f` (force) to stage these files.

---

## Example: Generating Laptop Charters

Here is a real example from this project:

1. **Input file:** `references/test_case_and_proper_defect_report_laptop.xlsx`
   - Contains test cases for the PrestaShop demo on Laptop
   - Several test cases FAILED (TC_04, TC_12, TC_13) with defects (DEF-03, DEF-07, DEF-08)

2. **Prompt sent to AI:**
   > I have a test case document for the **Laptop** platform, testing the **PrestaShop Demo Shop** at **https://demo.prestashop.com/#/en/front**. Please analyze the attached document and generate exploratory test charters following the SBTM format...

3. **Output generated:**
   - `CHARTERS-LAPTOP.html` — HTML overview of all laptop charters
   - `CHR-LAP-AUTH-003.md` — Detailed charter for Authentication area (prioritized because TC_04, TC_12, TC_13 all FAILED)

4. **Charter highlights:**
   - The charter references 3 failed test cases and 3 known defects
   - It includes 8 exploratory test ideas beyond the original test cases
   - It provides specific test data (emails, passwords, edge-case inputs)
   - It suggests a 90-minute time box for the session

---

## Tips for Better Results

| Tip | Why |
|---|---|
| Always mention which test cases FAILED | The AI will prioritize those areas and generate deeper test ideas |
| Include defect IDs and descriptions | The AI will reference them in the charter and suggest regression scenarios |
| Specify the platform clearly | The charter will include platform-specific preconditions (viewport size, touch targets, etc.) |
| Ask for one charter at a time if the document is large | Better quality than generating all at once |
| Request both Markdown and HTML output | Markdown is easy to read in code editors; HTML is good for sharing with the team |
| Review and edit the output | AI-generated charters are a starting point — add your domain knowledge |

---

## Frequently Asked Questions

### Q: Can I generate charters for test cases that all PASSED?
**Yes.** Even when test cases pass, charters are valuable for deeper exploratory testing beyond the scripted steps. The AI will focus on edge cases, boundary conditions, and areas not covered by the original test cases. See `CHR-TAB-CART-006.md` for an example — all 3 reference test cases passed, but the charter still includes 6 exploratory extensions.

### Q: What if I don't have an Excel/PDF file?
You can paste test case information directly into the AI prompt as text. Include: test case ID, title, steps, expected result, actual result, and pass/fail status.

### Q: How long should a testing session based on a charter take?
The recommended time box is **60–90 minutes** per charter. This is enough to execute the reference test cases and explore the additional test ideas.

### Q: Can I modify the charter template?
Yes. The sections listed in Step 2 are a recommended starting point. You can add or remove sections based on your team's needs. Common additions include: risk assessment, environment details, or links to related user stories.

---

## References

- **Session-Based Test Management (SBTM):** Bach, J. (1999). *Session-Based Test Management.*
- **Exploratory Testing Heuristics:**
  - GOLDFINGER — Does it follow conventions?
  - HICCUPS — History, Image, Comparable, Claims, User expectations, Product, Purpose, Standards
  - SFDIPOT — Structure, Function, Data, Interfaces, Platform, Operations, Time
  - FCC CUTS VIDS — Feature, Complexity, Claims, Configuration, Usability, Testability, Security, Compatibility, Usability, Timing, Stress, Installability, Development, Standards
- **PrestaShop Demo Shop:** https://demo.prestashop.com/#/en/front
