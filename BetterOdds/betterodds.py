import sqlite3
from sqlite3 import Error
from urllib.request import pathname2url

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import numpy
from math import floor
import time
from shutil import copy2
import datetime
import os

# Initialize Selenium Driver
options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(40)


def main_db_check():
    """Check for the existence of main database and rebuilds if non existent"""

    # Check for and rebuild main.db
    global main_cur
    global main_conn
    try:
        print("Connecting to main database...")
        maindburi = 'file:{}?mode=rw'.format(pathname2url('main.db'))
        main_conn = sqlite3.connect(maindburi, uri=True)
        main_cur = main_conn.cursor()
        print("Connection to main.db successful")

    except sqlite3.OperationalError:
        try:
            print("Connection to main.db unsuccessful. Attempting to rebuild database..")
            main_conn = sqlite3.connect('main.db')
            main_cur = main_conn.cursor()
            print("Main database successfully rebuilt")
        except Error as e:
            print("Rebuild of main.db unsuccessful. Exiting Application. Please see error message below \n", e)


# def archive_db_check():
#     """Check for the existence of archive database and rebuilds if non existent"""
#
#     # Check for an rebuild archive.db
#     global archive_cur
#     global archive_conn
#     try:
#         print("Connecting to archive database...")
#         archdburi = 'file:{}?mode=rw'.format(pathname2url('archive.db'))
#         archive_conn = sqlite3.connect(archdburi, uri=True)
#         archive_cur = archive_conn.cursor()
#         print("Connection to archive.db successful \n")
#         return archive_cur
#
#     except sqlite3.OperationalError:
#         try:
#             print("Connection to archive.db unsuccessful. Attempting to rebuild database..")
#             archive_conn = sqlite3.connect('archive.db')
#             archive_cur = archive_conn.cursor()
#             print("Archive database successfully rebuilt \n")
#             return archive_cur
#         except Error as e:
#             print("Rebuild of archive.db unsuccessful. Exiting Application. Please see error message below \n", e)


def db_table_check():
    """Check for the existence of tables in databases and rebuilds them if non existent"""

    leagues_create = '''CREATE TABLE IF NOT EXISTS `leagues` (
        `fid`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        `country_name`	TEXT NOT NULL,
        `league_name`	TEXT NOT NULL UNIQUE,
        `country_league_name`	TEXT NOT NULL,
        `league_url`	TEXT NOT NULL,
        `league_winperc`	INTEGER,
        `single_chnc_margin`	INTEGER,
        `double_chnc_margin`	INTEGER,
        `pos_weighting`	REAL,
        `team_name_weighting`	REAL,
        `form_weighting`	REAL,
        `gd_weighting`	REAL,
        `pos_winrate`	INTEGER,
        `team_name_winrate`	INTEGER,
        `form_winrate`	INTEGER,
        `gd_winrate`	INTEGER
      );'''

    match_data_create = '''CREATE TABLE IF NOT EXISTS `match_data` (
        `fid`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        `match_datetime`	TEXT,
        `country_name`	TEXT,
        `league_name`	TEXT,
        `country_league_name`	TEXT,
        `home_team_name`	TEXT,
        `home_team_ID`	TEXT,
        `away_team_name`	TEXT,
        `away_team_ID`	TEXT,
        `home_win`	REAL,
        `away_win`	REAL,
        `home_draw`	REAL,
        `away_draw`	REAL,
        `match_url`	TEXT
    );'''

    league_data_home_create = '''CREATE TABLE IF NOT EXISTS `league_data_home` (
        `fid`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        `country_name`	TEXT,
        `league_name`	TEXT,
        `country_league_name`	TEXT,
        `home_position`	INTEGER,
        `home_total_clubs`	INTEGER,
        `home_team_name`	TEXT,
        `home_team_id`	TEXT,
        `home_matches_played`	INTEGER,
        `home_matches_won`	INTEGER,
        `home_matches_draw`	INTEGER,
        `home_matches_loss`	INTEGER,
        `home_goal_diff`	INTEGER,
        `home_team_form`	INTEGER
    );'''

    league_data_away_create = '''CREATE TABLE IF NOT EXISTS `league_data_away` (
        `fid`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        `country_name`	TEXT,
        `league_name`	TEXT,
        `country_league_name`	TEXT,
        `away_position`	INTEGER,
        `away_total_clubs`	INTEGER,
        `away_team_name`	TEXT,
        `away_team_id`	TEXT,
        `away_matches_played`	INTEGER,
        `away_matches_won`	INTEGER,
        `away_matches_draw`	INTEGER,
        `away_matches_loss`	INTEGER,
        `away_goal_diff`	INTEGER,
        `away_team_form`	INTEGER
    );'''

    name_conversion_create = '''CREATE TABLE IF NOT EXISTS `name_conversion` (
        `fid`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        `uefa_team_name`	TEXT,
        `flashscore_team_name`	TEXT
    );'''

    uefa_team_ranking_create = '''CREATE TABLE IF NOT EXISTS `uefa_team_ranking` (
        `fid`	INTEGER PRIMARY KEY AUTOINCREMENT,
        `team_rank`	INTEGER,
        `team_name`	TEXT,
        `uefa_points`	REAL
    );'''

    match_analysis_create = '''CREATE TABLE IF NOT EXISTS `match_analysis` (
        `fid`	INTEGER PRIMARY KEY AUTOINCREMENT,
        `match_datetime`	TEXT,
        `country_name`	TEXT,
        `league_name`	TEXT,
        `country_league_name`	TEXT,
        `home_team_name`	TEXT,
        `home_team_id`	TEXT,
        `away_team_name`	TEXT,
        `away_team_ID`	TEXT,
        `home_win`	REAL,
        `home_draw`	REAL,
        `away_draw`	REAL,
        `away_win`	REAL,
        `home_position`	INTEGER,
        `away_position`	INTEGER,
        `total_clubs`	INTEGER,
        `home_matches_played`	INTEGER,
        `away_matches_played`	INTEGER,
        `home_matches_won`	INTEGER,
        `away_matches_won`	INTEGER,
        `home_matches_draw`	INTEGER,
        `away_matches_draw`	INTEGER,
        `home_matches_loss`	INTEGER,
        `away_matches_loss`	INTEGER,
        `home_goal_diff`	INTEGER,
        `away_goal_diff`	INTEGER,
        `home_team_form`	INTEGER,
        `away_team_form`	INTEGER,
        `home_team_name_rank`	REAL,
        `away_team_name_rank`	REAL,
        `home_position_rank`	REAL,
        `away_position_rank`	REAL,
        `home_form_rank`	REAL,
        `away_form_rank`	REAL,
        `home_gd_rank`	REAL,
        `away_gd_rank`	REAL,
        `home_points_total`	REAL,
        `away_points_total`	REAL,
        `rec_bet`	TEXT,
        `percentage_chance`	INTEGER,
        `percentage_rec`	INTEGER,
        `match_result`	TEXT,
        `bet_result`	TEXT,
        `TEST_rec_bet`	TEXT,
        `TEST_bet_result`	TEXT,
        `match_url`	TEXT UNIQUE
    );'''

    archive_table_create = '''CREATE TABLE IF NOT EXISTS `match_archive` (
        `fid`	INTEGER PRIMARY KEY AUTOINCREMENT,
        `match_datetime`	TEXT,
        `country_name`	TEXT,
        `league_name`	TEXT,
        `country_league_name`	TEXT,
        `home_team_name`	TEXT,
        `home_team_id`	TEXT,
        `away_team_name`	TEXT,
        `away_team_ID`	TEXT,
        `home_win`	REAL,
        `home_draw`	REAL,
        `away_draw`	REAL,
        `away_win`	REAL,
        `home_position`	INTEGER,
        `away_position`	INTEGER,
        `total_clubs`	INTEGER,
        `home_matches_played`	INTEGER,
        `away_matches_played`	INTEGER,
        `home_matches_won`	INTEGER,
        `away_matches_won`	INTEGER,
        `home_matches_draw`	INTEGER,
        `away_matches_draw`	INTEGER,
        `home_matches_loss`	INTEGER,
        `away_matches_loss`	INTEGER,
        `home_goal_diff`	INTEGER,
        `away_goal_diff`	INTEGER,
        `home_team_form`	INTEGER,
        `away_team_form`	INTEGER,
        `home_team_name_rank`	REAL,
        `away_team_name_rank`	REAL,
        `home_position_rank`	REAL,
        `away_position_rank`	REAL,
        `home_form_rank`	REAL,
        `away_form_rank`	REAL,
        `home_gd_rank`	REAL,
        `away_gd_rank`	REAL,
        `home_points_total`	REAL,
        `away_points_total`	REAL,
        `rec_bet`	TEXT,
        `percentage_chance`	INTEGER,
        `percentage_rec`	INTEGER,
        `match_result`	TEXT,
        `bet_result`	TEXT,
        `TEST_rec_bet`	TEXT,
        `TEST_bet_result`	TEXT,
        `match_url`	TEXT UNIQUE,
        `league_url`	TEXT NOT NULL,
        `league_winperc`	INTEGER,
        `single_chnc_margin`	INTEGER,
        `double_chnc_margin`	INTEGER,
        `pos_weighting`	REAL,
        `team_name_weighting`	REAL,
        `form_weighting`	REAL,
        `gd_weighting`	REAL,
        `pos_winrate`	INTEGER,
        `team_name_winrate`	INTEGER,
        `form_winrate`	INTEGER,
        `gd_winrate`	INTEGER
    );'''

    main_cur.execute(match_data_create)
    main_cur.execute(leagues_create)
    main_cur.execute(league_data_home_create)
    main_cur.execute(league_data_away_create)
    main_cur.execute(name_conversion_create)
    main_cur.execute(uefa_team_ranking_create)
    main_cur.execute(match_analysis_create)
    main_cur.execute(archive_table_create)
    main_conn.commit()


# -----------------------------------Leagues-------------------------------------------------

def leagues_display():
    """Prints the leagues from database"""

    main_cur.execute("SELECT fid, country_league_name, league_url FROM Leagues")
    leagues_view = main_cur.fetchall()

    if len(leagues_view) == 0:
        print("There are no leagues stored at the moment. Try adding some leagues \n")
    else:
        print("League List:")
        for fid, country_league_name, league_url in leagues_view:
            print(fid, country_league_name, league_url)
        print(" ")


def league_update_add():
    """Adds leagues to the league database"""

    while True:
        user_prompt = input("Please paste the league webpage link from flashscore.com here: ")
        driver.get(user_prompt)
        league_country = driver.find_element_by_xpath('//*[@id="mc"]/h2/a[2]').get_attribute('textContent')
        league_name = driver.find_element_by_xpath('//*[@id="mc"]/h2/a[3]').get_attribute('textContent')
        country_league_name = league_country + ' ' + league_name
        try:
            main_cur.execute("INSERT INTO Leagues (country_name, league_name, country_league_name, league_url) "
                             "VALUES (?, ?, ?, ?)",
                             (league_country, league_name, country_league_name, user_prompt.strip()))
            main_conn.commit()
            print(country_league_name, "was added to the database \n")
            break
        except sqlite3.IntegrityError:
            print(" ")
            print(country_league_name, "is already in the database. Please try adding another league. \n")
            print(" ")
            continue




def league_update_delete():
    """Deletes leagues from the league database"""

    while True:
        user_prompt = input("Please input the number next to the league you would like to delete: ")
        main_cur.execute("SELECT country_league_name FROM leagues WHERE fid = ?", (user_prompt,))
        league_title = main_cur.fetchall()
        if len(league_title) > 0:
            main_cur.execute("DELETE FROM leagues WHERE fid = ?", (user_prompt,))
            main_conn.commit()
            print(" ")
            print(league_title, "has been deleted")
            break
        else:
            print(" ")
            print(user_prompt, "is not a valid database entry. Please try again. \n")
            continue

def leagues_url_return():
    """Return League links from database"""

    main_cur.execute("SELECT league_url FROM leagues")
    leagues_url = main_cur.fetchall()

    return leagues_url


def league_names_return():
    """Return league names from database"""

    main_cur.execute("SELECT country_league_name FROM leagues")
    league_names = main_cur.fetchall()

    return league_names


# ------------------------------------Match Data--------------------------------------------

def match_data_delete():
    """Delete match data table"""

    main_cur.execute("DELETE FROM match_data WHERE fid IS NOT NULL")
    main_conn.commit()


def match_list_create(leagues_url):
    """Find upcoming matches"""

    match_list = []
    for league_url in leagues_url:
        driver.get(league_url[0])

        # find scheduled matches
        scheduled_matches = driver.find_element_by_xpath(
            '//*[@id="fs-summary-fixtures"]/table/tbody').find_elements_by_tag_name('tr')
        for match in scheduled_matches:
            smatch_id = match.get_attribute('id')
            if len(smatch_id) > 0:
                match_list.append(smatch_id[4:])
            else:
                continue

        # find today's matches
        try:
            today_matches = driver.find_element_by_xpath('//*[@id="fs"]/div/table/tbody').find_elements_by_tag_name(
                'tr')
            for tmatch in today_matches:
                tmatch_id = tmatch.get_attribute('id')
                if len(tmatch_id) > 0:
                    match_list.append(tmatch_id[4:])
                else:
                    continue
        except:
            continue
        # driver.close()
    return match_list


def match_info(match_list):
    """Gather match data"""

    total_matches = len(match_list)
    matches_scanned = 0

    for match_id in match_list:
        try:
            match_url = 'https://www.flashscore.com/match/' + match_id + '/#match-summary'
            driver.get(match_url)

            match_status = driver.find_element_by_css_selector(
                '#flashscore >   div.team-primary-content > div.match-info > div.info-status.mstat').get_attribute(
                'textContent')
            if match_status == 'Finished' or match_status == 'Postponed' or match_status == 'Cancelled':
                continue

            match_datetime_raw = driver.find_element_by_xpath('//*[@id="utime"]').get_attribute('textContent')

            match_datetime_split = match_datetime_raw.split(' ')
            match_time = match_datetime_split[1] + ':00'
            match_date = match_datetime_split[0].split('.')
            match_datetime = match_date[2] + '-' + match_date[1] + '-' + match_date[0] + ' ' + match_time

            match_country_name = str(driver.find_element_by_xpath(
                '//*[@id="detcon"]/div[1]/div[2]/div[1]/div/div[1]/span[2]').get_attribute('textContent')
                                     ).split(':')[0].capitalize()
            match_league_name = str(driver.find_element_by_xpath(
                '//*[@id="detcon"]/div[1]/div[2]/div[1]/div/div[1]/span[2]/a').get_attribute(
                'textContent')).split(' -')[0].strip()
            country_league_name = match_country_name + ' ' + match_league_name

            home_team_name = driver.find_element_by_xpath(
                '//*[@id="flashscore"]/div[1]/div[1]/div[2]/div/div/a').get_attribute('textContent')
            away_team_name = driver.find_element_by_xpath(
                '//*[@id="flashscore"]/div[1]/div[3]/div[2]/div/div/a').get_attribute('textContent')

            home_team_id = driver.find_element_by_xpath(
                '//*[@id="flashscore"]/div[1]/div[1]/div[1]/div/a').get_attribute(
                'onclick')[-25:-17]
            away_team_id = driver.find_element_by_xpath(
                '//*[@id="flashscore"]/div[1]/div[3]/div[1]/div/a').get_attribute(
                'onclick')[-25:-17]

            home_win_odds = driver.find_element_by_xpath(
                '//*[@id="default-odds"]/tbody/tr/td[2]/span/span[2]/span').get_attribute('textContent')
            if home_win_odds == '-':
                home_win_odds = 0.00
            away_win_odds = driver.find_element_by_xpath(
                '//*[@id="default-odds"]/tbody/tr/td[4]/span/span[2]/span').get_attribute('textContent')
            if away_win_odds == '-':
                away_win_odds = 0.00
            dc_odds_url = 'https://www.flashscore.com/match/' + match_id + '/#odds-comparison;double-chance;full-time'
            driver.get(dc_odds_url)

            home_draw_odds = driver.find_element_by_xpath('//*[@id="odds_dch"]/tbody/tr[1]/td[2]/span').get_attribute(
                'textContent')
            if home_draw_odds == '-':
                home_draw_odds = 0.00
            away_draw_odds = driver.find_element_by_xpath('//*[@id="odds_dch"]/tbody/tr[1]/td[4]/span').get_attribute(
                'textContent')
            if away_draw_odds == '-':
                away_draw_odds = 0.00

            main_cur.execute('''INSERT INTO match_data(match_datetime, country_name, league_name, country_league_name, 
            home_team_name, home_team_ID, away_team_name, away_team_ID, home_win, away_win, home_draw, away_draw, 
            match_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                             (match_datetime, match_country_name, match_league_name, country_league_name,
                              home_team_name, home_team_id, away_team_name, away_team_id, home_win_odds, away_win_odds,
                              home_draw_odds, away_draw_odds, match_url))
            main_conn.commit()

            matches_scanned += 1
            print("Scanning match", matches_scanned, "of", total_matches, "|", home_team_name, "vs", away_team_name)
            # driver.close()
        except:
            matches_scanned += 1
            print("Skipped match", matches_scanned, "of", total_matches, "|", match_url)
            continue


# ------------------------------------League Scrape-----------------------------------------

def league_table_delete():
    """Delete data in the home and away league tables"""

    main_cur.execute("DELETE FROM league_data_home")
    main_cur.execute("DELETE FROM league_data_away")
    main_conn.commit()


def league_data_home(leagues_url):
    """Retrieve home league data for listed leagues"""

    leagues_scanned = 0
    total_leagues = len(leagues_url)

    for league_url in leagues_url:
        driver.get(str(league_url[0]))

        try:
            driver.find_element_by_xpath('//*[@id="tabitem-table-home"]/span/a').click()
            tablerow = driver.find_element_by_xpath('//*[@id="table-type-1"]/tbody').find_elements_by_tag_name('tr')
        except:
            driver.find_element_by_xpath('//*[@id="tabitem-table"]/span/a').click()
            driver.find_element_by_xpath('//*[@id="tabitem-table-home"]/span/a').click()
            tablerow = driver.find_element_by_xpath('//*[@id="table-type-2"]/tbody').find_elements_by_tag_name('tr')

        counter = 1

        for row in tablerow:
            country_name = driver.find_element_by_xpath('//*[@id="mc"]/h2/a[2]').get_attribute('textContent')
            league_name = driver.find_element_by_xpath('//*[@id="fscon"]/div[1]/div[2]').get_attribute('textContent')
            country_league_name = country_name + ' ' + league_name
            home_position = counter
            home_total_clubs = len(tablerow)
            home_team_name = row.find_element_by_xpath(
                '//*[@id="table-type-2"]/tbody/tr[' + str(counter) + ']/td[2]/span[2]/a').get_attribute('textContent')
            home_team_id = row.find_element_by_xpath(
                '//*[@id="table-type-2"]/tbody/tr[' + str(counter) + ']/td[2]/span[2]/a').get_attribute('onclick')[
                           -12:-4]
            home_matches_played = int(
                row.find_element_by_xpath('//*[@id="table-type-2"]/tbody/tr[' + str(counter) + ']/td[3]').get_attribute(
                    'textContent'))
            home_matches_won = int(
                row.find_element_by_xpath('//*[@id="table-type-2"]/tbody/tr[' + str(counter) + ']/td[4]').get_attribute(
                    'textContent'))
            home_matches_draw = int(
                row.find_element_by_xpath('//*[@id="table-type-2"]/tbody/tr[' + str(counter) + ']/td[5]').get_attribute(
                    'textContent'))
            home_matches_loss = int(
                row.find_element_by_xpath('//*[@id="table-type-2"]/tbody/tr[' + str(counter) + ']/td[6]').get_attribute(
                    'textContent'))
            goal_fa = str(
                row.find_element_by_xpath('//*[@id="table-type-2"]/tbody/tr[' + str(counter) + ']/td[7]').get_attribute(
                    'textContent')).split(':')
            home_goal_diff = int(goal_fa[0]) - int(goal_fa[1])

            form_list = []
            home_team_form = 0

            try:
                form_game1 = row.find_element_by_xpath(
                    '//*[@id="table-type-2"]/tbody/tr[' + str(counter) + ']/td[9]/div/a[2]').get_attribute('class')[13]
                form_list.append(form_game1)
                form_game2 = row.find_element_by_xpath(
                    '//*[@id="table-type-2"]/tbody/tr[' + str(counter) + ']/td[9]/div/a[3]').get_attribute('class')[13]
                form_list.append(form_game2)
                form_game3 = row.find_element_by_xpath(
                    '//*[@id="table-type-2"]/tbody/tr[' + str(counter) + ']/td[9]/div/a[4]').get_attribute('class')[13]
                form_list.append(form_game3)
                form_game4 = row.find_element_by_xpath(
                    '//*[@id="table-type-2"]/tbody/tr[' + str(counter) + ']/td[9]/div/a[5]').get_attribute('class')[13]
                form_list.append(form_game4)
                form_game5 = row.find_element_by_xpath(
                    '//*[@id="table-type-2"]/tbody/tr[' + str(counter) + ']/td[9]/div/a[6]').get_attribute('class')[26]
                form_list.append(form_game5)

            except:
                form_game1 = row.find_element_by_xpath(
                    '//*[@id="table-type-2"]/tbody/tr[' + str(counter) + ']/td[9]/div/a[1]').get_attribute('class')[13]
                form_list.append(form_game1)
                form_game2 = row.find_element_by_xpath(
                    '//*[@id="table-type-2"]/tbody/tr[' + str(counter) + ']/td[9]/div/a[2]').get_attribute('class')[13]
                form_list.append(form_game2)
                form_game3 = row.find_element_by_xpath(
                    '//*[@id="table-type-2"]/tbody/tr[' + str(counter) + ']/td[9]/div/a[3]').get_attribute('class')[13]
                form_list.append(form_game3)
                form_game4 = row.find_element_by_xpath(
                    '//*[@id="table-type-2"]/tbody/tr[' + str(counter) + ']/td[9]/div/a[4]').get_attribute('class')[13]
                form_list.append(form_game4)
                form_game5 = row.find_element_by_xpath(
                    '//*[@id="table-type-2"]/tbody/tr[' + str(counter) + ']/td[9]/div/a[5]').get_attribute('class')[26]
                form_list.append(form_game5)

            for form in form_list:
                if form == 'w':
                    form = 3
                elif form == 'd':
                    form = 1
                else:
                    form = 0
                try:
                    home_team_form += form
                except:
                    home_team_form = int(input('Team: ' + home_team_name + '| Please Input Team Form Here: '))

            main_cur.execute('''INSERT INTO league_data_home (country_name, league_name, country_league_name, home_position, home_total_clubs, 
            home_team_name, home_team_id, home_matches_played, home_matches_won, home_matches_draw, home_matches_loss, 
            home_goal_diff, home_team_form)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (country_name, league_name, country_league_name, home_position, home_total_clubs, home_team_name, home_team_id,
                  home_matches_played, home_matches_won, home_matches_draw, home_matches_loss, home_goal_diff,
                  home_team_form))
            main_conn.commit()

            counter += 1
        leagues_scanned += 1
        print("Updated home table", leagues_scanned, "of", total_leagues, "|", country_league_name, "table")


def league_data_away(leagues_url):
    """Retrieve away league data for listed leagues"""

    leagues_scanned = 0
    total_leagues = len(leagues_url)

    for league_url in leagues_url:
        driver.get(str(league_url[0]))

        try:
            driver.find_element_by_xpath('//*[@id="tabitem-table-away"]/span/a').click()
            tablerow = driver.find_element_by_xpath('//*[@id="table-type-1"]/tbody').find_elements_by_tag_name('tr')
        except:
            driver.find_element_by_xpath('//*[@id="tabitem-table"]/span/a').click()
            driver.find_element_by_xpath('//*[@id="tabitem-table-away"]/span/a').click()
            tablerow = driver.find_element_by_xpath('//*[@id="table-type-3"]/tbody').find_elements_by_tag_name('tr')

        counter = 1

        for row in tablerow:
            country_name = driver.find_element_by_xpath('//*[@id="mc"]/h2/a[2]').get_attribute('textContent')
            league_name = driver.find_element_by_xpath('//*[@id="fscon"]/div[1]/div[2]').get_attribute('textContent')
            country_league_name = country_name + ' ' + league_name
            away_position = counter
            away_total_clubs = len(tablerow)
            time.sleep(0.1)
            away_team_name = row.find_element_by_xpath(
                '//*[@id="table-type-3"]/tbody/tr[' + str(counter) + ']/td[2]/span[2]/a').get_attribute('textContent')
            away_team_id = row.find_element_by_xpath(
                '//*[@id="table-type-3"]/tbody/tr[' + str(counter) + ']/td[2]/span[2]/a').get_attribute('onclick')[
                           -12:-4]
            away_matches_played = int(
                row.find_element_by_xpath('//*[@id="table-type-3"]/tbody/tr[' + str(counter) + ']/td[3]').get_attribute(
                    'textContent'))
            away_matches_won = int(
                row.find_element_by_xpath('//*[@id="table-type-3"]/tbody/tr[' + str(counter) + ']/td[4]').get_attribute(
                    'textContent'))
            away_matches_draw = int(
                row.find_element_by_xpath('//*[@id="table-type-3"]/tbody/tr[' + str(counter) + ']/td[5]').get_attribute(
                    'textContent'))
            away_matches_loss = int(
                row.find_element_by_xpath('//*[@id="table-type-3"]/tbody/tr[' + str(counter) + ']/td[6]').get_attribute(
                    'textContent'))
            goal_fa = str(
                row.find_element_by_xpath('//*[@id="table-type-3"]/tbody/tr[' + str(counter) + ']/td[7]').get_attribute(
                    'textContent')).split(':')
            away_goal_diff = int(goal_fa[0]) - int(goal_fa[1])

            form_list = []
            away_team_form = 0

            try:
                form_game1 = row.find_element_by_xpath(
                    '//*[@id="table-type-3"]/tbody/tr[' + str(counter) + ']/td[9]/div/a[2]').get_attribute('class')[13]
                form_list.append(form_game1)
                form_game2 = row.find_element_by_xpath(
                    '//*[@id="table-type-3"]/tbody/tr[' + str(counter) + ']/td[9]/div/a[3]').get_attribute('class')[13]
                form_list.append(form_game2)
                form_game3 = row.find_element_by_xpath(
                    '//*[@id="table-type-3"]/tbody/tr[' + str(counter) + ']/td[9]/div/a[4]').get_attribute('class')[13]
                form_list.append(form_game3)
                form_game4 = row.find_element_by_xpath(
                    '//*[@id="table-type-3"]/tbody/tr[' + str(counter) + ']/td[9]/div/a[5]').get_attribute('class')[13]
                form_list.append(form_game4)
                form_game5 = row.find_element_by_xpath(
                    '//*[@id="table-type-3"]/tbody/tr[' + str(counter) + ']/td[9]/div/a[6]').get_attribute('class')[26]
                form_list.append(form_game5)
            except:
                form_game1 = row.find_element_by_xpath(
                    '//*[@id="table-type-3"]/tbody/tr[' + str(counter) + ']/td[9]/div/a[1]').get_attribute('class')[13]
                form_list.append(form_game1)
                form_game2 = row.find_element_by_xpath(
                    '//*[@id="table-type-3"]/tbody/tr[' + str(counter) + ']/td[9]/div/a[2]').get_attribute('class')[13]
                form_list.append(form_game2)
                form_game3 = row.find_element_by_xpath(
                    '//*[@id="table-type-3"]/tbody/tr[' + str(counter) + ']/td[9]/div/a[3]').get_attribute('class')[13]
                form_list.append(form_game3)
                form_game4 = row.find_element_by_xpath(
                    '//*[@id="table-type-3"]/tbody/tr[' + str(counter) + ']/td[9]/div/a[4]').get_attribute('class')[13]
                form_list.append(form_game4)
                form_game5 = row.find_element_by_xpath(
                    '//*[@id="table-type-3"]/tbody/tr[' + str(counter) + ']/td[9]/div/a[5]').get_attribute('class')[26]
                form_list.append(form_game5)

            for form in form_list:
                if form == 'w':
                    form = 3
                elif form == 'd':
                    form = 1
                else:
                    form = 0
                try:
                    away_team_form += form
                except:
                    away_team_form = int(input('Team: ' + away_team_name + '| Please Input Team Form Here: '))

            main_cur.execute('''INSERT INTO league_data_away (country_name, league_name, country_league_name, away_position, away_total_clubs, 
                        away_team_name, away_team_id, away_matches_played, away_matches_won, away_matches_draw, away_matches_loss, 
                        away_goal_diff, away_team_form)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (country_name, league_name, country_league_name, away_position, away_total_clubs, away_team_name, away_team_id,
                              away_matches_played, away_matches_won, away_matches_draw, away_matches_loss,
                              away_goal_diff, away_team_form))
            main_conn.commit()

            counter += 1
        leagues_scanned += 1
        print("Updated away table", leagues_scanned, "of", total_leagues, "|", country_league_name, "table")


# ------------------------------------UEFA Rankings-----------------------------------------

def uefa_ranking_delete():
    """Delete the UEFA League Ranking Table"""

    main_cur.execute("DELETE FROM uefa_team_ranking")
    main_conn.commit()


def uefa_team_ranking():
    """Get the team ranking from the UEFA Coefficient website"""

    print("Updating Team Ranking Table")
    driver.get('https://www.uefa.com/memberassociations/uefarankings/club/seasonclub/') # Team ranking URL

    ranking_table = driver.find_element_by_xpath(
        '//*[@id="DataTables_Table_0"]/tbody')
    ranking_row = ranking_table.find_elements_by_tag_name('tr')

    position_counter = 1

    # Get Statistics
    for row in ranking_row:
        team_rank = position_counter
        team_name = str(row.find_element_by_xpath(
            '//*[@id="DataTables_Table_0"]/tbody/tr['
            + str(position_counter) + ']/td[2]/span/a[1]').get_attribute('textContent')).strip()
        uefa_points = float(row.find_element_by_xpath('//*[@id="DataTables_Table_0"]/tbody/tr['
                                                      + str(position_counter) + ']/td[6]').get_attribute('textContent'))
        position_counter += 1

        # Plug values into database
        main_cur.execute("INSERT INTO uefa_team_ranking (team_rank, team_name, uefa_points) VALUES (?, ?, ?)",
                         (team_rank, team_name, uefa_points))
        main_conn.commit()
    print("Updated Team Ranking Table")


# ---------------------------------League Win Calculations----------------------------------------

def league_winmargin(league_names):
    """Calculate the win margin for leagues in the database"""

    for country_league_name in league_names:
        main_cur.execute("SELECT percentage_chance FROM match_analysis WHERE country_league_name = ? "
                         "AND TEST_bet_result = 'Lost'", country_league_name)
        perc_win_data = main_cur.fetchall()

        if len(perc_win_data) < 10:
            main_cur.execute("UPDATE leagues SET single_chnc_margin = 65, double_chnc_margin = 35 "
                             "WHERE country_league_name = ?", country_league_name)
            main_conn.commit()
        else:
            double_chnc = int(round(numpy.percentile(perc_win_data, 75)))
            single_chnc = int(round(numpy.percentile(perc_win_data, 90)))

            main_cur.execute("UPDATE leagues SET single_chnc_margin = ?, double_chnc_margin = ? "
                             "WHERE country_league_name = ?", (single_chnc, double_chnc, country_league_name[0]))
            main_conn.commit()


def league_winrate(league_names):
    """Calculate the win rates of the leagues in the database for for all matches in a league"""

    for country_league_name in league_names:
        main_cur.execute("SELECT TEST_bet_result from match_analysis WHERE country_league_name = ? "
                         "AND TEST_bet_result IS NOT NULL", country_league_name)
        data = main_cur.fetchall()

        if len(data) == 0:
            if country_league_name == 'England Premier League':
                main_cur.execute("UPDATE leagues SET league_winperc = 61 "
                                 "WHERE country_league_name = 'England Premier League'")
                main_conn.commit()
            elif country_league_name == 'England Championship':
                main_cur.execute("UPDATE leagues SET league_winperc = 65 "
                                 "WHERE country_league_name = 'England Championship'")
                main_conn.commit()
            elif country_league_name == 'England League One':
                main_cur.execute("UPDATE leagues SET league_winperc = 57 "
                                 "WHERE country_league_name = 'England League One'")
                main_conn.commit()
            elif country_league_name == 'England League Two':
                main_cur.execute("UPDATE leagues SET league_winperc = 68 "
                                 "WHERE country_league_name = 'England League Two'")
                main_conn.commit()
            elif country_league_name == 'France Ligue 1':
                main_cur.execute("UPDATE leagues SET league_winperc = 67 "
                                 "WHERE country_league_name = 'France Ligue 1'")
                main_conn.commit()
            elif country_league_name == 'Germany Bundesliga':
                main_cur.execute("UPDATE leagues SET league_winperc = 66 "
                                 "WHERE country_league_name = 'Germany Bundesliga'")
                main_conn.commit()
            elif country_league_name == 'Italy Serie A':
                main_cur.execute("UPDATE leagues SET league_winperc = 72 "
                                 "WHERE country_league_name = 'Italy Serie A'")
                main_conn.commit()
            elif country_league_name == 'Netherlands Eredivisie':
                main_cur.execute("UPDATE leagues SET league_winperc = 56 "
                                 "WHERE country_league_name = 'Netherlands Eredivisie'")
                main_conn.commit()
            elif country_league_name == 'Spain LaLiga':
                main_cur.execute("UPDATE leagues SET league_winperc = 65 "
                                 "WHERE country_league_name = 'Spain LaLiga'")
                main_conn.commit()
            elif country_league_name == 'Spain LaLiga2':
                main_cur.execute("UPDATE leagues SET league_winperc = 67 "
                                 "WHERE country_league_name = 'Spain LaLiga2'")
                main_conn.commit()
            else:
                main_cur.execute("UPDATE leagues SET league_winperc = 0 "
                                 "WHERE country_league_name = ?", country_league_name)
                main_conn.commit()
        else:
            won = 0
            lost = 0
            total_played = 0

            for bet_result in data:
                if bet_result[0] == 'Won':
                    won += 1
                    total_played += 1
                elif bet_result[0] == 'Lost':
                    lost += 1
                    total_played += 1
                else:
                    continue

            league_winrate = floor((won / total_played) * 100)

            main_cur.execute("UPDATE leagues SET league_winperc = ? WHERE country_league_name = ?",
                             (league_winrate, country_league_name[0]))
            main_conn.commit()


# ---------------------------------Factor Weight Ranking------------------------------------

def position_ranking_winrate(league_names):
    """Calculate the winrate based solely on position ranking for all matches in a league"""

    for country_league_name in league_names:
        main_cur.execute("SELECT home_position_rank, away_position_rank, percentage_chance, TEST_bet_result "
                         "FROM match_analysis WHERE TEST_bet_result IS NOT NULL AND country_league_name = ?",
                         country_league_name)
        position_rank_data = main_cur.fetchall()

        if len(position_rank_data) == 0:
            main_cur.execute("UPDATE leagues SET pos_winrate = 71.52 WHERE country_league_name = ?",
                             country_league_name)
            main_conn.commit()
        else:
            won = 0
            lost = 0

            for home_position_rank, away_position_rank, percentage_chance, test_bet_result in position_rank_data:
                if home_position_rank > away_position_rank and test_bet_result == 'Won':
                    won += 1
                elif home_position_rank < away_position_rank and test_bet_result == 'Won':
                    won += 1
                elif home_position_rank > away_position_rank and test_bet_result == 'Lost':
                    lost += 1
                elif home_position_rank < away_position_rank and test_bet_result == 'Lost':
                    lost += 1
                else:
                    continue
            try:
                position_win_percentage = (won / (won + lost)) * 100
            except ZeroDivisionError:
                position_win_percentage = 71.52

            main_cur.execute("UPDATE leagues SET pos_winrate = ? WHERE country_league_name  = ?",
                             (position_win_percentage, country_league_name[0]))
            main_conn.commit()


def team_name_ranking_winrate(league_names):
    """Calculate winrate of team name ranbking"""

    for country_league_name in league_names:
        main_cur.execute("SELECT home_team_name_rank, away_team_name_rank, percentage_chance, TEST_bet_result "
                         "FROM match_analysis WHERE TEST_bet_result is not null and home_team_name_rank is not null "
                         "OR away_team_name_rank is not null and country_league_name = ?",
                         country_league_name)
        team_name_rank_data = main_cur.fetchall()

        if len(team_name_rank_data) == 0:
            main_cur.execute("UPDATE leagues SET team_name_winrate = 81.82 WHERE country_league_name = ?",
                             country_league_name)
            main_conn.commit()
        else:
            won = 0
            lost = 0

            for home_team_name_rank, away_team_name_rank, percentage_chance, test_bet_result in team_name_rank_data:
                if home_team_name_rank is None:
                    home_team_name_rank = 0
                if away_team_name_rank is None:
                    away_team_name_rank = 0

                if home_team_name_rank > away_team_name_rank and test_bet_result == 'Won':
                    won += 1
                elif home_team_name_rank < away_team_name_rank and test_bet_result == 'Won':
                    won += 1
                elif home_team_name_rank > away_team_name_rank and test_bet_result == 'Lost':
                    lost += 1
                elif home_team_name_rank < away_team_name_rank and test_bet_result == 'Lost':
                    lost += 1
                else:
                    continue

            try:
                team_name_win_percentage = (won / (won + lost)) * 100
            except ZeroDivisionError:
                team_name_win_percentage = 81.82

            main_cur.execute("UPDATE leagues SET team_name_winrate = ? WHERE country_league_name = ?",
                             (team_name_win_percentage, country_league_name[0]))
            main_conn.commit()


def form_ranking_winrate(league_names):
    """Calculate winrate of form ranking"""

    for country_league_name in league_names:
        main_cur.execute("SELECT home_form_rank, away_form_rank, percentage_chance, TEST_bet_result "
                         "FROM match_analysis WHERE TEST_bet_result IS NOT NULL AND country_league_name = ?",
                         country_league_name)
        form_rank_data = main_cur.fetchall()


        if len(form_rank_data) == 0:
            main_cur.execute("UPDATE leagues SET form_winrate = 68.31 WHERE country_league_name = ?",
                             country_league_name)
            main_conn.commit()
        else:
            won = 0
            lost = 0

            for home_form_rank, away_form_rank, percentage_chance, test_bet_result in form_rank_data:
                if home_form_rank > away_form_rank and test_bet_result == 'Won':
                    won += 1
                elif home_form_rank < away_form_rank and test_bet_result == 'Won':
                    won += 1
                elif home_form_rank > away_form_rank and test_bet_result == 'Lost':
                    lost += 1
                elif home_form_rank < away_form_rank and test_bet_result == 'Lost':
                    lost += 1
                else:
                    continue
            try:
                team_form_win_percentage = (won / (won + lost)) * 100
            except ZeroDivisionError:
                team_form_win_percentage = 68.31

            main_cur.execute("UPDATE leagues SET form_winrate = ? WHERE country_league_name = ?",
                             (team_form_win_percentage, country_league_name[0]))
            main_conn.commit()


def gd_ranking_winrate(league_names):
    """Calculate winrate of goal difference ranking"""

    for country_league_name in league_names:
        main_cur.execute("SELECT home_gd_rank, away_gd_rank, percentage_chance, TEST_bet_result "
                         "FROM match_analysis WHERE TEST_bet_result IS NOT NULL AND country_league_name = ?",
                         country_league_name)
        gd_rank_data = main_cur.fetchall()

        if len(gd_rank_data) == 0:
            main_cur.execute("UPDATE leagues SET gd_winrate = 72.81 WHERE country_league_name = ?",
                             country_league_name)
            main_conn.commit()
        else:
            won = 0
            lost = 0

            for home_gd_rank, away_gd_rank, percentage_chance, test_bet_result in gd_rank_data:
                if home_gd_rank is not None and test_bet_result == 'Won':
                    won += 1
                elif away_gd_rank is not None and test_bet_result == 'Won':
                    won += 1
                else:
                    lost += 1

            try:
                gd_win_percentage = (won / (won + lost)) * 100
            except ZeroDivisionError:
                gd_win_percentage = 72.81

            main_cur.execute("UPDATE leagues SET gd_winrate = ? WHERE country_league_name = ?",
                             (gd_win_percentage, country_league_name[0]))
            main_conn.commit()


def pos_weighting_calc(league_names):
    """"calculate weightings for position ranking"""

    for country_league_name in league_names:
        main_cur.execute("SELECT pos_winrate, team_name_winrate, form_winrate, gd_winrate FROM leagues "
                         "WHERE country_league_name = ?", country_league_name)
        ranking_data = main_cur.fetchall()

        for position_ranking_winrate, team_name_ranking_winrate, form_ranking_winrate, gd_ranking_winrate in ranking_data:
            total = position_ranking_winrate + team_name_ranking_winrate + form_ranking_winrate + gd_ranking_winrate
            position_weighting = (position_ranking_winrate / total) * 100

            main_cur.execute("UPDATE leagues SET pos_weighting = ? WHERE country_league_name = ?",
                             (position_weighting, country_league_name[0]))
            main_conn.commit()


def team_name_weighting_calc(league_names):
    """"calculate weightings for team reputation"""

    for country_league_name in league_names:
        main_cur.execute("SELECT pos_winrate, team_name_winrate, form_winrate, gd_winrate FROM leagues "
                         "WHERE country_league_name = ?", country_league_name)
        ranking_data = main_cur.fetchall()

        for position_ranking_winrate, team_name_ranking_winrate, form_ranking_winrate, gd_ranking_winrate in ranking_data:
            total = position_ranking_winrate + team_name_ranking_winrate + form_ranking_winrate + gd_ranking_winrate
            team_name_weighting = (team_name_ranking_winrate / total) * 100

            main_cur.execute("UPDATE leagues SET team_name_weighting = ? WHERE country_league_name = ?",
                             (team_name_weighting, country_league_name[0]))
            main_conn.commit()


def form_weighting_calc(league_names):
    """"calculate weightings for team form"""

    for country_league_name in league_names:
        main_cur.execute("SELECT pos_winrate, team_name_winrate, form_winrate, gd_winrate FROM leagues "
                         "WHERE country_league_name = ?", country_league_name)
        ranking_data = main_cur.fetchall()

        for position_ranking_winrate, team_name_ranking_winrate, form_ranking_winrate, gd_ranking_winrate in ranking_data:
            total = position_ranking_winrate + team_name_ranking_winrate + form_ranking_winrate + gd_ranking_winrate
            form_weighting = (form_ranking_winrate / total) * 100

            main_cur.execute("UPDATE leagues SET form_weighting = ? WHERE country_league_name = ?",
                             (form_weighting, country_league_name[0]))
            main_conn.commit()


def gd_weighting_calc(league_names):
    """"calculate weightings for goal differences"""

    for country_league_name in league_names:
        main_cur.execute("SELECT pos_winrate, team_name_winrate, form_winrate, gd_winrate FROM leagues "
                         "WHERE country_league_name = ?", country_league_name)
        rank_data = main_cur.fetchall()

        for position_ranking_winrate, team_name_ranking_winrate, form_ranking_winrate, gd_ranking_winrate in rank_data:
            total = position_ranking_winrate + team_name_ranking_winrate + form_ranking_winrate + gd_ranking_winrate
            gd_weighting = (gd_ranking_winrate / total) * 100

            main_cur.execute("UPDATE leagues SET gd_weighting = ? WHERE country_league_name = ?",
                             (gd_weighting, country_league_name[0]))
            main_conn.commit()


# -------------------------------------Analysis---------------------------------------------


def analysis_delete_3month():
    """Delete matches that have results and are older than two months"""

    main_cur.execute("DELETE FROM match_analysis where match_datetime < datetime('now', '-3 months')")
    main_conn.commit()


def analysis_delete_upcoming():
    """Delete matches that have not been played yet"""

    main_cur.execute("DELETE FROM match_analysis WHERE TEST_bet_result ISNULL")
    main_conn.commit()


def analysis_insert():
    """Populate match analysis table"""

    main_cur.execute("INSERT OR IGNORE INTO match_analysis (match_datetime, country_name, league_name, "
                     "country_league_name, home_team_name, home_team_id, away_team_name, away_team_ID, home_win, "
                     "home_draw, away_draw, away_win, home_position, away_position, total_clubs, home_matches_played, "
                     "away_matches_played, home_matches_won, away_matches_won, home_matches_draw, away_matches_draw, "
                     "home_matches_loss, away_matches_loss, home_goal_diff, away_goal_diff, home_team_form, "
                     "away_team_form, match_url) "
                     "SELECT match_datetime, match_data.country_name, match_data.league_name, "
                     "match_data.country_league_name, match_data.home_team_name, match_data.home_team_ID, "
                     "match_data.away_team_name, match_data.away_team_ID, home_win, home_draw, away_draw, away_win, "
                     "home_position, away_position, home_total_clubs, home_matches_played, away_matches_played, "
                     "home_matches_won, away_matches_won, home_matches_draw, away_matches_draw, home_matches_loss, "
                     "away_matches_loss, home_goal_diff, away_goal_diff, home_team_form, away_team_form, match_url "
                     "FROM match_data "
                     "INNER JOIN league_data_home ON match_data.home_team_name = league_data_home.home_team_name "
                     "INNER JOIN league_data_away ON match_data.away_team_name = league_data_away.away_team_name")
    main_conn.commit()


def team_ranking_calc_home():
    """Calculate team ranking"""

    main_cur.execute("SELECT flashscore_team_name, uefa_points "
                     "FROM name_conversion "
                     "INNER JOIN uefa_team_ranking on uefa_team_name = team_name")

    result = main_cur.fetchall()

    for index, rank in enumerate(result):
        if index == 0:
            top_point = rank[1]

    main_cur.execute("SELECT match_analysis.fid, flashscore_team_name, uefa_points, team_name_weighting "
                     "FROM name_conversion "
                     "INNER JOIN uefa_team_ranking on uefa_team_name = team_name INNER JOIN match_analysis "
                     "ON flashscore_team_name = match_analysis.home_team_name "
                     "INNER JOIN leagues ON leagues.country_league_name = match_analysis.country_league_name "
                     "WHERE TEST_bet_result IS NULL ")
    result = main_cur.fetchall()

    # Calculate team rank

    for fid, flashscore_team_name, uefa_points, team_name_weighting in result:
        team_rank = (uefa_points / top_point) * team_name_weighting

        main_cur.execute("UPDATE match_analysis SET home_team_name_rank = ? WHERE home_team_name = ? AND fid = ?",
                         (team_rank, flashscore_team_name, fid))
        main_conn.commit()


def team_ranking_calc_away():
    """Calculate team ranking"""

    main_cur.execute("SELECT flashscore_team_name, uefa_points "
                     "FROM name_conversion "
                     "INNER JOIN uefa_team_ranking on uefa_team_name = team_name")

    result = main_cur.fetchall()

    for index, rank in enumerate(result):
        if index == 0:
            top_point = rank[1]

    main_cur.execute("SELECT match_analysis.fid, flashscore_team_name, uefa_points, team_name_weighting "
                     "FROM name_conversion "
                     "INNER JOIN uefa_team_ranking on uefa_team_name = team_name INNER JOIN match_analysis "
                     "ON flashscore_team_name = match_analysis.away_team_name "
                     "INNER JOIN leagues ON leagues.country_league_name = match_analysis.country_league_name "
                     "WHERE TEST_bet_result IS NULL ")
    result = main_cur.fetchall()


    # Calculate team rank

    for fid, flashscore_team_name, uefa_points, team_name_weighting in result:
        team_rank = (uefa_points / top_point) * (team_name_weighting)

        main_cur.execute("UPDATE match_analysis SET away_team_name_rank = ? WHERE away_team_name = ? AND fid = ?",
                         (team_rank, flashscore_team_name, fid))
        main_conn.commit()


def form_ranking_calc():
    """Calculate form ranking"""

    main_cur.execute("SELECT match_analysis.fid, home_team_form, away_team_form, form_weighting FROM match_analysis "
                     "INNER JOIN leagues ON leagues.country_league_name = match_analysis.country_league_name "
                     "WHERE TEST_bet_result IS NULL ")
    result = main_cur.fetchall()

    for fid, home_team_form, away_team_form, form_weighting in result:
        home_team_form_ranking = (home_team_form / 15) * form_weighting
        away_team_form_ranking = (away_team_form / 15) * form_weighting

        main_cur.execute("UPDATE match_analysis SET home_form_rank = ? WHERE fid = ?", (home_team_form_ranking, fid))
        main_cur.execute("UPDATE match_analysis SET away_form_rank = ? WHERE fid = ?", (away_team_form_ranking, fid))
        main_conn.commit()


def league_position_ranking_calc():
    """Calculate league position ranking"""

    main_cur.execute("SELECT match_analysis.fid, home_matches_played, home_matches_won, home_matches_draw, "
                     "home_matches_loss, away_matches_played, away_matches_won, away_matches_draw, away_matches_loss, "
                     "pos_weighting FROM match_analysis "
                     "INNER JOIN leagues ON leagues.country_league_name = match_analysis.country_league_name "
                     "WHERE TEST_bet_result IS NULL ")
    result = main_cur.fetchall()

    for fid, hp, hw, hd, hl, ap, aw, ad, al, pw in result:
        points_ranking_home = ((hw * 3) + (hd * 1)) / (hp * 3) * pw
        points_ranking_away = ((aw * 3) + (ad * 1)) / (ap * 3) * pw

        main_cur.execute("UPDATE match_analysis SET home_position_rank = ? WHERE fid = ?", (points_ranking_home, fid))
        main_cur.execute("UPDATE match_analysis SET away_position_rank = ? WHERE fid = ?", (points_ranking_away, fid))
        main_conn.commit()


def goal_difference_ranking_calc():
    """Calculate goal difference ranking"""

    main_cur.execute("SELECT match_analysis.fid, home_goal_diff, away_goal_diff, gd_weighting FROM match_analysis "
                     "INNER JOIN leagues ON leagues.country_league_name = match_analysis.country_league_name "
                     "WHERE TEST_bet_result IS NULL ")
    result = main_cur.fetchall()

    for fid, home_gd, away_gd, gd_weighting in result:
        max_n = gd_weighting
        h2h_gd = home_gd - away_gd
        tru_gd = abs(h2h_gd)
        gd_rank = min(max_n, tru_gd)
        if h2h_gd > 0:
            main_cur.execute("UPDATE match_analysis SET home_gd_rank = ? WHERE fid = ?", (gd_rank, fid))
            main_conn.commit()
        elif h2h_gd < 0:
            main_cur.execute("UPDATE match_analysis SET away_gd_rank = ? WHERE fid = ?", (gd_rank, fid))
            main_conn.commit()
        else:
            continue


def generate_point_totals():
    """Generate the point totals using data in match analysis"""

    main_cur.execute("SELECT match_analysis.fid, home_team_name_rank, home_position_rank, home_form_rank, home_gd_rank,"
                     " away_team_name_rank, away_position_rank, away_form_rank, away_gd_rank, home_win, home_draw, "
                     "away_draw, away_win, double_chnc_margin, single_chnc_margin "
                     "from match_analysis INNER JOIN leagues "
                     "ON match_analysis.country_league_name = leagues.country_league_name "
                     "WHERE TEST_bet_result IS NULL ")
    results = main_cur.fetchall()

    for fid, htnr, hpr, hfr, hgdr, atnr, apr, afr, agdr, hw, hd, ad, aw, dcm, scm in results:
        if htnr is None:
            htnr = 0
        if hpr is None:
            hpr = 0
        if hfr is None:
            hfr = 0
        if hgdr is None:
            hgdr = 0
        if atnr is None:
            atnr = 0
        if apr is None:
            apr = 0
        if afr is None:
            afr = 0
        if agdr is None:
            agdr = 0

        home_total = float(htnr) + float(hpr) + float(hfr) + float(hgdr)
        away_total = float(atnr) + float(apr) + float(afr) + float(agdr)
        total_diff = home_total - away_total

        if total_diff > 0:
            percentage_chance = total_diff
            if scm > percentage_chance > dcm:
                rec_bet = '1x'
            elif percentage_chance >= scm:
                rec_bet = '1'
            else:
                rec_bet = 'Avoid'
        else:
            percentage_chance = abs(total_diff)
            if scm > percentage_chance > dcm:
                rec_bet = '2x'
            elif percentage_chance >= scm:
                rec_bet = '2'
            else:
                rec_bet = 'Avoid'

        # Test Recommended bet
        if total_diff >= 0:
            percentage_chance = total_diff
            if 60 > percentage_chance >= 0:
                test_rec_bet = '1x'
            else:
                test_rec_bet = '1'
        else:
            percentage_chance = abs(total_diff)
            if 60 > percentage_chance > 0:
                test_rec_bet = '2x'
            else:
                test_rec_bet = '2'

        main_cur.execute("UPDATE match_analysis SET home_points_total = ? WHERE fid = ?", (home_total, fid))
        main_cur.execute("UPDATE match_analysis SET away_points_total = ? WHERE fid = ?", (away_total, fid))
        main_cur.execute("UPDATE match_analysis SET rec_bet = ? WHERE fid = ?", (rec_bet, fid))
        main_cur.execute("UPDATE match_analysis SET percentage_chance = ? WHERE fid = ?", (percentage_chance, fid))
        main_cur.execute("UPDATE match_analysis SET TEST_rec_bet = ? WHERE fid = ?", (test_rec_bet, fid))
        main_conn.commit()


# ------------------------------------Bet Tickets-------------------------------------------

def percentage_rec_calc():
    """Calculate Percentage recommendation for each match"""

    main_cur.execute("SELECT match_analysis.fid, percentage_chance, league_winperc FROM match_analysis "
                     "INNER JOIN leagues ON  match_analysis.country_league_name = leagues.country_league_name "
                     "WHERE bet_result isnull")
    data = main_cur.fetchall()

    for fid, percentage_chance, league_winperc in data:
        percentage_rec = (percentage_chance + league_winperc) / 2

        main_cur.execute("UPDATE match_analysis SET percentage_rec = ? WHERE fid = ?", (percentage_rec, fid))
        main_conn.commit()


def view_all_recommended():
    """View all recommended bets"""

    main_cur.execute("SELECT match_datetime, match_analysis.country_league_name, home_team_name, "
                     "away_team_name, rec_bet, percentage_rec "
                     "FROM match_analysis where bet_result isnull AND rec_bet <> 'Avoid' "
                     "AND match_datetime > datetime('now') ORDER BY percentage_rec DESC")
    data = main_cur.fetchall()

    for match_datetime, country_league_name, home_tn, away_tn, rec_bet, percentage_rec in data:
        print(match_datetime + " | " + country_league_name + " | " + home_tn + " vs " + away_tn + " | " + rec_bet
              + " | " + str(round(percentage_rec, 2)))


def odds_list():
    """Returns the recommended odds for each match"""

    # draw matches from database
    main_cur.execute("SELECT fid, rec_bet, home_win, home_draw, away_draw, away_win "
                     "FROM match_analysis where bet_result isnull AND rec_bet <> 'Avoid' "
                     "AND match_datetime >= datetime('now', 'localtime') ORDER BY percentage_rec DESC")
    data = main_cur.fetchall()

    odds_data_list = []

    # determine odds and place in dictionary
    for fid, rec_bet, home_win, home_draw, away_draw, away_win in data:

        bet_odds = ' '
        if rec_bet == '1':
            bet_odds = float(home_win)
        elif rec_bet == '1x':
            bet_odds = float(home_draw)
        elif rec_bet == '2x':
            bet_odds = float(away_draw)
        elif rec_bet == '2':
            bet_odds = float(away_win)

        if bet_odds > 1.14:
            odds_data = (fid, bet_odds)
            odds_data_list.append(odds_data)
        else:
            continue

    return odds_data_list


def ticket_generation(acca_limit, odds_listing):
    """Create match tickets automatically"""

    acca = 1    # Default multiplier
    ticket_number = 1
    print("--------------------------- Ticket", ticket_number, "----------------------------------")

    for odds in odds_listing:
        acca = acca * odds[1]
        if acca <= acca_limit:
            main_cur.execute(
                "SELECT match_datetime, match_analysis.country_league_name, home_team_name, "
                "away_team_name, rec_bet, percentage_rec FROM match_analysis where fid = ? ", (odds[0],))
            data = main_cur.fetchall()

            for match_datetime, country_league_name, home_tn, away_tn, rec_bet, percentage_rec in data:
                print(match_datetime + " | " + country_league_name + " | " + home_tn + " vs " + away_tn + " | " +
                      rec_bet + " | " + str(odds[1]) + " | " + str(round(percentage_rec, 2)))
        else:
            print('Tickets Odds:', round((acca / odds[1]), 2))
            acca = 1
            ticket_number += 1
            print(' ')
            print("--------------------------- Ticket", ticket_number, "----------------------------------")
            acca = acca * odds[1]

            main_cur.execute(
                "SELECT match_datetime, match_analysis.country_league_name, home_team_name, "
                "away_team_name, rec_bet, percentage_rec "
                "FROM match_analysis where fid = ? ", (odds[0],))
            data = main_cur.fetchall()

            for match_datetime, country_league_name, home_tn, away_tn, rec_bet, percentage_rec in data:
                print(match_datetime + " | " + country_league_name + " | " + home_tn + " vs " + away_tn + " | " +
                      rec_bet + " | " + str(odds[1]) + " | " + str(round(percentage_rec, 2)))
    print('Tickets Odds:', round(acca, 2))

# ------------------------------------Results-----------------------------------------------


def match_results():
    """Gather match results"""

    print('Collecting match results...')
    main_cur.execute('SELECT fid, match_url FROM match_analysis WHERE match_result ISNULL')
    data = main_cur.fetchall()

    match_count = 0

    for fid, match_url in data:
        driver.get(match_url)
        match_status = driver.find_element_by_xpath('//*[@id="flashscore"]/div[1]/div[2]/div[2]'
                                                    ).get_attribute('textContent')
        if match_status == 'Finished':
            home_score = driver.find_element_by_xpath('//*[@id="event_detail_current_result"]/span[1]'
                                                      ).get_attribute('textContent')
            away_score = driver.find_element_by_xpath('//*[@id="event_detail_current_result"]/span[2]/span[2]'
                                                      ).get_attribute('textContent')
            match_result = int(home_score) - int(away_score)

            if match_result > 0:
                main_cur.execute("UPDATE match_analysis SET match_result = 'Home Win' WHERE fid = ?", (fid,))
                main_conn.commit()
                match_count += 1
            elif match_result < 0:
                main_cur.execute("UPDATE match_analysis SET match_result = 'Away Win' WHERE fid = ?", (fid,))
                main_conn.commit()
                match_count += 1
            elif match_result == 0:
                main_cur.execute("UPDATE match_analysis SET match_result = 'Draw' WHERE fid = ?", (fid,))
                main_conn.commit()
                match_count += 1
            else:
                print("There was an error retrieving a match result", match_url)
                continue
            print("Number of match results retrieved:", match_count)

        elif match_status == 'Postponed':
            main_cur.execute('DELETE FROM match_analysis WHERE fid = ?', (fid,))
            main_conn.commit()


def bet_result():
    """Calculate the bet result"""

    main_cur.execute("SELECT fid, rec_bet, match_result FROM match_analysis WHERE bet_result ISNULL AND match_result IS"
                     " NOT NULL")
    data = main_cur.fetchall()

    for fid, rec_bet, match_result in data:
        if match_result == 'Home Win' and (rec_bet == '1' or rec_bet == '1x'):
            main_cur.execute("UPDATE match_analysis SET bet_result ='Won' WHERE fid = ?", (fid,))
            main_conn.commit()
        elif match_result == 'Away Win' and (rec_bet == '2' or rec_bet == '2x'):
            main_cur.execute("UPDATE match_analysis SET bet_result ='Won' WHERE fid = ?", (fid,))
            main_conn.commit()
        elif match_result == 'Draw' and (rec_bet == '1x' or rec_bet == '2x'):
            main_cur.execute("UPDATE match_analysis SET bet_result ='Won' WHERE fid = ?", (fid,))
            main_conn.commit()
        elif match_result == 'Home Win' and (rec_bet == '2' or rec_bet == '2x'):
            main_cur.execute("UPDATE match_analysis SET bet_result ='Lost' WHERE fid = ?", (fid,))
            main_conn.commit()
        elif match_result == 'Away Win' and (rec_bet == '1' or rec_bet == '1x'):
            main_cur.execute("UPDATE match_analysis SET bet_result ='Lost' WHERE fid = ?", (fid,))
            main_conn.commit()
        elif match_result == 'Draw' and (rec_bet == '1' or rec_bet == '2'):
            main_cur.execute("UPDATE match_analysis SET bet_result ='Lost' WHERE fid = ?", (fid,))
            main_conn.commit()
        elif match_result == 'Home Win' and rec_bet == 'Avoid':
            main_cur.execute("UPDATE match_analysis SET bet_result = 'Avoided' WHERE fid = ?", (fid,))
            main_conn.commit()
        elif match_result == 'Away Win' and rec_bet == 'Avoid':
            main_cur.execute("UPDATE match_analysis SET bet_result = 'Avoided' WHERE fid = ?", (fid,))
            main_conn.commit()
        elif match_result == 'Draw' and rec_bet == 'Avoid':
            main_cur.execute("UPDATE match_analysis SET bet_result = 'Avoided' WHERE fid = ?", (fid,))
            main_conn.commit()
        else:
            print('There was an error processing the bet result', fid, rec_bet, match_result)
            continue


def test_bet_result():
    """Calculate the result of the test bet"""

    main_cur.execute("SELECT fid, TEST_rec_bet, match_result FROM match_analysis WHERE TEST_bet_result "
                     "ISNULL AND match_result IS NOT NULL")
    data = main_cur.fetchall()

    for fid, Test_rec_bet, match_result in data:
        if match_result == 'Home Win' and (Test_rec_bet == '1' or Test_rec_bet == '1x'):
            main_cur.execute("UPDATE match_analysis SET TEST_bet_result ='Won' WHERE fid = ?", (fid,))
            main_conn.commit()
        elif match_result == 'Away Win' and (Test_rec_bet == '2' or Test_rec_bet == '2x'):
            main_cur.execute("UPDATE match_analysis SET TEST_bet_result ='Won' WHERE fid = ?", (fid,))
            main_conn.commit()
        elif match_result == 'Draw' and (Test_rec_bet == '1x' or Test_rec_bet == '2x'):
            main_cur.execute("UPDATE match_analysis SET TEST_bet_result ='Won' WHERE fid = ?", (fid,))
            main_conn.commit()
        elif match_result == 'Home Win' and (Test_rec_bet == '2' or Test_rec_bet == '2x'):
            main_cur.execute("UPDATE match_analysis SET TEST_bet_result ='Lost' WHERE fid = ?", (fid,))
            main_conn.commit()
        elif match_result == 'Away Win' and (Test_rec_bet == '1' or Test_rec_bet == '1x'):
            main_cur.execute("UPDATE match_analysis SET TEST_bet_result ='Lost' WHERE fid = ?", (fid,))
            main_conn.commit()
        elif match_result == 'Draw' and (Test_rec_bet == '1' or Test_rec_bet == '2'):
            main_cur.execute("UPDATE match_analysis SET TEST_bet_result ='Lost' WHERE fid = ?", (fid,))
            main_conn.commit()
        else:
            print('There was an error processing the bet result', fid, Test_rec_bet, match_result)
            continue


def view_match_results_5days():
    """View match results for the last 5 days"""

    main_cur.execute("select match_datetime, match_analysis.country_league_name, home_team_name, "
                     "away_team_name, rec_bet, percentage_rec, match_result, bet_result from match_analysis "
                     "where match_datetime between datetime('now', '-5 days') and datetime('now') "
                     "and bet_result is not null ORDER BY match_datetime DESC")
    data = main_cur.fetchall()

    for match_datetime, country_league_name, home_tn, away_tn, rec_bet, percentage_rec, mr, br in data:
        print(match_datetime + " | " + country_league_name + " | " + home_tn + " vs " + away_tn + " | " + rec_bet
              + " | " + str(round(percentage_rec, 2)) + " | " + mr + " | " + br)


# ------------------------------------Match Archive-----------------------------------------

def match_archive_insert():
    """Insert completed matches into the match archive"""

    main_cur.execute('INSERT OR IGNORE INTO match_archive(match_datetime, country_name, league_name, '
                     'country_league_name, home_team_name, home_team_id, away_team_name, away_team_ID, home_win, '
                     'home_draw, away_draw, away_win, home_position, away_position, total_clubs, home_matches_played, '
                     'away_matches_played, home_matches_won, away_matches_won, home_matches_draw, away_matches_draw, '
                     'home_matches_loss, away_matches_loss, home_goal_diff, away_goal_diff, home_team_form, '
                     'away_team_form, home_team_name_rank, away_team_name_rank, home_position_rank, away_position_rank,'
                     ' home_form_rank, away_form_rank, home_gd_rank, away_gd_rank, home_points_total, '
                     'away_points_total, rec_bet, percentage_chance, percentage_rec, match_result, bet_result, '
                     'TEST_rec_bet, TEST_bet_result, match_url, league_url, league_winperc, single_chnc_margin, '
                     'double_chnc_margin, pos_weighting, team_name_weighting, form_weighting, gd_weighting, '
                     'pos_winrate, team_name_winrate, form_winrate, gd_winrate) '
                     'SELECT match_datetime, match_analysis.country_name, match_analysis.league_name, '
                     'match_analysis.country_league_name, home_team_name, home_team_id, away_team_name, away_team_ID, '
                     'home_win, home_draw, away_draw, away_win, home_position, away_position, total_clubs, '
                     'home_matches_played, away_matches_played, home_matches_won, away_matches_won, home_matches_draw, '
                     'away_matches_draw, home_matches_loss, away_matches_loss, home_goal_diff, away_goal_diff, '
                     'home_team_form, away_team_form, home_team_name_rank, away_team_name_rank, home_position_rank, '
                     'away_position_rank, home_form_rank, away_form_rank, home_gd_rank, away_gd_rank, home_points_total,'
                     ' away_points_total, rec_bet, percentage_chance, percentage_rec, match_result, bet_result, '
                     'TEST_rec_bet, TEST_bet_result, match_url, league_url, league_winperc, single_chnc_margin, '
                     'double_chnc_margin, pos_weighting, team_name_weighting, form_weighting, gd_weighting, '
                     'pos_winrate, team_name_winrate, form_winrate, gd_winrate '
                     'FROM main.match_analysis INNER JOIN main.leagues '
                     'ON match_analysis.league_name = leagues.league_name WHERE TEST_bet_result is not null '
                     'AND bet_result is not null')
    main_conn.commit()

# ------------------------------------Utility-----------------------------------------------


def backup_database():
    """Creates a backup for the main database"""
    print("Creating a restore point")
    datetime_now = datetime.datetime.now()
    datetimestamp = str(datetime_now.year) + '_' + str(datetime_now.month) + '_' + str(datetime_now.day) + '_' + \
                    str(datetime_now.hour) + str(datetime_now.minute) + str(datetime_now.second)
    copy2('main.db', 'databackup/archive_' + str(datetimestamp) + '.db')


def delete_oldest_database():
    """Deletes oldest database if the backup limit exceeds 30"""

    database_list = os.listdir('databackup')
    if len(database_list) > 10:
        os.remove('databackup/' + database_list[0])
    else:
        pass


def backup_restore():
    """Restore backup from archives"""

    while True:
        file_list = sorted(os.listdir('databackup'))[::-1]
        index = 0

        print('The following backup files are available:')
        print(' ')
        for file in file_list:
            index += 1
            print(str(index) + '.', file)
        print(' ')
        try:
            usr_prompt = int(input('Type the number corresponding with the backupfile you want to restore: ')) - 1
            copy2('databackup/' + file_list[usr_prompt], 'main.db')
            print(' ')
            print('Restored', file_list[usr_prompt], 'to main.db')
            divider()
            break
        except:
            pass
            print("please enter an option listed above")
            divider()


def country_league_combine():
    """ccc"""

    main_cur.execute("Select fid, country_name, league_name from match_archive")
    data = main_cur.fetchall()

    for fid, cn, ln in data:
        cnc = str(cn).capitalize()
        country_league_name = cnc + ' ' + ln

        main_cur.execute("UPDATE match_archive SET country_league_name = ?, country_name = ? WHERE fid = ?",
                         (country_league_name, cnc, fid))
        main_conn.commit()


def match_datetimeupdate():
    """Update match date time"""

    main_cur.execute("SELECT match_datetime, fid from match_analysis")
    data = main_cur.fetchall()

    for ma, fid in data:
        try:
            split_datetime = ma.split(' ')
            match_time = split_datetime[1]
            split_date = split_datetime[0].split(':')
            datetime_correct = split_date[0] + '-' + split_date[1] + '-' + split_date[2] + ' ' + match_time

            main_cur.execute("UPDATE match_analysis SET match_datetime = ? WHERE fid = ?", (datetime_correct, fid))
            main_conn.commit()
        except:
            split_datetime = ma.split(' ')
            match_time = split_datetime[1] + ":00"
            datetime_correct = split_datetime[0] + ' ' + match_time

            main_cur.execute("UPDATE match_analysis SET match_datetime = ? WHERE fid = ?", (datetime_correct, fid))
            main_conn.commit()


def divider():
    """Aesthetic divider"""

    print('''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
''')

# ------------------------------------Statistics------------------------------------------

def winrate_stats(league_names):
    """Show the program winrates and league winrates"""

    print("Winrates for leagues are: ")
    leagues_scanned = 0
    league_winadds = 0

    for country_league_name in league_names:
        main_cur.execute("SELECT bet_result from match_archive WHERE country_league_name = ? "
                         "AND bet_result IS NOT NULL AND rec_bet <> 'Avoid'", country_league_name)
        data = main_cur.fetchall()

        if len(data) < 1:
            league_winrate = 'There are no completed matches for this league in the database'
            print(country_league_name[0], ":", league_winrate)
        else:
            won = 0
            lost = 0
            total_played = 0
            for bet_result in data:
                if bet_result[0] == 'Won':
                    won += 1
                    total_played += 1
                elif bet_result[0] == 'Lost':
                    lost += 1
                    total_played += 1
                else:
                    continue

            league_winrate = floor((won / total_played) * 100)
            print(country_league_name[0], ":", league_winrate)
            league_winadds += int(league_winrate)
            leagues_scanned += 1
    program_winrate = league_winadds / leagues_scanned

    print(" ")
    print("Program winrate:", round(program_winrate, 2))


def odds_winrate():
    """Determine the winrate of lower odds"""

    main_cur.execute("SELECT home_win, away_win, match_result from match_archive")
    data = main_cur.fetchall()

    win_0_5 = 0
    win_1 = 0
    win_1_5 = 0
    win_2 = 0
    win_2_5 = 0
    win_3 = 0
    win_more_3 = 0

    loss_0_5 = 0
    loss_1 = 0
    loss_1_5 = 0
    loss_2 = 0
    loss_2_5 = 0
    loss_3 = 0
    loss_more_3 = 0

    for home_win, away_win, match_result in data:
        odds_diff = home_win - away_win
        if odds_diff >= 0:
            if 0.5 >= odds_diff >= 0:
                if match_result == 'Home Win':
                    win_0_5 += 1
                elif match_result == 'Draw':
                    win_0_5 += 1
                elif match_result == 'Away Win':
                    loss_0_5 += 1
                else:
                    print('Error')
                    break
            elif 1 >= odds_diff > 0.5:
                if match_result == 'Home Win':
                    win_1 += 1
                elif match_result == 'Draw':
                    win_1 += 1
                elif match_result == 'Away Win':
                    loss_1 += 1
                else:
                    print('Error')
                    break
            elif 1.5 >= odds_diff > 1:
                if match_result == 'Home Win':
                    win_1_5 += 1
                elif match_result == 'Draw':
                    win_1_5 += 1
                elif match_result == 'Away Win':
                    loss_1_5 += 1
                else:
                    print('Error')
                    break
            elif 2 >= odds_diff > 1.5:
                if match_result == 'Home Win':
                    win_2 += 1
                elif match_result == 'Draw':
                    win_2 += 1
                elif match_result == 'Away Win':
                    loss_2 += 1
                else:
                    print('Error')
                    break
            elif 2.5 >= odds_diff > 2:
                if match_result == 'Home Win':
                    win_2_5 += 1
                elif match_result == 'Draw':
                    win_2_5 += 1
                elif match_result == 'Away Win':
                    loss_2_5 += 1
                else:
                    print('Error')
                    break
            elif 3 >= odds_diff > 2.5:
                if match_result == 'Home Win':
                    win_3 += 1
                elif match_result == 'Draw':
                    win_3 += 1
                elif match_result == 'Away Win':
                    loss_3 += 1
                else:
                    print('Error')
                    break
            elif odds_diff > 3:
                if match_result == 'Home Win':
                    win_more_3 += 1
                elif match_result == 'Draw':
                    win_more_3 += 1
                elif match_result == 'Away Win':
                    loss_more_3 += 1
                else:
                    print('Error')
                    break
            else:
                print('Error')
                break
        elif odds_diff < 0:
            odds_diff = abs(odds_diff)
            if 0.5 >= odds_diff >= 0:
                if match_result == 'Away Win':
                    win_0_5 += 1
                elif match_result == 'Draw':
                    win_0_5 += 1
                elif match_result == 'Home Win':
                    loss_0_5 += 1
                else:
                    print('Error')
                    break
            elif 1 >= odds_diff > 0.5:
                if match_result == 'Away Win':
                    win_1 += 1
                elif match_result == 'Draw':
                    win_1 += 1
                elif match_result == 'Home Win':
                    loss_1 += 1
                else:
                    print('Error')
                    break
            elif 1.5 >= odds_diff > 1:
                if match_result == 'Away Win':
                    win_1_5 += 1
                elif match_result == 'Draw':
                    win_1_5 += 1
                elif match_result == 'Home Win':
                    loss_1_5 += 1
                else:
                    print('Error')
                    break
            elif 2 >= odds_diff > 1.5:
                if match_result == 'Away Win':
                    win_2 += 1
                elif match_result == 'Draw':
                    win_2 += 1
                elif match_result == 'Home Win':
                    loss_2  += 1
                else:
                    print('Error')
                    break
            elif 2.5 >= odds_diff > 2:
                if match_result == 'Away Win':
                    win_2_5 += 1
                elif match_result == 'Draw':
                    win_2_5 += 1
                elif match_result == 'Home Win':
                    loss_2_5 += 1
                else:
                    print('Error')
                    break
            elif 3 >= odds_diff > 2.5:
                if match_result == 'Away Win':
                    win_3 += 1
                elif match_result == 'Draw':
                    win_3 += 1
                elif match_result == 'Home Win':
                    loss_3 += 1
                else:
                    print('Error')
                    break
            elif odds_diff > 3:
                if match_result == 'Away Win':
                    win_more_3 += 1
                elif match_result == 'Draw':
                    win_more_3 += 1
                elif match_result == 'Home Win':
                    loss_more_3 += 1
                else:
                    print('Error')
                    break
            else:
                print('Error')
                break
        else:
            print('Error')
            break

    winrate_0_5 = (win_0_5 / (win_0_5 + loss_0_5)) * 100
    winrate_1 = (win_1 / (win_1 + loss_1)) * 100
    winrate_1_5 = (win_1_5 / (win_1_5 + loss_1_5)) * 100
    winrate_2 = (win_2 / (win_2 + loss_2)) * 100
    winrate_2_5 = (win_2_5 / (win_2_5 + loss_2_5)) * 100
    winrate_3 = (win_3 / (win_3 + loss_3)) * 100
    winrate_more_3 = (win_more_3 / (win_more_3 + loss_more_3)) * 100

    winrate_odds_all = (winrate_0_5 + winrate_1 + winrate_1_5 + winrate_2 + winrate_2_5 + winrate_3 + winrate_more_3)/7

    print("Odds winrates are as follows:")
    print("Odd difference ranges 0.5 or less:", round(winrate_0_5, 2))
    print("Odd difference ranges 0.6 to 1.0:", round(winrate_1, 2))
    print("Odd difference is ranges 1.1 and 1.5:", round(winrate_1_5, 2))
    print("Odd difference is ranges 1.6 and 2.0:", round(winrate_2, 2))
    print("Odd difference is ranges 2.1 and 2.5:", round(winrate_2_5, 2))
    print("Odd difference is ranges 2.6 and 3.0:", round(winrate_3, 2))
    print("Odd difference is greater than 3.0:", round(winrate_more_3, 2))
    print(" ")
    print("Average Odd Difference winrate:", winrate_odds_all)



# ------------------------------------Third level------------------------------------------

def sys_boot():
    """Run at startup"""

    main_db_check()
    # archive_db_check()
    db_table_check()


def leagues_sect():
    """Adjust and view leagues in the database"""

    divider()
    while True:
        print('''Edit Leagues:
        
What would you like to do? 
1. View Leagues
2. Add Leagues
3. Remove Leagues
4. Return        
        ''')
        user_prompt = int(input("Selection: "))

        if user_prompt == 1:
            divider()
            leagues_display()
            divider()
        elif user_prompt == 2:
            while True:
                divider()
                league_update_add()
                divider()
                user_prompt = input("Would you like to add more leagues? Enter Y/y or N/n:  ")
                if user_prompt == 'y':
                    continue
                elif user_prompt == 'n':
                    break
                else:
                    pass
                    print("Please enter Y/N")
                    divider()
        elif user_prompt == 3:
            while True:
                divider()
                leagues_display()
                divider()

                main_cur.execute("SELECT country_name, league_name FROM leagues")
                league_check = main_cur.fetchone()
                if league_check is None:
                    break
                else:
                    league_update_delete()
                    user_prompt = input("Would you like to delete more leagues? Enter Y/y or N/n: ")
                    if user_prompt == 'y':
                        continue
                    elif user_prompt == 'n':
                        break
                    else:
                        pass
                        print("Please enter Y/N")
                        divider()
        elif user_prompt == 4:
            break
        else:
            pass
            print("please enter an option listed above")
            divider()


def tips_sect():
    """Scrape and gather match data, then present the best tips"""

    while True:
        usr_input = input("Enter your maximum required accumulator: ")
        try:
            acca_limit = int(usr_input)

            break
        except:
            print('----------------------------------------------')
            print('Error! Please enter a number when prompted')
            print('----------------------------------------------')
            pass


    print('''Fetching Tips. Please be patient...
    ''')

    # Program Runtime
    start_time = time.time()

    # Create and manage restore points
    backup_database()
    delete_oldest_database()

    # Collect match and bet results
    match_results()
    bet_result()
    test_bet_result()
    match_archive_insert()

    # Delete databases over 3 months old and upcoming matches that haven't been played yet
    analysis_delete_3month()
    analysis_delete_upcoming()

    # Delete data in match table and collect new match information
    match_data_delete()
    match_info(match_list_create(leagues_url_return()))

    league_table_delete()
    league_data_home(leagues_url_return())
    league_data_away(leagues_url_return())

    uefa_ranking_delete()
    uefa_team_ranking()

    league_winmargin(league_names_return())
    league_winrate(league_names_return())
    print("Updated league win rates and margins")

    position_ranking_winrate(league_names_return())
    team_name_ranking_winrate(league_names_return())
    form_ranking_winrate(league_names_return())
    gd_ranking_winrate(league_names_return())
    print("Updated variable winrates")

    pos_weighting_calc(league_names_return())
    team_name_weighting_calc(league_names_return())
    form_weighting_calc(league_names_return())
    gd_weighting_calc(league_names_return())
    print("Updated variable weightings")

    analysis_insert()
    team_ranking_calc_home()
    team_ranking_calc_away()
    form_ranking_calc()
    league_position_ranking_calc()
    goal_difference_ranking_calc()
    generate_point_totals()
    percentage_rec_calc()
    print("Matches analysed")

    divider()
    print("Your recommended bets are:"
          " ")
    ticket_generation(acca_limit, odds_list())

    print(" ")
    print("--- Runtime: %s minutes ---" % ((time.time() - start_time) / 60))


def results_sect():
    """View recent results"""

    print("Fetching match result..."
          " ")
    match_results()
    print('Match results collected')
    print('Processing bet results')
    bet_result()
    test_bet_result()
    match_archive_insert()
    view_match_results_5days()


def statistics_sect():
    """View statistics"""

    while True:
        user_prompt = int(input('''Which statistic would you like to see?:

        1. See program and league winrates
        2. Odds difference winrates
        3. Return

    Selection: '''))

        if user_prompt == 1:
            divider()
            winrate_stats(league_names_return())
            divider()
        elif user_prompt == 2:
            divider()
            odds_winrate()
            divider()
        elif user_prompt == 3:
            break
        else:
            print("please enter an option listed above")
            divider()

# -------------------------------------Program--------------------------------------------------------------------------

def betterodds():
    """Betting Tips Program"""

    sys_boot()

    time.sleep(2)

    divider()
    # Welcome message
    print("Thank you for using this program. If you have any questions regarding the use of this program please contact"
          " Jinx13 at \nflystyle101@yahoo.com")
    divider()

    time.sleep(2)

    while True:
        user_prompt = int(input('''Hi! Please enter the number corresponding the selection you would like to make

    1. Get tips now!
    2. View Match Results
    3. Edit Leagues
    4. See Statistics
    5. Restore Database
    6. Exit Program

Selection: '''))

        if user_prompt == 1:
            divider()
            tips_sect()
            divider()
        elif user_prompt == 2:
            divider()
            results_sect()
            divider()
        elif user_prompt == 3:
            leagues_sect()
            divider()
        elif user_prompt == 4:
            divider()
            statistics_sect()
            divider()
        elif user_prompt == 5:
            divider()
            backup_restore()
            divider()
        elif user_prompt == 6:
            divider()
            print('Exiting Program...Goodbye')
            driver.quit()
            break
        else:
            pass
            print("please enter an option listed above")

betterodds()

# TODO create database most recent date feature
# TODO Create split between ticket display and retrieval
# TODO handle entry of league that is already in the database
# TODO handle match data collection with no leagues

