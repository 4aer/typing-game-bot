from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pyautogui
import keyboard
import time

def get_text_to_type(driver):
    
    time.sleep(1)
    src = driver.page_source
    soup = BeautifulSoup(src, "html.parser")
    span = soup.find_all("span")
    text = ""

    for i in span:
        if i.get("unselectable") == "on":
            text += i.text

    if not text:
        print("No text found.")
        return None
    else:
        print("Text to type: ", text)
        return text
    
def type_text(text):
    pyautogui.typewrite(text, interval=0.05)

def main():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://play.typeracer.com/")

    keyboard.wait("ctrl+alt+t")

    text_to_type = get_text_to_type(driver)
    if text_to_type:
        type_text(text_to_type)

main()