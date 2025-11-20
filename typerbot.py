from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pyautogui
import keyboard
import time
import threading
import sys

# dictionary for different typing sites
TYPING_SITES = {
    1: {
        "name": "TypeRacer",
        "url": "https://play.typeracer.com/",
        "interval": 0.03
    },
    2: {
        "name": "Nitro Type", 
        "url": "https://www.nitrotype.com/race",
        "interval": 0.01
    },
    3: {
        "name": "Human Benchmark",
        "url": "https://humanbenchmark.com/tests/typing",
        "interval": 0
    },
    4: {
        "name": "Monkeytype (works fine at 15 seconds)",
        "url": "https://monkeytype.com/",
        "interval": 0.03
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
    time.sleep(1)

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

# Global flag to control script execution
stop_script = False
is_typing = False

def emergency_stop():
    """Emergency stop function - only works during typing"""
    global stop_script
    if is_typing:
        stop_script = True
        print("\n[!] EMERGENCY STOP ACTIVATED!")

def setup_emergency_stop():
    """Set up emergency stop hotkey"""
    # Use ESC key instead - more reliable and less prone to accidents
    keyboard.on_press_key('esc', lambda _: emergency_stop())
    print("Emergency stop: Press ESC during typing to stop")

def cleanup_keyboard():
    """Remove all keyboard hooks"""
    try:
        keyboard.unhook_all()
    except:
        pass

def type_text(text, bot_type):
    """Type the text with appropriate interval for the selected site"""
    global stop_script, is_typing
    interval = TYPING_SITES[bot_type]["interval"]
    is_typing = True
    
    if interval == 0:
        chunk_size = 50
        for i in range(0, len(text), chunk_size):
            if stop_script:
                print("Typing stopped by user.")
                break
            chunk = text[i:i+chunk_size]
            pyautogui.typewrite(chunk, interval=0)
            time.sleep(0.01)
    else:
        chunk_size = 20
        for i in range(0, len(text), chunk_size):
            if stop_script:
                print("Typing stopped by user.")
                break
            chunk = text[i:i+chunk_size]
            pyautogui.typewrite(chunk, interval=interval)
    
    is_typing = False

def main():
    global stop_script
    
    # Select which site to use
    bot_type = select_site()
    selected_site = TYPING_SITES[bot_type]
    
    print(f"\nStarting bot for {selected_site['name']}")
    print(f"URL: {selected_site['url']}")
    print("\nInstructions:")
    print("1. Click on the typing area in the browser")
    print("2. Press Ctrl+Alt+T to start typing")
    print("3. Press ESC during typing to stop early")
    
    driver = None
    
    try:
        # Setup Chrome driver with less verbose logging
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_argument('--log-level=3')  # Suppress logs
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(selected_site['url'])
        
        # Set up emergency stop AFTER browser is ready
        setup_emergency_stop()
        
        # Main loop - keep running until user wants to quit
        while True:
            # Reset stop flag for each run
            stop_script = False
            
            print("\nWaiting for Ctrl+Alt+T...")
            keyboard.wait("ctrl+alt+t")
            
            # Get text and type it
            print("Starting to type...")
            text_to_type = get_text_to_type(driver, bot_type)
            
            if text_to_type and not stop_script:
                type_text(text_to_type, bot_type)
                if not stop_script:
                    print("\nTyping completed successfully!")
            else:
                print("Failed to extract text from the page or stopped by user.")
            
            # Ask if user wants to continue
            print("\n" + "="*50)
            choice = input("Run again? (y/n): ").strip().lower()
            
            if choice != 'y':
                print("Exiting...")
                break
            
            print("Ready for next round! Start a new race/test in the browser.")
        
        # Clean up keyboard hooks before closing
        cleanup_keyboard()
        
        input("\nPress Enter to close the browser...")
        driver.quit()
        print("Browser closed. Adios.")
        
    except KeyboardInterrupt:
        print("\n[!] Script interrupted by user (Ctrl+C)")
        cleanup_keyboard()
        if driver:
            driver.quit()
        sys.exit(0)
    except Exception as e:
        print(f"[!] An error occurred: {e}")
        cleanup_keyboard()
        if driver:
            driver.quit()
        sys.exit(1)
    finally:
        # Ensure keyboard hooks are cleaned up
        cleanup_keyboard()

if __name__ == "__main__":
    main()