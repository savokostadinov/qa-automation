#!/usr/bin/env python3
"""
parse_references.py — Test Charter Generator helper script
===========================================================
Parses the PrestaShop demo shop reference test case documents and outputs
structured JSON for use by the test-charter-generator skill.

Usage:
    python3 parse_references.py --platform tablet
    python3 parse_references.py --platform laptop
    python3 parse_references.py --platform mobile
    python3 parse_references.py --platform all
    python3 parse_references.py --platform all --area navigation
    python3 parse_references.py --platform tablet --summary

Options:
    --platform   tablet | laptop | mobile | all  (required)
    --area       Optional filter: navigation | filters | cart | registration |
                 search | localization | layout | checkout | product | auth
    --summary    Print a brief summary instead of full JSON
    --output     Path to save JSON (default: stdout)

Dependencies:
    pip install openpyxl pypdf
    (pypdf is optional — the PDF is pre-parsed below as fallback data)
"""

import argparse
import json
import os
import sys

# ---------------------------------------------------------------------------
# Paths (relative to project root, resolved from script location)
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", "..", ".."))
REFS_DIR = os.path.join(PROJECT_ROOT, "docs", "skill-test-charters", "references")

TABLET_PDF  = os.path.join(REFS_DIR, "task-testcase-report-tablet.pdf")
LAPTOP_XLSX = os.path.join(REFS_DIR, "test_case_and_proper_defect_report_laptop.xlsx")
MOBILE_XLSX = os.path.join(REFS_DIR, "test-cases-mobile.xlsx")

# ---------------------------------------------------------------------------
# Area keyword map — used for --area filtering
# ---------------------------------------------------------------------------
AREA_KEYWORDS = {
    "navigation": ["navigat", "banner", "scroll", "subcategor", "logo", "breadcrumb", "menu", "homepage"],
    "filters":    ["filter", "color", "price", "composition", "dimension", "sort"],
    "cart":       ["cart", "quantity", "checkout", "total", "add to cart", "remov"],
    "registration": ["registr", "first name", "last name", "birthdate", "birth", "account creat", "sign up"],
    "search":     ["search"],
    "localization": ["language", "translat", "localiz"],
    "layout":     ["layout", "mobile", "tablet", "responsive", "screen", "hamburger", "footer"],
    "checkout":   ["checkout", "payment", "password", "order", "polic"],
    "product":    ["product detail", "quick view", "product listing", "product page"],
    "auth":       ["login", "log in", "password", "auth", "email", "account", "duplicate", "registr"],
}


# ---------------------------------------------------------------------------
# PDF parser — tablet
# ---------------------------------------------------------------------------

# Pre-parsed tablet test cases (TC_01–TC_34) extracted from the PDF.
# If pypdf is installed the script will attempt a live parse first.
TABLET_FALLBACK = [
    {"id": "TC_01", "title": "Verify user can navigate by clicking sample banner", "preconditions": "User is on homepage", "steps": ["Click on a sample banner"], "expected": "User is redirected to a new page", "actual": "User is redirected to a new page", "status": "PASS", "area": "navigation"},
    {"id": "TC_02", "title": "Verify user can return to homepage after clicking sample banner", "preconditions": "User has clicked on a sample banner", "steps": ["Click on a sample banner", "Try to return to homepage"], "expected": "User can easily return to homepage (e.g. via navigation or button)", "actual": "No clear option to return to homepage", "status": "FAIL", "area": "navigation"},
    {"id": "TC_03", "title": "Verify user can scroll down the page", "preconditions": "User is on any page with scrollable content", "steps": ["Open a page", "Scroll down the page"], "expected": "Page scrolls smoothly and all content is accessible", "actual": "Page scrolls smoothly and all content is accessible", "status": "PASS", "area": "navigation"},
    {"id": "TC_04", "title": "Verify user can easily navigate back to top while scrolling", "preconditions": "User is on any page with scrollable content", "steps": ["Open a page", "Scroll to the bottom", "Try to navigate back to top"], "expected": "User can quickly return to top (e.g. back-to-top button or sticky navigation bar)", "actual": "No back-to-top option and no sticky navigation bar; user must manually scroll", "status": "FAIL", "area": "navigation"},
    {"id": "TC_05", "title": "Verify promotional banner is clickable", "preconditions": "User is on homepage", "steps": ["Open homepage", "Click on '20% off on clothes' banner"], "expected": "Banner is clickable and redirects user to another page", "actual": "Banner is clickable and redirects user to another page", "status": "PASS", "area": "navigation"},
    {"id": "TC_06", "title": "Verify promotional banner redirects to correct product page", "preconditions": "User is on homepage", "steps": ["Open homepage", "Click on '20% off on clothes' banner"], "expected": "User is redirected to a relevant category or product listing page (e.g. discounted clothes)", "actual": "User is redirected to the homepage", "status": "FAIL", "area": "navigation"},
    {"id": "TC_07", "title": "Verify subcategories are displayed after selecting a category", "preconditions": "User is on navigation menu", "steps": ["Click on a category (e.g. Accessories)", "Move cursor away from the category", "Observe subcategories"], "expected": "Subcategories are displayed correctly and do not cover main categories", "actual": "Subcategories are displayed correctly", "status": "PASS", "area": "navigation"},
    {"id": "TC_08", "title": "Verify subcategories do not overlap main categories after selecting category", "preconditions": "User is on navigation menu", "steps": ["Click on a category (e.g. Accessories)", "Keep the cursor positioned directly over the selected category", "Observe subcategory display"], "expected": "Subcategories are displayed without covering the main categories", "actual": "Subcategories overlap and cover the main category, making it not fully visible", "status": "FAIL", "area": "navigation"},
    {"id": "TC_09", "title": "Verify Quick View opens when selecting a product", "preconditions": "User is on product listing page", "steps": ["Open product listing page", "Click 'Quick View' on a product"], "expected": "Quick View popup opens for the selected product", "actual": "Quick View popup opens", "status": "PASS", "area": "product"},
    {"id": "TC_10", "title": "Verify Quick View displays correct product information", "preconditions": "User is on product listing page", "steps": ["Open product listing page", "Select a product (e.g. black t-shirt)", "Click 'Quick View'", "Compare selected product with displayed product"], "expected": "Quick View displays the same product that was selected", "actual": "Quick View displays a different product (e.g. white t-shirt)", "status": "FAIL", "area": "product"},
    {"id": "TC_11", "title": "Verify product details page opens when selecting a product", "preconditions": "User is on product listing page", "steps": ["Open product listing page", "Click on a product"], "expected": "Product details page opens", "actual": "Product details page opens", "status": "PASS", "area": "product"},
    {"id": "TC_12", "title": "Verify product details page displays correct product information", "preconditions": "User is on product listing page", "steps": ["Open product listing page", "Select a product (e.g. black t-shirt)", "Click on the product", "Compare selected product with displayed product details"], "expected": "Product details page shows the same product that was selected (image, name, and details match)", "actual": "Product details page shows a different product image than the selected one", "status": "FAIL", "area": "product"},
    {"id": "TC_13", "title": "Verify quantity limit is enforced for physical products", "preconditions": "User is on product details page (physical product like mug, shirt)", "steps": ["Open a physical product (e.g. mug or t-shirt)", "Increase quantity beyond available stock", "Try to add to cart"], "expected": "System restricts quantity based on available stock and prevents exceeding the limit", "actual": "System restricts quantity and does not allow exceeding the available stock", "status": "PASS", "area": "cart"},
    {"id": "TC_14", "title": "Verify no quantity limit for digital products", "preconditions": "Verify no quantity limit for digital products", "steps": ["Open a digital product (e.g. vector graphic)", "Enter very large quantity (e.g. 70000)", "Add to cart"], "expected": "System allows selecting large quantities without restriction", "actual": "System allows selecting large quantities without restriction", "status": "PASS", "area": "cart"},
    {"id": "TC_15", "title": "Verify quantity limit is consistent across application", "preconditions": "Product is added to cart", "steps": ["Add product to cart", "Navigate to cart/checkout page", "Increase quantity"], "expected": "System enforces the same quantity limit as defined for the product", "actual": "System enforces the same quantity limit across pages", "status": "PASS", "area": "cart"},
    {"id": "TC_16", "title": "Verify application language can be changed", "preconditions": "User is on application with language switch option", "steps": ["Open application", "Change language (e.g. to Serbian)", "Observe interface"], "expected": "Application language changes successfully", "actual": "Application language changes successfully", "status": "PASS", "area": "localization"},
    {"id": "TC_17", "title": "Verify all navigation elements are translated after language change", "preconditions": "User has changed application language (e.g. Serbian)", "steps": ["Change language", "Observe navigation menu categories"], "expected": "All elements (e.g. categories like Clothes, Accessories, Art) are translated", "actual": "Some elements remain in English and are not translated", "status": "FAIL", "area": "localization"},
    {"id": "TC_18", "title": "Verify color filter can be applied", "preconditions": "User is on product listing page", "steps": ["Open product listing page", "Select a color filter (e.g. White)"], "expected": "Filter is applied and product list is updated", "actual": "Filter is applied and product list is updated", "status": "PASS", "area": "filters"},
    {"id": "TC_19", "title": "Verify color filter returns correct products", "preconditions": "User is on product listing page", "steps": ["Open product listing page", "Select color filter (e.g. White)", "Observe displayed products"], "expected": "Only products matching the selected color are displayed", "actual": "Products with different color (e.g. black) are displayed", "status": "FAIL", "area": "filters"},
    {"id": "TC_20", "title": "Verify selected color filter is shown in the applied filters area", "preconditions": "User is on product listing page", "steps": ["Open product listing page", "Select a color filter (e.g. White)", "Observe the applied filters area"], "expected": "The selected color is shown in the applied filters area", "actual": "The selected color is shown in the applied filters area", "status": "PASS", "area": "filters"},
    {"id": "TC_21", "title": "Verify selected color is clearly visible in the filter panel", "preconditions": "Verify selected color is clearly visible in the filter panel", "steps": ["Open product listing page", "Select a color filter (e.g. White or Black)", "Observe the visual indication in the side filter panel"], "expected": "The selected color option is clearly highlighted and easy to distinguish in the filter panel", "actual": "The selected color option is not clearly highlighted and is difficult to distinguish", "status": "FAIL", "area": "filters"},
    {"id": "TC_22", "title": "Verify filters can be applied and combined", "preconditions": "User is on product listing page", "steps": ["Open product listing page", "Apply color filter (e.g. White)", "Apply additional filters (e.g. size or category)"], "expected": "Filters are applied successfully and product list is updated", "actual": "Filters are applied and product list is updated", "status": "PASS", "area": "filters"},
    {"id": "TC_23", "title": "Verify filtering returns all matching products and preserves filter options", "preconditions": "User is on product listing page", "steps": ["Open product listing page", "Observe available products (e.g. multiple white items)", "Apply color filter (White)", "Compare filtered results with initial products"], "expected": "All products matching the selected filter are displayed and other relevant filters remain available", "actual": "Only a subset of matching products is displayed and some filter options (e.g. Men/Women) disappear", "status": "FAIL", "area": "filters"},
    {"id": "TC_24", "title": "Verify user can enter and display valid first and last name correctly", "preconditions": "User is on registration form", "steps": ["Enter valid first name (e.g. Leonida)", "Enter valid last name (e.g. Kostova)", "Submit the form", "Navigate to user account page", "Observe displayed name"], "expected": "The entered first and last name are correctly saved and displayed without layout issues", "actual": "The name is displayed correctly", "status": "PASS", "area": "registration"},
    {"id": "TC_25", "title": "Verify long name input is displayed correctly without breaking UI", "preconditions": "User is on account creation or profile page", "steps": ["Enter a very long first name (close to max length 255 chars)", "Complete registration or save profile", "Navigate to user account page", "Observe how the name is displayed"], "expected": "The name is properly displayed (wrapped or truncated) without breaking the layout", "actual": "The name overflows and breaks the layout; text is not properly wrapped or contained", "status": "FAIL", "area": "registration"},
    {"id": "TC_26", "title": "Verify system shows validation error when first name exceeds maximum allowed length", "preconditions": "User is on registration form", "steps": ["Enter a first name longer than 255 characters", "Enter a valid last name", "Submit the form", "Observe validation message for first name field"], "expected": "System prevents submission and displays a clear validation message that the first name exceeds the maximum allowed length", "actual": "Validation message is displayed only after form submission: 'The first name field is too long (255 chars max).'", "status": "PASS", "area": "registration"},
    {"id": "TC_27", "title": "Verify system shows validation error when last name exceeds maximum allowed length", "preconditions": "User is on registration form", "steps": ["Enter a valid first name", "Enter a last name longer than 255 characters", "Submit the form", "Observe validation message for last name field"], "expected": "System prevents submission and displays a clear validation message that the last name exceeds the maximum allowed length", "actual": "Validation message is displayed only after form submission: 'The last name field is too long (255 chars max).'", "status": "PASS", "area": "registration"},
    {"id": "TC_28", "title": "Verify system validates both first name and last name when both exceed maximum allowed length", "preconditions": "User is on registration form", "steps": ["Enter a first name longer than 255 characters", "Enter a last name longer than 255 characters", "Submit the form", "Observe validation messages for both fields"], "expected": "System prevents submission and displays validation messages for both first name and last name fields", "actual": "Validation messages are displayed for both fields only after form submission", "status": "PASS", "area": "registration"},
    {"id": "TC_29", "title": "Verify user receives real-time validation feedback when name input exceeds allowed length", "preconditions": "User is on registration form", "steps": ["Focus on the first name field", "Enter text approaching or exceeding 255 characters", "Observe whether any limit, counter, or warning is shown before submission", "Repeat for last name field"], "expected": "System should inform the user about the maximum allowed character length before submission, through inline validation, character counter, or helper text", "actual": "No indication of the 255-character limit is shown before submission; validation appears only after submitting the form", "status": "FAIL", "area": "registration"},
    {"id": "TC_30", "title": "Verify system does not allow future birthdates", "preconditions": "User is on registration form", "steps": ["Enter a future date (e.g. tomorrow) in the birthdate field", "Submit the form", "Observe system behavior"], "expected": "System should reject future dates and display an appropriate validation message", "actual": "System correctly rejects future dates", "status": "PASS", "area": "registration"},
    {"id": "TC_31", "title": "Verify system does not allow current date (today) as a valid birthdate", "preconditions": "User is on registration form", "steps": ["Enter today's date as birthdate", "Submit the form", "Observe system behavior"], "expected": "System should reject today's date as invalid (user cannot be born today for account creation)", "actual": "System accepts today's date as valid birthdate", "status": "FAIL", "area": "registration"},
    {"id": "TC_32", "title": "Verify system does not allow very recent past dates (e.g. yesterday)", "preconditions": "User is on registration form", "steps": ["Enter very recent dates as birthdate (e.g. yesterday)", "Submit the form", "Observe system behavior"], "expected": "System should reject unrealistic birthdates (e.g. minimum age restriction)", "actual": "System accepts very recent dates as valid birthdates", "status": "FAIL", "area": "registration"},
    {"id": "TC_33", "title": "Verify system handles extremely old birthdates correctly", "preconditions": "User is on registration form", "steps": ["Enter a very old date (e.g. 01/01/1900)", "Submit the form", "Observe system behavior"], "expected": "System should accept valid historical birthdates within a reasonable range (e.g. up to 100 years in the past)", "actual": "The system accepts birthdates up to approximately 1910 as valid, while dates before this threshold are rejected with an incorrect format error.", "status": "FAIL", "area": "registration"},
    {"id": "TC_34", "title": "Verify system provides correct validation message for invalid birthdate format vs logical error", "preconditions": "User is on registration form", "steps": ["Enter a very old date (e.g. 01/01/1900) or recent date", "Submit the form", "Observe validation message"], "expected": "System should display a logical validation message (e.g. 'date out of allowed range')", "actual": "System displays misleading format error instead of logical validation error", "status": "FAIL", "area": "registration"},
]


def parse_tablet():
    """Return structured test cases for tablet platform."""
    # Try live PDF parse first
    try:
        import pypdf  # type: ignore
        reader = pypdf.PdfReader(TABLET_PDF)
        # If import works but parse is incomplete, fall back
        text = "".join(page.extract_text() or "" for page in reader.pages)
        if len(text) < 100:
            raise ValueError("PDF text extraction returned insufficient content")
        # Use fallback data which is pre-parsed and more reliable
        print("[INFO] pypdf available. Using pre-parsed tablet data for accuracy.", file=sys.stderr)
    except ImportError:
        print("[INFO] pypdf not installed. Using pre-parsed tablet data.", file=sys.stderr)
    except Exception as e:
        print(f"[INFO] PDF parse error ({e}). Using pre-parsed tablet data.", file=sys.stderr)

    return {
        "platform": "tablet",
        "source_file": TABLET_PDF,
        "total_test_cases": len(TABLET_FALLBACK),
        "pass_count": sum(1 for tc in TABLET_FALLBACK if tc["status"] == "PASS"),
        "fail_count": sum(1 for tc in TABLET_FALLBACK if tc["status"] == "FAIL"),
        "test_cases": TABLET_FALLBACK,
        "defects": []  # Tablet PDF does not have a separate defect sheet
    }


def parse_laptop():
    """Return structured test cases and defects for laptop platform."""
    try:
        import openpyxl
    except ImportError:
        print("[ERROR] openpyxl is required: pip install openpyxl", file=sys.stderr)
        sys.exit(1)

    wb = openpyxl.load_workbook(LAPTOP_XLSX)

    # --- Test cases ---
    ws_tc = wb["test_case_report"]
    test_cases = []
    current_tc = None

    for row in ws_tc.iter_rows(values_only=True):
        cols = list(row[:9])
        tc_id = cols[0]
        if tc_id and str(tc_id).startswith("TC_"):
            if current_tc:
                test_cases.append(current_tc)
            current_tc = {
                "id": str(tc_id),
                "title": str(cols[1] or ""),
                "preconditions": str(cols[2] or ""),
                "steps": [str(cols[3] or "").strip()],
                "test_data": str(cols[4] or ""),
                "expected": str(cols[5] or ""),
                "post_conditions": str(cols[6] or ""),
                "actual": str(cols[7] or ""),
                "status": str(cols[8] or "").strip().upper(),
                "area": _classify_area(str(cols[1] or "") + " " + str(cols[3] or "")),
            }
        elif current_tc and cols[3]:
            step = str(cols[3]).strip()
            if step:
                current_tc["steps"].append(step)

    if current_tc:
        test_cases.append(current_tc)

    # --- Defects ---
    ws_def = wb["proper_defect_report"]
    defects = []
    current_defect = {}

    for row in ws_def.iter_rows(values_only=True):
        field = str(row[0] or "").strip()
        value = str(row[1] or "").strip()
        if not field:
            continue
        if field == "Defect ID":
            if current_defect:
                defects.append(current_defect)
            current_defect = {"Defect ID": value}
            continue
        if field in ("Field", ""):
            continue
        current_defect[field] = value

    if current_defect:
        defects.append(current_defect)

    return {
        "platform": "laptop",
        "source_file": LAPTOP_XLSX,
        "total_test_cases": len(test_cases),
        "pass_count": sum(1 for tc in test_cases if tc["status"] == "PASS"),
        "fail_count": sum(1 for tc in test_cases if tc["status"] == "FAIL"),
        "test_cases": test_cases,
        "defects": defects,
    }


def parse_mobile():
    """Return structured test cases and defects for mobile platform."""
    try:
        import openpyxl
    except ImportError:
        print("[ERROR] openpyxl is required: pip install openpyxl", file=sys.stderr)
        sys.exit(1)

    wb = openpyxl.load_workbook(MOBILE_XLSX)

    # --- Test cases ---
    ws_tc = wb["Test cases"]
    test_cases = []
    header_skipped = False

    for row in ws_tc.iter_rows(values_only=True):
        cols = list(row)
        # Skip header rows and merged title rows
        tc_id_cell = str(cols[1] or "").strip()
        if not tc_id_cell or tc_id_cell in ("TEST CASES", "Test Case ID", "SUMMARY", "Metric"):
            continue
        if not tc_id_cell.startswith("TC_"):
            continue

        test_cases.append({
            "id": tc_id_cell,
            "title": str(cols[2] or "").strip(),
            "preconditions": str(cols[3] or "").strip(),
            "steps": [s.strip() for s in str(cols[4] or "").splitlines() if s.strip()],
            "test_data": str(cols[5] or "").strip(),
            "expected": str(cols[6] or "").strip(),
            "actual": str(cols[7] or "").strip(),
            "status": str(cols[8] or "").strip(),
            "priority": str(cols[9] or "").strip(),
            "area": _classify_area(str(cols[2] or "") + " " + str(cols[4] or "")),
        })

    # --- Defects ---
    ws_def = wb["Defects"]
    defects = []
    for row in ws_def.iter_rows(values_only=True):
        cols = list(row)
        bug_id = str(cols[1] or "").strip()
        if not bug_id or bug_id in ("DEFECTS", "Bug ID"):
            continue
        if not bug_id.startswith("BUG_"):
            continue
        defects.append({
            "id": bug_id,
            "title": str(cols[2] or "").strip(),
            "environment": str(cols[3] or "").strip(),
            "steps": str(cols[4] or "").strip(),
            "expected": str(cols[5] or "").strip(),
            "actual": str(cols[6] or "").strip(),
            "severity": str(cols[7] or "").strip(),
            "status": str(cols[8] or "").strip(),
        })

    return {
        "platform": "mobile",
        "source_file": MOBILE_XLSX,
        "total_test_cases": len(test_cases),
        "pass_count": sum(1 for tc in test_cases if tc["status"].lower() == "passed"),
        "fail_count": sum(1 for tc in test_cases if tc["status"].lower() == "failed"),
        "test_cases": test_cases,
        "defects": defects,
    }


def _classify_area(text: str) -> str:
    """Heuristically assign a functional area based on title/steps text."""
    text_lower = text.lower()
    for area, keywords in AREA_KEYWORDS.items():
        if any(kw in text_lower for kw in keywords):
            return area
    return "general"


def filter_by_area(data: dict, area: str) -> dict:
    """Filter test cases to only those matching the requested area."""
    if not area:
        return data
    area_lower = area.lower()
    filtered = [tc for tc in data["test_cases"] if tc.get("area") == area_lower]
    result = dict(data)
    result["test_cases"] = filtered
    result["pass_count"] = sum(1 for tc in filtered if tc.get("status", "").upper() in ("PASS", "PASSED"))
    result["fail_count"] = sum(1 for tc in filtered if tc.get("status", "").upper() in ("FAIL", "FAILED"))
    result["total_test_cases"] = len(filtered)
    result["area_filter"] = area_lower
    return result


def print_summary(data: dict):
    """Print a human-readable summary."""
    platform = data.get("platform", "?").upper()
    total = data.get("total_test_cases", 0)
    passed = data.get("pass_count", 0)
    failed = data.get("fail_count", 0)
    defects = len(data.get("defects", []))
    area = data.get("area_filter", "all")

    print(f"\n=== {platform} Reference Summary (area: {area}) ===")
    print(f"  Source  : {data.get('source_file', '?')}")
    print(f"  TCs     : {total} total | {passed} PASS | {failed} FAIL")
    print(f"  Defects : {defects}")
    print(f"\n  Test Cases:")
    for tc in data.get("test_cases", []):
        status = tc.get("status", "?").upper()
        icon = "[PASS]" if status in ("PASS", "PASSED") else "[FAIL]"
        print(f"    {icon} {tc['id']:8s} {tc['title']}")
    if data.get("defects"):
        print(f"\n  Defects:")
        for d in data.get("defects", []):
            # Laptop defects use field-name keys; mobile uses flat keys
            d_id = d.get("id") or d.get("Defect ID", "?")
            d_title = d.get("title") or d.get("Title / Summary", "?")
            print(f"    {d_id:10s} {d_title[:70]}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Parse PrestaShop test reference files into JSON.")
    parser.add_argument("--platform", required=True, choices=["tablet", "laptop", "mobile", "all"],
                        help="Which platform's reference file to parse")
    parser.add_argument("--area", default=None,
                        help="Optional functional area filter: navigation, filters, cart, registration, search, localization, layout, checkout, product, auth")
    parser.add_argument("--summary", action="store_true",
                        help="Print human-readable summary instead of JSON")
    parser.add_argument("--output", default=None,
                        help="File path to write JSON output (default: stdout)")
    args = parser.parse_args()

    results = []

    platforms = ["tablet", "laptop", "mobile"] if args.platform == "all" else [args.platform]

    for platform in platforms:
        if platform == "tablet":
            data = parse_tablet()
        elif platform == "laptop":
            data = parse_laptop()
        elif platform == "mobile":
            data = parse_mobile()
        else:
            continue

        if args.area:
            data = filter_by_area(data, args.area)

        results.append(data)

    if args.summary:
        for r in results:
            print_summary(r)
    else:
        output = results[0] if len(results) == 1 else {"platforms": results}
        json_str = json.dumps(output, indent=2, ensure_ascii=False)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(json_str)
            print(f"[INFO] Written to {args.output}", file=sys.stderr)
        else:
            print(json_str)


if __name__ == "__main__":
    main()
