import sqlite3

class StudentCollection:
    """
    Parent class of StudentCollection and CCACollection

    Attributes
    ----------
    (-) dbname
    (-) tblname

    Methods
    -------
    (+) view
    (+) insert
    (+) edit
    """
    def __init__(self, dbname, tblname):
        self.dbname = dbname
        self.tblname = tblname

    def __repr__(self):
        return f'{self.dbname} --> {self.tblname}'

    def view(self, tbl):
        query = f'''
        SELECT * 
        '''
        return self._pass_to(query)
        
    def _pass_to(self, query):
        with sqlite3.connect(self.dbname) as conn:
            cur = conn.cursor()
            cur.execute(query)
            ret_all = cur.fetchall()
            return ret_all


        


    