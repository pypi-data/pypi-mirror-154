import os
import re
import requests
import time
from bs4 import BeautifulSoup as BS 


from .static import StaticSpell
from .dynamic import DynamicSpell

class WebSpell:
    # Initializes a StaticSpell (requests) or DynamicSpell (selenium)
    def __init__(self, url, method='static', **kwargs):
        self.url = url
        self.method = method
        self.keys = kwargs
    

    def cast(self):
        if self.method.lower().strip() == 'static':
            return StaticSpell(url=self.url)
        elif self.method.lower().strip() == 'dynamic':
            driver_path = None
            driver_path = self.keys['driver_path'] if 'driver_path' in self.keys else None
            ghost = self.keys['ghost'] if 'ghost' in self.keys else False
            browser = self.keys['browser'] if 'browser' in self.keys else 'chrome'
            return DynamicSpell(url=self.url, driver_path=driver_path, ghost=ghost, browser=browser)


