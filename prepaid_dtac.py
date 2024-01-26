import web_scraper_prepaid

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
      }
   ],
   "webdriver_timeout":15
}"""

print(web_scraper_prepaid.scrape_web(request, normalize_result=True, raw_list_result=False))