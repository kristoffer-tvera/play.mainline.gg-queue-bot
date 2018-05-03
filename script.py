"""Scans the list of EU games, plays a sound when a new one is found, and opens it in new browser"""
import winsound
import webbrowser
import requests
import time
from bs4 import BeautifulSoup

BRUKER_NAVN = 'yyyyyy'
PASSORD = 'xxxxx'
TEAM_ID = '8330'  # Ikke rør, dette er din team id

URL = "https://play.mainline.gg/pubg"
CURRENT = []
sess = requests.Session()


def login():
    site = sess.get('https://play.mainline.gg/user/login')
    # print(site)
    csrf = parse_for_csrf(site)
    payload = {'_csrf': csrf,
               'LoginForm[identity]': BRUKER_NAVN,
               'LoginForm[password]': PASSORD,
               'LoginForm[rememberMe]': '0',
               'login-button': ''
               }
    sess.post('https://play.mainline.gg/user/login', data=payload)
    print('Login complete (unable to see if it was success or fail)')


def prepopulate_match_list():
    matches = get_match_list()
    for match in matches:
        CURRENT.append(match.get('data-key'))


def beep():
    winsound.Beep(600, 500)


def get_match_list():
    site = requests.get(URL)
    site_soup = BeautifulSoup(site.text, 'html.parser')
    match_list = site_soup.select(
        'div.eu-tab div.matches div.list-view div[data-key]')
    return match_list


def filter_match_list(matches):
    for match in matches:
        if match.get('data-key') not in CURRENT:
            CURRENT.append(match.get('data-key'))
            print('found new')
            onclick = match.div.get('onclick')
            filtered = filter_href(onclick)
            # webbrowser.open(filtered)
            get_join_code_page(filtered)


def filter_href(href):
    return href[15:-2]


def loop():
    while 1:
        time.sleep(1)
        filter_match_list(get_match_list())
        print('.')


def parse_for_csrf(site):
    soup = BeautifulSoup(site.text, 'html.parser')
    elem = soup.select('input[name=_csrf]')
    return elem[0].get('value')


def get_join_code_page(url):
    print(url)
    site = sess.get(url)
    parse_for_join_href(site)


def parse_for_join_href(site):
    soup = BeautifulSoup(site.text, 'html.parser')
    elem = soup.select('a.join-button')
    href = elem[0].get('href')
    parse_for_comp_form(href)


def parse_for_comp_form(url):
    print(url)
    site = sess.get(url)
    csrf = parse_for_csrf(site)
    submit_compete(csrf, url)


def submit_compete(csrf, url):
    payload = {'_csrf': csrf,
               'EventTeamSelectForm[team_id]': TEAM_ID
               }
    sess.post(url, data=payload)
    print('you are PROBABLY in the competition right now. gl hf idiots')
    beep()


login()
prepopulate_match_list()
loop()
