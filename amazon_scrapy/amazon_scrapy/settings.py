# -*- coding: utf-8 -*-

# Scrapy settings for amazon_scrapy project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'amazon_scrapy'

SPIDER_MODULES = ['amazon_scrapy.spiders']
NEWSPIDER_MODULE = 'amazon_scrapy.spiders'

ITEM_PIPELINES = {'amazon_scrapy.pipelines.ValidateItemPipeline': 100,
					'amazon_scrapy.pipelines.WriteItemPipeline': 50}

# Retry many times since proxies often fail
RETRY_TIMES = 10
# Retry on most error codes since proxies fail for different reasons
RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408]

DOWNLOADER_MIDDLEWARES = {
    #'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110, # keep this for ProxyMiddleware
    #'amazon_scrapy.middlewares.ProxyMiddleware': 100,  # keep this for ProxyMiddleware
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
    'scrapy_proxies.RandomProxy': 100,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
}

# Proxy list containing entries like
# http://host1:port
# http://username:password@host2:port
# http://host3:port
# https://quentinpicard:5Kxbqqek@173.246.165.0:60099
# ...
PROXY_LIST = './amazon_scrapy/proxy_list.txt'

# Proxy mode
# 0 = Every requests have different proxy
# 1 = Take only one proxy from the list and assign it to every requests
# 2 = Put a custom proxy to use in the settings
PROXY_MODE = 0

# If proxy mode is 2 uncomment this sentence :
#CUSTOM_PROXY = "http://host1:port"


#Template
# PROXIES = [{'ip_port': '168.63.249.35:80', 'user_pass': ''},
#            {'ip_port': '162.17.98.242:8888', 'user_pass': ''},
#            {'ip_port': '177.55.64.38:8080', 'user_pass': ''},]


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'amazon_scrapy (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.5


# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 8
CONCURRENT_REQUESTS_PER_IP = 0

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

#Maximum number of concurrent items (per response) to process in parallel in the Item Processor (default: 100)
CONCURRENT_ITEMS = 200

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                           'accept-encoding': 'gzip, deflate, sdch',
                           'accept-language': 'en-US,en;q=0.8',
                           'upgrade-insecure-requests': '1',
                           'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3'}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'amazon_scrapy.middlewares.AmazonScrapySpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'amazon_scrapy.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# DEPTH_PRIORITY - a negative value will increase priority, i.e., higher depth requests will be processed sooner (DFO)
DEPTH_PRIORITY = -1

# DEPTH_STATS
DEPTH_STATS = True  # Default: True
# If this is enabled, the number of requests for each depth is collected in the stats.
DEPTH_STATS_VERBOSE = True # Default: False


# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'amazon_scrapy.pipelines.AmazonScrapyPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
