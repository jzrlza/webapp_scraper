let input__keyword = document.getElementById("input__keyword")
//let input__url = document.getElementById("input__url")
//let input__csv_file = document.getElementById("input__csv_file")
//let input__mode = document.getElementById("input__mode")
let button__scrape = document.getElementById("button__scrape")

button__scrape.onclick = function() {
	//console.log(input__keyword.value)

	let urls = []

	let url_obj = {
		url_link: "", //str
		operator_id: 0, //enum, ais = 0, dtac = 1, true = 2
		plans: [], // plan_obj[]
	}

	let plan_obj = {
		plan_name: "", //str
		capture_mode: 0, //enum, 0 = card, 1 = ul list, 2, numerical capture
		has_term_and_condition: false, //bool
	}

	let planned_inputs = [
		{
			url_link: "https://www.ais.th/consumers/package/exclusive-plan/5g-max-professionals", //str
			operator_id: 0, //enum, ais = 0, dtac = 1, true = 2
			plans: [
				{
					plan_name: "5G Max Professionals​", //str
					capture_mode: 0, //enum, 0 = card, 1 = ul list, 2, numerical capture
					has_term_and_condition: false, //bool
				},
			], // plan_obj[]
		},
		{
			url_link: "https://www.ais.th/consumers/package/exclusive-plan/5g-max-experience", //str
			operator_id: 0, //enum, ais = 0, dtac = 1, true = 2
			plans: [
				{
					plan_name: "AIS 5G Max Experience", //str
					capture_mode: 0, //enum, 0 = card, 1 = ul list, 2, numerical capture
					has_term_and_condition: false, //bool
				},
			], // plan_obj[]
		},
		{
			url_link: "https://www.ais.th/consumers/package/postpaid/postpaid-plans", //str
			operator_id: 0, //enum, ais = 0, dtac = 1, true = 2
			plans: [
				{
					plan_name: "แพ็กเกจมหามงคล", //str
					capture_mode: 1, //enum, 0 = card, 1 = ul list, 2, numerical capture
					has_term_and_condition: false, //bool
				},
				{
					plan_name: "5G Serenade", //str
					capture_mode: 1, //enum, 0 = card, 1 = ul list, 2, numerical capture
					has_term_and_condition: false, //bool
				},
				{
					plan_name: "Online MAX", //str
					capture_mode: 1, //enum, 0 = card, 1 = ul list, 2, numerical capture
					has_term_and_condition: false, //bool
				},
				{
					plan_name: "Other", //str
					capture_mode: 1, //enum, 0 = card, 1 = ul list, 2, numerical capture
					has_term_and_condition: false, //bool
				},
			], // plan_obj[]
		},
		/*
		{
			url_link: "https://www.dtac.co.th/postpaid/products/package.html", //str
			operator_id: 1, //enum, ais = 0, dtac = 1, true = 2
			plans: [
				{
					plan_name: "dtac 5G Better+", //str
					capture_mode: 0, //enum, 0 = card, 1 = ul list, 2, numerical capture
					has_term_and_condition: false, //bool
				},
			], // plan_obj[]
		},
		{
			url_link: "https://www.dtac.co.th/postpaid/products/net.html", //str
			operator_id: 1, //enum, ais = 0, dtac = 1, true = 2
			plans: [
				{
					plan_name: "dtac 5G Better+", //str
					capture_mode: 1, //enum, 0 = card, 1 = ul list, 2, numerical capture
					has_term_and_condition: false, //bool
				},
			], // plan_obj[]
		},
		{
			url_link: "https://web.archive.org/web/20230322124658/https://www.true.th/truemoveh/postpaid/mass", //str
			operator_id: 2, //enum, ais = 0, dtac = 1, true = 2
			plans: [
				{
					plan_name: "5G Together+", //str
					capture_mode: 0, //enum, 0 = card, 1 = ul list, 2, numerical capture
					has_term_and_condition: false, //bool
				},
				{
					plan_name: "5G Net Ultra Max Speed", //str
					capture_mode: 0, //enum, 0 = card, 1 = ul list, 2, numerical capture
					has_term_and_condition: false, //bool
				},
			], // plan_obj[]
		},*/

	]

	let query = {
		price_keywords: ["บาท", ".-", "Baht", "THB", "฿"],
		urls: planned_inputs,
		webdriver_timeout: 5,
	}
	//'?&keyword='+input__keyword.value+'&input_url='+input__url.value+'&file_output_name='+input__csv_file.value+'&mode='+input__mode.value

	fetch('scrape_web',{
		  method: "POST",
		  headers: {
		      "Content-Type": "application/json",
		      // 'Content-Type': 'application/x-www-form-urlencoded',
		    },
		  body: JSON.stringify(query)
		})
   .then(response => response.json())
   .then(json => {
   	console.log(json)
   }).catch(e => {
   	console.error(e)
   })
}