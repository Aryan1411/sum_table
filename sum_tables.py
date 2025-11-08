# sum_tables.py
import re
import sys
from playwright.sync_api import sync_playwright

SEEDS = list(range(1, 11))
URLS = [f"https://sanand0.github.io/tdsdata/js_table/?seed={s}" for s in SEEDS]

NUMBER_RE = re.compile(r"-?\d+(?:\.\d+)?")

def extract_numbers(text: str):
    if not text:
        return []
    return [float(m) for m in NUMBER_RE.findall(text)]

def main():
    grand_total = 0.0
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for url in URLS:
            print(f"Visiting: {url}")
            page.goto(url, wait_until="domcontentloaded", timeout=60_000)
            # Wait for at least one table to appear (JS renders them)
            page.wait_for_selector("table", timeout=60_000)

            # Collect text from all tables on the page
            table_handles = page.query_selector_all("table")
            page_sum = 0.0
            for th in table_handles:
                text = th.inner_text()
                nums = extract_numbers(text)
                page_sum += sum(nums)

            print(f"Page sum: {page_sum}")
            grand_total += page_sum

        browser.close()

    # Final total printed for the grader to capture
    print(f"TOTAL_SUM={grand_total}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Script error: {e}", file=sys.stderr)
        sys.exit(1)
