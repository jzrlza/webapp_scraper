test_rows = [
	[
		{
			"value": "399",
			"row_span": 1
		},
		{
			"value": "20 GB",
			"row_span": 1
		},
		{
			"value": "100 นาที",
			"row_span": 1
		},
		{
			"value": "ไม่จำกัด",
			"row_span": 20
		},
		{
			"value": "ความคุ้มครองสูงสุด 220,000 บ.",
			"row_span": 2
		},
		{
			"value": "รับชมความบันเทิงซีรีย์ดัง",
			"row_span": 1
		},
		{
			"value": "Welcome Member",
			"row_span": 2
		}
	],
	[
		{
			"value": "499",
			"row_span": 1
		},
		{
			"value": "40 GB",
			"row_span": 1
		},
		{
			"value": "250 นาที",
			"row_span": 1
		},
		{
			"value": "ดูฟรี 3 แอปดัง + รับชมความบันเทิงซีรีย์ดัง",
			"row_span": 4
		}
	],
	[
		{
			"value": "599",
			"row_span": 1
		},
		{
			"value": "50 GB",
			"row_span": 1
		},
		{
			"value": "250 นาที",
			"row_span": 1
		},
		{
			"value": "ความคุ้มครองสูงสุด 320,000 บ.",
			"row_span": 8
		},
		{
			"value": "Silver Member",
			"row_span": 3
		}
	],
	[
		{
			"value": "699",
			"row_span": 1
		},
		{
			"value": "60 GB",
			"row_span": 1
		},
		{
			"value": "300 นาที",
			"row_span": 1
		}
	],
	[
		{
			"value": "899",
			"row_span": 1
		},
		{
			"value": "80 GB",
			"row_span": 1
		},
		{
			"value": "300 นาที",
			"row_span": 1
		}
	],
	[
		{
			"value": "1199",
			"row_span": 1
		},
		{
			"value": "ไม่จำกัด",
			"row_span": 5
		},
		{
			"value": "350 นาที",
			"row_span": 1
		},
		{
			"value": "รับชมบอลพรีเมียร์ลีก + ดูฟรี 3 แอปดัง + รับชมความบันเทิงซีรีย์ดัง",
			"row_span": 5
		},
		{
			"value": "Gold Member",
			"row_span": 2
		}
	],
	[
		{
			"value": "1499",
			"row_span": 1
		},
		{
			"value": "650 นาที",
			"row_span": 1
		}
	],
	[
		{
			"value": "1699",
			"row_span": 1
		},
		{
			"value": "1000 นาที",
			"row_span": 1
		},
		{
			"value": "Platinum Member",
			"row_span": 3
		}
	],
	[
		{
			"value": "1999",
			"row_span": 1
		},
		{
			"value": "1300 นาที",
			"row_span": 1
		}
	],
	[
		{
			"value": "2199",
			"row_span": 1
		},
		{
			"value": "1700 นาที",
			"row_span": 1
		}
	]
]

final_rows = []
column_rowspan_states = {}
column_rowspan_value_states = {}
column_rowspan_bool_is_span_states = {}
max_columns = 9999

print("<<<Test rowspan table reading algorithm>>>")

print("""
States storage uses 3 dict objects to fetch by indices easily
(These are accessed using 'column id + id offset' value)
-Rowspan num states
-Cell values states according to previous rowspans
-Boolean states to tell to fetch from previous rowspans or not

"To do with states and values" meanings (only if row_id > 0):

Lock On => "Rowspan num states" value of previous was = 1 && 'column id' < 'total length of in-html columns', actions :
1. update "Rowspan num states" of given 'column id + id offset' index
2. update "Cell values states" of given 'column id + id offset' index
3. Insert value into row data
 3.1 If "Boolean states" of old un-updated 'column id + id offset' index is True, then insert the previous value
   3.1.1 If that value of "rowspan num" by same index above is 1, set "boolean state" to false to prevent next row record this one
 3.2 Else, insert new value
4. set "Boolean states", if rowspan > 1, True, else False
5. Break the while loop

Offsetting => "Rowspan num states" value of previous was > 1 && 'column id' < 'total length of in-html columns', actions :
1. Insert value into row data using index of 'column id + id offset' rather than just 'column id'
2. deduct "Rowspan num states" of old un-updated 'column id + id offset' index by 1
3. Check offset until 3.1 condition is False
 3.1 If 'column id + id offset' is < max columns minus 1 , then add 'id offset' by 1
 3.2 Else, break the while loop

Leftover Lock On => "Rowspan num states" value of previous was = 1 && 'column id' >= 'total length of in-html columns', actions :
1. Insert value into row data
 1.1 If "Boolean states" of old un-updated 'column id + id offset' index is True, then insert the previous value
   1.1.1 If that value of "rowspan num" by same index above is 1, set "boolean state" to false to prevent next row record this one
 1.2 Else, skip
2. Break the while loop

Leftover Offsetting => "Rowspan num states" value of previous was > 1 && 'column id' >= 'total length of in-html columns', actions :
1. Insert value into row data using index of 'column id + id offset' rather than just 'column id'
2. deduct "Rowspan num states" of old un-updated 'column id + id offset' index by 1
3. Check offset until 3.1 condition is False
 3.1 If 'column id + id offset' is < max columns minus 1 , then add 'id offset' by 1
 3.2 Else, break the while loop
(this one is surprisingly the same steps as "Offsetting" one, both just ignores HTML source and focus on state dicts)

----
<<<BEGIN>>>
	""")

for row_id in range(len(test_rows)) :
	print(f"Row ID : {row_id}, {row_id+1} out of {len(test_rows)}\n")
	columns = test_rows[row_id]
	values = []
	if row_id == 0 :
		max_columns = len(columns)
	column_id = 0
	id_offset = 0
	print("Now iterating while loop with condition : column_id+id_offset < max_columns")
	while column_id+id_offset < max_columns :
		if column_id < len(columns) :
			value_item = columns[column_id]
		else :
			#things get real mk2
			searching_offset = True
			while searching_offset :
				print(f"\ncolumn id: {column_id} ({column_id+1} out of {len(columns)} in real html ***Overflown but not over yet)| id offset: {id_offset} | column id + id offset : {column_id+id_offset} ({column_id+id_offset+1} out of {max_columns} columns)")
				print(f"Rowspan num state of {column_id+id_offset} from previous row is {column_rowspan_states[column_id+id_offset]}")
				print(f"Rowspan value state of {column_id+id_offset} from previous row is {column_rowspan_value_states[column_id+id_offset]}")
				print(f"Rowspan bool state of {column_id+id_offset} from previous row is {column_rowspan_bool_is_span_states[column_id+id_offset]}")
				if column_rowspan_states[column_id+id_offset] > 1 :
					print("To do with states and values : Leftover Offsetting")
					values.append(column_rowspan_value_states[column_id+id_offset])
					column_rowspan_states[column_id+id_offset] -= 1
					if column_id+id_offset < max_columns-1 :
						id_offset += 1
					else :
						searching_offset = False
						break
				else :
					print("To do with states and values : Leftover Lock On")
					if column_rowspan_bool_is_span_states[column_id+id_offset] :
						values.append(column_rowspan_value_states[column_id+id_offset])
						if column_rowspan_states[column_id+id_offset] <= 1 :
							column_rowspan_bool_is_span_states[column_id+id_offset] = False
					searching_offset = False
					break
			break
		if row_id == 0 :
			print(f"\ncolumn id: {column_id} ({column_id+1} out of {len(columns)} in real html)| id offset: {id_offset} | column id + id offset : {column_id+id_offset+1} out of {max_columns} columns")
			print(f"Init rowspan state of {column_id} as {value_item['row_span']}")
			column_rowspan_states[column_id] = value_item['row_span']
			column_rowspan_value_states[column_id] = value_item["value"]
			if value_item['row_span'] > 1 :
				column_rowspan_bool_is_span_states[column_id] = True
			else :
				column_rowspan_bool_is_span_states[column_id] = False
			values.append(value_item["value"])
		else :
			#things get real
			searching_offset = True
			while searching_offset :
				print(f"\ncolumn id: {column_id} ({column_id+1} out of {len(columns)} in real html)| id offset: {id_offset} | column id + id offset : {column_id+id_offset+1} out of {max_columns} columns")
				print(f"Rowspan num state of {column_id+id_offset} from previous row is {column_rowspan_states[column_id+id_offset]}")
				print(f"Rowspan value state of {column_id+id_offset} from previous row is {column_rowspan_value_states[column_id+id_offset]}")
				print(f"Rowspan bool state of {column_id+id_offset} from previous row is {column_rowspan_bool_is_span_states[column_id+id_offset]}")
				if column_rowspan_states[column_id+id_offset] > 1 :
					print("To do with states and values : Offsetting")
					values.append(column_rowspan_value_states[column_id+id_offset])
					column_rowspan_states[column_id+id_offset] -= 1
					if column_id+id_offset < max_columns-1 :
						id_offset += 1
					else :
						searching_offset = False
						break
				else :
					print("To do with states and values : Lock On")
					column_rowspan_states[column_id+id_offset] = value_item['row_span']
					column_rowspan_value_states[column_id+id_offset] = value_item["value"]
					
					if column_rowspan_bool_is_span_states[column_id+id_offset] :
						values.append(column_rowspan_value_states[column_id+id_offset])
						if column_rowspan_states[column_id+id_offset] <= 1 :
							column_rowspan_bool_is_span_states[column_id+id_offset] = False
					else :
						values.append(value_item["value"])

					if value_item['row_span'] > 1 :
						column_rowspan_bool_is_span_states[column_id+id_offset] = True
					else :
						column_rowspan_bool_is_span_states[column_id+id_offset] = False
					
					searching_offset = False
					break
		column_id += 1


	print("\n==States storage, using 3 dict objects to fetch by indices easily==")
	print("(These are accessed using 'column id + id offset' value)")
	print(f"Rowspan num states : \n {column_rowspan_states}")
	print(f"Cell values states according to previous rowspans : \n {column_rowspan_value_states}")
	print(f"Boolean states to tell to fetch from previous rowspans or not : \n {column_rowspan_bool_is_span_states}")
	print("====\n")
	print("Result row below :")
	print(values)
	print("----")
	final_rows.append(values)

print("<<<END>>>")
print("==== Final result ====")
for row_values in final_rows :
	print(row_values)
