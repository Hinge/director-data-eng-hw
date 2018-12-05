drop table if exists ratings_staging.fake_ratings_stg;

create table ratings_staging.fake_ratings_stg
("timestamp" timestamp sortkey
, player_id varchar(100)
, subject_id varchar(100)
, rating_type smallint
, load_date timestamp default getdate()
);

drop table if exists ratings.rating_type_dim;

create table ratings.rating_type_dim
(
rating_id smallint
, rating_description varchar(20)
, create_date timestamp default getdate()
, update_date timestamp default getdate()
);

insert into ratings.rating_type_dim
(rating_id, rating_description)
select 0, 'skip'
union
select 1, 'like'
union
select 2, 'comment'
union
select 3, 'remove/block/reject'
union
select 4, 'report'
union
select 5, 'match'
;

drop table if exists ratings.ratings_by_day;

create table ratings.ratings_by_day
(
rating_date date
, rating_description varchar(20)
, total_players bigint
, total_subjects bigint
, create_date timestamp default getdate()
, update_date timestamp default getdate()
);