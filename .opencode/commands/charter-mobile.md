---
description: Generate SBTM test charters from mobile reference (TC_001–TC_017 + 15 bugs) and open as HTML in browser
---

Here is the parsed content of the mobile reference test cases and defects:

!`python3 /Users/skostadi/IdeaProjects/qa-automation-sk/.opencode/skills/test-charter-generator/scripts/parse_references.py --platform mobile --summary 2>/dev/null`

Using the test-charter-generator skill, generate complete SBTM test charters for the mobile platform based on the above data. Follow the charter template defined in the skill. Save each charter to docs/skill-test-charters/output/ as individual markdown files named CHR-MOB-[AREA]-[NNN].md.

Once all charter .md files are saved, run this command to combine them into a single styled HTML file and open it in the browser:

!`python3 /Users/skostadi/IdeaProjects/qa-automation-sk/.opencode/skills/test-charter-generator/scripts/combine_charters.py --platform mobile --open 2>/dev/null`

Tell the user the HTML file has been generated and opened in the browser. It can be printed to PDF using File → Print (or Cmd+P) in the browser.
