import web_scraper_postpaid

request = """{
   "price_keywords":[
      "บาท",
      ".-",
      "Baht",
      "THB",
      "฿"
   ],
   "service_type": 2,
   "urls":[
   	{
         "url_link":"https://www.ais.th/consumers/package/exclusive-plan/5g-max-professionals",
         "operator_id":0,
         "track_new_mega_row": false,
         "plans":[
            {
               "plan_name":"5G Max Professionals",
               "capture_mode":0,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ]
      },
      {
         "url_link":"https://www.ais.th/consumers/package/exclusive-plan/5g-max-experience",
         "operator_id":0,
         "track_new_mega_row": false,
         "plans":[
            {
               "plan_name":"AIS 5G Max Experience",
               "capture_mode":0,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ]
      },
      {
         "url_link":"https://www.ais.th/consumers/package/postpaid/postpaid-plans",
         "operator_id":0,
         "track_new_mega_row": false,
         "plans":[
            {
               "plan_name":"แพ็กเกจมหามงคล",
               "capture_mode":1,
               "has_extra_table":false,
               "has_term_and_condition":false
            },
            {
               "plan_name":"5G Serenade",
               "capture_mode":1,
               "has_extra_table":false,
               "has_term_and_condition":false
            },
            {
               "plan_name":"Online MAX",
               "capture_mode":1,
               "has_extra_table":false,
               "has_term_and_condition":false
            },
            {
               "plan_name":"Other",
               "capture_mode":1,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ]
      },
      {
         "url_link":"https://www.ais.th/consumers/package/exclusive-plan/5g-netflix",
         "operator_id":0,
         "track_new_mega_row": false,
         "plans":[
            {
               "plan_name":"แพ็กเกจ 5G Netflix",
               "capture_mode":0,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ]
      },
      {
         "url_link":"https://www.ais.th/consumers/package/exclusive-plan/5g-smart-share",
         "operator_id":0,
         "track_new_mega_row": false,
         "plans":[
            {
               "plan_name":"แพ็กเกจ 5G SMART SHARE",
               "capture_mode":0,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ]
      },
      {
         "url_link":"https://www.ais.th/consumers/package/exclusive-plan/zeed-5g/5g-postpaid",
         "operator_id":0,
         "track_new_mega_row": false,
         "plans":[
            {
               "plan_name":"แพ็กเกจ AIS ZEED 5G รายเดือน",
               "capture_mode":0,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ]
      },
      {
         "url_link":"https://www.ais.th/consumers/package/postpaid/3bb-welcome",
         "operator_id":0,
         "track_new_mega_row": false,
         "plans":[
            {
               "plan_name":"3BB Welcome Package",
               "capture_mode":0,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ]
      },
      {
         "url_link":"https://www.ais.th/en/consumers/package/postpaid/postpaid-plans/vai-5g-rsme-tungngern-399-20gb-ul-swifi",
         "operator_id":0,
         "track_new_mega_row": false,
         "plans":[
            {
               "plan_name":"AIS 5G TungNgern",
               "capture_mode":2,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ]
      },
      {
         "url_link":"https://www.ais.th/en/consumers/package/postpaid/postpaid-plans/vai-5g-rsme-tungngern-499-30gb-ul-swifi",
         "operator_id":0,
         "track_new_mega_row": false,
         "plans":[
            {
               "plan_name":"AIS 5G TungNgern",
               "capture_mode":2,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ]
      },
      {
         "url_link":"https://www.ais.th/en/consumers/package/postpaid/postpaid-plans/5g_rsme_seller_699b_45gb",
         "operator_id":0,
         "track_new_mega_row": false,
         "plans":[
            {
               "plan_name":"AIS 5G Seller",
               "capture_mode":2,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ]
      },
      {
         "url_link":"https://www.ais.th/en/consumers/package/postpaid/postpaid-plans/5g_rsme_seller_899b_80gb",
         "operator_id":0,
         "track_new_mega_row": false,
         "plans":[
            {
               "plan_name":"AIS 5G Seller",
               "capture_mode":2,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ]
      },
      {
         "url_link":"https://www.ais.th/en/consumers/package/postpaid/postpaid-plans/5g_rsme_seller_1299b_400Min",
         "operator_id":0,
         "track_new_mega_row": false,
         "plans":[
            {
               "plan_name":"AIS 5G Seller",
               "capture_mode":2,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ]
      },
      {
         "url_link":"https://www.ais.th/en/consumers/package/postpaid/postpaid-plans/vai-5g-rsme-tiktok-699-50gb6mbpsul-swifi",
         "operator_id":0,
         "track_new_mega_row": false,
         "plans":[
            {
               "plan_name":"AIS 5G TikTok Shop",
               "capture_mode":2,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ]
      },
      {
         "url_link":"https://www.ais.th/en/consumers/package/postpaid/postpaid-plans/vai-5g-rsme-tiktok-899-70gb6mbpsul-swifi",
         "operator_id":0,
         "track_new_mega_row": false,
         "plans":[
            {
               "plan_name":"AIS 5G TikTok Shop",
               "capture_mode":2,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ]
      },
      {
         "url_link":"https://www.ais.th/en/consumers/package/postpaid/postpaid-plans/5g-rsme-tiktokshop-1199b-netul-swifi",
         "operator_id":0,
         "track_new_mega_row": false,
         "plans":[
            {
               "plan_name":"AIS 5G TikTok Shop",
               "capture_mode":2,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ]
      }
   ],
   "webdriver_timeout":15
}"""

print(web_scraper_postpaid.scrape_web(request, normalize_result=True, raw_list_result=False))