# How to Generate Test Charters with AI

This guide explains how to use AI tools to generate **exploratory test charters** from existing test case documents. No prior experience is required — follow the steps below.

This project supports **two methods** for generating charters:

| Method | Tool | Best For |
|---|---|---|
| **Method A** | **OpenCode** (terminal AI tool with pre-built commands) | Fast, repeatable generation using pre-configured commands |
| **Method B** | **Any AI tool** (ChatGPT, Copilot, Claude, etc.) | Manual generation with custom prompts |

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

## What Is OpenCode?

**[OpenCode](https://github.com/opencode-ai/opencode)** is an open-source, terminal-based AI coding assistant. Think of it as an AI chatbot that runs directly in your terminal (command line) and can read, write, and execute files in your project.

### Key Features

- **Runs in the terminal** — no browser or IDE needed, just type `opencode` in your project folder
- **Has access to your project files** — it can read your test case documents and write charter files directly
- **Supports custom commands** — pre-built shortcuts (like `/charter-laptop`) that run complex tasks with a single command
- **Supports custom skills** — reusable instructions that teach the AI how to perform specific tasks (like generating charters in the correct format)
- **Works with multiple AI providers** — OpenAI, Anthropic, AWS Bedrock, Google, and more

### How OpenCode Commands and Skills Work

This project includes a **custom skill** and **pre-built commands** inside the `.opencode/` folder:

```
.opencode/
├── package.json                    # OpenCode plugin dependency
├── commands/                       # Pre-built commands (shortcuts)
│   ├── charter-all.md              # Generate charters for ALL platforms
│   ├── charter-laptop.md           # Generate all laptop charters
│   ├── charter-tablet.md           # Generate all tablet charters
│   ├── charter-mobile.md           # Generate all mobile charters
│   ├── charter-laptop-auth.md      # Generate laptop auth charter only
│   ├── charter-tablet-cart.md      # Generate tablet cart charter only
│   └── ... (24 commands total)     # One per platform + area combination
└── skills/
    └── test-charter-generator/     # Custom skill definition
        ├── SKILL.md                # Instructions the AI follows to generate charters
        └── scripts/
            ├── parse_references.py     # Parses Excel/PDF test case files into structured data
            └── combine_charters.py     # Combines .md charters into styled HTML files
```

**Commands** (`/charter-*`) are shortcuts — when you type one, OpenCode reads the command file and executes the instructions inside it. Each command:
1. Runs the `parse_references.py` script to extract test cases from the reference documents
2. Uses the `test-charter-generator` skill to generate charters in the correct SBTM format
3. Saves the output as `.md` files in `docs/skill-test-charters/output/`
4. Runs `combine_charters.py` to create a styled HTML file and opens it in your browser

**Skills** are detailed instructions that tell the AI *how* to do something. The `test-charter-generator` skill contains the charter template, grouping rules, naming conventions, and quality guidelines.

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

# Method A: Using OpenCode (Recommended)

This is the fastest way to generate charters. OpenCode has pre-built commands that automate the entire process.

## Prerequisites

1. **Install OpenCode** (if not already installed):

   ```bash
   # macOS (Homebrew)
   brew install opencode-ai/tap/opencode

   # Or check the latest install instructions at:
   # https://github.com/opencode-ai/opencode
   ```

   Verify installation:
   ```bash
   opencode --version
   ```

2. **Configure an AI provider** — OpenCode needs an API key for an AI provider. Set one of these environment variables:

   ```bash
   # Option 1: OpenAI
   export OPENAI_API_KEY="your-key-here"

   # Option 2: Anthropic (Claude)
   export ANTHROPIC_API_KEY="your-key-here"
   ```

3. **Python 3** — needed for the parser and combiner scripts:
   ```bash
   python3 --version
   ```

4. **Python dependencies** — install the required packages:
   ```bash
   pip3 install openpyxl pdfplumber
   ```

## Step 1: Open OpenCode in the Project

Navigate to the project root and start OpenCode:

```bash
cd /path/to/qa-automation-sk
opencode
```

You will see a terminal interface (TUI) with a text input area where you can type messages or commands.

## Step 2: Run a Charter Command

Type `/` followed by the command name. Here are all available commands:

### Generate All Charters for a Platform

| Type This | What It Does |
|---|---|
| `/charter-laptop` | Generates all laptop charters (Navigation, Auth, Cart, Search, Filters, Product) |
| `/charter-tablet` | Generates all tablet charters (Navigation, Product, Cart, Localization, Filters, Registration) |
| `/charter-mobile` | Generates all mobile charters (Search, Filters, Localization, Navigation, Auth, Cart, Layout) |
| `/charter-all` | Generates charters for **all three platforms** in one run |

### Generate a Charter for a Specific Area

If you only need a charter for one functional area, use the area-specific command:

**Laptop:**

| Type This | Area | Reference Test Cases |
|---|---|---|
| `/charter-laptop-auth` | Authentication & Registration | TC_04, TC_12, TC_13 + DEF-03, DEF-07, DEF-08 |
| `/charter-laptop-cart` | Shopping Cart | TC_03, TC_16–TC_19 + DEF-02 |
| `/charter-laptop-navigation` | Navigation & Banners | TC_05, TC_11, TC_18 + DEF-04 |
| `/charter-laptop-search` | Search | TC_14, TC_20 + DEF-09 |
| `/charter-laptop-filters` | Filters & Sorting | TC_06–TC_10 + DEF-05, DEF-06 |
| `/charter-laptop-localization` | Localization | TC_01 + DEF-01 |
| `/charter-laptop-product` | Product Details | TC_15 |

**Tablet:**

| Type This | Area | Reference Test Cases |
|---|---|---|
| `/charter-tablet-navigation` | Navigation & Banners | TC_01–TC_08 |
| `/charter-tablet-product` | Product Discovery | TC_09–TC_12 |
| `/charter-tablet-cart` | Shopping Cart | TC_13–TC_15 |
| `/charter-tablet-localization` | Localization | TC_16–TC_17 |
| `/charter-tablet-filters` | Filters | TC_18–TC_23 |
| `/charter-tablet-registration` | Registration & Validation | TC_24–TC_34 |

**Mobile:**

| Type This | Area | Reference Test Cases |
|---|---|---|
| `/charter-mobile-search` | Search | TC_001, TC_015 + BUG_001, BUG_002 |
| `/charter-mobile-filters` | Filters | TC_002, TC_003 + BUG_003–005, BUG_010, BUG_015 |
| `/charter-mobile-localization` | Localization | TC_004 + BUG_011 |
| `/charter-mobile-navigation` | Navigation | TC_005, TC_009, TC_010, TC_013 + BUG_013 |
| `/charter-mobile-auth` | Auth & Login | TC_006 + BUG_006, BUG_014 |
| `/charter-mobile-cart` | Shopping Cart | TC_007, TC_011, TC_014 + BUG_007, BUG_008 |
| `/charter-mobile-layout` | Responsiveness & Layout | TC_008, TC_016, TC_017 + BUG_009, BUG_012 |

## Step 3: Wait for Output

After you type the command, OpenCode will:

1. **Parse** the reference test case document (Excel or PDF)
2. **Generate** the charter(s) using the AI model
3. **Save** the `.md` file(s) to `docs/skill-test-charters/output/`
4. **Combine** them into a styled HTML file
5. **Open** the HTML file in your default browser

The HTML file can be **printed to PDF** using `File → Print` (or `Cmd+P` on Mac) in your browser.

## Step 4: Review and Commit

Review the generated files, then commit and push:

```bash
git add docs/skill-test-charters/output/
git commit -m "Add test charters for [Platform]"
git push origin your-branch-name
```

---

## OpenCode: Quick Example

Here is the full workflow to generate a laptop authentication charter:

```bash
# 1. Navigate to the project
cd /path/to/qa-automation-sk

# 2. Start OpenCode
opencode

# 3. Inside OpenCode, type:
/charter-laptop-auth

# 4. Wait — the charter is generated, saved, and opened in the browser
# Output file: docs/skill-test-charters/output/CHR-LAP-AUTH-003.md
# HTML file:   docs/skill-test-charters/output/CHARTERS-LAPTOP.html

# 5. After reviewing, commit the output
# (exit OpenCode first with Ctrl+C, then run git commands)
```

You can also type a free-form message in OpenCode instead of using a command. For example:

```
Create a test charter for the tablet shopping cart area
```

The AI will recognize this request and use the `test-charter-generator` skill automatically.

---

# Method B: Using Any AI Tool (Manual Prompt)

If you don't have OpenCode installed, you can use any AI tool that supports file attachments.

## Prerequisites

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

## Step 1: Prepare Your Test Case Document

Place your test case file (Excel or PDF) in the `references/` folder:

```
docs/skill-test-charters/references/your-test-cases.xlsx
```

Before proceeding, review the document and identify:
- Which test cases **FAILED** (these are high-priority candidates for charters)
- Which **functional areas** are covered (e.g., Authentication, Shopping Cart, Navigation)
- Any **defect reports** linked to the failed test cases

## Step 2: Write the AI Prompt

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

## Step 3: Attach the Document and Run

1. **Attach** your test case file to the AI conversation (upload the `.xlsx` or `.pdf`)
2. **Paste** the prompt from Step 2 (with your values filled in)
3. **Send** the message and wait for the AI to generate the charters

## Step 4: Review the Generated Charters

The AI will produce one or more charters. Review each one for:

- ✅ **Completeness** — all sections present?
- ✅ **Accuracy** — do the test ideas match the original test cases?
- ✅ **Defect references** — are known defects correctly cited?
- ✅ **Test data** — are realistic test values suggested (emails, passwords, quantities)?
- ✅ **Scope boundaries** — is the scope clear and reasonable?

> **Tip:** The AI may group test cases differently than you expect. You can ask it to split or merge charters by providing follow-up instructions.

## Step 5: Save the Output

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

## Step 6: Commit and Push

```bash
git add docs/skill-test-charters/output/
git commit -m "Add test charters for [Platform]"
git push origin your-branch-name
```

---

# Comparison: OpenCode vs. Manual AI Prompting

| Feature | OpenCode (Method A) | Manual AI (Method B) |
|---|---|---|
| **Setup required** | Install OpenCode + API key | None (use web-based AI) |
| **Speed** | Fast — single command generates everything | Slower — copy prompts, upload files, copy output |
| **Consistency** | High — same skill/template every time | Variable — depends on how you write the prompt |
| **File access** | Direct — reads and writes project files | Manual — upload input, copy-paste output |
| **HTML output** | Automatic — generates and opens in browser | Manual — you need to create HTML yourself |
| **Repeatable** | Yes — same command, same format | No — results vary between sessions |

---

## Example: Generating Laptop Charters

Here is a real example from this project:

1. **Input file:** `references/test_case_and_proper_defect_report_laptop.xlsx`
   - Contains test cases for the PrestaShop demo on Laptop
   - Several test cases FAILED (TC_04, TC_12, TC_13) with defects (DEF-03, DEF-07, DEF-08)

2. **Using OpenCode:**
   ```
   opencode
   /charter-laptop
   ```

3. **Or using manual AI prompt:**
   > I have a test case document for the **Laptop** platform, testing the **PrestaShop Demo Shop** at **https://demo.prestashop.com/#/en/front**. Please analyze the attached document and generate exploratory test charters following the SBTM format...

4. **Output generated:**
   - `CHARTERS-LAPTOP.html` — HTML overview of all laptop charters
   - `CHR-LAP-AUTH-003.md` — Detailed charter for Authentication area (prioritized because TC_04, TC_12, TC_13 all FAILED)

5. **Charter highlights:**
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
Yes. The sections listed in the prompt template are a recommended starting point. You can add or remove sections based on your team's needs. If using OpenCode, edit the skill file at `.opencode/skills/test-charter-generator/SKILL.md` to change the template permanently.

### Q: Do I need to use OpenCode, or can I use another terminal AI tool?
OpenCode is optional. The pre-built commands and skills make it faster and more consistent, but you can achieve the same results with any AI tool using Method B (manual prompting). The key value is in the **skill definition** (charter template and grouping rules) and the **helper scripts** (parser and combiner), which can also be run independently.

### Q: How do I add a new command for a new platform or area?
Create a new `.md` file in `.opencode/commands/` following the existing pattern. For example, to add a command for a new "Accessibility" area on laptop, create `charter-laptop-accessibility.md` with the same structure as the other command files.

### Q: Can I use the OpenCode commands with a completely new set of test cases (e.g., a different project)?
**Not directly.** The pre-built `/charter-*` commands and the `parse_references.py` script are **hardcoded** to work with the current three reference files. See the section below for full details on what would need to change and what workarounds exist.

---

# Using the Skill with New / Different Test Cases

## Current Limitations

The OpenCode commands and parser script were built specifically for the three PrestaShop demo reference files. Several parts are hardcoded:

### What is hardcoded

| Component | What is hardcoded | Where |
|---|---|---|
| **`parse_references.py`** | File names: `task-testcase-report-tablet.pdf`, `test_case_and_proper_defect_report_laptop.xlsx`, `test-cases-mobile.xlsx` | Lines 40–42 |
| **`parse_references.py`** | Excel sheet names: `test_case_report`, `proper_defect_report`, `Test cases`, `Defects` | Lines 144, 175, 218, 245 |
| **`parse_references.py`** | Column positions (which column contains the test case ID, title, steps, etc.) | Lines 149–163, 225–241 |
| **`parse_references.py`** | Fallback data: all 34 tablet test cases are embedded directly in Python code | Lines 67–101 |
| **`parse_references.py`** | Platform names: only `tablet`, `laptop`, `mobile` are recognized | Throughout |
| **Commands** (`/charter-*`) | Specific platforms and test case ranges (e.g., `TC_01–TC_20`, `TC_01–TC_34`) | All command files |
| **`combine_charters.py`** | Platform prefixes (`CHR-TAB-`, `CHR-LAP-`, `CHR-MOB-`) | Lines 33–38 |

### What is NOT hardcoded (works generically)

| Component | What is generic | Notes |
|---|---|---|
| **Skill template** (`SKILL.md`) | The SBTM charter format, section structure, grouping rules, quality guidelines | Can be used with any test case data |
| **`combine_charters.py`** | The HTML styling and formatting | Works with any `.md` file that follows the charter template format |
| **Area classification** | The keyword-based area detection (`AREA_KEYWORDS`) | Works for common functional areas (navigation, cart, auth, etc.) |

## Workaround: Use Free-Form Messages (No Script Changes Needed)

Even without modifying the scripts, you can generate charters from new test case files by typing a **free-form message** in OpenCode instead of using a `/charter-*` command:

```
Read the file docs/skill-test-charters/references/my-new-project-tests.xlsx 
and generate SBTM test charters using the test-charter-generator skill.
The platform is "Desktop" and the application URL is https://my-app.example.com.
Save the output to docs/skill-test-charters/output/.
```

The AI will:
1. Read the file directly (without using `parse_references.py`)
2. Use the `test-charter-generator` skill's template to format the charters
3. Save the `.md` files to the output folder

**Limitations of this workaround:**
- The AI reads the file directly, so it may not parse complex Excel structures as accurately as the Python script
- The `combine_charters.py` HTML combiner may not work if the platform prefix doesn't match `TAB`, `LAP`, or `MOB`
- Results may vary between sessions (no script = no guaranteed consistency)

## Full Approach: Adding Support for a New Reference File

If you want the `/charter-*` commands to work with a new set of test cases, follow these steps:

### Step 1: Add the reference file

Place your new test case file in the references folder:

```bash
docs/skill-test-charters/references/your-new-test-cases.xlsx
```

### Step 2: Modify `parse_references.py`

Open `.opencode/skills/test-charter-generator/scripts/parse_references.py` and add:

1. **A new file path constant** (around line 40):
   ```python
   NEW_PROJECT_XLSX = os.path.join(REFS_DIR, "your-new-test-cases.xlsx")
   ```

2. **A new parser function** (after the existing `parse_mobile()` function). You need to know your Excel file's structure — which sheet contains the test cases and which columns contain the ID, title, steps, expected result, actual result, and status:
   ```python
   def parse_new_project():
       """Return structured test cases for the new project."""
       import openpyxl
       wb = openpyxl.load_workbook(NEW_PROJECT_XLSX)
       ws = wb["YourSheetName"]  # <-- Change to your sheet name
       test_cases = []
       for row in ws.iter_rows(min_row=2, values_only=True):
           cols = list(row)
           tc_id = str(cols[0] or "").strip()  # <-- Adjust column index
           if not tc_id.startswith("TC_"):
               continue
           test_cases.append({
               "id": tc_id,
               "title": str(cols[1] or ""),       # <-- Adjust column index
               "preconditions": str(cols[2] or ""),
               "steps": [str(cols[3] or "")],
               "expected": str(cols[4] or ""),
               "actual": str(cols[5] or ""),
               "status": str(cols[6] or "").strip().upper(),
               "area": _classify_area(str(cols[1] or "")),
           })
       return {
           "platform": "new_project",  # <-- Choose a platform name
           "source_file": NEW_PROJECT_XLSX,
           "total_test_cases": len(test_cases),
           "pass_count": sum(1 for tc in test_cases if tc["status"] == "PASS"),
           "fail_count": sum(1 for tc in test_cases if tc["status"] == "FAIL"),
           "test_cases": test_cases,
           "defects": [],
       }
   ```

3. **Register the new platform** in the `main()` function's platform dispatch (find the `if platform == "tablet"` block and add your new platform):
   ```python
   elif platform == "new_project":
       data = parse_new_project()
   ```

### Step 3: Update `combine_charters.py`

Add your new platform to the dictionaries (around lines 33–45):

```python
PLATFORM_PREFIX["new_project"] = "CHR-NEW-"
PLATFORM_LABEL["new_project"] = "New Project"
PLATFORM_COLOR["new_project"] = "#E74C3C"  # Choose a color
```

### Step 4: Create new commands

Create a new command file, e.g., `.opencode/commands/charter-new-project.md`:

```markdown
---
description: Generate SBTM test charters from new project reference
---

Here is the parsed content of the new project reference test cases:

!`python3 /path/to/qa-automation-sk/.opencode/skills/test-charter-generator/scripts/parse_references.py --platform new_project --summary 2>/dev/null`

Using the test-charter-generator skill, generate complete SBTM test charters for the new_project platform based on the above data. Follow the charter template defined in the skill. Save each charter to docs/skill-test-charters/output/ as individual markdown files named CHR-NEW-[AREA]-[NNN].md.

Once all charter .md files are saved, run this command to combine them into a single styled HTML file and open it in the browser:

!`python3 /path/to/qa-automation-sk/.opencode/skills/test-charter-generator/scripts/combine_charters.py --platform new_project --open 2>/dev/null`

Tell the user the HTML file has been generated and opened in the browser.
```

### Step 5: Test

```bash
opencode
/charter-new-project
```

### Summary: Effort Required

| Task | Effort | Required? |
|---|---|---|
| Add reference file to `references/` | 1 minute | Yes |
| Write a new parser function in `parse_references.py` | 15–30 minutes | Yes (for commands) |
| Update `combine_charters.py` platform maps | 2 minutes | Yes (for HTML output) |
| Create new command `.md` file(s) | 5–10 minutes | Optional (can use free-form instead) |
| **Use free-form message workaround (no code changes)** | **0 minutes** | **Alternative to all of the above** |

---

## References

- **OpenCode:** https://github.com/opencode-ai/opencode — Open-source terminal AI assistant
- **Session-Based Test Management (SBTM):** Bach, J. (1999). *Session-Based Test Management.*
- **Exploratory Testing Heuristics:**
  - GOLDFINGER — Does it follow conventions?
  - HICCUPS — History, Image, Comparable, Claims, User expectations, Product, Purpose, Standards
  - SFDIPOT — Structure, Function, Data, Interfaces, Platform, Operations, Time
  - FCC CUTS VIDS — Feature, Complexity, Claims, Configuration, Usability, Testability, Security, Compatibility, Usability, Timing, Stress, Installability, Development, Standards
- **PrestaShop Demo Shop:** https://demo.prestashop.com/#/en/front
