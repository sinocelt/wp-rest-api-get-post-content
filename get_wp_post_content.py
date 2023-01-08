# This Python file accompanies a YouTube video
# How To Get The Text Content Of A WordPress Blog Post With The WP REST API
# https://www.youtube.com/watch?v=ZBD8jCgs8pw

import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse

# STEP 1. Get the id of the post. You can do that by viewing the HTML code and copying it, or getting it with Python

# by default, all WP installs have WP Rest API code like the following:
# <link rel="https://api.w.org/" href="https://techcrunch.com/wp-json/" /><link rel="alternate" type="application/json" 
# href="https://techcrunch.com/wp-json/wp/v2/posts/2466432" /><link rel="EditURI" type="application/rsd+xml" title="RSD" 
# href="https://techcrunch.com/xmlrpc.php?rsd" />

# first find https://api.w.org/
# then find post number

# just be concerned with
# <link rel="https://api.w.org/" href="https://techcrunch.com/wp-json/" /><link rel="alternate" type="application/json" 
# href="https://techcrunch.com/wp-json/wp/v2/posts/2466432" 

# note the following function won't work on every possible case in WordPress (especially if the site is using a heavily modified themed),
# but it works on a lot.
def get_wp_post_num(orig_url):
    # get the HTML code of the page
    wp_article_text = requests.get(orig_url).text

    # extact the text starting at api.w.org and ending at the post number
    # make sure it is non-greedy
    try: 
        cur_match = re.search(r'https://api\.w\.org.*?wp-json\/wp\/v2\/posts\/[0-9]+', wp_article_text).group()
        # now delete everything up to wp-json/wp/v2/posts/
        post_id = re.sub(r"^.*wp-json\/wp\/v2\/posts\/", "", cur_match)

    except:
        return "Sorry the regex broke. You'll either need to manually find the post id, or change the regex in this function."

    # we'll keep the post id as a string instead of an integer because we will concatenate late
# much of code is based off code from the following article
    return post_id



# EDIT THE main_url with whichever WordPress-based URL you want.

main_url = "https://techcrunch.com/2023/01/07/ai-guided/"
# main_url = 'https://blog.ted.com/dare-to-discover-tedinarabic-hosts-third-regional-event-in-ben-guerir-morocco/'
# main_url = 'https://www.sonymusic.com/sonymusic/rachel-chernoff-appointed-to-senior-vice-president-of-data-science-and-analytics/'
# main_url = 'https://blog.playstation.com/2023/01/04/introducing-project-leonardo-for-playstation-5-a-highly-customizable-accessibility-controller-kit/'

# cases where regex needs to be modified to get the post id
# main_url = 'https://time.com/6245246/spare-royal-memoir-history/'
# https://api.time.com/wp-admin/post.php?post&#x3D;6245246&amp;action&#x3D;edit"

# main_url = 'https://news.microsoft.com/europe/features/as-the-world-goes-digital-datacenters-that-make-the-cloud-work-look-to-renewable-energy-sources/'
# p=90619' />

article_id_num = get_wp_post_num(main_url)
print(article_id_num)

# article_id_num = '90619'
wp_api_url_part = 'wp-json/wp/v2/posts/'
parts = urlparse(main_url)
domain_part = parts.scheme + "://" + parts.netloc + "/"
wp_url_for_api = domain_part + wp_api_url_part + article_id_num
print(wp_url_for_api)

entry = requests.get(wp_url_for_api).json()
print('the keys of the article for which you can get data are', list(entry.keys()))

# entry_date = entry['date_gmt']
entry_date = entry['date']
entry_title = entry['title']['rendered']
entry_content = entry['content']['rendered']
entry_text = BeautifulSoup(entry_content).get_text()

# much of code is based off code from the following article
# https://samantha-delfin.medium.com/wordpress-blog-scraping-with-beautifulsoup-916a22a46869
