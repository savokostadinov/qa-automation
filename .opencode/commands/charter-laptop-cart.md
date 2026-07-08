---
description: Generate SBTM charter — Laptop · Shopping Cart & Pricing Accuracy
---

Here are the laptop test cases for the Cart area:

!`python3 /Users/skostadi/IdeaProjects/qa-automation-sk/.opencode/skills/test-charter-generator/scripts/parse_references.py --platform laptop --area cart --summary 2>/dev/null`

Using the test-charter-generator skill, generate a complete SBTM test charter for the **Laptop — Shopping Cart** area based on the above data. Include relevant defects (DEF-02: cart total rounding). Follow the charter template in the skill. Save the output to docs/skill-test-charters/output/CHR-LAP-CART-002.md.

Once the .md file is saved, run this command to combine all laptop charters into a single styled HTML file and open it in the browser:

!`python3 /Users/skostadi/IdeaProjects/qa-automation-sk/.opencode/skills/test-charter-generator/scripts/combine_charters.py --platform laptop --open 2>&1`

Tell the user the HTML file has been generated and opened in the browser. It can be printed to PDF using File → Print (or Cmd+P) in the browser.
