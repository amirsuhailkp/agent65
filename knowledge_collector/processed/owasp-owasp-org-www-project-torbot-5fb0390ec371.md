---
title: OWASP TorBot
source: owasp.org
url: https://owasp.org/www-project-torbot/
collector: owasp
category: web-security
tags:
- web-security
- torbot
- completed
- new
- feature
date_collected: '2026-07-26T12:46:04.832467Z'
language: unknown
---

# OWASP TorBot
```
                     ████████╗ ██████╗ ██████╗     ██████╗  ██████╗ ████████╗
                     ╚══██╔══╝██╔═══██╗██╔══██╗    ██╔══██╗██╔═████╗╚══██╔══╝
                        ██║   ██║   ██║██████╔╝    ██████╔╝██║██╔██║   ██║
                        ██║   ██║   ██║██╔══██╗    ██╔══██╗████╔╝██║   ██║
                        ██║   ╚██████╔╝██║  ██║    ██████╔╝╚██████╔╝   ██║
                        ╚═╝    ╚═════╝ ╚═╝  ╚═╝    ╚═════╝  ╚═════╝    ╚═╝
        
                        Open Source Intelligence Tool for the Dark Web
```

## Working Procedure/Basic Plan

The basic procedure executed by the web crawling algorithm takes a list of seed URLs as its input and repeatedly executes
the following steps:
```
URLs = input(url)
while(URLs is not empty) do
    dequeue url
    request page
    parse for Links
    for(link in Links) do 
        if (link islive && link is not visited) then 
            add link to URLs
    store page content
```

</code>

### Features

- Onion Crawler (.onion).(Completed)
- Returns Page title and address with a short description about the site.(Partially Completed)
- Save links to database.(PR to be reviewed)
- Get emails from site.(Completed)
- Save crawl info to JSON file.(Completed)
- Crawl custom domains.(Completed)
- Check if the link is live.(Completed)
- Built-in Updater.(Completed)
- TorBot GUI (In progress)
- Social Media integration.(not Started) …(will be updated)

## Contribute

Contributions to this project are always welcome.
To add a new feature fork the dev branch and give a pull request when your new feature is tested and complete.
If its a new module, it should be put inside the modules directory.
The branch name should be your new feature name in the format <Feature\_featurename\_version(optional)>. For example, *Feature\_FasterCrawl\_1.0*.
Contributor name will be updated to the below list. 😀

 **NOTE : The PR should be made only to dev branch of TorBot.**

### OS Dependencies

- Tor
- Python 3.x
- Golang 1.x (Not Currently Used)

### Python Dependencies

- beautifulsoup4
- pyinstaller
- PySocks
- termcolor
- requests
- requests\_mock
- yattag

## Basic setup

Before you run the torBot make sure the following things are done properly:

- Run tor service
  ```
  sudo service tor start
  ```
- Make sure that your torrc is configured to SOCKS\_PORT localhost:9050
- Install TorBot Python requirements
  ```
  pip3 install -r requirements.txt
  ```

On Linux platforms, you can make an executable for TorBot by using the install.sh script.
You will need to give the script the correct permissions using
```
chmod +x install.sh
```

Now you can run
```
./install.sh
```

to create the torBot binary.
Run
```
./torBot
```

to execute the program.

An alternative way of running torBot is shown below, along with help instructions.
```
python3 torBot.py or use the -h/--help argument
```
```
usage: torBot.py [-h] [-v] [--update] [-q] [-u URL] [-s] [-m] [-e EXTENSION]
                 [-l] [-i]

optional arguments:
  -h, --help            Show this help message and exit
  -v, --version         Show current version of TorBot.
  --update              Update TorBot to the latest stable version
  -q, --quiet           Prevent header from displaying
  -u URL, --url URL     Specifiy a website link to crawl, currently returns links on that page
  -s, --save            Save results to a file in json format
  -m, --mail            Get e-mail addresses from the crawled sites
  -e EXTENSION, --extension EXTENSION
                        Specifiy additional website extensions to the
                        list(.com or .org etc)
  -l, --live            Check if websites are live or not (slow)
  -i, --info            Info displays basic info of the scanned site (very
                        slow)`
```

- NOTE: All flags under -u URL, –url URL must also be passed a -u flag.

Read more about torrc here : [Torrc](https://github.com/DedSecInside/TorBoT/blob/master/Tor.md)

#### Using the GUI

#### Using Docker

- Ensure than you have a tor container running on port 9050.
- Build the image using following command:
  ```
  docker build -t dedsecinside/torbot .
  ```
- Run the container (make sure to link the tor container as
  ```
  tor
  ```

  ):
  ```
  docker run --link tor:tor --rm -ti dedsecinside/torbot
  ```

### Have ideas?

If you have new ideas which is worth implementing, mention those by starting a new issue with the title [FEATURE\_REQUEST]. If the idea is worth implementing, congratz, you are now a contributor.

### Cite this [paper](https://link.springer.com/chapter/10.1007/978-981-15-0146-3_19)
```
```
@InProceedings{10.1007/978-981-15-0146-3_19,
author="Narayanan, P. S.
and Ani, R.
and King, Akeem T. L.",
editor="Ranganathan, G.
and Chen, Joy
and Rocha, {\'A}lvaro",
title="TorBot: Open Source Intelligence Tool for Dark Web",
booktitle="Inventive Communication and Computational Technologies",
year="2020",
publisher="Springer Singapore",
address="Singapore",
pages="187--195",
abstract="The dark web has turned into a dominant source of illegal activities. With several volunteered networks, it is      becoming more difficult to track down these services. Open source intelligence (OSINT) is a technique used to gather intelligence on targets by harvesting publicly available data. Performing OSINT on the Tor network makes it a challenge for both researchers and developers because of the complexity and anonymity of the network. This paper presents a tool which shows OSINT in the dark web. With the use of this tool, researchers and Law Enforcement Agencies can automate their task of crawling and identifying different services in the Tor network. This tool has several features which can help extract different intelligence.",
isbn="978-981-15-0146-3"
}```
```

### References
```
```
1.  M. Glassman and M. J. Kang, “Intelligence in the internet age: The emergence and evolution of Open Source Intelligence (OSINT),” Comput. Human Behav., vol. 28, no. 2, pp. 673–682, 2012.
2.  D. Bradbury, “In plain view: open source intelligence,” Comput. Fraud Secur., vol. 2011, no. 4, pp. 5–9, 2011.
3.  B. Butler, B. Wardman, and N. Pratt, “REAPER: an automated, scalable solution for mass credential harvesting and OSINT,” 2016 APWG Symp. Electron. Crime Res., pp. 1–10, 2016.
4.  B. Zantout and R. A. Haraty, “I2P Data Communication System I2P Data Communication System,” no. April 2002, 2014.
5.  J. Qin, Y. Zhou, G. Lai, E. Reid, M. Sageman, and H. Chen, “The dark web portal project: collecting and analyzing the presence of terrorist groups on the web,” in Proceedings of the 2005 IEEE international conference on Intelligence and Security Informatics, 2005, pp. 623–624.
6.  D. Moore, T. Rid, D. Moore, and T. Rid, “Cryptopolitik and the Darknet Cryptopolitik and the Darknet,” vol. 6338, 2016.
7.  G. Weimann, “Going dark: Terrorism on the dark Web,” Stud. Confl. Terror., vol. 39, no. 3, pp. 195–206, 2016.
8.  A. T. Zulkarnine, R. Frank, B. Monk, J. Mitchell, and G. Davies, “Surfacing collaborated networks in dark web to find illicit and criminal content,” in Intelligence and Security Informatics (ISI), 2016 IEEE Conference on, 2016, pp. 109–114.
9.  T. Minárik and A.-M. Osula, “Tor does not stink: Use and abuse of the Tor anonymity network from the perspective of law,” Comput. Law Secur. Rev., vol. 32, no. 1, pp. 111–127, 2016.
10. K. Loesing, S. J. Murdoch, and R. Dingledine, “A Case Study on Measuring Statistical Data in the {T}or Anonymity Network,” in Proceedings of the Workshop on Ethics in Computer Security Research (WECSR 2010), 2010.
11. B. Nafziger, “Data Mining in the Dark : Darknet Intelligence Automation,” 2017.
12. I. Sanchez-Rola, D. Balzarotti, and I. Santos, “The onions have eyes: A comprehensive structure and privacy analysis of tor hidden services,” in Proceedings of the 26th International Conference on World Wide Web, 2017, pp. 1251–1260.
13. Mouli VR, Jevitha KP. “Web Services Attacks and Security-A Systematic Literature Review.”, Procedia Computer Science. 2016 Jan 1;93:870-7.
14. Cova M, Felmetsger V, Vigna G. "Vulnerability analysis of web-based applications. InTest and Analysis of Web Services" 2007 (pp. 363-394). Springer, Berlin, Heidelberg.
15. B. R. Holland, “Enabling Open Source Intelligence (OSINT) in private social networks,” 2012.
16. S. Nakamoto, “Bitcoin: A Peer-to-Peer Electronic Cash System,” Cryptogr. Mail. List https//metzdowd.com, 2009.
17. M. Wesam, A. Nabki, E. Fidalgo, E. Alegre, and I. De Paz, “Classifying Illegal Activities on Tor Network Based on Web Textual Contents”, vol. 1, pp. 35–43, 2017.
18. Sathyadevan S, Gangadharan S.“Crime analysis and prediction using data mining”. In Networks & Soft Computing (ICNSC), 2014 First International Conference on 2014 Aug 19 (pp. 406-412). IEEE.
19. Chau M, Chen H. "A machine learning approach to web page filtering using content and structure analysis. Decision Support Systems." 2008 Jan 1;44(2):482-94.
20. Ani R, Jose J, Wilson M, Deepa OS. “Modified Rotation Forest Ensemble Classifier for Medical Diagnosis in Decision Support Systems”, In Progress in Advanced Computing and Intelligent Engineering 2018 (pp. 137-146). Springer, Singapore.
21. Ani R, Augustine A, Akhil N.C. and Deepa O.S., 2016. “Random Forest Ensemble Classifier to Predict the Coronary Heart Disease Using Risk Factors”, In Proceedings of the International Conference on Soft Computing Systems (pp. 701-710). Springer, New Delhi.```
```

## License

GNU Public License

## Example

Put whatever you like here: news, screenshots, features, supporters, or remove this file and don’t use tabs at all.
