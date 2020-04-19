"""
A class to solve Quizlet scatter games.

The program uses selenium to launch a webbrowser and grab information, and then
uses pyautogui to click the pairs. The user can specify how many times to play
the game, as there can be some difference in scores between games. The set
should be exported with a custom separator of ///// and then stored in
quizlet.txt.

Author: David Chen
"""
import pyautogui
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep

USER_DATA_DIR = None  # keep browser settings across runs
USER_DATA_DIR = '--user-data-dir=/home/dchen327/.config/google-chrome/Profile 2'
CLICK_LOC = (350, 525)  # location to click to start game
pyautogui.PAUSE = 0  # no delay between clicks
LINK = 'https://quizlet.com/29813075/'  # remove anything after the numbers
NUM_PLAYS = 1
PATH_TO_SET = 'quizlet.txt'  # exported set in txt file
TERM_DEF_DELIMITER = '|||'  # custom delimiter used to separate terms and definitions in export
ROW_DELIMITER = '||||'  # custom delimter used to separate rows in export
X_RNG = (655, 1625)  # range of pixel values to click in grid
Y_RNG = (370, 940)
X_STEP = 485  # space between tiles
Y_STEP = 190


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
            sleep(0.5)

    def get_pairs(self):
        """ Get term-definition pairs from text file """
        pairs = {}
        with open(PATH_TO_SET) as f:
            for pair in f.read().split(ROW_DELIMITER):
                if pair:
                    term, definition = pair.split(TERM_DEF_DELIMITER)
                    pairs[term] = definition
        return pairs

    def setup_grid(self):
        """ Setup pixel positions for cards """
        positions = []
        for y in range(Y_RNG[0], Y_RNG[1] + 1, Y_STEP):
            for x in range(X_RNG[0], X_RNG[1] + 1, X_STEP):
                positions.append((x, y))
        return positions

    def launch_browser(self):
        """ Launch chrome and go to game link """
        options = Options()
        if USER_DATA_DIR:
            options.add_argument(USER_DATA_DIR)
        options.add_experimental_option('excludeSwitches', ['enable-automation'])  # remove the little popup in corner
        options.add_experimental_option('detach', True)  # allow instance to keep running after function ends
        options.add_argument('--start-maximized')
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(self.link + 'micromatch')

    def get_cards(self):
        """ Get values of cards from current game """
        sleep(0.5)
        pyautogui.click(*CLICK_LOC)
        sleep(0.7)  # wait for words to show up, since there is a fade in animation
        card_elements = self.driver.find_elements_by_class_name('MatchModeQuestionGridBoard-tile')
        cards = [card.text for card in card_elements]
        print(cards)
        return cards

    def play_game(self, cards):
        """ Clicks on all pairs """
        for i in range(len(cards)):
            if cards[i] in self.pairs:  # is a term, click the term then definition
                pyautogui.click(self.grid[i])
                definition = self.pairs[cards[i]]
                j = cards.index(definition)
                pyautogui.click(self.grid[j])


if __name__ == '__main__':
    solver = ScatterSolver(LINK, NUM_PLAYS)
