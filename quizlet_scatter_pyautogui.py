import pyautogui
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep

pyautogui.PAUSE = 0  # no delay between clicks


class ScatterSolver:
    def __init__(self, link, num_games=1):
        self.link = link
        self.num_games = num_games
        self.pairs = self.get_pairs()
        self.grid = self.setup_grid()
        self.launch_browser()
        for _ in range(num_games):
            cards = self.get_cards()
            self.play_game(cards)

    def get_pairs(self):
        """ Get term-definition pairs from text file """
        pairs = {}
        with open('quizlet.txt') as f:
            for pair in f.read().splitlines():
                term, definition = pair.split('/////')
                pairs[term] = definition
        return pairs

    def setup_grid(self):
        """ Setup pixel positions for cards """
        x_rng = (655, 1625)
        y_rng = (370, 940)
        x_step = 485
        y_step = 190
        positions = []
        for y in range(y_rng[0], y_rng[1] + 1, y_step):
            for x in range(x_rng[0], x_rng[1] + 1, x_step):
                positions.append((x, y))
        return positions

    def launch_browser(self):
        options = Options()
        options.add_argument(
            '--user-data-dir=/home/dchen327/.config/google-chrome/Profile 2')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('detach', True)
        options.add_argument('--start-maximized')
        driver = webdriver.Chrome(options=options)
        driver.get(self.link + 'micromatch')

    def get_cards(self):
        """ Launch browser and get cards """
        sleep(0.5)
        pyautogui.click(350, 525)
        sleep(0.5)  # wait for words to show up, since there is a fade in animation
        card_elements = self.driver.find_elements_by_class_name('MatchModeQuestionGridBoard-tile')
        cards = [card.text for card in card_elements]
        return cards

    def play_game(self, cards):
        """ Clicks on all pairs """
        for i in range(len(cards)):
            if cards[i] in self.pairs:  # is a term
                pyautogui.click(self.grid[i])
                definition = self.pairs[cards[i]]
                j = cards.index(definition)
                pyautogui.click(self.grid[j])


if __name__ == '__main__':
    link = 'https://quizlet.com/340870200/'
    num_plays = 5
    solver = ScatterSolver(link, num_plays)
