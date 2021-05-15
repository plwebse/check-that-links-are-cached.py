# check-that-links-are-cached.py

A small python script that parse a html page for all a tags href attribute and check the http headers response for each href attribute value i.e url that starts with http

## Basic usage

python check-that-links-are-cached.py -u https://github.com/plwebse/

### Will output something like this:

    Checking headers ['cache-control', 'via', 'x-cache'] for all urls in html @ url:https://github.com/plwebse/ 1 time(s) parsing href values True
    url     code    cache-control   via     x-cache
    https://docs.github.com/articles/why-are-my-contributions-not-showing-up-on-my-profile  200     private, no-store       1.1 vegur, 1.1 varnish  MISS
    https://support.github.com      200     max-age=0, private, must-revalidate
    https://education.github.com    200     max-age=0, private, must-revalidate
    https://github.com/plwebse?tab=stars    200     max-age=0, private, must-revalidate

## Options

    -u http://url no defualt value
    -t nr of times to check each url (default value 1)
    -h list of headers to look for default values (['cache-control', 'via', 'x-cache'])
    -p true or false (defualt value true)
    or
    --url= http://url no defualt value
    --times= nr of times to check each url (default value 1)
    --http-headers= list of headers to look for default values ('cache-control', 'via', 'x-cache')
    --p=true true or false (defualt value true)
