def rowspan_handle(array_of_rows) :
	final_rows = []
	column_rowspan_states = {}
	column_rowspan_value_states = {}
	column_rowspan_bool_is_span_states = {}
	max_columns = 9999
	for row_id in range(len(array_of_rows)) :
		#print(f"Row ID : {row_id}, {row_id+1} out of {len(array_of_rows)}\n")
		columns = array_of_rows[row_id]
		values = []
		if row_id == 0 :
			max_columns = len(columns)
		column_id = 0
		id_offset = 0
		#print("Now iterating while loop with condition : column_id+id_offset < max_columns")
		while column_id+id_offset < max_columns :
			if column_id < len(columns) :
				value_item = columns[column_id]
			else :
				#things get real mk2
				searching_offset = True
				while searching_offset :
					#print(f"\ncolumn id: {column_id} ({column_id+1} out of {len(columns)} in real html ***Overflown but not over yet)| id offset: {id_offset} | column id + id offset : {column_id+id_offset} ({column_id+id_offset+1} out of {max_columns} columns)")
					#print(f"Rowspan num state of {column_id+id_offset} from previous row is {column_rowspan_states[column_id+id_offset]}")
					#print(f"Rowspan value state of {column_id+id_offset} from previous row is {column_rowspan_value_states[column_id+id_offset]}")
					#print(f"Rowspan bool state of {column_id+id_offset} from previous row is {column_rowspan_bool_is_span_states[column_id+id_offset]}")
					if column_rowspan_states[column_id+id_offset] > 1 :
						#print("To do with states and values : Leftover Offsetting")
						values.append(column_rowspan_value_states[column_id+id_offset])
						column_rowspan_states[column_id+id_offset] -= 1
						if column_id+id_offset < max_columns-1 :
							id_offset += 1
						else :
							searching_offset = False
							break
					else :
						#print("To do with states and values : Leftover Lock On")
						if column_rowspan_bool_is_span_states[column_id+id_offset] :
							values.append(column_rowspan_value_states[column_id+id_offset])
							if column_rowspan_states[column_id+id_offset] <= 1 :
								column_rowspan_bool_is_span_states[column_id+id_offset] = False
						searching_offset = False
						break
				break
			if row_id == 0 :
				#print(f"\ncolumn id: {column_id} ({column_id+1} out of {len(columns)} in real html)| id offset: {id_offset} | column id + id offset : {column_id+id_offset+1} out of {max_columns} columns")
				#print(f"Init rowspan state of {column_id} as {value_item['row_span']}")
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
					#print(f"\ncolumn id: {column_id} ({column_id+1} out of {len(columns)} in real html)| id offset: {id_offset} | column id + id offset : {column_id+id_offset+1} out of {max_columns} columns")
					#print(f"Rowspan num state of {column_id+id_offset} from previous row is {column_rowspan_states[column_id+id_offset]}")
					#print(f"Rowspan value state of {column_id+id_offset} from previous row is {column_rowspan_value_states[column_id+id_offset]}")
					#print(f"Rowspan bool state of {column_id+id_offset} from previous row is {column_rowspan_bool_is_span_states[column_id+id_offset]}")
					if column_rowspan_states[column_id+id_offset] > 1 :
						#print("To do with states and values : Offsetting")
						values.append(column_rowspan_value_states[column_id+id_offset])
						column_rowspan_states[column_id+id_offset] -= 1
						if column_id+id_offset < max_columns-1 :
							id_offset += 1
						else :
							searching_offset = False
							break
					else :
						#print("To do with states and values : Lock On")
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
		final_rows.append(values)
	return final_rows
