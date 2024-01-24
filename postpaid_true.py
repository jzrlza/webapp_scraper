import web_scraper_postpaid

request = """{
   "price_keywords":[
      "บาท",
      ".-",
      "Baht",
      "THB",
      "฿"
   ],
   "urls":[
      {
         "url_link":"https://www.true.th/truemoveh/postpaid/mass",
         "operator_id":2,
         "pricing_type":1,
         "track_new_mega_row": true,
         "plans":[
            {
               "plan_name":"5G Super Asian",
               "capture_mode":0,
               "has_extra_table":false,
               "has_term_and_condition":false
            },
            {
               "plan_name":"5G Super sport",
               "capture_mode":0,
               "has_extra_table":false,
               "has_term_and_condition":false
            },
            {
               "plan_name":"5G Together+",
               "capture_mode":0,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ]
      }
   ],
   "webdriver_timeout":15
}"""

print(web_scraper_postpaid.scrape_web(request, normalize_result=True, raw_list_result=False))