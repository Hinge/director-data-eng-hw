
AWS_CONFIG = dict(
    AWS_ACCESS_KEY= 'AKIAJKCJCYRPQZ5I667A',
    AWS_SECRET_KEY= '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',
    BUCKET= 'hinge-homework',
	SUBFOLDER= 'director-data-engineering/ratings',
	PATH= "s3://hinge-homework/director-data-engineering/ratings",
	USER= 'arn:aws:iam::954192691408:role/myTestRSRole',
	DELIMITER='\t',
	REGION= 'us-east-1'
)

DB_CONFIG = dict(
	HOST="hw-instance.cuyrcmr4ffad.us-east-1.redshift.amazonaws.com",
	DBNAME='hgtestdb',
	USER='testuser' ,
	PASSWORD='Bbqlbmys1!',
	PORT = '5439',
	DEST_STAGING_SCHEMA = 'ratings_staging',
	DEST_STAGING_TABLE = 'fake_ratings_stg',
	DEST_MAIN_SCHEMAA = 'ratings',
	DEST_MAIN_TABLE = 'ratings_by_day'
				)


params =  "host = %s dbname = %s user = %s password = %s port = %s" %(DB_CONFIG["HOST"] \
			, DB_CONFIG["DBNAME"], DB_CONFIG["USER"], DB_CONFIG["PASSWORD"], DB_CONFIG["PORT"])
	