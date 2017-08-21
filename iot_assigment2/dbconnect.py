import pymssql


#pymssql: https://docs.microsoft.com/en-us/sql/connect/python/pymssql/step-1-configure-development-environment-for-pymssql-python-development


def connection():
		conn = pymssql.connect(host='iotdatabase.c9va1deornpk.us-west-2.rds.amazonaws.com',database='iotdatabase',user='administrator',password='Robots123.')
		
		c = conn.cursor()
		return c, conn