use YELP_DB;

load data INFILE '/var/lib/mysql-files/yelp_business.csv' 
into table Business fields terminated BY ',' IGNORE 1 LINES
(business_id,name,@vNB,address,city,state,postal_code,latitude,longitude,stars,review_count,is_open,categories) 
SET neighborhood = nullif(@vNB, '');

load data INFILE '/var/lib/mysql-files/yelp_checkin.csv' 
into table Checkin fields terminated BY ',' IGNORE 1 LINES
(business_id,weekday,hour,checkins);

