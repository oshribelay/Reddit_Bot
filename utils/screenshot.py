import json
import re
from pathlib import Path
from typing import Dict, Final
from reddit import *
from dotenv import dotenv_values
import translators as ts
from playwright.async_api import async_playwright  # pylint: disable=unused-import
from playwright.sync_api import ViewportSize, sync_playwright
from rich.progress import track

config = dotenv_values("../.env")


def get_screenshots_of_reddit_posts(reddit_object: dict, screenshot_num: int):
    """Downloads screenshots of reddit posts as seen on the web. Downloads to assets/temp/png
    Args:
        reddit_object (Dict): Reddit object received from reddit/subreddit.py
        screenshot_num (int): Number of screenshots to download
    """
    # manually define values
    W: Final[int] = 1920  # width of the screenshots
    H: Final[int] = 1080  # height of the screenshots
    lang: Final[str] = "en-us"  # language of the post

    print("Downloading screenshots of reddit posts...")
    reddit_id = re.sub(r"[^\w\s-]", "", reddit_object["Id"])
    # ! Make sure the reddit screenshots folder exists
    Path(f"../screenshots/{reddit_id}").mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        print("Launching Headless Browser...")

        browser = p.chromium.launch(headless=True)  # headless=False will show the browser for debugging purposes
        context = browser.new_context()
        # Device scale factor (or dsf for short) allows us to increase the resolution of the screenshots
        # When the dsf is 1, the width of the screenshot is 600 pixels
        # so we need a dsf such that the width of the screenshot is greater than the final resolution of the video
        dsf = (W // 600) + 1

        context = browser.new_context(
            locale=lang or "en-us",
            color_scheme="dark",
            viewport=ViewportSize(width=W, height=H),
            device_scale_factor=dsf,
        )

        # Login to Reddit
        print("Logging in to Reddit...")
        page = context.new_page()
        page.goto("https://www.reddit.com/login", timeout=0)
        page.set_viewport_size(ViewportSize(width=1920, height=1080))
        page.wait_for_load_state()

        page.locator('[name="username"]').fill(config["REDDIT_USER"])
        page.locator('[name="password"]').fill(config["REDDIT_PASS"])
        page.locator("button:has-text('Log In')").click()

        # Go to the post URL
        print("Loading comments...")
        post_url = f"https://www.reddit.com/comments/{reddit_object['Id']}"
        page.goto(post_url, timeout=0)
        # Check if the "NSFW" screen is shown
        # Check if the "NSFW" screen is shown
        nsfw_button = page.query_selector('button:has-text("I\'m over 18")')
        if nsfw_button:
            nsfw_button.click()
            page.wait_for_selector(".Comment")
            # Check if login prompt appears
            login_button = page.query_selector_all("button:has-text('Log In')")
            if login_button:
                print("Logging in to Reddit...")
                page.locator('[name="username"]').fill(config["REDDIT_USER"])
                page.locator('[name="password"]').fill(config["REDDIT_PASS"])
                page.locator("button:has-text('Log In')").click()
                page.wait_for_selector(".Comment")
        else:
            page.wait_for_selector(".Comment")
        
        # Take screenshots of the post and each comment
        print("Taking screenshots...")
        comments = page.query_selector_all('.Comment')
        top_level_comments = [c for c in comments if c.query_selector('.Comment__parent') is None][:screenshot_num]
        for i, comment in enumerate(top_level_comments):
            screenshot_path = f"../screenshots/{reddit_id}/comment-{i}.png"
            comment.screenshot(path=screenshot_path)
            print(f"saving screenshot {i+1} ...")
        # Close the browser
        browser.close()


subreddit = initialize_subreddit_object()
data = get_data_from_subreddit(subreddit)
df = data[0]
print(df.loc[1])
wanted_thread = df.loc[1]
comments_array = data[1]
num_of_comments = convert_comments_to_audio(comments_array)
get_screenshots_of_reddit_posts(wanted_thread, num_of_comments)
