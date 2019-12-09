#!/usr/bin/python3.6
# coding: utf-8
from rootme_class.scrapper import scrapper
from flask import Flask, redirect, jsonify

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route('/', methods=['GET'])
def home():
	"""
	Root page

	@return: Creator and creator Team
	@rtype: json
	"""
	presentation = {
						"Creator": {
							"Created by": "Magnussen",
							"Root-Me Profile": "https://www.root-me.org/Magnussen",
							"Personal Website": "https://www.magnussen.funcmylife.fr",
							"Github Profile": "https://github.com/magnussen7",
							"Gitlab Profile": "https://gitlab.com/magnussen7",
							"Twitter Profile": "https://twitter.com/_magnussen_"
						},
						"Team": {
							"Team": "funcMyLife()",
							"Team Website": "https://www.funcmylife.fr",
							"Github Profile": "https://github.com/funcMyLife",
							"Gitlab Profile": "https://gitlab.com/funcmylife"
						}
					}

	return jsonify(presentation)

@app.route('/<username>', methods=['GET'])
def info(username):
	"""
	User info
	@param username: Get info for this username
	@type value: string

	@return: User's info (username, lang, status, total score, number of posts, number of message in Chatbox, website and biography)
	@rtype: json
	"""
	username = scrapper(username)
	return jsonify(username.extract_info())

@app.route('/<username>/challenges', methods=['GET'])
def challenges(username):
	"""
	User solved challenges
	@param username: Get solved challenges for this username
	@type value: string

	@return: User's solved challenges : username, challenges_info(score, number of solved challenges, number of challenges, rank, rank total, rank name), challenges_by_category(category name, category description, category url, score in category, number of solved challenges in category, total of challenges in category), challenges in category(name challenge, points of challenge, challenge flag by user, url challenge)
	@rtype: json
	"""
	username = scrapper(username)
	return jsonify(username.extract_challenges())

@app.route('/<username>/ctf', methods=['GET'])
def ctf(username):
	"""
	User solved challenges
	@param username: Get solved ctf for this username
	@type value: string

	@return: User's solved ctf : username, number of solved ctf, number of attempts, number of ctf, ctf(name of ctf, solved by user, number of attempts, number of success, best time of success)
	@rtype: json
	"""
	username = scrapper(username)
	return jsonify(username.extract_ctf())

@app.route('/<username>/stats', methods=['GET'])
def stats(username):
	"""
	User stats
	@param username: Get stats for this username
	@type value: string

	@return: User's stats : username, score for each difficulty, score total, list of solved challenges (name challenge, category of challenge, url challenge, difficulty challenge, score for this difficulty when flagged, flag date) order from oldest to latest
	@rtype: json
	"""
	username = scrapper(username)
	return jsonify(username.extract_stats())

if __name__ == "__main__":
	app.run(host='127.0.0.1', port='7777', threaded=True)
