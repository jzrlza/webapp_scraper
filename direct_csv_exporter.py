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
   "service_type": 2,
   "predefined_g_no": "5G",
   "predefined_g_no_if_free": "4G",
   "urls":[
      {
         "url_link":"https://www.ais.th/consumers/fibre/package/home-fibre-lan",
         "operator_id":0,
         "track_new_mega_row": false,
         "collect_sub_urls": false,
         "urls_class_type_id": 0,
         "plans":[
            {
               "plan_name":"Home Fibre Lan",
               "capture_sub_names": false,
               "capture_mode":0,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ],
         "special_case_plans": []
      },
      {
         "url_link":"https://www.ais.th/consumers/fibre/package/smart-ai-gamer/",
         "operator_id":0,
         "track_new_mega_row": false,
         "collect_sub_urls": false,
         "urls_class_type_id": 0,
         "plans":[
            {
               "plan_name":"Smart AI Gamer",
               "capture_sub_names": false,
               "capture_mode":1,
               "has_extra_table":true,
               "has_term_and_condition":false
            }
         ],
         "special_case_plans": []
      },
      {
         "url_link":"https://www.ais.th/consumers/fibre/package/power4-welcome",
         "operator_id":0,
         "track_new_mega_row": false,
         "collect_sub_urls": false,
         "urls_class_type_id": 0,
         "plans":[
            {
               "plan_name":"Power4 Welcome",
               "capture_sub_names": false,
               "capture_mode":0,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ],
         "special_case_plans": []
      },
      {
         "url_link":"https://www.ais.th/consumers/fibre/package/2gbps",
         "operator_id":0,
         "track_new_mega_row": false,
         "collect_sub_urls": false,
         "urls_class_type_id": 0,
         "plans":[
            {
               "plan_name":"2Gbps Fibre",
               "capture_sub_names": false,
               "capture_mode":0,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ],
         "special_case_plans": []
      },
      {
         "url_link":"https://olmd.azurewebsites.net/consumers/fibre/package_supermeshplus_hbo.html",
         "operator_id":0,
         "track_new_mega_row": false,
         "collect_sub_urls": false,
         "urls_class_type_id": 0,
         "plans":[
            {
               "plan_name":"Super Mesh Plus",
               "capture_sub_names": false,
               "capture_mode":-999,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ],
         "special_case_plans": []
      },
      {
         "url_link":"https://www.ais.th/consumers/fibre/package/netflix-lover",
         "operator_id":0,
         "track_new_mega_row": false,
         "collect_sub_urls": false,
         "urls_class_type_id": 0,
         "plans":[
            {
               "plan_name":"Netflix Lover",
               "capture_sub_names": false,
               "capture_mode":0,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ],
         "special_case_plans": []
      },
      {
         "url_link":"https://www.ais.th/consumers/fibre/package/serenade",
         "operator_id":0,
         "track_new_mega_row": false,
         "collect_sub_urls": false,
         "urls_class_type_id": 0,
         "plans":[
            {
               "plan_name":"Serenade",
               "capture_sub_names": false,
               "capture_mode":0,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ],
         "special_case_plans": []
      },
      {
         "url_link":"https://www.ais.th/consumers/fibre/package/byod",
         "operator_id":0,
         "track_new_mega_row": false,
         "collect_sub_urls": false,
         "urls_class_type_id": 0,
         "plans":[
            {
               "plan_name":"BYOD",
               "capture_sub_names": false,
               "capture_mode":0,
               "has_extra_table":false,
               "has_term_and_condition":false
            }
         ],
         "special_case_plans": []
      },
      {
         "url_link":"https://www.ais.th/consumers/fibre/package/broadband24",
         "operator_id":0,
         "track_new_mega_row": false,
         "collect_sub_urls": false,
         "urls_class_type_id": 0,
         "plans":[
            {
               "plan_name":"Broadband24",
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

raw_result = web_scraper_boardband.scrape_web(request, normalize_result=True, raw_list_result=True)
print(raw_result)

with open('output_test.csv', 'w', newline='', encoding="utf-8") as file:
	writer = csv.writer(file)

	writer.writerow(raw_result[0].keys())

	for row in raw_result :
		writer.writerow(row.values())
