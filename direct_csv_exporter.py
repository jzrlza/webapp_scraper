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
         "url_link":"https://www.ais.th/consumers/package/exclusive-plan/sim-netmarathon-max",
         "operator_id":0,
         "track_new_mega_row": false,
         "plans":[
            {
               "plan_name":"แพ็กเกจเสริม เน็ตมาราธอน แมกซ์",
               "capture_sub_names": false,
               "capture_mode":1,
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
