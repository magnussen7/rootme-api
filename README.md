# Root-me API

A python script which creates an API for https://www.root-me.org

## List of endpoints

You need to use the username from the profile url.  
Exemple :  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;https://www.root-me.org/Magnussen?lang=fr

### API info : /
Example :
```
> curl 127.0.0.1:7777
{
	"Created by":"Magnussen",
	"Team":"funcMyLife()"
}
```
### User info : /*username*
Example :
```
> curl 127.0.0.1:7777/Magnussen
{
	"info":
	{
		"achievements":
		[
			{"title":"Web developer Rookie : a valid\u00e9 50% des challenges de type web-client"},
			{"title":"Steganograph Rookie : a valid\u00e9 50% des challenges de type st\u00e9ganographie"},
			{"title":"Web Admin Rookie : a valid\u00e9 50% des challenges de type web-serveur"},
			{"title":"Net Admin Newbie : a valid\u00e9 25% des challenges de type r\u00e9seau"},
			{"title":"Sys Admin Newbie : a valid\u00e9 25% des challenges de type app-script"},
			{"title":"Forensic Newbie : a valid\u00e9 25% des challenges de type forensic"}
		],
		"bio":"<p>CTF player | Member of funcMyLife()</p>",
		"chatbox":0,
		"ctf_solved":5,
		"lang":"fr",
		"logo":"https://www.root-me.org/local/cache-vignettes/L96xH96/auton89823-eb677.jpg
		,
		"post":0,
		"rank":737,
		"score":
		{
			"category":
			[
				{"name":"Web - Client","progression":"73%"},
				{"name":"Programmation","progression":"46%"},
				{"name":"Cryptanalyse","progression":"33%"},
				{"name":"St\u00e9ganographie","progression":"52%"},
				{"name":"Web - Serveur","progression":"100%"},
				{"name":"Cracking","progression":"22%"},
				{"name":"R\u00e9aliste","progression":"48%"},
				{"name":"R\u00e9seau","progression":"50%"},
				{"name":"App - Script","progression":"56%"},
				{"name":"App - Syst\u00e8me","progression":"8%"},
				{"name":"Forensic","progression":"40%"}
			],
			"last_10_flags":
			[
				{"category":"Realiste","name":"IPBX - call me maybe"},
				{"category":"CTF All the day","name":"VulnVoIP"},
				{"category":"Programmation","name":"Quick Response Code"},
				{"category":"App-Script","name":"Python - PyJail 2"},
				{"category":"Web-Serveur","name":"Insecure Code Management"},
				{"category":"Forensic","name":"Exfiltration DNS"},
				{"category":"Web-Serveur","name":"JSON Web Token (JWT) - Secret faible"},
				{"category":"Web-Serveur","name":"JSON Web Token (JWT) - Cl\u00e9 publique"},
				{"category":"Web-Serveur","name":"JSON Web Token (JWT) - Introduction"},
				{"category":"Web-Client","name":"XSS - Stock\u00e9e 2"}
			],
			"solved_challenges":165,
			"total_challenges":356,
			"total_progression":"46%"
		},
		"solved_challenges":165,
		"status":"Visiteur",
		"website":"https://www.magnussen.funcmylife.fr"}
}
```

### User info : /*username*/challenges
Example :
```
> curl 127.0.0.1:7777/Magnussen/challenges
{
	"challenges":
	{
		"challenges_info":
		{
			"challenges_solved":149
			,"challenges_total":341,
			"rank":851,
			"score":3570,
			"rank_total"143595,
			"rank_title":"lamer"
		},
		"username":"Magnussen",
		"challenges_by_category":
		[{
			"name":"App - Script",
			"score":135,
			"description":"Cette s\u00e9rie d'\u00e9preuve vous confronte aux vuln\u00e9rabilit\u00e9s li\u00e9es \u00e0 des faiblesses d'environnement, de configuration ou encore \u00e0 des erreurs de d\u00e9veloppement dans des langages de script ou de programmation."
			"url":"https://www.root-me.org/fr/Challenges/App-Script/",
			"solved_challenges":8,
			"challenges":
			[{
				"challenge_name":"Bash - System 1",
				"challenge_score":5,
				"challenge_validation":true,
				"challenge_url":"https://www.root-me.org/fr/Challenges/App-Script/ELF32-System-1"
			},
			{
				"challenge_name":"sudo - faiblesse de configuration",
				"challenge_score":5,
				"challenge_validation":true,
				"challenge_url":"https://www.root-me.org/fr/Challenges/App-Script/sudo-faiblesse-de-configuration"
			},
			.
			.
			.
		}],
			.
			.
			.
	}
}
```

### User info : /*username*/ctf
Example :
```
> curl 127.0.0.1:7777/Magnussen/ctf
{
	"ctf_all_the_day":
	{
		"username":"Magnussen",
		"solved":4,
		"ctf_total_attempts":28,
		"ctf_total":50,
		"ctf":
		[{
			"name":"/dev/random\u00a0: Pipe",
			"solved":false,
			"attempts":0,
			"success":0,
			"best_time":null
		},
		{
			"name":"/dev/random\u00a0: Relativity",
			"solved":false,
			"attempts":0,
			"success":0,
			"best_time":null
		},
			.			.
			.
			.
		]
	}
}
```

### User info : /*username*/stats
Example :
```
> curl 127.0.0.1:7777/Magnussen/stats
{
	"stats":
	{
		"username":"Magnussen",
		"score_by_difficulty":
		{
			"very easy":180,
			"easy":490,
			"medium":2385,
			"hard":515,
			"very hard":0
		},
		"score_total":3570,
		"challenges":
		[{
			"name":"Encodage - ASCII",
			"category":"Cryptanalyse",
			"url":"https://www.root-me.org/fr/Challenges/Cryptanalyse/Encodage-ASCII",
			"difficulty":"very easy",
			"total_score_difficulty":5,
			"datetime":"Fri, 24 Mar 2017 16:53:02 GMT"
		},
		{
			"name":"Javascript - Authentification",
			"category":"Web-Client",
			"url":"https://www.root-me.org/fr/Challenges/Web-Client/Javascript-Authentification",
			"difficulty":"very easy",
			"total_score_difficulty":10,
			"datetime":"Sun, 02 Apr 2017 17:06:56 GMT"
		},
			.
			.
			.
		]
	}
}
```

## Installing

First you have to clone this repo :
```
git clone https://github.com/magnussen7/rootme-api.git
```
Then you can create a virtualenv and install the mandatory packages.
```
cd rootme-api/
pip install -r requirements.txt
```

You can now run the api with :
```
python3.6 api.py
```
If you want to use the API in production you should run it with Nginx, all WSGI files are available in this repository.

Nginx configurations example :
```
> cat /etc/nginx/sites-available/api_rootme.com.conf
server {
    listen 80;
    server_name api_rootme.com www.api_rootme.com;

    location / {
        include uwsgi_params;
        uwsgi_pass unix:/path/to/api/folder/api_rootme.sock;
    }
}
> sudo ln -s /etc/nginx/sites-available/api_rootme.com.conf /etc/nginx/sites-enabled
> sudo service nginx restart
```
Don't forget to change the server name and the path to the socket.
Of course it's highly recommended to set a certificate.

### Help for Flask server in production
* https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04

## Authors

* **Magnussen**
