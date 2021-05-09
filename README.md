# check-that-links-are-cached.py

A small python script that parse a html page for all a tags href attribute and check the http headers response for each href attribute value i.e url that starts with http 

## Usage

python check-that-links-are-cached.py -u https://github.com/plwebse/

## Will output something like this:

    Checking headers ['cache-control', 'via', 'x-cache'] for all urls in html @ url:https://github.com/plwebse/ 1 times
    https://github.com/plwebse?tab=stars	200	max-age=0, private, must-revalidate
    https://github.com/security	200	max-age=0, private, must-revalidate
    https://github.com	200	max-age=0, private, must-revalidate
    https://stars.github.com	200	max-age=600	1.1 varnish	HIT
## Options
    -u url  
    -t nr of times to check each url 
    -h list of headers to look for
