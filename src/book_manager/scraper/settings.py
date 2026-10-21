"""Configuración del scraper de Cúspide."""

BOT_NAME = "cuspide_scraper"

SPIDER_MODULES = ["book_manager.scraper.spiders"]
NEWSPIDER_MODULE = "book_manager.scraper.spiders"

ROBOTSTXT_OBEY = True
CONCURRENT_REQUESTS = 4
DOWNLOAD_DELAY = 1.0
USER_AGENT = "Mozilla/5.0 (compatible; BookCatalogScraper/1.0)"

ITEM_PIPELINES = {
    "book_manager.scraper.pipelines.CuspidePipeline": 300,
}

FEED_EXPORT_ENCODING = "utf-8"
