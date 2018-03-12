# -*- coding: utf-8 -*-

BOT_NAME = 'Dajie_Scrapy'

SPIDER_MODULES = ['Dajie_Scrapy.spiders']
NEWSPIDER_MODULE = 'Dajie_Scrapy.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Referer的Urlencode变量
REFERER_NAME = "大数据"

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# 大街网COOKIE
DAJIE_COOKIE = ""

# MONGODB配置
MONGODB_HOST = "localhost"
MONGODB_PORT = 27017
MONGODB_USER = ""
MONGODB_PASS = ""
MONGODB_DB_NAME = "fwwb"
MONGODB_COL_NAME = "DaJie"

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1

# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Enable or disable spider middlewares
# SPIDER_MIDDLEWARES = {
#    'Dajie_Scrapy.middlewares.DajieScrapySpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'Dajie_Scrapy.middlewares.DaJieScrapyUserAgentMiddleware': 400,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
ITEM_PIPELINES = {
   'Dajie_Scrapy.pipelines.DajieScrapyPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
