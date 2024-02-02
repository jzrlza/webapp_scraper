import web_scraper_prepaid
import web_scraper_postpaid
import web_scraper_boardband
import csv

request = """{
   "price_keywords":[
      "บาท",
      ".-",
      "Baht",
      "THB",
      "฿"
   ],
   "sub_price_keywords":[
      "สต.",
      "สตางค์"
   ],
   "service_type": 1,
   "predefined_g_no": "5G",
   "predefined_g_no_if_free": "4G",
   "urls":[
      {
         "url_link":"https://www.dtac.co.th/prepaid/simdtac.html",
         "operator_id":1,
         "track_new_mega_row": false,
         "plans":[
            {
               "plan_name":"ซิมเติมเงินดีแทค",
               "capture_sub_names": true,
               "capture_mode":0,
               "has_extra_table":false,
               "has_term_and_condition":false
            },
            {
               "plan_name":"ซิมดีแทคเติมเงินอื่น",
               "capture_sub_names": true,
               "capture_mode":1,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ]
      },
      {
         "url_link":"https://www.true.th/truemoveh/prepaid/",
         "operator_id":2,
         "track_new_mega_row": false,
         "plans":[
            {
               "plan_name":"ซิมเติมเงิน",
               "capture_sub_names": true,
               "capture_mode":0,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ]
      }
   ],
   "webdriver_timeout":15
}"""

raw_result = web_scraper_prepaid.scrape_web(request, normalize_result=True, raw_list_result=True)
print(raw_result)

with open('output_test.csv', 'w', newline='', encoding="utf-8") as file:
	writer = csv.writer(file)

	writer.writerow(raw_result[0].keys())

	for row in raw_result :
		writer.writerow(row.values())
