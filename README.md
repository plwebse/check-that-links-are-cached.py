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



url code    cache-control   via x-cache
https://www.ticket.fi/index 200 max-age=600, no-cache="Set-Cookie", must-revalidate     1.1 8583d317c3b0492356857e1a1a67d192.cloudfront.net (CloudFront)       Miss from cloudfront
https://www.facebook.com/ticketresor    200     private, no-cache, no-store, must-revalidate
https://www.ticket.dk/index     200     max-age=600, no-cache="Set-Cookie", must-revalidate     1.1 4bdc4e02725e6de1af31e5bb25800f69.cloudfront.net (CloudFront)       Miss from cloudfront
https://www.ticket.se/blogg     200     no-store, no-cache, must-revalidate     1.1 6528f10684ec39317f94ed2a540d88b4.cloudfront.net (CloudFront)        Miss from cloudfront
https://www.ticket.no/index     200     max-age=600, no-cache="Set-Cookie", must-revalidate     1.1 d6561aeeccb210202cf78b99f07c5235.cloudfront.net (CloudFront)       Miss from cloudfront