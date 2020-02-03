class pgload:
    def __init__(self):

        self.valid_keys = ["data", "type", "index", "unique", "table", "schema"]
        self.valid_keys.sort()

        self.valid_schema_keys = ["name", "owner", "grant"]
        self.valid_schemagrant_keys = ["all", "usage"]
        self.required_schemagrant_keys = ["all"]
        self.valid_table_keys = ["name", "owner", "grant"]
        self.valid_tablegrant_keys = ["all", "select"]
        self.required_tablegrant_keys = ["all"]

        self.valid_date_types = [
            "date",
            "time without time zone",
            "timestamp without time zone",
            "timestamp with time zone",
        ]
        self.valid_date_types.sort()

        self.valid_num_types = ["integer", "bigint", "double precision"]
        self.valid_num_types.sort()

        self.valid_char_types = ["character"]
        self.valid_char_types.sort()

        self.valid_types = list()
        self.valid_types = self.valid_types + self.valid_date_types
        self.valid_types = self.valid_types + self.valid_num_types
        self.valid_types = self.valid_types + self.valid_char_types
        self.valid_types.sort()

        self.invalid_date_values = ["", "0:0:0", "0000-00-00"]
        self.invalid_date_values.sort()

        self.invalid_num_values = ["", "."]
        self.invalid_num_values.sort()

        self.db_conn_str = "host=<host name> port=<port> dbname=<database> user=<user name> password=<password>"

    def validate_data(self, data):

        # ----------------------------------------------------------------------------------------
        # order of operations
        # ----------------------------------------------------------------------------------------
        #
        # --- check data is a dict
        # --- check keys are valid
        # --- check we have all top level keys we expect
        # --- lower case all top level type keys
        # --- check top level keys are expected types
        # --- check we have all `schema` keys we expect
        # --- check `schema.grant` is dict
        # --- check we have all `schema.grant` keys we expect
        # --- check we have all `table` keys we expect
        # --- check `table.grant` is dict
        # --- check we have all `table.grant` keys we expect
        # --- check we have data
        # --- check types are valid
        # --- check index columns are in types
        # --- check unique columns are in types
        # --- check keys in data rows are in types
        # --- lower case all data row keys
        # --- lower case all type keys
        # --- lower case all index keys
        # --- lower case all index keys
        # --- lower case all schema keys
        # --- upper case all schema.grant keys
        # --- lower case all table keys
        # --- upper case all table.grant keys
        # --- check timestamp type columns for invalid data values
        # --- check numeric type columns for invalid data values
        #
        # ----------------------------------------------------------------------------------------

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

        # --- lower case all top level type keys
        data = dict((k.lower(), v) for k, v in data.items())

        # --- check top level keys are expected types
        if not isinstance(data["type"], dict):
            raise ValueError(
                "Top Level key `type` is not a dict, type {0} passed.".format(
                    type(data["type"])
                )
            )

        if not isinstance(data["index"], list):
            raise ValueError(
                "Top Level key `index` is not a list, type {0} passed.".format(
                    type(data["index"])
                )
            )

        if not isinstance(data["unique"], list):
            raise ValueError(
                "Top Level key `unique` is not a list, type {0} passed.".format(
                    type(data["unique"])
                )
            )

        if not isinstance(data["schema"], dict):
            raise ValueError(
                "Top Level key `schema` is not a dict, type {0} passed.".format(
                    type(data["schema"])
                )
            )

        if not isinstance(data["table"], dict):
            raise ValueError(
                "Top Level key `table` is not a dict, type {0} passed.".format(
                    type(data["table"])
                )
            )

        # --- check we have all `schema` keys we expect
        invalid_schema_keys = list()
        for k in data["schema"].keys():
            if k.lower() not in self.valid_schema_keys:
                invalid_schema_keys.append(k)

        if len(invalid_schema_keys) > 0:
            raise KeyError(
                "Invalid `schema` level key(s) found: {0}. Valid keys are limited to {1}.".format(
                    invalid_schema_keys, self.valid_schema_keys
                )
            )

        missing_schema_keys = list()
        for k in self.valid_schema_keys:
            if k not in [x.lower() for x in data["schema"].keys()]:
                missing_schema_keys.append(k)

        if len(missing_schema_keys) > 0:
            raise KeyError(
                "Missing `schema` level key(s): {0}. Please add.".format(
                    missing_schema_keys
                )
            )
        del invalid_schema_keys, missing_schema_keys

        # --- check `schema.grant` is dict
        if not isinstance(data["schema"]["grant"], dict):
            raise ValueError(
                "Key `schema.grant` is not a dict, type {0} passed.".format(
                    type(data["schema"]["grant"])
                )
            )

        # --- check we have all `schema.grant` keys we expect
        invalid_schemagrant_keys = list()
        for k in data["schema"]["grant"].keys():
            if k.lower() not in self.valid_schemagrant_keys:
                invalid_schemagrant_keys.append(k)

        if len(invalid_schemagrant_keys) > 0:
            raise KeyError(
                "Invalid `schema.grant` level key(s) found: {0}. Valid keys are limited to {1}.".format(
                    invalid_schemagrant_keys, self.valid_schemagrant_keys
                )
            )

        missing_schemagrant_keys = list()
        for k in self.required_schemagrant_keys:
            if k.lower() not in [x.lower() for x in data["schema"]["grant"].keys()]:
                missing_schemagrant_keys.append(k)

        if len(missing_schemagrant_keys) > 0:
            raise KeyError(
                "Missing `schema.grant` level key(s): {0}. Please add.".format(
                    missing_schemagrant_keys
                )
            )
        del invalid_schemagrant_keys, missing_schemagrant_keys

        # --- check we have all `table` keys we expect
        invalid_table_keys = list()
        for k in data["table"].keys():
            if k.lower() not in self.valid_table_keys:
                invalid_table_keys.append(k)

        if len(invalid_table_keys) > 0:
            raise KeyError(
                "Invalid `table` level key(s) found: {0}. Valid keys are limited to {1}.".format(
                    invalid_table_keys, self.valid_table_keys
                )
            )

        missing_table_keys = list()
        for k in self.valid_table_keys:
            if k.lower() not in [x.lower() for x in data["table"].keys()]:
                missing_table_keys.append(k)

        if len(missing_table_keys) > 0:
            raise KeyError(
                "Missing `table` level key(s): {0}. Please add.".format(
                    missing_table_keys
                )
            )

        # --- check `table.grant` is dict
        if not isinstance(data["table"]["grant"], dict):
            raise ValueError(
                "Key `table.grant` is not a dict, type {0} passed.".format(
                    type(data["table"]["grant"])
                )
            )

        # --- check we have all `table.grant` keys we expect
        invalid_tablegrant_keys = list()
        for k in data["table"]["grant"].keys():
            if k.lower() not in self.valid_tablegrant_keys:
                invalid_tablegrant_keys.append(k)

        if len(invalid_tablegrant_keys) > 0:
            raise KeyError(
                "Invalid `table.grant` level key(s) found: {0}. Valid keys are limited to {1}.".format(
                    invalid_tablegrant_keys, self.valid_tablegrant_keys
                )
            )

        missing_tablegrant_keys = list()
        for k in self.required_tablegrant_keys:
            if k.lower() not in [x.lower() for x in data["table"]["grant"].keys()]:
                missing_tablegrant_keys.append(k)

        if len(missing_tablegrant_keys) > 0:
            raise KeyError(
                "Missing `table.grant` level key(s): {0}. Please add.".format(
                    missing_tablegrant_keys
                )
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
        date_columns = list()
        num_columns = list()
        for t in data["type"]:
            column_names.append(t.lower())
            if data["type"][t].lower() not in self.valid_types:
                invalid_types.append(t + ":" + data["type"][t])
            if data["type"][t].lower() in self.valid_date_types:
                date_columns.append(t.lower())
            if data["type"][t].lower() in self.valid_num_types:
                num_columns.append(t.lower())

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
            if i.lower() not in column_names:
                invalid_index.append(i)

        invalid_index.sort()
        if len(invalid_index) > 0:
            raise KeyError(
                "Column(s) in index list not in type list found: {0}".format(
                    invalid_index
                )
            )
            return False

        # --- check unique columns are in types
        invalid_unique = list()
        for i in data["unique"]:
            if i.lower() not in column_names:
                invalid_unique.append(i)

        invalid_unique.sort()
        if len(invalid_unique) > 0:
            raise KeyError(
                "Column(s) in unique list not in type list found: {0}".format(
                    invalid_unique
                )
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

        # --- lower case all data row keys
        for i in range(len(data["data"])):
            r = dict((k.lower(), v) for k, v in data["data"][i].items())
            r = {k: r[k] for k in sorted(r)}
            data["data"][i] = r

        # --- lower case all type keys
        d = dict((k.lower(), v) for k, v in data["type"].items())
        data["type"] = {k: d[k] for k in sorted(d)}

        # --- lower case all index keys
        data["index"] = [x.lower() for x in data["index"]]

        # --- lower case all index keys
        data["unique"] = [x.lower() for x in data["unique"]]

        # --- lower case all schema keys
        d = dict((k.lower(), v) for k, v in data["schema"].items())
        data["schema"] = {k: d[k] for k in sorted(d)}

        # --- upper case all schema.grant keys
        d = dict((k.lower(), v) for k, v in data["schema"]["grant"].items())
        data["schema"]["grant"] = {k: d[k] for k in sorted(d)}

        # --- lower case all table keys
        d = dict((k.lower(), v) for k, v in data["table"].items())
        data["table"] = {k: d[k] for k in sorted(d)}

        # --- upper case all table.grant keys
        d = dict((k.lower(), v) for k, v in data["table"]["grant"].items())
        data["table"]["grant"] = {k: d[k] for k in sorted(d)}

        # --- check timestamp type columns for invalid data values
        invalid_date_values = 0
        for i in range(len(data["data"])):
            for c in date_columns:
                if data["data"][i][c] in self.invalid_date_values:
                    data["data"][i][c] = None
                    invalid_date_values += 1

        if invalid_date_values > 0:
            print(
                "NOTE: {0} date values updated due to invalude data.".format(
                    invalid_date_values
                )
            )
            print(
                "      Invalide date values are limited to {0}".format(
                    self.invalid_date_values
                )
            )

        # --- check numeric type columns for invalid data values
        invalid_num_values = 0
        for i in range(len(data["data"])):
            for c in num_columns:
                if data["data"][i][c] in self.invalid_num_values:
                    data["data"][i][c] = None
                    invalid_num_values += 1

        if invalid_num_values > 0:
            print(
                "NOTE: {0} numeric values updated due to invalude data.".format(
                    invalid_num_values
                )
            )
            print(
                "      Invalide numeric values are limited to {0}".format(
                    self.invalid_num_values
                )
            )

        print("NOTE: Validate Data Complete.")
        return data

    def scd2_load(self, data, max_rows=100000):

        import psycopg2
        import os
        import socket

        # ----------------------------------------------------------------------------------------
        # order of operations
        # ----------------------------------------------------------------------------------------
        #
        # --- call validate function
        # --- create cursor
        # --- check/create schema
        # --- get char column lengths
        # --- get columns
        # --- check create table
        #    check if columns are the same and update
        #    if updates made, then update hash
        #    generate create table code
        #    apply permissions
        #    setup default indexs and constraints
        #    create specified indexes
        # --- create tmp tabe for data insert
        #    first drop if exists
        #    next create tmp table
        #    apply permissions
        # --- insert into tmp table
        # --- create insert data list
        # --- we dont need the data anymore
        # --- split data and insert
        # --- we dont need idata anymore
        # --- now that the data is in lets check for dupes vs permanent table
        # --- update end date for records where we have updates
        # --- insert into permanent table and tidy up
        #
        # ----------------------------------------------------------------------------------------

        # --- call validate function
        data = self.validate_data(data)

        # --- create cursor
        conn = psycopg2.connect(self.db_conn_str)
        cursor = conn.cursor()

        # --- check/create schema
        cursor.execute(
            "select distinct schema_name from information_schema.schemata where schema_name = '"
            + data["schema"]["name"]
            + "'"
        )
        if cursor.rowcount >= 1:
            pass
        else:
            sql = (
                "CREATE SCHEMA "
                + data["schema"]["name"]
                + ' AUTHORIZATION "'
                + data["schema"]["owner"]
                + '"'
            )
            print("NOTE:", sql)
            cursor.execute(sql)
            conn.commit()

            for g in data["schema"]["grant"].keys():
                sql = (
                    "GRANT "
                    + g.upper()
                    + " ON SCHEMA "
                    + data["schema"]["name"]
                    + ' TO "'
                    + data["schema"]["grant"][g]
                    + '"'
                )
                print("NOTE:", sql)
                cursor.execute(sql)
                conn.commit()

        # --- get char column lengths
        char_columns = list()
        for c in data["type"]:
            if data["type"][c] in self.valid_char_types:
                char_columns.append(c.lower())

        char_column_lens = dict()
        for c in char_columns:
            char_column_lens[c] = 0

        for r in data["data"]:
            for k in r.keys():
                if k in char_columns:
                    l = len(r[k].strip())
                    if char_column_lens[k] < l:
                        char_column_lens[k] = l

        # --- get columns
        column_list_char = ("".join(str(e) + "," for e in data["type"].keys()))[:-1]

        # --- check create table
        cursor.execute(
            "select distinct table_name from information_schema.tables where upper(table_schema) = upper('"
            + data["schema"]["name"]
            + "') and upper(table_name) = upper('"
            + data["table"]["name"]
            + "')"
        )
        if cursor.rowcount >= 1:
            # --- check if columns are the same and update
            sql = (
                "select column_name \
            , data_type \
            , character_maximum_length \
            from information_schema.columns \
            where table_schema = '"
                + data["schema"]["name"]
                + "' \
            and table_name = '"
                + data["table"]["name"]
                + "' \
            and column_name not like 'db_%'"
            )

            cursor.execute(sql)
            rows = cursor.fetchall()

            column_updates = False
            for k in char_column_lens.keys():
                for r in rows:

                    if k == r[0]:

                        if char_column_lens[k] > r[2]:
                            sql = (
                                "ALTER TABLE "
                                + data["schema"]["name"]
                                + "."
                                + data["table"]["name"]
                                + " ALTER COLUMN "
                                + k
                                + " TYPE character("
                                + str(char_column_lens[k])
                                + ")"
                            )
                            print("NOTE:", sql)
                            cursor.execute(sql)
                            conn.commit()
                            column_updates = True

            # --- if updates made, then update hash
            if column_updates == True:

                sql = (
                    "UPDATE "
                    + data["schema"]["name"]
                    + "."
                    + data["table"]["name"]
                    + " SET db_hash_id = md5(CAST(("
                    + column_list_char
                    + ")AS text))::uuid"
                )
                print("NOTE:", sql)
                cursor.execute(sql)
                conn.commit()

        else:
            # --- generate create table code
            for c in char_column_lens:
                data["type"][c] = "character(" + str(char_column_lens[c]).strip() + ")"

            sql = (
                "CREATE TABLE "
                + data["schema"]["name"]
                + "."
                + data["table"]["name"]
                + " ("
            )

            for c in data["type"]:

                sql = sql + c + " " + data["type"][c] + ","

            sql = (
                sql
                + "db_id bigserial NOT NULL, db_hash_id uuid, \
        db_insert_dt timestamp with time zone DEFAULT timezone('utc'::text, now()), \
        db_update_dt timestamp with time zone NOT NULL DEFAULT timezone('utc'::text, '9999-09-09 00:00:00'))"
            )

            print("NOTE:", sql)
            cursor.execute(sql)
            conn.commit()

            # --- apply permissions
            sql = (
                "ALTER TABLE "
                + data["schema"]["name"]
                + "."
                + data["table"]["name"]
                + ' OWNER TO "'
                + data["table"]["owner"]
                + '"'
            )
            print("NOTE:", sql)
            cursor.execute(sql)
            conn.commit()

            for g in data["table"]["grant"].keys():
                sql = (
                    "GRANT "
                    + g.upper()
                    + " ON TABLE "
                    + data["schema"]["name"]
                    + "."
                    + data["table"]["name"]
                    + ' TO "'
                    + data["table"]["grant"][g]
                    + '"'
                )
                print("NOTE:", sql)
                cursor.execute(sql)
                conn.commit()

            # --- setup default indexs and constraints
            sql = (
                "ALTER TABLE "
                + data["schema"]["name"]
                + "."
                + data["table"]["name"]
                + " ADD CONSTRAINT "
                + data["schema"]["name"]
                + "_"
                + data["table"]["name"]
                + "_db_id_pk PRIMARY KEY (db_id)"
            )
            print("NOTE:", sql)
            cursor.execute(sql)
            conn.commit()

            sql = (
                "CREATE INDEX "
                + data["schema"]["name"]
                + "_"
                + data["table"]["name"]
                + "_db_id_index ON "
                + data["schema"]["name"]
                + "."
                + data["table"]["name"]
                + " (db_id)"
            )
            print("NOTE:", sql)
            cursor.execute(sql)
            conn.commit()

            sql = (
                "CREATE INDEX "
                + data["schema"]["name"]
                + "_"
                + data["table"]["name"]
                + "_db_hash_id_index ON "
                + data["schema"]["name"]
                + "."
                + data["table"]["name"]
                + " (db_hash_id)"
            )
            print("NOTE:", sql)
            cursor.execute(sql)
            conn.commit()

            # --- create specified indexes
            for i in data["index"]:

                sql = (
                    "CREATE INDEX "
                    + data["schema"]["name"]
                    + "_"
                    + data["table"]["name"]
                    + "_"
                    + i
                    + "_index ON "
                    + data["schema"]["name"]
                    + "."
                    + data["table"]["name"]
                    + " ("
                    + i
                    + ")"
                )
                print("NOTE:", sql)
                cursor.execute(sql)
                conn.commit()

        # --- create tmp tabe for data insert

        # first drop if exists
        pid = str(os.getpid())
        hn = str(socket.gethostname())
        tmp_tbl = (
            "tmp_" + pid + "_" + socket.gethostname() + "_" + data["table"]["name"]
        )
        sql = "DROP TABLE IF EXISTS " + data["schema"]["name"] + "." + tmp_tbl
        print("NOTE:", sql)
        cursor.execute(sql)
        conn.commit()

        # next create tmp table
        sql = (
            "CREATE TABLE "
            + data["schema"]["name"]
            + "."
            + tmp_tbl
            + " AS SELECT * FROM "
            + data["schema"]["name"]
            + "."
            + data["table"]["name"]
            + " WHERE 1=2;"
        )
        print("NOTE:", sql)
        cursor.execute(sql)
        conn.commit()

        # apply permissions
        sql = (
            "ALTER TABLE "
            + data["schema"]["name"]
            + "."
            + tmp_tbl
            + ' OWNER TO "'
            + data["table"]["owner"]
            + '"'
        )
        print("NOTE:", sql)
        cursor.execute(sql)
        conn.commit()

        for g in data["table"]["grant"].keys():
            sql = (
                "GRANT "
                + g.upper()
                + " ON TABLE "
                + data["schema"]["name"]
                + "."
                + tmp_tbl
                + ' TO "'
                + data["table"]["grant"][g]
                + '"'
            )
            print("NOTE:", sql)
            cursor.execute(sql)
            conn.commit()

        # --- insert into tmp table

        sql = (
            "INSERT INTO "
            + data["schema"]["name"]
            + "."
            + tmp_tbl
            + "( "
            + column_list_char
            + " ) VALUES "
        )

        morg_special_chars = "("
        for i in data["type"].keys():
            morg_special_chars = morg_special_chars + "%s, "

        morg_special_chars = morg_special_chars.strip()[:-1] + ")"

        print("NOTE: {0}".format(column_list_char))
        print("NOTE: {0}".format(morg_special_chars))

        # --- create insert data list
        idata = []
        for l_item in data["data"]:
            tmp_idata = []
            for key, value in l_item.items():
                tmp_idata.append(value)
            idata.append(tmp_idata)

        # --- we dont need the data anymore
        data["data"] = None

        # --- split data and insert
        split_count = round(len(idata) / max_rows)

        for i in range(split_count):

            if i == 0:

                start_row = 0

                if split_count == 1:
                    end_row = len(idata)
                else:
                    end_row = max_rows

            elif i == split_count - 1:

                start_row = end_row
                end_row = len(idata)

            else:

                start_row = end_row
                end_row = start_row + max_rows

            print("NOTE: Inserting", end_row, "of", len(idata))

            args_str = b",".join(
                cursor.mogrify(morg_special_chars, x) for x in idata[start_row:end_row]
            )

            args_str = args_str.decode("utf-8")

            cursor.execute(sql + args_str)
            conn.commit()

        # --- we dont need idata anymore
        del idata

        # --- now that the data is in lets check for dupes vs permanent table
        sql = (
            "UPDATE "
            + data["schema"]["name"]
            + "."
            + tmp_tbl
            + " SET db_hash_id = md5(CAST(("
            + column_list_char
            + ")AS text))::uuid"
        )
        cursor.execute(sql)
        conn.commit()

        sql = (
            "DELETE FROM "
            + data["schema"]["name"]
            + "."
            + tmp_tbl
            + " B USING "
            + data["schema"]["name"]
            + "."
            + data["table"]["name"]
            + " C WHERE B.db_hash_id = C.db_hash_id"
        )
        cursor.execute(sql)
        conn.commit()

        # --- update end date for records where we have updates
        u_count = len(data["unique"])
        _count = 1
        unique_str = ""
        for c in data["unique"]:

            unique_str = unique_str + "B." + c.strip() + " = C." + c

            if _count != u_count:
                unique_str = unique_str + " and "

            _count += 1

        sql = (
            "UPDATE "
            + data["schema"]["name"]
            + "."
            + data["table"]["name"]
            + " B SET db_update_dt = timezone('utc'::text, now()) FROM "
            + data["schema"]["name"]
            + "."
            + tmp_tbl
            + " C WHERE "
            + unique_str
        )
        cursor.execute(sql)
        conn.commit()

        # --- insert into permanent table and tidy up
        sql = (
            "INSERT INTO "
            + data["schema"]["name"]
            + "."
            + data["table"]["name"]
            + " ("
            + column_list_char
            + ") SELECT "
            + column_list_char
            + " FROM "
            + data["schema"]["name"]
            + "."
            + tmp_tbl
        )
        cursor.execute(sql)
        conn.commit()

        sql = (
            "UPDATE "
            + data["schema"]["name"]
            + "."
            + data["table"]["name"]
            + " SET db_hash_id = md5(CAST(("
            + column_list_char
            + ")AS text))::uuid WHERE db_hash_id IS NULL"
        )
        cursor.execute(sql)
        conn.commit()

        sql = "drop table if exists " + data["schema"]["name"] + "." + tmp_tbl
        cursor.execute(sql)
        conn.commit()

        print("NOTE: SCD2 Load Complete.")
        conn.close()
