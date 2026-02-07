"""Typing site configurations and text extraction logic."""

from typing import Optional
from bs4 import BeautifulSoup
from selenium.webdriver.remote.webdriver import WebDriver
import time
import logging

logger = logging.getLogger(__name__)


class TypingSite:
    """Base class for typing site configuration."""
    
    def __init__(self, name: str, url: str, interval: float = 0.03, variation: float = 0.01):
        self.name = name
        self.url = url
        self.interval = interval
        self.variation = variation
    
    def extract_text(self, driver: WebDriver) -> Optional[str]:
        """Extract text to type from the page."""
        raise NotImplementedError