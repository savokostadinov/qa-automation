---
description: Generate SBTM charter — Laptop · Localization & Language Switch
---

Here are the laptop test cases for the Localization area:

!`python3 /Users/skostadi/IdeaProjects/qa-automation-sk/.opencode/skills/test-charter-generator/scripts/parse_references.py --platform laptop --area localization --summary 2>/dev/null`

Using the test-charter-generator skill, generate a complete SBTM test charter for the **Laptop — Localization** area based on the above data. Include relevant defects from the laptop defect report (DEF-01). Follow the charter template in the skill. Save the output to docs/skill-test-charters/output/CHR-LAP-LOCALE-001.md.

Once the .md file is saved, run this command to combine all laptop charters into a single styled HTML file and open it in the browser:

!`python3 /Users/skostadi/IdeaProjects/qa-automation-sk/.opencode/skills/test-charter-generator/scripts/combine_charters.py --platform laptop --open 2>&1`

Tell the user the HTML file has been generated and opened in the browser. It can be printed to PDF using File → Print (or Cmd+P) in the browser.
