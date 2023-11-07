let input__keyword = document.getElementById("input__keyword")
let input__url = document.getElementById("input__url")
let input__csv_file = document.getElementById("input__csv_file")
let input__mode = document.getElementById("input__mode")
let button__scrape = document.getElementById("button__scrape")

button__scrape.onclick = function() {
	//console.log(input__keyword.value)

	let query = {
		keyword: input__keyword.value,
		input_url: input__url.value,
		file_output_name: input__csv_file.value,
		mode: parseInt(input__mode.value),
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