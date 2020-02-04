import pyautogui
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep

pyautogui.PAUSE = 0  # no delay between clicks


def get_pairs():
    """ Get term-definition pairs from text file """
    pairs = {}
    with open('quizlet.txt') as f:
        for pair in f.read().splitlines():
            term, definition = pair.split('/////')
            pairs[term] = definition
    return pairs


def setup_grid():
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


def get_cards(link):
    """ Launch browser and get cards """
    options = Options()
    options.add_argument(
        '--user-data-dir=/home/dchen327/.config/google-chrome/Profile 2')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('detach', True)
    options.add_argument('--start-maximized')
    driver = webdriver.Chrome(options=options)
    driver.get(link + 'micromatch')
    for _ in range(5):
        sleep(0.5)
        pyautogui.click(350, 525)
        sleep(0.5)  # wait for words to show up, since there is a fade in animation
        card_elements = driver.find_elements_by_class_name('MatchModeQuestionGridBoard-tile')
        cards = [card.text for card in card_elements]
        play_game(cards)
        sleep(1)


def play_game(cards):
    """ Clicks on all pairs """
    for i in range(len(cards)):
        if cards[i] in pairs:  # is a term
            pyautogui.click(positions[i])
            definition = pairs[cards[i]]
            j = cards.index(definition)
            pyautogui.click(positions[j])


if __name__ == '__main__':
    link = 'https://quizlet.com/340870200/'
    pairs = get_pairs()
    positions = setup_grid()
    get_cards(link)
