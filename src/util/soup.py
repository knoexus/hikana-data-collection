from bs4 import BeautifulSoup
from .io import IO


class Soup:
    def __init__(self, soup_mode: str = 'html.parser') -> None:
        self.soup_mode = soup_mode
    
    def get_soup_content(self, file: bytes) -> BeautifulSoup:
        return BeautifulSoup(file, self.soup_mode)
    
    def load_soup_content(self, path: str) -> BeautifulSoup:
        file = IO.load_file(path)
        return self.get_soup_content(file)