=============================================================
  TEST CHARTER
=============================================================

Charter ID    : CHR-TAB-CART-006
Platform      : Tablet
Target URL    : https://demo.prestashop.com/#/en/front
Test Session  :

-------------------------------------------------------------
MISSION
-------------------------------------------------------------
Explore the Shopping Cart area of the PrestaShop demo shop on Tablet to
discover defects and verify that quantity management rules are enforced
correctly for both physical and digital products, and that those limits
are applied consistently across the product detail page and the cart/checkout
page.

Focus Areas:
  - Quantity limit enforcement for physical products (stock-based cap)
  - Absence of quantity restriction for digital/downloadable products
  - Consistency of quantity rules between the product detail page and the cart
  - Edge-case boundary inputs (0, negative, max, max+1, non-numeric, decimals)
  - UI feedback quality when a quantity rule is violated (inline error, cap, or block)
  - Cart totals and line-item price accuracy after quantity changes

-------------------------------------------------------------
SCOPE — WHAT IS COVERED
-------------------------------------------------------------
This session focuses on quantity management behaviour in the cart and on the
product detail page for both physical and digital product types on a tablet
viewport.

Reference Test Cases Included:
  - TC_13 : Verify quantity limit is enforced for physical products      [PASS]
  - TC_14 : Verify no quantity limit for digital products                [PASS]
  - TC_15 : Verify quantity limit is consistent across application       [PASS]

-------------------------------------------------------------
SCOPE — WHAT IS NOT COVERED
-------------------------------------------------------------
  - Payment processing or checkout completion (no real transactions)
  - Back-end stock management or inventory administration
  - Performance or load testing of the cart API
  - Accessibility standards (WCAG) beyond basic tap-reachability
  - Guest vs. logged-in price differences (out of scope for this session)
  - Shipping cost calculations and coupon/discount codes
  - Wishlist or save-for-later features

-------------------------------------------------------------
START CONDITIONS (Preconditions)
-------------------------------------------------------------
  - Device / Browser: Tablet viewport (768–1024 px wide) — Chrome or Safari
  - URL: https://demo.prestashop.com/#/en/front
  - Account status: logged out (guest) — re-test key steps logged in if time permits
  - Cart state: empty at session start; clear cart between sub-scenarios
  - Physical product identified: a product with a visible stock quantity
    (e.g. "Hummingbird Printed T-Shirt" or "Mug The Best Is Yet To Come")
  - Digital product identified: a downloadable/virtual product
    (e.g. a vector graphic from the "Stationery" category)
  - Test quantity values prepared: 0, 1, max-1, max, max+1, 70000, -1, 0.5, "abc"
  - Note the displayed maximum on the product page before each test and record it

-------------------------------------------------------------
TEST IDEAS & EXPLORATION NOTES
-------------------------------------------------------------
From Reference Test Cases:

  1. TC_13 — On a physical product page, locate and note the stated maximum
     quantity (displayed as "Max: X", greyed-out stepper cap, or validation
     tooltip). Attempt to type max+1 directly into the quantity field.
     Verify the system either caps the value at max, shows an inline error,
     or prevents Add-to-Cart. Then test at max-1 (should be accepted),
     at max (should be accepted), and at 0 or a negative value (should be
     rejected with a clear error message). Record the exact UI response for
     each boundary value.

  2. TC_14 — Open a digital product (e.g., vector graphic). Attempt to enter
     a very large quantity (e.g., 70000) into the quantity field. Verify the
     system accepts it without restriction and adds the item to the cart
     successfully. Confirm no stock-cap message appears and no error is shown.
     Also verify the cart line-item total reflects the large quantity correctly.

  3. TC_15 — Add a physical product to the cart at its maximum allowed quantity
     (confirmed from TC_13). Navigate to the Cart page. Attempt to increment
     the quantity further from within the cart. Verify the same stock limit is
     enforced on the cart page as on the product detail page. Then test the same
     consistency check for the digital product: confirm there is still no
     restriction when updating quantity from within the cart.

Exploratory Extensions (not in reference docs):

  1. Stepper button behaviour — Use the + / stepper buttons (rather than
     typing) to reach the maximum for a physical product. Verify the + button
     becomes disabled or stops incrementing once the max is reached, rather
     than allowing over-limit values silently.

  2. Non-numeric and decimal inputs — Type "abc", "0.5", "-5", and an empty
     string into the quantity field for a physical product. Verify appropriate
     validation messages appear and the cart is not updated with an invalid value.

  3. Cart badge / mini-cart count — Verify that the cart icon badge in the
     header accurately reflects the total number of items after each add,
     remove, or quantity-change action on a tablet viewport.

  4. Remove item from cart — Add a product, then reduce quantity to 0 or click
     the remove icon. Verify the item is removed cleanly and the cart empty state
     is shown without layout issues on the tablet viewport.

  5. Multiple product types in one cart — Add one physical product at max
     quantity and one digital product at a high quantity (e.g., 500) in the same
     cart session. Verify both line-item totals and the order total are
     mathematically correct and the physical product limit is still respected
     while the digital product remains unrestricted.

  6. Session persistence — Add items to the cart, navigate away to a category
     page, then return to the cart. Verify the quantity values are preserved
     and the limits are still enforced after navigation.

  A. Investigate whether the quantity field enforces limits on blur/focus-out
     or only on form submission (lazy vs. eager validation).
  B. Check whether the same product added twice (once from the product page,
     once from quick-view) accumulates quantity correctly and the total does
     not exceed the stock limit.

-------------------------------------------------------------
ORACLE — HOW TO DETERMINE PASS/FAIL
-------------------------------------------------------------
  - TC_13 expected: the system prevents the tester from adding more units than
    the displayed available stock for a physical product. The quantity field
    must not accept a value above the stated maximum; any attempt must result
    in the value being capped, an inline validation message, or a blocked
    Add-to-Cart action. Adding at max-1 and max must succeed.
  - TC_14 expected: a digital (downloadable) product has no stock-based
    quantity cap. Entering 70000 must be accepted and the product must be
    added to the cart successfully. No "maximum quantity" error should appear.
  - TC_15 expected: the quantity limit visible on the product detail page and
    the limit enforced on the cart page must be identical for the same product.
    Changing quantity in the cart must not allow values that the product page
    would have blocked.
  - General cart correctness: line-item price = unit price × quantity (no
    rounding errors visible at any tested quantity).
  - UI quality: error messages must be readable and clearly positioned on a
    tablet viewport; no layout overflow or truncated text when error banners appear.
  - PrestaShop conventions: interactive quantity controls (stepper buttons,
    input fields) must be reachable by tap; no element should require hover to
    activate on a touch device.

-------------------------------------------------------------
KNOWN DEFECTS & RISKS (from reference docs)
-------------------------------------------------------------
  No FAIL results were recorded for TC_13, TC_14, or TC_15 in the reference
  document. All three test cases passed in the reference session.

  Residual risks to probe:
  - The reference steps for TC_13 specify testing "beyond available stock" but
    do not record the exact max value used. Re-confirm the current stock level
    is consistent with the reference run (stock may change on the live demo).
  - TC_14 used 70000 as the large-quantity test value. Verify this value still
    renders without UI truncation or JavaScript overflow on the current demo build.

-------------------------------------------------------------
EXPLORATORY TESTING AREAS (beyond reference TCs)
-------------------------------------------------------------
  Heuristics to apply:
  - GOLDFINGER: Does quantity enforcement follow the same rules as other
    e-commerce shops the tester knows? Are the error messages industry-standard?
  - HICCUPS: Is the behaviour consistent between product detail page and cart?
    Are prices correct? Is the UI usable (no truncated messages, no overflow)?
  - SFDIPOT: Structure (cart widget layout on tablet), Function (add/remove/update),
    Data (boundary quantities, non-numeric inputs), Interfaces (stepper buttons,
    direct text input), Platform (tablet touch targets, viewport), Operations
    (multi-step: add → navigate → update), Time (session persistence)
  - FCC CUTS VIDS: Correct (prices match), Consistent (limits same on both pages),
    Complete (all product types enforced), Unambiguous (error messages clear)

  Specific areas to probe:
  - Verify stepper (+/-) buttons are large enough to tap accurately on a tablet
    (minimum 44×44 px touch target per mobile UX guidelines)
  - Verify that the quantity input field is wide enough to display 5-digit values
    (e.g., 70000) without truncation on tablet viewport
  - Check that updating quantity via the cart page triggers a visible recalculation
    of the line total before the user navigates away (no silent background update)
  - Verify that removing all instances of a product leaves the cart in a clean
    empty state with a visible "Your cart is empty" message and a clear CTA

-------------------------------------------------------------
EXIT CONDITIONS (When to stop this session)
-------------------------------------------------------------
  - Time box reached (recommended: 90 minutes)
  - TC_13, TC_14, and TC_15 have been fully re-executed against the live demo
  - All six numbered exploratory extensions have been investigated or explicitly
    deferred with a note
  - Any critical blocker (e.g., cart completely non-functional) is stopped and
    reported immediately without waiting for the time box to expire

-------------------------------------------------------------
OUTPUT / DELIVERABLES
-------------------------------------------------------------
  - Completed session sheet (time-on-test, time-on-bugs, time-on-other recorded)
  - New defect reports for any bugs found during the session
  - Notes on exploratory observations including unexpected UI behaviours,
    boundary values that produced surprising results, or inconsistencies
    between product detail page and cart page quantity handling
  - Recommendation for each reference TC: reconfirmed pass, new failure,
    or behaviour changed since reference run
  - Session debrief: report time-on-test, time-on-bugs, and time-on-other
    activities; bring all new defect reports and open questions to the debrief
    meeting

-------------------------------------------------------------
REFERENCES
-------------------------------------------------------------
  Source file : task-testcase-report-tablet.pdf (TC_13–TC_15, area: cart)
  Platform    : Tablet
  SBTM method : Bach, J. (1999). Session-Based Test Management.
  Shop URL    : https://demo.prestashop.com/#/en/front
=============================================================
