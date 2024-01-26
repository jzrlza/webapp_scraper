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
         "url_link":"https://www.dtac.co.th/postpaid/products/package.html",
         "operator_id":1,
         "track_new_mega_row": false,
         "plans":[
            {
               "plan_name":"dtac 5G Better+",
               "capture_mode":0,
               "has_extra_table":true,
               "has_term_and_condition":false
            }
         ]
      },
      {
         "url_link":"https://www.dtac.co.th/dtac-go-plus",
         "operator_id":1,
         "track_new_mega_row": false,
         "plans":[
            {
               "plan_name":"dtac GO+",
               "capture_mode":0,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ]
      },
      {
         "url_link":"https://www.dtac.co.th/postpaid/products/net.html",
         "operator_id":1,
         "track_new_mega_row": false,
         "plans":[
            {
               "plan_name":"Tablet Net Non-Stop",
               "capture_mode":1,
               "has_extra_table":false,
               "has_term_and_condition":true
            },
            {
               "plan_name":"SMP Entry 240",
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