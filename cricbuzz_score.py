from playwright.sync_api import sync_playwright, TimeoutError
import re

match_url = "https://www.cricbuzz.com/live-cricket-scores/176129/rdc-vs-ara-6th-match-abu-dhabi-t10-league-2026"

score_pattern = re.compile(r"^\d{1,3}-\d{1,2}\(\d+(?:\.\d+)?\)$")

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=False)
    page = browser.new_page()

    try:
        page.goto(match_url, wait_until="domcontentloaded")

        scores = page.get_by_text(score_pattern)
        scores.first.wait_for(state="visible", timeout=20000)

        unique_scores = list(dict.fromkeys(scores.all_inner_texts()))

        print("CRICKET SCORES:")
        for score in unique_scores:
            print(score)

        print("Score extraction successful!")

    except TimeoutError:
        print("No score available. There may be no match score displayed.")

    finally:
        page.screenshot(path="score.png", full_page=True)
        print("Screenshot saved successfully!")
        browser.close()