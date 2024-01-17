import boardband_ais
import web_scraper_boardband

input_request = boardband_ais.request

raw_result_string = web_scraper_boardband.scrape_web(input_request, normalize_result=True, raw_list_result=True)