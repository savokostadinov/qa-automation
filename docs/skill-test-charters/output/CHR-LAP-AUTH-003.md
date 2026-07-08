=============================================================
  TEST CHARTER
=============================================================

Charter ID    : CHR-LAP-AUTH-003
Platform      : Laptop
Target URL    : https://demo.prestashop.com/#/en/front
Test Session  :

-------------------------------------------------------------
MISSION
-------------------------------------------------------------
Explore the Account Creation, Login, and Email Uniqueness area of the
PrestaShop demo shop on Laptop to discover defects related to registration
flow, password requirement visibility, duplicate email enforcement, and
authentication integrity after duplicate registration.

Focus Areas:
  - Account registration flow via checkout "Create an account" path
  - Password requirements visibility and inline feedback during input
  - Email uniqueness enforcement at registration time
  - Login behavior and account integrity after duplicate email registration
  - Inline form validation: required fields, field formats, error messages
  - Edge cases: special characters in name/email, very long inputs, empty submissions

-------------------------------------------------------------
SCOPE — WHAT IS COVERED
-------------------------------------------------------------
This session covers the full account creation and login surface on the
laptop browser, including the checkout-triggered registration path and the
dedicated registration/login pages. It re-executes the three reference test
cases that FAILED and adds exploratory depth around the known defect areas.

Reference Test Cases Included:
  - TC_04 : Test password requirements visibility during account creation  [FAIL]
  - TC_12 : Test unique email enforcement during registration              [FAIL]
  - TC_13 : Test login behavior after duplicate email registration         [FAIL]

-------------------------------------------------------------
SCOPE — WHAT IS NOT COVERED
-------------------------------------------------------------
  - Back-end authentication implementation or database layer
  - Password reset / forgot-password flow (separate charter)
  - Social login or third-party OAuth integrations
  - Admin panel user management
  - Performance or load testing of registration endpoints
  - Accessibility audit (WCAG compliance)
  - Payment processing during checkout
  - Guest checkout path (no account creation)

-------------------------------------------------------------
START CONDITIONS (Preconditions)
-------------------------------------------------------------
  - Browser/Device: Chrome (latest) and Safari on MacBook (macOS)
  - URL: https://demo.prestashop.com/#/en/front
  - Account status: logged out (no active session)
  - Cart state: contains at least one product (to reach checkout registration path)
  - Test data prepared before session:
      * Primary email:   testuser+lap003a@mailinator.com
      * Secondary email: testuser+lap003b@mailinator.com
      * Duplicate email for DEF-07/08 scenarios: testuser+lap003dup@mailinator.com
      * Weak password (fails complexity): password123
      * Strong password (meets complexity): Test@1234!
      * Password missing special char: TestPass99
      * Password missing uppercase: test@1234!
      * First name with 255 chars and with special characters (e.g. "José")
      * Email without @ symbol (malformed): notanemail.com
  - Network: standard broadband (no throttling)

-------------------------------------------------------------
TEST IDEAS & EXPLORATION NOTES
-------------------------------------------------------------

From Reference Test Cases:

1. TC_04 — Password requirements visibility during account creation
   Navigate to checkout, select "Create an account". Locate the password field.
   Before typing anything, check whether password rules (minimum length, required
   character types) are displayed inline, as a tooltip, or are absent entirely.
   Type a weak password (e.g. "password123") and attempt to submit; observe whether
   the error message names the specific unmet rule(s) or shows a generic failure.
   Verify that a compliant password (e.g. "Test@1234!") is accepted without error.
   Note: the reference test reports requirements are not shown clearly before submission
   — confirm and document the exact UX gap (no hint / hint appears only after submit /
   hint appears on focus but is incomplete).

2. TC_12 — Email uniqueness enforcement during registration
   Register a new account with testuser+lap003dup@mailinator.com and complete the flow.
   Log out. Return to the registration page. Attempt a second registration with the
   identical email address. Observe whether the system:
   (a) shows an inline error immediately on the email field, or
   (b) allows the form to submit and then shows a page-level error, or
   (c) silently creates a duplicate account (the known failure mode).
   If a second account is created, note whether the user is auto-logged-in under
   the new account or encounters an error.

3. TC_13 — Login after duplicate email registration
   Following the TC_12 duplicate registration scenario, attempt to log in using
   the original account credentials (same email, original password).
   Verify whether login succeeds, fails silently, or produces an error message.
   If login fails, attempt login with the second account's password to determine
   which credential set the system now accepts.

Exploratory Extensions (not in reference docs):

1. Password field — character-type boundary probing
   Systematically test passwords that are missing exactly one complexity requirement
   at a time: (a) no uppercase, (b) no digit, (c) no special character, (d) too short
   by one character. Confirm each produces a specific, actionable error message rather
   than a generic "invalid password" response.

2. Password visibility toggle
   Check whether a show/hide toggle exists on the password field. If present, verify
   it toggles the field type between "password" and "text". If absent, note as a
   usability gap (no severity defect, but noteworthy for UX).

3. Email field — format validation before submit
   Enter a malformed email (notanemail.com, user@, @domain.com) and tab out of the
   field. Verify whether inline validation fires on blur or only on form submit.
   Confirm the error message is specific ("Please enter a valid email address").

4. Required field handling — empty form submission
   Leave all fields blank and click submit. Verify all required fields are highlighted
   and an actionable error is shown for each. Note if any required field is unmarked.

5. Name fields — boundary and special character input
   Enter a first name of 255 characters; verify the field either accepts or caps it
   with a visible counter. Enter a name with accented characters (e.g. "José Müller")
   and verify the value is preserved correctly after account creation.

6. Account creation via login page vs. checkout path
   Locate whether there is a standalone registration page (separate from checkout).
   If one exists, verify whether the same password-requirements and email-uniqueness
   bugs are present on that path as on the checkout path.

7. Post-registration — account landing state
   After a successful registration, verify the user is automatically logged in, their
   name appears in the header, and they can navigate to "My Account" to see their
   details. Verify the email address saved in the account matches what was entered.

8. Session persistence
   After registering and being auto-logged-in, refresh the page and verify the session
   is maintained (user remains logged in, cart content preserved).

-------------------------------------------------------------
ORACLE — HOW TO DETERMINE PASS/FAIL
-------------------------------------------------------------

  - TC_04 expected: The password input field displays the complexity rules (minimum
    length, required character types) inline on the form — either as a persistent hint
    below the field, a tooltip on focus, or a progressive strength indicator — so the
    user knows the requirements BEFORE attempting submission. A generic post-submit
    error with no prior hint is incorrect behavior.

  - TC_12 expected: When submitting a registration form with an email address already
    associated with an existing account, the system must prevent account creation and
    display a clear validation message (e.g. "An account already exists for this email
    address"). No new account should be created; the existing account must remain intact.

  - TC_13 expected: After any failed or successful registration attempt, the original
    account created with a given email address must remain fully accessible. Login with
    the original email and password must succeed. If a duplicate was created, the
    system must at minimum protect the original account's credentials and session.

  - General form validation: all required-field errors must identify the specific field
    and the specific constraint violated; generic "form has errors" messages without
    field-level attribution are a usability defect.

  - PrestaShop UX conventions: error messages appear inline adjacent to the offending
    field; no page reload required for field-level validation feedback.

  - Data integrity: the email stored in the account after registration must exactly
    match the input (no silent trimming, no case conversion without display feedback).

-------------------------------------------------------------
KNOWN DEFECTS & RISKS (from reference docs)
-------------------------------------------------------------

  - TC_04 FAILED: Password requirements are not shown clearly before form submission.
    The user receives a rejection after submitting a non-compliant password with no
    advance guidance on what the rules are.
    DEFECT DEF-03: "Page content is not fully translated after language switch"
    (Note: DEF-03 title appears to be a copy-paste error in the source document;
    the description correctly describes the password requirements visibility issue
    in the Authentication module. Severity: Minor / Priority: Medium.)

  - TC_12 FAILED: Duplicate accounts can be created with the same email address.
    DEFECT DEF-07: "System allows creation of multiple accounts with the same email
    address." Severity: Major / Priority: High. The email uniqueness constraint is
    not enforced at the application layer.

  - TC_13 FAILED: Original account login is broken after a duplicate registration.
    DEFECT DEF-08: "Duplicate account registration with same email prevents login to
    original account." Severity: Critical / Priority: High. A second registration with
    the same email renders the original credentials invalid — a critical authentication
    integrity failure that can lead to account takeover or permanent lockout.

  Risk note: DEF-07 and DEF-08 are chained: DEF-07 is the root cause that enables
  DEF-08. If a fix is applied that blocks duplicate registrations (DEF-07), DEF-08
  should be re-tested to confirm the original account is also protected retroactively.

-------------------------------------------------------------
EXPLORATORY TESTING AREAS (beyond reference TCs)
-------------------------------------------------------------

  Heuristics to apply:
  - GOLDFINGER: Does the registration form follow established web conventions
    (inline validation, clear labeling, password rules visible)?
  - HICCUPS: Is the UI consistent (same validation style across all fields)?
    Is it correct (email stored matches email entered)? Is it usable (can a new
    user register without external help)?
  - SFDIPOT: Data — are edge-case inputs (empty, max-length, special chars)
    handled gracefully? Interfaces — does the checkout registration path behave
    identically to the standalone registration path?
  - FCC CUTS VIDS: Correct (no duplicate accounts), Complete (all required
    validations present), Consistent (same rules on all registration entry points).

  Specific areas to probe:
  1. Verify whether password rules are documented anywhere on the page (help text,
     tooltip, modal) — even if not shown inline, a link to requirements would be
     better than silence.
  2. Test the "Forgot password" link visibility on the login page — confirm it exists
     and leads to a recoverable flow (scope: verify link is present only; do not
     execute the full reset flow in this session).
  3. Attempt to register with an email that has leading/trailing spaces
     (e.g. " user@test.com ") — verify trimming behavior.
  4. Verify the "Sign in" and "Create account" CTAs are clearly distinguishable on
     the login/registration page to avoid user confusion.
  5. Cross-browser check: repeat TC_04 in both Chrome and Safari to determine if the
     password-hint gap is browser-specific (source defect was reported on Safari).

-------------------------------------------------------------
EXIT CONDITIONS (When to stop this session)
-------------------------------------------------------------
  - Time box reached (recommended: 90 minutes)
  - TC_04, TC_12, TC_13 have all been re-executed and results recorded
  - All numbered exploratory ideas (1–8) have been investigated or explicitly deferred
  - Any Critical-severity defect (e.g. account lockout replication of DEF-08) is
    immediately reported and the session lead is notified
  - All new defects have draft defect reports created before session close

-------------------------------------------------------------
OUTPUT / DELIVERABLES
-------------------------------------------------------------
  - Completed session sheet (tester fills in: actual results, time log, notes)
  - Re-execution results for TC_04, TC_12, TC_13 (PASS / FAIL / BLOCKED)
  - New defect reports for any bugs found beyond DEF-03, DEF-07, DEF-08
  - Notes on exploratory observations (unexpected behaviors, UX gaps)
  - Confirmed status of DEF-03, DEF-07, DEF-08: still reproducible / fixed / changed
  - Recommendation: re-test, defer, escalate, or close for each open defect
  - Session debrief: report time-on-test, time-on-bugs, and time-on-other activities;
    bring all new defect reports and open questions to the debrief meeting

-------------------------------------------------------------
REFERENCES
-------------------------------------------------------------
  Source file : test_case_and_proper_defect_report_laptop.xlsx
  Platform    : Laptop
  Area        : Auth & Registration (TC_04, TC_12, TC_13 | DEF-03, DEF-07, DEF-08)
  SBTM method : Bach, J. (1999). Session-Based Test Management.
  Shop URL    : https://demo.prestashop.com/#/en/front
=============================================================
