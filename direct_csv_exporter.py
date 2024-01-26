import web_scraper_prepaid
import web_scraper_postpaid
import web_scraper_boardband

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

raw_result = web_scraper_postpaid.scrape_web(request, normalize_result=True, raw_list_result=True)

for row in raw_result :
	print(row)