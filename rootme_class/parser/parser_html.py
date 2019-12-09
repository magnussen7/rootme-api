#!/usr/bin/python3.6
# coding: utf-8
import re
from datetime import datetime

class parser_html(object):
    def get_challenges_solved_total(self, html):
        """
        Split html string to retrieve number of solved challenges and total challenges
        @param self: Object himself
        @type value: Object
        @param html: Html to parse
        @type value: string

        @return: number of solved challenges and total number of challenges
        @rtype: integer
        """
        regex_challenges_achievement = "(?P<challenges_solved>\d*)\/(?P<challenges_total>\d*)"

        challenges_achievement = re.search(regex_challenges_achievement, str(html))

        if challenges_achievement is not None:
            if challenges_achievement.group('challenges_solved') == '':
                challenges_solved = 0
            else:
                challenges_solved = int(challenges_achievement.group('challenges_solved'))

            challenges_total = int(challenges_achievement.group('challenges_total'))

            return challenges_solved, challenges_total
        else:
            return None, None

    def get_challenge_validation(self, css_class):
        """
        Convert css class in boolean to know if flag or not
        @param self: Object himself
        @type value: Object
        @param css_class: CSS class to check
        @type value: string

        @return: True if flag, false otherwise
        @rtype: boolean
        """
        if css_class == 'vert':
            return True
        elif css_class == 'rouge':
            return False
        else:
            return None

    def get_score_ctf(self, html):
        """
        Split html string to retrieve number of solved ctf and total of ctf all the day
        @param self: Object himself
        @type value: Object
        @param html: Html to parse
        @type value: string

        @return: number of solved ctf and number of ctf
        @rtype: integer
        """
        regex_score_ctf = "(?P<solved_ctf>\d*)\Wmachine\(s\) compromise\(s\)\Wen\W(?P<ctf_total>\d*)\Wtentatives"

        score_ctf = re.match(regex_score_ctf, str(html))

        if score_ctf is not None:
            if score_ctf.group('solved_ctf') == '':
                solved_ctf = 0
            else:
                solved_ctf = int(score_ctf.group('solved_ctf'))

            ctf_total = int(score_ctf.group('ctf_total'))

            return solved_ctf, ctf_total
        else:
            return None, None

    def get_ctf_validation(self, src_img):
        """
        Convert img src in boolean to know if flag or not
        @param self: Object himself
        @type value: Object
        @param css_class: Source Image to check
        @type value: string

        @return: True if flag, false otherwise
        @rtype: boolean
        """
        if 'squelettes/img/valide.svg' in src_img:
            return True
        elif 'squelettes/img/pas_valide.svg' in src_img:
            return False
        else:
            return None

    def get_ctf_duration(self, duration):
        """
        Return best time for ctf
        @param self: Object himself
        @type value: Object
        @param duration: best time
        @type value: string

        @return: Best time
        @rtype: string
        """
        if duration != '-':
            return str(duration)
        else:
            return None

    def get_js_challenges(self, raw_js):
        """
        Return only the js line with challenges stats
        @param self: Object himself
        @type value: Object
        @param raw_js: js string
        @type value: string

        @return: Js line with challenges stats
        @rtype: string
        """
        js_pattern = re.compile(".*validations.push\({\n'date'\s*:\s'(?P<datetime>.*)',\n'titre'\s*:\s'<a\shref=\"https://www.root-me.org/fr/Challenges/(?P<category>.*)/\"\stitle=\".*\"><img\ssrc=\".*\"\sclass=\"vmiddle\"/></a>\s*<a\shref=\"(?P<url>.*)\">(?P<name>.*)</a>',\n'difficulte'\s*:\s(?P<difficulty>\d),\n'score'\s*:\s(?P<score>\d*),\s\n}\);.*")
        js_challenges = js_pattern.findall(raw_js)

        if js_challenges is not None:
            return js_challenges
        else:
            return None

    def get_parsed_challenge(self, js):
        """
        Return challenges stats
        @param self: Object himself
        @type value: Object
        @param js: js string
        @type value: string

        @return: Dictionnary with stats (name challenge, category of challenge, url challenge, difficulty challenge, score for this difficulty when flagged, flag date)
        @rtype: dictionnary
        """
        regex_parse_challenge = "evolution_data(?P<difficulty>\d*)\.push\(new\WArray\(\"(?P<datetime>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\",(?P<score_difficulty>\d*), \"(?P<challenge_name>[\w\W]*)\", \"(?P<challenge_url>[\w\W]*)\"\)\);"

        parse_challenge = re.match(regex_parse_challenge, str(js))

        if parse_challenge is not None:
            parse_challenge_category = self.get_category_name(str(parse_challenge.group('challenge_url')))
            solved_datetime = datetime.strptime(parse_challenge.group('datetime'), "%Y-%m-%d %H:%M:%S")
            parse_challenge = {'name': parse_challenge.group('challenge_name'), 'category': parse_challenge_category.group('challenge_category'), 'url': 'https://www.root-me.org/' + parse_challenge.group('challenge_url'), 'difficulty': self.get_difficulty_challenge(int(parse_challenge.group('difficulty'))), 'total_score_difficulty': int(parse_challenge.group('score_difficulty')), 'datetime': solved_datetime}

            return parse_challenge
        else:
            return None

    def get_difficulty_challenge(self, difficulty_number):
        """
        Convert difficulty number in difficulty string
        @param self: Object himself
        @type value: Object
        @param difficulty_number: difficulty
        @type value: integer

        @return: Difficulty name
        @rtype: string
        """
        if difficulty_number == 1:
            return 'very easy'
        elif difficulty_number == 2:
            return 'easy'
        elif difficulty_number == 3:
            return 'medium'
        elif difficulty_number == 4:
            return 'hard'
        elif difficulty_number == 36:
            return 'very hard'
        else:
            return None

    def get_category_name(self, category):
        """
        Return the name of the category in a URL
        @param self: Object himself
        @type value: Object
        @param category: URL of the category
        @type value: string

        @return: Category name
        @rtype: string
        """
        regex_get_category = "fr\/Challenges\/(?P<challenge_category>[\w\W]*)\/[\w\W]*"
        parsed_category = re.match(regex_get_category, category)

        if parsed_category is not None:
            return parsed_category.group('challenge_category')
        else:
            return None
