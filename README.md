# Root-me API

Python script wich create an API for https://www.root-me.org

### List of endpoints

You need to use the username from the profile url.  
Exemple :  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;https://www.root-me.org/Magnussen?lang=fr

#### API info : /
Example :
```
> curl 127.0.0.1:7777
{
	"Created by":"Magnussen",
	"Team":"funcMyLife()"
}
```
#### User info : /*username*
Example :
```
> curl 127.0.0.1:7777/Magnussen
{
	"info":
	{
		"username":"Magnussen",
		"lang":"fr",
		"status":"Visiteur",
		"score":3570,
		"post":0,
		"chatbox":0,
		"website":null,
		"bio":"<p>CTF player | Member of funcMyLife()</p>"
	}
}
```

#### User info : /*username*/challenges
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

#### User info : /*username*/ctf
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

#### User info : /*username*/stats
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

### Installing

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
