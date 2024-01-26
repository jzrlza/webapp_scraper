import web_scraper_boardband

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
   "service_type": 3,
   "predefined_g_no": "5G",
   "predefined_g_no_if_free": "4G",
   "urls":[
      {
         "url_link":"https://www.ais.th/consumers/fibre/package",
         "operator_id":0,
         "track_new_mega_row": false,
         "collect_sub_urls": true,
         "urls_class_type_id": 0,
         "plans":[],
         "plans_template": {
             "plan_name":"",
             "capture_sub_names": false,
             "capture_mode":0,
             "has_extra_table":false,
             "has_term_and_condition":false
         },
         "special_case_plans": []
      },
      {
         "url_link":"https://www.ais.th/consumers/fibre",
         "operator_id":0,
         "track_new_mega_row": false,
         "collect_sub_urls": true,
         "urls_class_type_id": 1,
         "plans":[],
         "plans_template": {
             "plan_name":"",
             "capture_sub_names": false,
             "capture_mode":0,
             "has_extra_table":false,
             "has_term_and_condition":false
         },
         "special_case_plans": [
            {
                "plan_name":"Smart AI Gamer",
                "sub_url": "https://www.ais.th/consumers/fibre/package/smart-ai-gamer/",
                "capture_sub_names": false,
                "capture_mode":1,
                "has_extra_table":true,
                "has_term_and_condition":false
            }
         ]
      }
   ],
   "webdriver_timeout":15
}"""

print(web_scraper_boardband.scrape_web(request, normalize_result=True, raw_list_result=False))