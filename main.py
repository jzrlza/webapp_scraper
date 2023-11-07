#import yaml
import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi_utils.session import FastAPISessionMaker
from fastapi_utils.tasks import repeat_every
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
import re

def distinctStringSet(list_string) :
	auxiliaryList = []
	for word in list_string:
		if word not in auxiliaryList:
			auxiliaryList.append(word)
	return auxiliaryList

def modifyMainDictArrayByPrice(main_arr, price, field_edit, field_value) :
	for i in range(len(main_arr)) :
		dict_member = main_arr[i]
		#print(dict_member, field_edit, field_value)
		if dict_member["Price per Month"] == price :
			main_arr[i][field_edit] = field_value
			break

app = FastAPI()

#config_file = "config.yaml"
#sql_file = "test.sqlite"

#if os.path.exists(config_file):
#    with open(config_file, "r", encoding="utf-8") as f:
        #config = yaml.safe_load(f)
#else:
#    print("Configuration file not found; using default configuration")
#    config = {}
#app.include_router(info.router)
#app.include_router(form.router)

@app.on_event("startup")
def on_startup():
	print("App is starting up.")


    #initialize_databases(sql_file, config)


@app.post("/scrape_web")
#@repeat_every(seconds=30) #works
async def scrape_web(request: Request):
	qr = await request.json()
	keyword = qr['keyword']#.decode('utf8', 'replace')
	input_url = qr['input_url']#.decode('utf8', 'replace')
	file_output_name = qr['file_output_name']#.decode('utf8', 'replace')
	mode = qr['mode']

	timeout = 5

	driver = webdriver.Chrome()
	driver.implicitly_wait(timeout)

	url = input_url

	#nov_2023 --> https://web.archive.org/web/20231106043121/https://www.dtac.co.th/postpaid/products/package.html

	driver.get(url)

	target_string = keyword

	web_contents = driver.find_elements(By.XPATH,"//*[text()[contains(., '"+target_string+"')]]")

	list_of_rows = []
	field_names = []

	if mode == 0 : #DTAC if get()
		field_names = ['Price per Month'] 

		#phase 1
		for i in range(len(web_contents)) :
			try :
				baht_group_elem = web_contents[i].find_element(By.XPATH, "..")
				#print(baht_group_elem.get_attribute('class'))

				if not baht_group_elem.get_attribute('class') == "packPro" :
					continue

				raw_txt = baht_group_elem.find_elements(By.XPATH, '*')[0].get_attribute('innerHTML')

				pattern = r'\d{1,3}(?:,\d{3})*(?:\.\d+)?'

				matches = re.findall(pattern, raw_txt)

				numbers = [float(match.replace(',', '')) for match in matches]

				row_dict = {
					'Price per Month' : numbers[0]
				}

				mega_parent_elem = baht_group_elem.find_element(By.XPATH, "..").find_element(By.XPATH, "..")
				details_elem = mega_parent_elem.find_elements(By.XPATH, '*')[1].find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')[0]
				details_elems = details_elem.find_elements(By.XPATH, '*')

				for i in range(len(details_elems)) :
					details_elem_i = details_elems[i]
					#print(details_elem_i.get_attribute('class'))
					the_strings = details_elem_i.get_attribute('innerHTML').replace('<br>', ' ').strip().split("</i>")[1].split('<span class="fBetterMed">')[1].split('</span>')
					#print(the_strings)
					if len(the_strings) == 2 :
						field_name = " "
						if the_strings[1] != "" :
							field_name = the_strings[1].strip()
						else :
							if "รับสิทธิ์" in the_strings[0] :
								field_name = "DTAC Reward"
							else :
								continue
						field_names.append(field_name)
						row_dict[field_name] = the_strings[0].strip()	
				#print(row_dict)
				list_of_rows.append(row_dict)

			except Exception as e:
				print(e)

		#phase 2, table time
		try :
			tables = driver.find_elements(By.XPATH, '//table')
			table_content = None
			for i in range(len(tables)) :
				if "responsive" in tables[0].find_element(By.XPATH, "..").get_attribute('class') :
					table_content = tables[0]
					break
			#print(table_content.get_attribute('class'))
			hunt_keyword_1 = "คุ้มครอง"
			hunt_keyword_1_field = "ประกันชีวิตและอุบัติเหตุ"
			hunt_keyword_2 = "ความบันเทิงซีรีย์ดัง"
			hunt_keyword_2_field = "ความบันเทิงซีรีย์ดัง"
			hunt_keyword_2_1 = "แอปดัง"
			hunt_keyword_2_1_field = "ความบันเทิง 3 แอปดัง"
			hunt_keyword_2_2 = "พรีเมียร์ลีก"
			hunt_keyword_2_2_field = "ความบันเทิงพรีเมียร์ลีก"

			bodies_elem = table_content.find_elements(By.XPATH, '*')[1]
			bodies_arr = bodies_elem.find_elements(By.XPATH, '*')
			row_span_1 = 0
			row_span_info_1 = ""
			row_span_2 = 0
			row_span_info_2 = ""
			row_span_info_2_1 = ""
			row_span_info_2_2 = ""
			for tr_i in range(len(bodies_arr)) :
				trow = bodies_arr[tr_i]
				trows_tds = trow.find_elements(By.XPATH, '*')
				trow_price = 0.0
				for td_i in range(len(trows_tds)) :
					td_elem = trows_tds[td_i]
					td_elem_txt = td_elem.get_attribute('innerHTML').strip()
					if td_i == 0 : #price
						if "แนะนำ" in td_elem_txt :
							trow_price = float(td_elem.find_elements(By.XPATH, '*')[1].get_attribute('innerHTML').strip())
							field_names.append("แนะนำหรือไม่")
							modifyMainDictArrayByPrice(list_of_rows, trow_price, "แนะนำหรือไม่", "แนะนำ")
						else :
							trow_price = float(td_elem.find_elements(By.XPATH, '*')[0].get_attribute('innerHTML').strip())
					elif hunt_keyword_1 in td_elem_txt :
						row_span_1 = td_elem.get_attribute('rowspan')
						if td_elem.get_attribute('rowspan') == None :
							row_span_1 = 1
						else :
							row_span_1 = int(row_span_1)
						print("fetching info 1... maximum "+str(timeout)+" seconds")
						row_span_info_1 = td_elem.find_elements(By.XPATH,"descendant::*[text()[contains(., '"+hunt_keyword_1+"')]]")
						if row_span_info_1 != None :
							if len(row_span_info_1) > 0 :
								row_span_info_1 = row_span_info_1[0].get_attribute('innerHTML').strip().split('<small>')[0].replace('<br>', '')
						
					elif hunt_keyword_2 in td_elem_txt :
						row_span_2 = td_elem.get_attribute('rowspan')
						if td_elem.get_attribute('rowspan') == None :
							row_span_2 = 1
						else :
							row_span_2 = int(row_span_2)
						print("fetching info 2... maximum "+str(timeout)+" seconds")
						row_span_info_2 = td_elem.find_elements(By.XPATH,"descendant::*[text()[contains(., '"+hunt_keyword_2+"')]]")
						print("fetching info 2_1... maximum "+str(timeout)+" seconds")
						row_span_info_2_1 = td_elem.find_elements(By.XPATH,"descendant::*[text()[contains(., '"+hunt_keyword_2_1+"')]]")
						print("fetching info 2_2... maximum "+str(timeout)+" seconds")
						row_span_info_2_2 = td_elem.find_elements(By.XPATH,"descendant::*[text()[contains(., '"+hunt_keyword_2_2+"')]]")
						if row_span_info_2 != None :
							if len(row_span_info_2) > 0 :
								row_span_info_2 = row_span_info_2[0].get_attribute('innerHTML').strip().split('<small>')[0].replace('<br>', '')
						
						if row_span_info_2_1 != None :
							if len(row_span_info_2_1) > 0 :
								row_span_info_2_1 = row_span_info_2_1[0].get_attribute('innerHTML').strip().split('<small>')[0].replace('<br>', '')

						if row_span_info_2_2 != None :
							if len(row_span_info_2_2) > 0 :
								row_span_info_2_2 = row_span_info_2_2[0].get_attribute('innerHTML').strip().split('<small>')[0].replace('<br>', '')

				if row_span_1 > 0 :
					#print(row_span_info_1)
					field_names.append(hunt_keyword_1_field)
					modifyMainDictArrayByPrice(list_of_rows, trow_price, hunt_keyword_1_field, row_span_info_1)
					row_span_1 -= 1
				if row_span_2 > 0 :
					#print(row_span_info_2)
					if row_span_info_2 != None :
						field_names.append(hunt_keyword_2_field)
						modifyMainDictArrayByPrice(list_of_rows, trow_price, hunt_keyword_2_field, row_span_info_2)
					#print(row_span_info_2_1)
					if row_span_info_2_1 != None :
						field_names.append(hunt_keyword_2_1_field)
						modifyMainDictArrayByPrice(list_of_rows, trow_price, hunt_keyword_2_1_field, row_span_info_2_1)
					#print(row_span_info_2_2)
					if row_span_info_2_2 != None :
						field_names.append(hunt_keyword_2_2_field)
						modifyMainDictArrayByPrice(list_of_rows, trow_price, hunt_keyword_2_2_field, row_span_info_2_2)
					row_span_2 -= 1

		except Exception as e:
			print(e)

	elif mode == 1: #True
		field_names = ['Price per Month'] 

		for i in range(len(web_contents)) :
			try :
				baht_elem = web_contents[i]

				if not "price-unit" in baht_elem.get_attribute('class') :
					continue

				per_month_check = web_contents[i].find_elements(By.XPATH, '*')[0]

				big_elem = baht_elem.find_element(By.XPATH, "..")
				num_price_elem = big_elem.find_elements(By.XPATH, '*')[0]
				
				#print(num_price_elem.get_attribute('class'))

				raw_txt = num_price_elem.get_attribute('innerHTML')

				#print(raw_txt)

				pattern = r'\d{1,3}(?:,\d{3})*(?:\.\d+)?'

				matches = re.findall(pattern, raw_txt)

				numbers = [float(match.replace(',', '')) for match in matches]
				#print(numbers)

				row_dict = {
					'Price per Month' : numbers[0]
				}

				#print(row_dict)

				#BIG ROOT
				root_parent_elem = big_elem.find_element(By.XPATH, "..").find_element(By.XPATH, "..")
				#print(root_parent_elem.get_attribute('class')) for test

				secondary_info_elem = root_parent_elem.find_elements(By.XPATH, '*')[1]
				secondary_info_elems = secondary_info_elem.find_elements(By.XPATH, '*')
				for i in range(len(secondary_info_elems)) :
					secondary_info_elem_set = secondary_info_elems[i]
					secondary_info_elem_set_title = secondary_info_elem_set.find_elements(By.XPATH, '*')[0]
					raw_header_title = secondary_info_elem_set_title.get_attribute('innerHTML').split('<')[0]
					field_names.append(raw_header_title)
					#print(raw_header_title)
					secondary_info_elem_set_info = secondary_info_elem_set.find_elements(By.XPATH, '*')[1].find_elements(By.XPATH, '*')
					raw_info = ""
					for i in range(len(secondary_info_elem_set_info)) :
						elem_raw = secondary_info_elem_set_info[i].get_attribute('innerHTML')
						raw_info += elem_raw.replace(',', '')
					#print(raw_info)
					row_dict[raw_header_title] = raw_info

				wifi_info_elem = root_parent_elem.find_elements(By.XPATH, '*')[3]
				HD_info_elem = root_parent_elem.find_elements(By.XPATH, '*')[4]
				bottom_info_elem = root_parent_elem.find_elements(By.XPATH, '*')[5]
				bottom_info_elems = bottom_info_elem.find_elements(By.XPATH, '*')[1].find_elements(By.XPATH, '*')
				for i in range(len(bottom_info_elems)) :
					bottom_info_elem_set = bottom_info_elems[i]
					#print(bottom_info_elem_set.get_attribute('class'))
					iterator_for_elem = bottom_info_elem_set.find_elements(By.XPATH, '*')

					for i in range(len(iterator_for_elem)) :
						elem_raw = iterator_for_elem[i].get_attribute('innerHTML')
						if "<img" in elem_raw:
							continue
						elem_title = ""
						if "card" in elem_raw :
							elem_title = "Card"
						elif "ฟุตบอล" in elem_raw :
							elem_title = "Football"
						elif "โค้ดความบันเทิง" in elem_raw :
							elem_title = "Entertain Code"
						elif "ประกัน" in elem_raw :
							elem_title = "Insurance"
						elif "ซีรีย์ดัง" in elem_raw :
							elem_title = "Popular Series"
						else :
							elem_title = "Null Title"
						field_names.append(elem_title)
						row_dict[elem_title] = elem_raw

				list_of_rows.append(row_dict)

			except Exception as e:
				print(e)

	elif mode == 2: #AIS
		field_names = ['Package Name', 'Price per Month'] 

		for i in range(len(web_contents)) :
			try :
				big_elem = web_contents[i].find_element(By.XPATH, "..").find_element(By.XPATH, "..").find_element(By.XPATH, "..").find_element(By.XPATH, "..").find_element(By.XPATH, "..")
				raw_txt = big_elem.get_attribute('innerHTML')

				if raw_txt.find('ต่อเดือน') < 0 :
					continue

				desiredSubstringTitle = "cmp-package-card-info-title"
				title_elem = big_elem.find_elements(By.CSS_SELECTOR, f".{desiredSubstringTitle}")[0].find_elements(By.XPATH, '*')[0]
				raw_title = title_elem.get_attribute('innerHTML')

				#print(raw_txt)

				pattern = r'\d{1,3}(?:,\d{3})*(?:\.\d+)?'

				matches = re.findall(pattern, raw_txt)

				numbers = [float(match.replace(',', '')) for match in matches]
				#print(numbers)

				target_number = None
				target_index = raw_txt.find(target_string)
				for i, match in enumerate(matches):
					match_index = raw_txt.find(match)
					#print(match_index, target_index, match)
					if match_index >= 0 and match_index == target_index - (len(match)+1):
						target_number = numbers[i]
						break

				row_dict = {
					'Package Name' : raw_title,
					'Price per Month' : target_number
				}


				info_elem = big_elem.find_elements(By.XPATH, '*')[2].find_elements(By.XPATH, '*')[0].find_elements(By.XPATH, '*')[0]

				#print(info_elem.get_attribute('class'))

				info_elem_list = info_elem.find_elements(By.XPATH, '*')
				for i in range(len(info_elem_list)) :
					elems = info_elem_list[i].find_elements(By.XPATH, '*')
					if len(elems) >= 2 :
						elem = elems[1]
						#print(elem.get_attribute('class'))
						elem_rows = elem.find_elements(By.XPATH, '*')
						key_name = ""
						for i in range(len(elem_rows)) :
							the_inner_text = elem_rows[i].get_attribute('innerHTML')
							print(the_inner_text)
							if '<a class="cmp-package-card-details-lnk"></a>' in the_inner_text :
								continue
							if i == 0 :
								key_name = the_inner_text.strip()
								field_names.append(key_name)
								row_dict[key_name] = ""
							else :
								row_dict[key_name] += the_inner_text.strip() + " "

				#print(row_dict)
				list_of_rows.append(row_dict)
			except Exception as e:
				print(e)
	#print(list_of_rows)

	field_names = distinctStringSet(field_names)
	psudo_fields = {}

	for i in range(len(field_names)) :
		psudo_fields[field_names[i]] = " "

	with open(file_output_name, 'w', encoding='UTF8', newline='') as f:
	    writer = csv.writer(f)

	    writer = csv.DictWriter(f, fieldnames = psudo_fields.keys())
	    writer.writeheader()
	    for i in range(len(list_of_rows)) :
	    	writer.writerow(list_of_rows[i])

	return {"result" : list_of_rows}

    #session = database.get_session()
    #image_task = await task.get_next_task(current_user.email, image_id, session=session)
    #if image_task is not None:
    #    return await get_image_internal(session, image_task)
    #else:
    #    image_task = await task.get_task(current_user.email, image_id, session=session)
    #    return_data = await create_new_task(session, current_user, image_task["provider_id"], preferred_width, preferred_height)

    # await session.close()
    #return return_data

app.mount("/", StaticFiles(directory="web"), name="web")
