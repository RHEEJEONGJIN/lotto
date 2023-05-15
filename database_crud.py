from database_init import Databases

class CRUD(Databases):
    def insertDB(self,schema,table,colum,data):
        sql = f" INSERT INTO {schema}.\"{table}\"({colum}) VALUES ({data}) ;"
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e :
            print(str(e.args[0]))
            print(" insert DB err ",e) 
            Databases.__del__(self)
            Databases.__init__(self)
    
    def readDB(self,schema,table,colum):
        sql = f" SELECT {colum} FROM {schema}.\"{table}\""
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
        except Exception as e :
            result = (" read DB err",e)
            Databases.__del__(self)
            Databases.__init__(self)
        
        return result

    def updateDB(self,schema,table,colum,value,condition):
        sql = f" UPDATE {schema}.\"{table}\" SET {colum}='{value}' WHERE {colum}='{condition}' "
        try :
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e :
            print(" update DB err",e)
            Databases.__del__(self)
            Databases.__init__(self)

    def deleteDB(self,schema,table,condition):
        sql = f" delete from {schema}.\"{table}\" where {condition} ; "
        try :
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print( "delete DB err", e)
            Databases.__del__(self)
            Databases.__init__(self)


# if __name__ == "__main__":
#     db = CRUD()
#     db.insertDB(schema='myschema',table='table',colum='ID',data='유동적변경')
#     print(db.readDB(schema='myschema',table='table',colum='ID'))
#     db.updateDB(schema='myschema',table='table',colum='ID', value='와우',condition='유동적변경')
#     db.deleteDB(schema='myschema',table='table',condition ="id != 'd'")