#!/usr/bin/env python

import sys
import func_s3_managefiles
import func_dbexecute
import config


# S3 details
source_bucket = config.AWS_CONFIG['BUCKET']
source_subfolder = config.AWS_CONFIG['SUBFOLDER']
source_path = config.AWS_CONFIG['PATH']
iam_user = config.AWS_CONFIG['USER']
file_delimiter = config.AWS_CONFIG['DELIMITER']
file_region = config.AWS_CONFIG['REGION']

# Redshift details
staging_schema = config.DB_CONFIG['DEST_STAGING_SCHEMA']
staging_table = config.DB_CONFIG['DEST_STAGING_TABLE']
main_schema = config.DB_CONFIG['DEST_MAIN_SCHEMAA']
main_table = config.DB_CONFIG['DEST_MAIN_TABLE']

# Input parameters
ddl_file_path = sys.argv[1]
files_to_process = sys.argv[2]

# Sql scripts
schema_ddl_file = ddl_file_path + '/schemas_ddl.sql'
table_ddl_file = ddl_file_path + '/tables_ddl.sql'
# print('ddl file path....\n', (ddl_file))



files_processed = 1

# Retreive list of files to be proccessed
source_files = func_s3_managefiles.getfilelist(source_bucket, source_subfolder, files_to_process)

if(source_files):
	print('There are files to process')

	print('Creating schemas/tables in dest db...\n')
	schema_ddl_exec_qry = func_dbexecute.executefile(schema_ddl_file)

	table_ddl_exec_QRY = func_dbexecute.executefile(table_ddl_file)

	if (schema_ddl_exec_qry == 0) and table_ddl_exec_QRY == 0:
		print('DDL scripts successfully executed')


	for file in source_files:
		dest_queries =[]

		if (files_processed == 1):
			trunc_staging_qry = 'truncate table %s.%s' %(staging_schema, staging_table)
			# trunc_main_qry = 'truncate table %s.%s' %(staging_schema, staging_table)
			dest_queries.append(trunc_staging_qry)

		drop_qry = 'drop table if exists %s."%s"' %(staging_schema, file)
		dest_queries.append(drop_qry)

		create_qry = 'create table %s."%s"("timestamp" timestamp, player_id varchar(100), subject_id varchar(100), rating_type smallint)' %(staging_schema, file)
		dest_queries.append(create_qry)

		# Prepare copy qurey since all destination tables have the same structure
		copy_qry = """copy %s."%s" from  '%s/%s'  credentials 'aws_iam_role=%s' delimiter '%s'  """ %(staging_schema, file, source_path, file, iam_user, file_delimiter)
		dest_queries.append(copy_qry)

		# Merge data into main table
		insert_qry = 'insert into %s.%s select * from %s."%s" group by 1, 2, 3, 4' %(staging_schema, staging_table, staging_schema, file)
		dest_queries.append(insert_qry)

		files_processed += 1

		exec_qry = func_dbexecute.executequery(dest_queries)
		# print(exec_qry)
		# exec_qry = 0

		if (exec_qry < 0):
			print('Error processing the file:  %s'%(file))

		# print(dest_queries)

	print("Populating main table...\n")
	main_table_qry = ['insert into %s.%s\
						select trunc(stg."timestamp"), dim.rating_description, count(distinct stg.player_id) as players, count(distinct stg.subject_id) as subjects \
						from %s.%s stg \
						join ratings.rating_type_dim dim \
						on stg.rating_type = dim.rating_id \
						group by 1, 2;'%(main_schema, main_table, staging_schema, staging_table)]
	# print(main_table_qry)

	main_qry = func_dbexecute.executequery(main_table_qry)

	if (main_qry == 0):
		print('Main table successfully populated\n')


else:
	print('no files to process')
