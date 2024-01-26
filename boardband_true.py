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
   "service_type": 2,
   "predefined_g_no": "5G",
   "predefined_g_no_if_free": "4G",
   "urls":[
      {
         "url_link":"https://www.true.th/trueonline/package-types/true-fiber-to-room",
         "operator_id":2,
         "track_new_mega_row": false,
         "collect_sub_urls": false,
         "urls_class_type_id": 0,
         "plans":[
            {
               "plan_name":"True Fiber To Room",
               "capture_sub_names": false,
               "capture_mode":0,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ],
         "special_case_plans": []
      },
      {
         "url_link":"https://www.true.th/trueonline/package-types/true-gigatex-pro-special-ssv/",
         "operator_id":2,
         "pricing_type":2,
         "track_new_mega_row": false,
         "collect_sub_urls": false,
         "urls_class_type_id": 0,
         "plans":[
            {
               "plan_name":"True Gigatex PRO Special",
               "capture_sub_names": false,
               "capture_mode":0,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ],
         "special_case_plans": []
      },
      {
         "url_link":"https://www.true.th/trueonline/package-types/true-gigatex-pro",
         "operator_id":2,
         "pricing_type":2,
         "track_new_mega_row": false,
         "collect_sub_urls": false,
         "urls_class_type_id": 0,
         "plans":[
            {
               "plan_name":"True Gigatex PRO",
               "capture_sub_names": false,
               "capture_mode":0,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ],
         "special_case_plans": []
      },
      {
         "url_link":"https://www.true.th/trueonline/package-types/true-gigatex-pro-security",
         "operator_id":2,
         "pricing_type":2,
         "track_new_mega_row": false,
         "collect_sub_urls": false,
         "urls_class_type_id": 0,
         "plans":[
            {
               "plan_name":"True Gigatex PRO Security",
               "capture_sub_names": false,
               "capture_mode":0,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ],
         "special_case_plans": []
      },
      {
         "url_link":"https://www.true.th/trueonline/package-types/true-gigatex-pro-gold/",
         "operator_id":2,
         "pricing_type":2,
         "track_new_mega_row": false,
         "collect_sub_urls": false,
         "urls_class_type_id": 0,
         "plans":[
            {
               "plan_name":"True Gigatex PRO Gold",
               "capture_sub_names": false,
               "capture_mode":0,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ],
         "special_case_plans": []
      },
      {
         "url_link":"https://www.true.th/trueonline/package-types/true-gigatex-pro-cyod/",
         "operator_id":2,
         "pricing_type":2,
         "track_new_mega_row": false,
         "collect_sub_urls": false,
         "urls_class_type_id": 0,
         "plans":[
            {
               "plan_name":"True Gigatex PRO CYOD",
               "capture_sub_names": false,
               "capture_mode":0,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ],
         "special_case_plans": []
      },
      {
         "url_link":"https://www.true.th/trueonline/package-types/true-gigatex-pro-gamer/",
         "operator_id":2,
         "pricing_type":2,
         "track_new_mega_row": false,
         "collect_sub_urls": false,
         "urls_class_type_id": 0,
         "plans":[
            {
               "plan_name":"True Gigatex PRO Gamer",
               "capture_sub_names": false,
               "capture_mode":0,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ],
         "special_case_plans": []
      },
      {
         "url_link":"https://www.true.th/en/trueonline/package-types/true-gigatex-pro-sme/",
         "operator_id":2,
         "pricing_type":2,
         "track_new_mega_row": false,
         "collect_sub_urls": false,
         "urls_class_type_id": 0,
         "plans":[
            {
               "plan_name":"True Gigatex PRO SME",
               "capture_sub_names": false,
               "capture_mode":0,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ],
         "special_case_plans": []
      }
   ],
   "webdriver_timeout":15
}"""

print(web_scraper_boardband.scrape_web(request, normalize_result=True, raw_list_result=False))