class pgload:
    def __init__(self):

        self.valid_keys = ["data", "type", "index", "unique", "table", "schema"]
        self.valid_keys.sort()

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

        # --- check data is a dict
        if not isinstance(data, dict):
            raise ValidationError(
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
            raise ValidationError(
                "Invalid top level key(s) found: {0}. Valid keys are limited to {1}.".format(
                    invalid_keys, self.valid_keys
                )
            )
        del invalid_keys

        # --- check we have all the keys we expect
        missing_keys = list()
        data_keys = list()
        for k in data.keys():
            data_keys.append(k.lower())

        for k in self.valid_keys:
            if k not in data_keys:
                missing_keys.append(k)

        if len(missing_keys) > 0:
            raise ValidationError(
                "Missing top level key(s) found: {0}. Please add.".format(missing_keys)
            )
        del missing_keys, data_keys

        # --- check we have data
        if not isinstance(data["data"], list):
            raise ValidationError(
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
            raise ValidationError(
                "Invalid DB type(s) found: {0}. Valid types are limited to {1}".format(
                    invalid_types, self.valid_types
                )
            )
            return False
        del invalid_types, column_names

        # --- check index columns are in types
        invalid_index = list()
        for i in data["index"]:
            if i not in column_names:
                invalid_index.append(i)

        invalid_index.sort()
        if len(invalid_index) > 0:
            raise ValidationError(
                "Column(s) in index list not in type list {0}".format()
            )
            return False

        # --- check unique columns are in types
        invalid_unique = list()
        for i in data["unique"]:
            if i not in column_names:
                invalid_unique.append(i)

        invalid_unique.sort()
        if len(invalid_unique) > 0:
            raise ValidationError(
                "Column(s) in index list not in type list {0}".format()
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
            raise ValidationError(
                "Key(s) found in data row not in type list {0}.".format(invalid_dr_keys)
            )
            return False
        del invalid_dr_keys

        return True
