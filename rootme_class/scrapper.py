#!/usr/bin/python3.6
# coding: utf-8
import re
import requests
from .parser import parser_html
from bs4 import BeautifulSoup
from datetime import datetime

class scrapper(object):
    def __init__(self, username):
        """
        Class init
        @param self: Object himself
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
        @param self: Object himself
        @type value: Object
        @param username: Username for all query
        @type value: string
        """
        self.__username = str(username)

    def get_username(self):
        """
        Return username
        @param self: Object himself
        @type value: string

        @return: username
        @rtype: string
        """
        return self.__username

    def extract_info(self):
        """
        Get info for username of object
        @param self: Object himself
        @type value: Object

        @return: all user info in a dictionnary
        @rtype: dictionnary
        """
        request = requests.get('https://www.root-me.org/' + self.get_username() + '?inc=info&lang=fr')
        info = {'info': {}}

        if request.status_code == 200:
            soup = BeautifulSoup(request.text, 'html.parser')
            info_container = soup.find('div', {'class': 't-body'})
            row_info = info_container.findAll('div', {'class': 'row'})
            profile_summary = self.__parse_profile_summary__(row_info[0], row_info[2])
            del profile_summary['solved_challenges']
            score_overview = self.__parse_overview_score__(row_info[3])
            achievements = self.__parse_achievements__(row_info[4])
            last_10_flags = self.__parse_last_10_flags__(row_info[5])

            info['info']['username'] = self.get_username()
            info['info'] = profile_summary
            info['info']['score_overview'] = score_overview
            info['info']['score_overview']['last_10_flags'] = last_10_flags
            info['info']['achievements'] = achievements

        return info

    def extract_challenges(self):
        """
        Get challenges for username of object
        @param self: Object himself
        @type value: Object

        @return: all challenges in a dictionnary
        @rtype: dictionnary
        """
        request = requests.get('https://www.root-me.org/' + self.get_username() + '?inc=score&lang=fr')
        challenges = {'challenges': {}}

        if request.status_code == 200:
            soup = BeautifulSoup(request.text, 'html.parser')
            info_container = soup.find('div', {'class': 't-body'})
            row_info = info_container.findAll('div', {'class': 'row'})
            profile_summary = self.__parse_profile_summary__(row_info[0])
            score_summary = self.__parse_score_summary__(row_info[2])
            profile_summary.update(score_summary)
            list_challenges = self.__parse_challenges__(row_info[3])
            challenges['challenges'] = {'username': self.get_username(), 'challenges_info': profile_summary, 'challenges_by_category': list_challenges}

        return challenges

    def extract_ctf(self):
        """
        Get list ctf for username object
        @param self: Object himself
        @type value: Object

        @return: all ctf in a dictionnary
        @rtype: dictionnary
        """
        request = requests.get('https://www.root-me.org/' + self.get_username() + '?inc=ctf&lang=fr')
        ctf_all_the_day = {'ctf_all_the_day': {}}

        if request.status_code == 200:
            if 'Cet auteur ne participe pas au CTF all the day.' not in request.text:
                parser = parser_html.parser_html()
                soup = BeautifulSoup(request.text, 'html.parser')
                info_container = soup.find('div', {'class': 't-body'})
                row_info = info_container.findAll('div', {'class': 'row'})
                profile_summary = self.__parse_profile_summary__(row_info[0])
                solved_ctf, ctf_total_attempts = parser.get_score_ctf(info_container.find('p').findAll('span')[1].text.strip())
                ctf = self.__parse_ctf__(info_container.find('tbody'))
                ctf_all_the_day['ctf_all_the_day'] = {'username': self.get_username(), 'solved': solved_ctf, 'ctf_total_attempts': ctf_total_attempts, 'ctf_total': len(ctf), 'ctf': ctf}

        return ctf_all_the_day


    def extract_stats(self):
        """
        Get stats for username object
        @param self: Object himself
        @type value: Object

        @return: all stats in a dictionnary
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

            for js_challenge in js_challenges:
                solved_datetime = datetime.strptime(js_challenge[0], "%Y-%m-%d %H:%M:%S")

                challenge = {
                    'name': js_challenge[3],
                    'category': js_challenge[1],
                    'url': 'https://www.root-me.org/' + js_challenge[2],
                    'difficulty': parser.get_difficulty_challenge(int(js_challenge[4])),
                    'total_score_difficulty': int(js_challenge[5]),
                    'datetime': solved_datetime,
                }
                challenges.append(challenge)

                score_difficulty[challenge['difficulty']] += int(challenge['total_score_difficulty'])

            for value in score_difficulty:
                score_total += score_difficulty[value]

            return {'stats': {'username': self.get_username(), 'score_by_difficulty': score_difficulty, 'score_total': score_total, 'challenges': challenges}}


    def __parse_profile_summary__(self, header, profile=None):
        """
        Parse header and section user information in info page
        @param self: Object himself
        @type value: Object
        @param header: Header soup Object
        @type value: Object
        @param profile: section user information Soup Object
        @type value: Object

        @return: Dictionnary with user information
        @rtype: dictionnary
        """
        list_columns = header.findAll('div', {'class': 'columns'})
        img_list = list_columns[0].findAll('img', alt=True)
        overview_list = list_columns[1].findAll('h3')

        logo = 'https://www.root-me.org/' + img_list[0].get('src')
        lang = img_list[1].get('alt')

        rank = int(overview_list[0].text.strip())
        score = int(overview_list[1].text.strip())
        solved_challenges = int(overview_list[2].text.strip())
        ctf_solved = int(overview_list[3].text.strip())

        if profile is not None:
            list_info = [element for element in profile.find('ul', {'class': 'spip'}).contents if element != "\n"]

            if len(list_info) >= 3:
                status = list_info[0].text.replace('Statut : ', '')
                post = int(list_info[1].find('span').text)
                chatbox = int(list_info[2].text.replace('ChatBox : ', ''))

                if len(list_info) >= 4:
                    if 'Site web : ' in list_info[3]:
                        website = list_info[3].a.get('href')
                    else:
                        website = None
                        bio = list_info[3].text.replace('Biographie\xa0:', '')

                    if len(list_info) >= 5:
                        bio = list_info[4].text.replace('Biographie\xa0:', '')
                else:
                    website = None
                    bio = None

            return {
                    'status': status,
                    'lang': lang,
                    'post': post,
                    'chatbox': chatbox,
                    'website': website,
                    'bio': bio,
                    'logo': logo,
                    'rank': rank,
                    'score': score,
                    'solved_challenges': solved_challenges,
                    'ctf_solved': ctf_solved
                }
        else:
            return {
                    'rank': rank,
                    'score': score,
                    'solved_challenges': solved_challenges,
                    'ctf_solved': ctf_solved
                }

    def __parse_overview_score__(self, soup):
        """
        Parse score section of info page
        @param self: Object himself
        @type value: Object
        @param soup: soup Object
        @type value: Object

        @return: Dictionnary with user scores
        @rtype: dictionnary
        """
        parser = parser_html.parser_html()
        score_category = []
        overview_score = soup.findAll('h3')[1]
        total_progression = overview_score.text[:overview_score.text.find('%')+1]
        solved_challenges, total_challenges = parser.get_challenges_solved_total(overview_score.text)
        list_category = soup.findAll('a')

        for link in list_category:
            score_category.append({'name': link['title'], 'progression': link.text})

        return {
                'challenges_solved': solved_challenges,
                'challenges_total': total_challenges,
                'total_progression': total_progression,
                'category': score_category
                }

    def __parse_achievements__(self, soup):
        """
        Parse achievement of info page
        @param self: Object himself
        @type value: Object
        @param soup: soup Object
        @type value: Object

        @return: Dictionnary with user achievements
        @rtype: dictionnary
        """
        achievements = []

        for achievement in soup.findAll('img'):
            achievements.append({'title': achievement['title']})
        return achievements

    def __parse_last_10_flags__(self, soup):
        """
        Parse last 10 flags of info page
        @param self: Object himself
        @type value: Object
        @param soup: soup Object
        @type value: Object

        @return: Dictionnary with last 10 flags of user
        @rtype: dictionnary
        """
        parser = parser_html.parser_html()
        last_10_flags = []
        list_flag = soup.findAll('li')
        del list_flag[0]
        for flag in list_flag:
            if 'ctf_alltheday' in flag.a['href']:
                category = 'CTF All the day'
            else:
                category = parser.get_category_name(flag.a['href'])
            last_10_flags.append({'name': flag.a.text, 'category': category})

        return last_10_flags

    def __parse_score_summary__(self, soup):
        """
        Parse score header of score page
        @param self: Object himself
        @type value: Object
        @param soup: soup Object
        @type value: Object

        @return: Dictionnary with user score
        @rtype: dictionnary
        """
        parser = parser_html.parser_html()
        score_summary = soup.findAll('span')
        solved_challenges, total_challenges = parser.get_challenges_solved_total(score_summary[0].text)
        rank, rank_total = parser.get_challenges_solved_total(score_summary[2].text)
        rank_title = score_summary[4].text.strip()

        return {
                'challenges_solved': solved_challenges,
                'challenges_total': total_challenges,
                'rank': rank,
                'rank_total': rank_total,
                'rank_title': rank_title
        }

    def __parse_challenges__(self, soup):
        """
        Parse challenges of score page
        @param self: Object himself
        @type value: Object
        @param soup: soup Object
        @type value: Object

        @return: Dictionnary with challenges by category
        @rtype: dictionnary
        """
        parser = parser_html.parser_html()
        list_columns = soup.findAll('div', {'class': 'columns'})
        categories = []

        for column in list_columns:
            challenges = []
            category_name = column.h4.a.text
            category_url = 'https://www.root-me.org/' + column.h4.a['href']
            category_description = column.h4.a['title']
            category_score = column.findAll('span')[1].text
            category_score = int(category_score[:category_score.find('Points')].replace('\n', ''))
            category_solved_challenges, category_total_challenges = parser.get_challenges_solved_total(column.findAll('span')[1].text)
            list_challenges = column.findAll('li')

            for challenge in list_challenges:
                challenge_name = challenge.a.string.strip()[2:]
                challenge_score = int(challenge.a.get('title').replace(' Points', ''))
                challenge_validation = parser.get_challenge_validation(challenge.a.get('class')[0])
                challenge_url = 'https://www.root-me.org/' + challenge.a.get('href')
                challenges.append({
                                    'challenge_name': challenge_name,
                                    'challenge_score': challenge_score,
                                    'challenge_validation': challenge_validation,
                                    'challenge_url': challenge_url})

            categories.append({
                'name': category_name,
                'description': category_description,
                'url': category_url,
                'score': category_score,
                'challenges_solved': category_solved_challenges,
                'challenges_total': category_total_challenges,
                'challenges': challenges})

        return categories

    def __parse_ctf__(self, soup):
        """
        Parse CTF of ctf page
        @param self: Object himself
        @type value: Object
        @param soup: soup Object
        @type value: Object

        @return: Dictionnary with CTF
        @rtype: dictionnary
        """
        parser = parser_html.parser_html()
        list_ctf = soup.findAll('tr')
        ctf = []

        for tr_ctf in list_ctf:
            info_ctf = tr_ctf.findAll('td')
            ctf_name = info_ctf[1].text
            ctf_flag = parser.get_ctf_validation(info_ctf[0].img.get('src'))
            ctf_attempts = int(info_ctf[2].string)
            ctf_success = int(info_ctf[3].string)
            ctf_duration = parser.get_ctf_duration(info_ctf[4].string)

            ctf.append({'name': ctf_name, 'solved': ctf_flag, 'attempts': ctf_attempts, 'success': ctf_success, 'best_time': ctf_duration})

        return ctf
