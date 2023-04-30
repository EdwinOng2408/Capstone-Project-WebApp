import sqlite3

class JuncTableCollection:
    """
    Parent class for Student_Activity and Student_Class collections

    Incorporates the editing of membership for data

    Attributes
    ----------
    (-) dbname: str
    (-) tblname: str

    Methods
    -------
    (+) edit
    (-) _findall
    (-) _execute_dql
    (-) _execute_dml
    """
    def __init__(self, dbname):
        self._dbname = dbname
        self._tblname = "student_cca"
        self._keys = ["student_id", "cca_id"]
           
    def __repr__(self):
        return f'{self._dbname} --> {self._tblname}'

    def _search(self, student_tbl, student_name, tbl_2, secondary_data):
        student_query = f'''
        SELECT "id" FROM "{student_tbl}"
        WHERE "name" = "{student_name}"
        '''
        data_query = f'''
        SELECT "id" FROM "{tbl_2}"
        WHERE "name" = "{secondary_data}"
        '''
        data_dict = dict()
        data_dict[self._keys[0]] = self._execute_dql(student_query)
        data_dict[self._keys[1]] = self._execute_dql(data_query)
        print(data_dict)
        return data_dict
    
    def edit(self, student_tbl, student_name, tbl_2, secondary_data, function):
        """
        Method to insert or delete data from the junction table
        Parameter function: "edit" OR "insert"
        """
        
        data = self._search(student_tbl, student_name, tbl_2, secondary_data)
        
        if function == "delete":
            query = f'''
            DELETE FROM "{self._tblname}"
            WHERE "{self._keys[0]}" = ? AND "{self._keys[1]}" = ?
            '''
        elif function == "insert":
            query = f'''
            INSERT INTO "{self._tblname}"
            VALUES (?, ?);
            '''
        values = (data[self._keys[0]], data[self._keys[1]],)
        print(values)
        self._execute_dml(query, values)
        
    def _execute_dml(self, query, data):
        with sqlite3.connect(self._dbname) as conn:
            cur = conn.cursor()
            cur.execute(query, data)
            conn.commit()

    def _execute_dql(self, query, **kwargs):
        with sqlite3.connect(self._dbname) as conn:
            cur = conn.cursor()
            cur.execute(query)
            return cur.fetchone()[0]

    def _findall(self):
        query = f'''
        SELECT * FROM {self._tblname}
        '''
        with sqlite3.connect(self._dbname) as conn:
            cur = conn.cursor()
            cur.execute(query)
            return cur.fetchall()
            
class StudentCCA(JuncTableCollection):
    """
    Child class of JuncTableCollection that accesses the student_cca junction table
    """
    def __init__(self, dbname):
        super().__init__(dbname)

class StudentActivity(JuncTableCollection):
    """
    Child class of JuncTableCollection that accesses the student_activity junction table
    """
    def __init__(self, dbname):
        super().__init__(dbname)
        self._keys = ["student_id", "activity_id"]
        self._tblname = "student_activity"

class StudentData:
    """
    Class containing all data of a student

    Attributes
    ----------
    (-) _tblname
    (-) _dbname

    Methods
    -------
    (-) _join_class
    (-) _join_subject
    (-) _join_cca
    (-) _join_activity
    (-) _data_compile
    (-) _execute_dql
    (+) get_all
    (+) get_one
    """
    def __init__(self, dbname):
        self._dbname = dbname
        self._tblname = "student"

    def __repr__(self):
        return f'{self._dbname} --> {self._tblname}'

    def _execute_dql(self, query, find="one", search_by=None):
        
        with sqlite3.connect(self._dbname) as conn:
            cur = conn.cursor()
            if find == "one":
                cur.execute(query, (search_by,))
            else:
                cur.execute(query)
            return cur.fetchall()

    def _join_class(self, name=None):
        '''inner joins student and class tables'''
        
        query = '''
        SELECT 
        "student"."name",
        "student"."year_enrolled",
        "class"."name",
        "class"."level"
        FROM "student"
        INNER JOIN "class" ON "student"."class_id" = "class"."id"
        '''
        find = "many"
        if name is not None:
            specific_query = '''WHERE "student"."name" = ?'''
            
            query += specific_query
            find = "one"
            
        data = self._execute_dql(query, find=find, search_by=name)
            
        return self._data_compile(data, "student_details", ["student_name", "year_enrolled", "class_name", "class_level"])
        
    def _data_compile(self, data, key, key_names):
        '''
        helper function to store tuple data in a dictionary
        
        Parameters
        ----------
        data: post-execute_dql data (list of tuples)
        key: activity, cca, subject (general name for data)
        key_names: individual data names (ie. role, type)
        
        Returns a dictionary with key name "key" and values as a list of dictionaries
        Eg. {"cca": [{"name": "Basketball", "type": "Sport"}, {"name": "Nanyang Astronomy Club", "type": "SIG"}]}
        '''
        storage = []
        size = len(data)
        if data == []:
            return data
        for i, record in enumerate(data, start=1):
            records = {}
            temp = {}
            for j, r in enumerate(record):
                temp[key_names[j]] = r
            if size > 1:
                keyname = key + "_" + str(i)
                records[keyname] = temp
            else:
                records[key] = temp
            storage.append(records)
            
        return storage
            
    def _join_subject(self, name):
        '''inner join for student and subject tables'''
        
        query = '''
        SELECT "subject"."name", "subject"."level"
        FROM "student_subject"
        INNER JOIN "student" ON 
        "student"."id" = "student_subject"."student_id"
        INNER JOIN "subject" ON 
        "subject"."id" = "student_subject"."subject_id"
        WHERE "student"."name" = ?
        '''
        return self._data_compile(self._execute_dql(query, search_by=name), "subject", ["subject_name", "subject_level"])

    def _join_activity(self, name):
        '''inner join for student and activity tables'''
        
        query = '''
        SELECT
        "activity"."name", "activity"."start_date",
        "activity"."end_date", "activity"."description",
        "student_activity"."category", "student_activity"."award",
        "student_activity"."hours", "student_activity"."role"
        
        FROM "student_activity"
        INNER JOIN "student" ON "student"."id" = "student_activity"."student_id"
        
        INNER JOIN "activity" ON "activity"."id" = "student_activity"."activity_id"

        WHERE "student"."name" = ?
        '''
        return self._data_compile(self._execute_dql(query, search_by=name), "activity", ["name", "start_date", "end_date", "description", "category", "award", "hours", "role"])

    def _join_cca(self, name):
        '''inner join for student and cca tables'''
        
        query = '''
        SELECT
        "cca"."name",
        "cca"."type"
        
        FROM "student_cca"
        INNER JOIN "student" ON "student"."id" = "student_cca"."student_id"
        INNER JOIN "cca" ON "cca"."id" = "student_cca"."cca_id"
        WHERE "student"."name" = ?
        '''
        return self._data_compile(self._execute_dql(query, search_by=name), "cca", ["name", "type"])

    def get_all(self):
        storage = []
        for record in self._join_class():
            for key, value in record.items():
                storage.append(value)
        return storage

    def get_one(self, name):
        storage = self._join_class(name) + self._join_cca(name) + self._join_activity(name) + self._join_subject(name)
        
        return storage
        