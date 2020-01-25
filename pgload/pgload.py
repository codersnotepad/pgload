class pgload:
    def __init__(self):

        self.valid_keys = ["data", "type", "index", "unique", "table", "schema"]
        self.valid_keys.sort()

        self.valid_schema_keys = ["name","owner","grant"]
        self.valid_schemagrant_keys = ["all","usage"]
        self.required_schemagrant_keys = ["all"]
        self.valid_table_keys = ["name","owner","grant"]
        self.valid_tablegrant_keys = ["all","select"]
        self.required_tablegrant_keys = ["all"]

        self.valid_date_types = [
            "date",
            "time without time zone",
            "timestamp without time zone",
            "timestamp with time zone",
        ]
        self.valid_date_types.sort()

        self.valid_num_types = ["bigint", "double precision"]
        self.valid_num_types.sort()

        self.valid_char_types = ["character"]
        self.valid_char_types.sort()

        self.valid_types = list()
        self.valid_types = self.valid_types + self.valid_date_types
        self.valid_types = self.valid_types + self.valid_num_types
        self.valid_types = self.valid_types + self.valid_char_types
        self.valid_types.sort()

    def validate_data(self, data):

        #----------------------------------------------------------------------------------------
        # order of operations
        #----------------------------------------------------------------------------------------
        #
        # --- check data is a dict
        # --- check keys are valid
        # --- check we have all top level keys we expect
        # --- check top level keys are expected types
        # --- check we have all `schema` keys we expect
        # --- check `schema.grant` is dict
        # --- check we have all `schema.grant` keys we expect
        # --- check we have all `table` keys we expect
        # --- check we have all `table.grant` keys we expect
        # --- check we have data
        # --- check types are valid
        # --- check index columns are in types
        # --- check unique columns are in types
        # --- check keys in data rows are in types
        #
        #----------------------------------------------------------------------------------------



        # --- check data is a dict
        if not isinstance(data, dict):
            raise ValueError(
                "Object is not a dictionary, type {0} passed.".format(type(data))
            )
            return False

        # --- check keys are valid
        invalid_keys = list()
        for k in data.keys():
            if k.lower() not in self.valid_keys:
                invalid_keys.append(k)

        invalid_keys.sort()
        if len(invalid_keys) > 0:
            raise KeyError(
                "Invalid top level key(s) found: {0}. Valid keys are limited to {1}.".format(
                    invalid_keys, self.valid_keys
                )
            )
        del invalid_keys

        # --- check we have all top level keys we expect
        missing_keys = list()
        data_keys = list()
        for k in data.keys():
            data_keys.append(k.lower())

        for k in self.valid_keys:
            if k not in data_keys:
                missing_keys.append(k)

        if len(missing_keys) > 0:
            raise KeyError(
                "Missing top level key(s): {0}. Please add.".format(missing_keys)
            )
        del missing_keys, data_keys

        # --- checktop level keys are expected types
        if not isinstance(data['type'], dict):
            raise ValueError("Top Level key `type` is not a dict, type {0} passed.".format(type(data['type'])))

        if not isinstance(data['index'], list):
            raise ValueError("Top Level key `index` is not a list, type {0} passed.".format(type(data['index'])))

        if not isinstance(data['unique'], list):
            raise ValueError("Top Level key `unique` is not a list, type {0} passed.".format(type(data['unique'])))

        if not isinstance(data['schema'], dict):
            raise ValueError("Top Level key `schema` is not a dict, type {0} passed.".format(type(data['schema'])))

        if not isinstance(data['table'], dict):
            raise ValueError("Top Level key `table` is not a dict, type {0} passed.".format(type(data['table'])))

        # --- check we have all `schema` keys we expect
        invalid_schema_keys = list()
        for k in data['schema'].keys():
            if k not in self.valid_schema_keys:
                invalid_schema_keys.append(k)

        if len(invalid_schema_keys) >0:
            raise KeyError("Invalid `schema` level key(s) found: {0}. Valid keys are limited to {1}.".format(invalid_schema_keys,self.valid_schema_keys))

        missing_schema_keys = list()
        for k in self.valid_schema_keys:
            if k not in data['schema'].keys():
                missing_schema_keys.append(k)

        if len(missing_schema_keys) > 0:
            raise KeyError(
                "Missing `schema` level key(s): {0}. Please add.".format(missing_schema_keys)
            )
        del invalid_schema_keys, missing_schema_keys

        # --- check `schema.grant` is dict
        if not isinstance(data['schema']['grant'], dict):
            raise ValueError("Key `schema.grant` is not a dict, type {0} passed.".format(type(data['schema']['grant'])))

        # --- check we have all `schema.grant` keys we expect
        invalid_schemagrant_keys = list()
        for k in data['schema']['grant'].keys():
            if k not in self.valid_schemagrant_keys:
                invalid_schemagrant_keys.append(k)

        if len(invalid_schemagrant_keys) >0:
            raise KeyError("Invalid `schema.grant` level key(s) found: {0}. Valid keys are limited to {1}.".format(invalid_schemagrant_keys,self.valid_schemagrant_keys))

        missing_schemagrant_keys = list()
        for k in self.required_schemagrant_keys:
            if k not in data['schema']['grant'].keys():
                missing_schemagrant_keys.append(k)

        if len(missing_schemagrant_keys) > 0:
            raise KeyError(
                "Missing `schema.grant` level key(s): {0}. Please add.".format(missing_schemagrant_keys)
            )
        del invalid_schemagrant_keys, missing_schemagrant_keys

        # --- check we have all `table` keys we expect
        invalid_table_keys = list()
        for k in data['table'].keys():
            if k not in self.valid_table_keys:
                invalid_table_keys.append(k)

        if len(invalid_table_keys) >0:
            raise KeyError("Invalid `table` level key(s) found: {0}. Valid keys are limited to {1}.".format(invalid_table_keys,self.valid_table_keys))

        missing_table_keys = list()
        for k in self.valid_table_keys:
            if k not in data['table'].keys():
                missing_table_keys.append(k)

        if len(missing_table_keys) > 0:
            raise KeyError(
                "Missing `table` level key(s): {0}. Please add.".format(missing_table_keys)
            )

        # --- check `table.grant` is dict
        if not isinstance(data['table']['grant'], dict):
            raise ValueError("Key `table.grant` is not a dict, type {0} passed.".format(type(data['table']['grant'])))

        # --- check we have all `schema.grant` keys we expect
        invalid_tablegrant_keys = list()
        for k in data['table']['grant'].keys():
            if k not in self.valid_tablegrant_keys:
                invalid_tablegrant_keys.append(k)

        if len(invalid_tablegrant_keys) >0:
            raise KeyError("Invalid `table.grant` level key(s) found: {0}. Valid keys are limited to {1}.".format(invalid_tablegrant_keys,self.valid_tablegrant_keys))

        missing_tablegrant_keys = list()
        for k in self.required_tablegrant_keys:
            if k not in data['table']['grant'].keys():
                missing_tablegrant_keys.append(k)

        if len(missing_tablegrant_keys) > 0:
            raise KeyError(
                "Missing `table.grant` level key(s): {0}. Please add.".format(missing_tablegrant_keys)
            )
        del invalid_tablegrant_keys, missing_tablegrant_keys

        # --- check we have data
        if not isinstance(data["data"], list):
            raise ValueError(
                "Data is not a list, type {0} passed.".format(type(data["data"]))
            )
            return False
        else:
            if len(data["data"]) == 0:
                raise ValidationError("No data rows to process.")
                return False

        # --- check types are valid
        invalid_types = list()
        column_names = list()
        for t in data["type"]:
            column_names.append(t.lower())
            if data["type"][t].lower() not in self.valid_types:
                invalid_types.append(t + ":" + data["type"][t])

        invalid_types.sort()
        if len(invalid_types) > 0:
            raise ValueError(
                "Invalid DB type(s) found: {0}. Valid types are limited to {1}".format(
                    invalid_types, self.valid_types
                )
            )
            return False
        del invalid_types

        # --- check index columns are in types
        invalid_index = list()
        for i in data["index"]:
            if i not in column_names:
                invalid_index.append(i)

        invalid_index.sort()
        if len(invalid_index) > 0:
            raise KeyError(
                "Column(s) in index list not in type list {0}".format(invalid_index)
            )
            return False

        # --- check unique columns are in types
        invalid_unique = list()
        for i in data["unique"]:
            if i not in column_names:
                invalid_unique.append(i)

        invalid_unique.sort()
        if len(invalid_unique) > 0:
            raise KeyError(
                "Column(s) in unique list not in type list {0}".format(invalid_unique)
            )
            return False
        del invalid_unique

        # --- check keys in data rows are in types
        invalid_dr_keys = list()
        for r in data["data"]:
            for k in r.keys():
                if k.lower() not in column_names:
                    invalid_dr_keys.append(k)
            invalid_dr_keys = list(set(invalid_dr_keys))

        invalid_dr_keys.sort()
        if len(invalid_dr_keys) > 0:
            raise KeyError(
                "Key(s) found in data row not in type list {0}.".format(invalid_dr_keys)
            )
            return False
        del invalid_dr_keys, column_names

        return True
