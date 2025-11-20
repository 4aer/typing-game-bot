# Multi-Site Typing Bot

A Python automation bot that types on typing test websites. Built for fun and learning automation concepts.

## What it does

- Automatically types text on 4 different typing test sites
- Configurable typing speeds to avoid detection
- Emergency stop controls for safety

## Supported Sites

- TypeRacer
- Nitro Type  
- Human Benchmark
- Monkeytype

## Requirements

```bash
pip install selenium beautifulsoup4 pyautogui keyboard
```

- Chrome browser
- Python 3.6+

## Note

If you want to skip the installation process, check the dist/ folder to download the executable file of this app. Windows may flag the executable as unsafe because it's not code-signed. This is normal for unsigned apps. Click "More info" → "Run anyway" to proceed. The source code is available for review if you prefer to run it directly with Python.

## Usage

```bash
python typerbot.py
```

1. Choose a typing site (1-4)
2. Browser opens automatically
3. Press `Ctrl+Alt+T` to start typing
4. Use `Caps Lock+S` to emergency stop

## Why I built this

I created this project out of boredom and curiosity. It sounded fun and interesting to see if I could automate typing tests. It's purely for learning purposes - to understand web automation, text parsing, and keyboard controls.

## Technical stuff

- Uses Selenium for browser automation
- BeautifulSoup for extracting text from websites
- PyAutoGUI for simulating keystrokes
- Different parsing logic for each site

## Note

This is just a learning project. Use responsibly and respect the terms of service of typing websites.