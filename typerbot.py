from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime
import pyautogui
import keyboard
import time
import random
import threading
import sys

# dictionary for different typing sites
TYPING_SITES = {
    1: {
        "name": "TypeRacer",
        "url": "https://play.typeracer.com/",
        "interval": 0.03,
        "variation": 0.01
    },
    2: {
        "name": "Nitro Type", 
        "url": "https://www.nitrotype.com/race",
        "interval": 0.01,
        "variation": 0.005
    },
    3: {
        "name": "Human Benchmark",
        "url": "https://humanbenchmark.com/tests/typing",
        "interval": 0,
        "variation": 0
    },
    4: {
        "name": "Monkeytype (works fine at 15 seconds)",
        "url": "https://monkeytype.com/",
        "interval": 0.03,
        "variation": 0.01
    }
}

session_stats = {
    "races_completed": 0,
    "total_characters": 0,
    "start_time": None,
    "errors_made": 0
}

def select_site():
    """Allow user to select which typing site to use"""
    print("\nAvailable typing sites:")
    print("\n" + "="*50)
    print("TYPING BOT - Site Selection")
    print("="*50)
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

def configure_speed():
    """Let user adjust typing speed"""
    print("\n" + "="*50)
    print("Speed Configuration")
    print("="*50)
    print("1. Ultra Fast (may get detected)")
    print("2. Fast (default)")
    print("3. Normal (more human-like)")
    print("4. Slow (very human-like)")
    print("5. Custom")
    
    while True:
        try:
            choice = int(input("\nSelect speed (1-5): "))
            if choice == 1:
                return 0.01, 0.005, "Ultra Fast"
            elif choice == 2:
                return 0.03, 0.01, "Fast"
            elif choice == 3:
                return 0.05, 0.02, "Normal"
            elif choice == 4:
                return 0.08, 0.03, "Slow"
            elif choice == 5:
                interval = float(input("Enter base interval (0.01-0.2): "))
                variation = float(input("Enter variation (0.005-0.05): "))
                return interval, variation, "Custom"
            else:
                print("Invalid choice. Please select 1-5.")
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
        print(f"Length: {len(text)} characters")
    return text.strip()

# Global flag to control script execution
stop_script = False
is_typing = False
pause_typing = False

def emergency_stop():
    """Emergency stop function - only works during typing"""
    global stop_script
    if is_typing:
        stop_script = True
        print("\nEMERGENCY STOP ACTIVATED!")

def setup_hotkeys():
    """Set up emergency stop hotkey and pause hotkeys"""
    # Use ESC key instead - more reliable and less prone to accidents
    keyboard.on_press_key('esc', lambda _: emergency_stop())
    keyboard.on_press_key('p', lambda _: toggle_pause())
    print("Emergency stop: Press ESC during typing to stop")
    print("Pause/Resume: Press P during typing")

def cleanup_keyboard():
    """Remove all keyboard hooks"""
    try:
        keyboard.unhook_all()
    except:
        pass

def type_text(text, base_interval, variation, human_like=True):
    """Type the text with human-like variations"""
    global stop_script, is_typing, pause_typing, session_stats
    is_typing = True
    chars_typed = 0

    print(f"\nStarting typing... ({len(text)} chars)")
    
    for i, char in enumerate(text): 
        # Check for stop
        if stop_script:
            print("\nTyping stopped by user.")
            break
        # Check for pause
        while pause_typing and not stop_script:
            time.sleep(0.1)
        
        # Human-like typing with variation
        if human_like and base_interval > 0:
            # Random variation
            interval = base_interval + random.uniform(-variation, variation)
            interval = max(0.001, interval)
            
            # Occasionally simulate a typo
            if simulate_human_error(char):
                # Type wrong char
                wrong_char = random.choice('abcdefghijklmnopqrstuvwxyz')
                pyautogui.typewrite(wrong_char, interval=interval)
                time.sleep(0.1)
                # Backspace
                pyautogui.press('backspace')
                time.sleep(0.05)
                # Error counter
                session_stats["errors_made"] += 1
            
            # Type correct char
            pyautogui.typewrite(char, interval=interval)
            chars_typed += 1
            
            # Occasional micro-pause (like thinking)
            if i > 0 and i % 50 == 0 and random.random() < 0.3:
                time.sleep(random.uniform(0.1, 0.3))
        else:
            # Fast mode
            pyautogui.typewrite(char, interval=base_interval)

        chars_typed += 1

        if chars_typed % 50 == 0:
            progress = (chars_typed / len(text)) * 100
            print(f"[{progress:.0f}%] {chars_typed}/{len(text)} characters")
    
    is_typing = False
    session_stats["total_characters"] += chars_typed

    if not stop_script:
        print(f"\n Typed {chars_typed} characters successfully.")

def simulate_human_error(char, error_rate=0.02):
    """Randomly introduce typos then correct them"""
    if random.random() < error_rate:
        return True
    return False

def toggle_pause():
    """Pause/resume typing"""
    global pause_typing
    if is_typing:
        pause_typing = not pause_typing
        if pause_typing:
            print("\nPAUSED - Press P to resume")
        else:
            print("\nRESUMED")

def display_stats():
    """Display session statistics"""
    if session_stats["start_time"]:
        elapsed = time.time() - session_stats["start_time"]
        mins = int(elapsed // 60)
        secs = int(elapsed % 60)
        
        print("\n" + "="*50)
        print("SESSION STATISTICS")
        print("="*50)
        print(f"Races completed: {session_stats['races_completed']}")
        print(f"Total characters: {session_stats['total_characters']}")
        print(f"Simulated errors: {session_stats['errors_made']}")
        print(f"Session time: {mins}m {secs}s")
        print("="*50)

def main():
    global stop_script, pause_typing, session_stats
    
    # Select which site to use
    bot_type = select_site()
    selected_site = TYPING_SITES[bot_type]

    # Configure typing speed
    base_interval, variation, speed_name = configure_speed()
    
    print("\n" + "="*50)
    human_like = input("Enable human-like typing? (y/n): ").strip().lower() == 'y'

    print(f"\nStarting bot for {selected_site['name']}")
    print(f"URL: {selected_site['url']}")
    print("\nINSTRUCTIONS:")
    print("1. Click on the typing area in the browser")
    print("2. Press Ctrl+Alt+T to start typing")
    print("3. Press ESC during typing to stop early")
    print("4. Press P during typing to pause/resume")
    
    driver = None
    session_stats["start_time"] = time.time()
    
    try:
        # Setup Chrome driver with less verbose logging
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_argument('--log-level=3')  # Suppress logs
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(selected_site['url'])
        
        # Set up emergency stop AFTER browser is ready
        setup_hotkeys()
        
        # Main loop - keep running until user wants to quit
        while True:
            # Reset stop flag for each run
            stop_script = False
            pause_typing = False
            
            print("\nWaiting for Ctrl+Alt+T...")
            keyboard.wait("ctrl+alt+t")
            
            # Get text and type it
            print("Starting to type...")
            text_to_type = get_text_to_type(driver, bot_type)
            
            if text_to_type and not stop_script:
                type_text(text_to_type, base_interval, variation, human_like)
                if not stop_script:
                    session_stats["races_completed"] += 1
                    display_stats()
                    print("\nTyping completed successfully!")
            else:
                print("Failed to extract text from the page or stopped by user.")
                display_stats()
                
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
        print("\nScript interrupted by user (Ctrl+C)")
        cleanup_keyboard()
        display_stats()
        if driver:
            driver.quit()
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {e}")
        cleanup_keyboard()
        if driver:
            driver.quit()
        sys.exit(1)
    finally:
        # Ensure keyboard hooks are cleaned up
        cleanup_keyboard()

if __name__ == "__main__":
    main()