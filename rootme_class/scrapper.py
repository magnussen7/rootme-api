#!/usr/bin/python3.6
# coding: utf-8
import re
import requests
from .parser import parser_html
from bs4 import BeautifulSoup

class scrapper(object):
    def __init__(self, username):
        """
        Class init
        @param self: Object himslef
        @type value: Object
        @param username: Username for all query
        @type value: string

        @return: scrapper object
        @rtype: object
        """
        self.set_username(username)

    def set_username(self, username):
        """
        Set username for object
        @param self: Object himslef
        @type value: Object
        @param username: Username for all query
        @type value: string
        """
        self.username = str(username)

    def get_username(self):
        """
        Return username
        @param self: Object himslef
        @type value: string

        @return: username
        @rtype: string
        """
        return self.username

    def extract_info(self):
        """
        Get info for username of object
        @param self: Object himself
        @type value: Object

        @return: all user info in a dictionnary (username, lang, status, total score, number of posts, number of message in Chatbox, website and biography)
        @rtype: dictionnary
        """
        request = requests.get('https://www.root-me.org/' + self.get_username() + '?inc=info&lang=fr')

        if request.status_code == 200:
            soup = BeautifulSoup(request.text, 'html.parser')
            list_info = soup.find('ul', {'class': 'spip'}).contents
            list_info = [element for element in list_info if element != "\n"]

            if len(list_info) > 4:
                lang = list_info[0].img.get('alt')
                statut = list_info[1].string.replace('Statut : ', '')
                score = int(list_info[2].span.string)
                post = int(list_info[3].span.string)
                chatbox = int(list_info[4].string.replace('ChatBox : ', ''))

                if len(list_info) > 5:
                    if 'Site web : ' in list_info[5]:
                        website = list_info[5].a.get('href')
                    else:
                        website = None
                        del list_info[5].contents[0]
                        del list_info[5].contents[0]
                        bio = ''.join([str(value) for value in list_info[5]])

                    if len(list_info) > 6:
                        del list_info[6].contents[0]
                        del list_info[6].contents[0]
                        bio = ''.join([str(value) for value in list_info[6]])
                else:
                    website = None
                    bio = None

                info = {"info": {"username": self.get_username(), "lang": lang, "status": statut, "score": score, "post": post, "chatbox": chatbox, "website": website, "bio": bio}}
            else:
                info = {"info": {"username": self.get_username(), "lang": None, "status": None, "score": None, "post": None, "chatbox": None, "website": None, "bio": None}}
        else:
            info = {"info": {"username": self.get_username(), "lang": None, "status": None, "score": None, "post": None, "chatbox": None, "website": None, "bio": None}}

        return(info)

    def extract_challenges(self):
        """
        Get challenges for username of object
        @param self: Object himself
        @type value: Object

        @return: all challenges in a dictionnary (username, challenges_info(score, number of solved challenges, number of challenges, rank, rank total, rank name), challenges_by_category(category name, category description, category url, score in category, number of solved challenges in category, total of challenges in category), challenges in category(name challenge, points of challenge, challenge flag by user, url challenge))
        @rtype: dictionnary
        """
        request = requests.get('https://www.root-me.org/' + self.get_username() + '?inc=score&lang=fr')

        if request.status_code == 200:
            soup = BeautifulSoup(request.text, 'html.parser')
            info_challenges = self.extract_info_challenges(soup)
            challenges = self.extract_all_challenges(soup)

            challenges = {'challenges': {'username': self.get_username(), 'challenges_info': info_challenges, 'challenges_by_category': challenges}}

        return challenges

    def extract_info_challenges(self, soup):
        """
        Get info challenges from beautiful soup object
        @param self: Object himself
        @type value: Object
        @param soup: Beautiful soup object
        @type value: Object

        @return: all challenges info in a dictionnary (score, number of solved challenges, number of challenges, rank, rank total, rank name))
        @rtype: dictionnary
        """
        parser = parser_html.parser_html()

        info_challenges = soup.find('div', {'class': 'small-12 columns'}).ul.findAll('span')

        score = int(info_challenges[0].contents[0].strip().replace(' Points', ''))
        challenges_solved, challenges_total = parser.get_challenges_achievement(info_challenges[1].contents[0].strip())
        rank = int(info_challenges[2].contents[0].strip())
        rank_total = int(info_challenges[3].contents[0].strip()[1::])
        rank_title = info_challenges[4].contents[0].strip()

        return {"score": score, "challenges_solved": challenges_solved, "challenges_total": challenges_total, "rank": rank, "rank_total": rank_total, "rank_title": rank_title}

    def extract_all_challenges(self, soup):
        """
        Get list challenges from beautiful soup object
        @param soup: Beautiful soup object
        @type value: Object

        @return: all challenges in a dictionnary (challenges_by_category(category name, category description, category url, score in category, number of solved challenges in category, total of challenges in category), challenges in category(name challenge, points of challenge, challenge flag by user, url challenge))
        @rtype: dictionnary
        """
        parser = parser_html.parser_html()

        unparsed_category = soup.findAll('div', {'class': 'animated_box'})
        all_category = []

        for value in unparsed_category:
            all_category.append([element for element in value.contents if element != "\n"])

        categories = []

        for category in all_category:
            category_name = category[0].a.string
            category_description = category[0].a.get('title')
            category_url = 'https://www.root-me.org/' + category[0].a.get('href')
            category_score, category_solved_challenges, category_total_challenges = parser.get_category_score(category[1].string)

            challenges = []

            for challenge in category[2].findAll('li'):
                challenge_name = challenge.a.string.strip()[2:]
                challenge_score = int(challenge.a.get('title').replace(' Points', ''))

                challenge_validation = parser.get_challenge_validation(challenge.a.get('class')[0])
                challenge_url = 'https://www.root-me.org/' + challenge.a.get('href')

                challenges.append({'challenge_name': challenge_name, 'challenge_score': challenge_score, 'challenge_validation': challenge_validation, 'challenge_url': challenge_url})

            categories.append({'name': category_name, 'description': category_description, 'url': category_url, 'score': category_score, 'solved_challenges': category_solved_challenges, 'total_challenges': category_total_challenges, 'challenges': challenges})

        return categories

    def extract_ctf(self):
        """
        Get list ctf for username object
        @param self: Object himself
        @type value: Object

        @return: all ctf in a dictionnary (username, number of solved ctf, number of attempts, number of ctf, ctf(name of ctf, solved by user, number of attempts, number of success, best time of success))
        @rtype: dictionnary
        """
        request = requests.get('https://www.root-me.org/' + self.get_username() + '?inc=ctf&lang=fr')

        if request.status_code == 200:
            parser = parser_html.parser_html()
            soup = BeautifulSoup(request.text, 'html.parser')

            if 'Cet auteur ne participe pas au CTF all the day.' not in request.text:
                unparsed_ctf = soup.find('div', {'t-body tb-padding'})

                ctf_solved, ctf_total_attempts = parser.get_score_ctf(unparsed_ctf.find('span', {'color1 txl'}).string.strip())

                ctf = []

                for value in unparsed_ctf.tbody.findAll('tr'):
                    value = [element for element in value.contents if element != "\n"]
                    ctf_name = value[1].string
                    ctf_flag = parser.get_ctf_validation(value[0].img.get('src'))
                    ctf_attempts = int(value[2].string)
                    ctf_success = int(value[3].string)
                    ctf_duration = parser.get_ctf_duration(value[4].string)

                    ctf.append({'name': ctf_name, 'solved': ctf_flag, 'attempts': ctf_attempts, 'success': ctf_success, 'best_time': ctf_duration})


                return {'ctf_all_the_day': {'username': self.get_username(), 'solved': ctf_solved, 'ctf_total_attempts': ctf_total_attempts, 'ctf_total': len(ctf), 'ctf': ctf}}
        return {'ctf_all_the_day': {'username': self.get_username(), 'solved': None, 'ctf_total_attempts': None, 'ctf_total': None, 'ctf': None}}

    def extract_stats(self):
        """
        Get stats for username object
        @param self: Object himself
        @type value: Object

        @return: all stats in a dictionnary (User's stats : username, score for each difficulty, score total, list of solved challenges (name challenge, category of challenge, url challenge, difficulty challenge, score for this difficulty when flagged, flag date) order from oldest to latest)
        @rtype: dictionnary
        """
        request = requests.get('https://www.root-me.org/' + self.get_username() + '?inc=statistiques&lang=fr')

        if request.status_code == 200:
            parser = parser_html.parser_html()
            soup = BeautifulSoup(request.text, 'html.parser')

            js_challenges = parser.get_js_challenges(soup.findAll('script')[3].get_text())

            challenges = []
            score_difficulty = {'very easy': 0, 'easy': 0, 'medium': 0, 'hard': 0, 'very hard': 0}
            score_total = 0

            for challenge in js_challenges:
                chall = parser.get_parsed_challenge(challenge)
                challenges.append(chall)

                score_difficulty[chall['difficulty']] = chall['total_score_difficulty']

            for value in score_difficulty:
                score_total += score_difficulty[value]

            return {'stats': {'username': self.get_username(), 'score_by_difficulty': score_difficulty, 'score_total': score_total, 'challenges': challenges}}
