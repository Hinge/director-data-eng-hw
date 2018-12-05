#!/usr/bin/env python

import psycopg2
import config

'''
	Executes queries on Redshift database that's passed as the parameter
 '''

def executequery(queries, db=config.params):

	'''
	This function executes queries, which are  passed as a list
	'''
	
	#Setup connection to db
	conn = psycopg2.connect(db)

	#Create a cursor
	cur = conn.cursor()

	#Error count executing the query
	errors = 0

	#Loop through queries
	for query in queries:

		try:
			# print(query)
			cur.execute(query)
			

		except psycopg2.Error as e:
			print(e.__doc__)
			errors += 1

	conn.commit()
	cur.close()
	conn.close()

	#Return success or failure codes based on errors 
	if (errors > 0):
		return -10

	else:
		return 0

def executefile(sqlfile, db=config.params):
	# print('db params...', config.db_params)

	try:

		#Error count executing the query
		errors = 0

		#Setup connection to db
		conn = psycopg2.connect(db)

		#Create a cursor
		cur = conn.cursor()

		#Execute the SQL file
		cur.execute(open(sqlfile, 'r').read())

	except psycopg2.Error as e:
		print(str(e).strip('\n'))
		errors += 1

	finally:		
		#Close cursor and connection
		conn.commit()
		cur.close()
		conn.close()

	#Return success or failure codes based on errors 
	if (errors > 0):
		return -10

	else:
		return 0



if __name__ == '__main__':
	print('Running tests')





