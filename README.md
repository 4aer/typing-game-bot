# 🤖 Multi-Site Typing Bot

A Python automation bot that can type on various typing test websites with configurable speeds and emergency stop controls.

## ✨ Features

- **Multi-Site Support**: Works with 4 popular typing test websites
- **Configurable Speed**: Different typing intervals for each site to avoid detection
- **Emergency Stop**: Multiple ways to stop the bot safely
- **Smart Text Extraction**: Site-specific text parsing for accurate typing
- **Chunk-Based Typing**: Optimized performance while maintaining stop controls

## 🎯 Supported Sites

| Site | URL | Interval | Notes |
|------|-----|----------|-------|
| TypeRacer | https://play.typeracer.com/ | 0.05s | Classic racing game |
| Nitro Type | https://www.nitrotype.com/race | 0.01s | Fast-paced racing |
| Human Benchmark | https://humanbenchmark.com/tests/typing | 0s | Maximum speed mode |
| Monkeytype | https://monkeytype.com/ | 0.03s | Works best at 15 seconds |

## 📋 Requirements

### Python Packages
```bash
pip install -r requirements.txt
```

### System Requirements
- **Chrome Browser**: Required for Selenium automation
- **Python 3.6+**: Tested on Python 3.6 and above

### Basic Usage
```bash
python typerbot.py
```

### Step-by-Step Process
1. **Run the script**: Execute the Python file
2. **Select a site**: Choose from the 4 available typing sites (1-4)
3. **Browser opens**: Chrome will automatically navigate to your chosen site
4. **Get ready**: Make sure that you're about to type
5. **Start typing**: Press `Ctrl+Alt+T` to begin automated typing
6. **Completion**: Script will finish and wait for you to close the browser

## ⌨️ Controls

### Start Typing
- **Hotkey**: `Ctrl+Alt+T`
- **Action**: Begins the automated typing process

### Emergency Stops
- **Ctrl+Shift+Q**: Immediate script termination
- **Ctrl+C**: Graceful shutdown in terminal
- **Close Terminal**: Force stop the script

## ⚙️ Configuration

### Adjusting Speed
Modify the `interval` values in `TYPING_SITES`:
- `0` = Maximum speed (instant typing)
- `0.01` = Very fast (100 chars/second)
- `0.05` = Moderate (20 chars/second)
- `0.1` = Slow (10 chars/second)

### Chunk Size Settings
In the `type_text()` function:
- **interval = 0**: Uses 50-character chunks
- **interval > 0**: Uses 20-character chunks

## 🛠️ How It Works

### Text Extraction Process
1. **Page Loading**: Waits for the website to fully load
2. **HTML Parsing**: Uses BeautifulSoup to parse page source
3. **Site-Specific Extraction**: Different parsing logic for each site
4. **Text Cleaning**: Strips whitespace and formats text properly

### Site-Specific Parsing
- **TypeRacer**: Looks for spans with "unselectable" attribute
- **Nitro Type**: Finds spans with "dash-letter" class
- **Human Benchmark**: Searches for spans with "incomplete" class
- **Monkeytype**: Extracts letters from word divs

### Typing Strategy
- **Chunk-Based**: Types in small chunks rather than character-by-character
- **Stop Checks**: Regularly checks for emergency stop signals
- **Error Handling**: Graceful recovery from typing interruptions

## ⚠️ Important Notes

### Responsible Use
- **Educational Purpose**: This bot is for learning automation concepts
- **Respect Terms of Service**: Check each site's ToS before using
- **Don't Abuse**: Use reasonable speeds to avoid detection
- **Fair Play**: Consider the impact on legitimate users

### Site-Specific Tips
- **Monkeytype**: Works best with 15-second tests
- **Human Benchmark**: Uses maximum speed (interval = 0)
- **TypeRacer**: Moderate speed to avoid suspicion
- **Nitro Type**: May require manual navigation to race

### Troubleshooting
- **Text Not Found**: Site structure may have changed
- **Slow Performance**: Check your interval settings
- **Can't Stop**: Use Ctrl+Shift+Q for emergency stop

## 🔧 Technical Details

### Dependencies
- `selenium`: Web browser automation
- `beautifulsoup4`: HTML parsing and text extraction
- `pyautogui`: Keyboard automation
- `keyboard`: Global hotkey detection
- `time`: Timing controls and delays

### Architecture
- **Modular Design**: Each site has dedicated parsing logic
- **Global State**: Uses global flags for emergency stops
- **Error Resilience**: Comprehensive exception handling
- **Resource Management**: Proper browser cleanup on exit

## 📝 License

This project is for educational purposes. Please use responsibly and respect the terms of service of the typing test websites.

## 🤝 Contributing

Feel free to contribute by:
- Adding support for new typing sites
- Improving text extraction accuracy
- Optimizing typing performance
- Enhancing error handling

---

**Happy Typing!** 🎯⌨️
