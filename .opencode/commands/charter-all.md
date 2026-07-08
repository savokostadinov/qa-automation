---
description: Generate SBTM test charters for ALL platforms (tablet + laptop + mobile) and open as HTML in browser
---

Here is the parsed content of all three platform reference files:

!`python3 /Users/skostadi/IdeaProjects/qa-automation-sk/.opencode/skills/test-charter-generator/scripts/parse_references.py --platform all --summary 2>/dev/null`

Using the test-charter-generator skill, generate complete SBTM test charters for all three platforms (tablet, laptop, mobile) based on the above data. Follow the charter template defined in the skill. Save each charter to docs/skill-test-charters/output/ as individual markdown files using the naming convention CHR-[PLATFORM]-[AREA]-[NNN].md.

Once all charter .md files are saved, run this command to combine them all into a single styled HTML file and open it in the browser:

!`python3 /Users/skostadi/IdeaProjects/qa-automation-sk/.opencode/skills/test-charter-generator/scripts/combine_charters.py --platform all --open 2>/dev/null`

Tell the user the HTML file has been generated and opened in the browser. It can be printed to PDF using File → Print (or Cmd+P) in the browser.
