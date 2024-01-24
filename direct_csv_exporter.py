import postpaid_true
import web_scraper_postpaid
#import web_scraper_prepaid
#import web_scraper_boardband

input_request = postpaid_true.request

raw_result = web_scraper_postpaid.scrape_web(input_request, normalize_result=True, raw_list_result=True)

for row in raw_result :
	print(row)