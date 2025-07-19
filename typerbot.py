from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pyautogui
import keyboard
import time

# dictionary for different typing sites
TYPING_SITES = {
    1: {
        "name": "TypeRacer",
        "url": "https://play.typeracer.com/",
        "interval": 0.05
    },
    2: {
        "name": "Nitro Type", 
        "url": "https://www.nitrotype.com/race",
        "interval": 0.01
    },
    3: {
        "name": "Human Benchmark",
        "url": "https://humanbenchmark.com/tests/typing",
        "interval": 0.01
    },
    4: {
        "name": "Monkeytype (works fine at 15 seconds)",
        "url": "https://monkeytype.com/",
        "interval": 0.05
    }
}

def select_site():
    """Allow user to select which typing site to use"""
    print("\nAvailable typing sites:")
    for key, site in TYPING_SITES.items():
        print(f"{key}. {site['name']}")
    
    while True:
        try:
            choice = int(input("\nSelect a site (1-4): "))
            if choice in TYPING_SITES:
                return choice
            else:
                print("Invalid choice. Please select 1-4.")
        except ValueError:
            print("Please enter a valid number.")

def get_text_to_type(driver, bot_type):
    time.sleep(1) # wait for page to load

    # select current page source
    if bot_type == 2:
        driver.switch_to.window(driver.window_handles[-1])
    
    src = driver.page_source
    soup = BeautifulSoup(src, "html.parser")
    text = ""

    if bot_type == 1: # TypeRacer
        spans = soup.find_all("span")
        for span in spans:
            if "unselectable" in str(span):
                text += span.text
    
    elif bot_type == 2: # Nitro Type
        spans = soup.find_all("span", {"class": "dash-letter"})
        for span in spans:
            text += span.text
        text = " ".join(text.split())
    
    elif bot_type == 3: # Human Benchmark Typing Test
        spans = soup.find_all("span", {"class": "incomplete"})
        for span in spans:
            text += span.text
    
    elif bot_type == 4: # Monkeytype 
        divs = soup.find_all("div", {"class": "word"})
        for div_element in divs:
            letters = div_element.find_all("letter")
            for letter in letters:
                text += letter.text
            text += " "
    
    if not text:
        print("No text found")
        return None
    else:
        print(f"Text to type: {text[:50]}..." if len(text) > 50 else f"Text to type: {text}")
    return text.strip()

def type_text(text, bot_type):
    """Type the text with appropriate interval for the selected site"""
    interval = TYPING_SITES[bot_type]["interval"]
    pyautogui.typewrite(text, interval=interval)

def main():
    # select which site to use
    bot_type = select_site()
    selected_site = TYPING_SITES[bot_type]
    
    print(f"\nStarting bot for {selected_site['name']}")
    print(f"URL: {selected_site['url']}")
    print("Press Ctrl+Alt+T when ready to start typing...")
    
    # setup Chrome driver
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)
    
    # navigate to selected site
    driver.get(selected_site['url'])
    
    # wait for user signal
    keyboard.wait("ctrl+alt+t")
    
    # get text and type it
    text_to_type = get_text_to_type(driver, bot_type)
    if text_to_type:
        type_text(text_to_type, bot_type)
        print("Typing completed!")
    else:
        print("Failed to extract text from the page.")
    
    input("Press Enter to close the browser...")
    driver.quit()

if __name__ == "__main__":
    main()