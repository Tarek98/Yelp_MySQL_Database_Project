use YELP_DB;

load data INFILE '/var/lib/mysql-files/yelp_business.csv' 
into table Business fields terminated BY ',' IGNORE 1 LINES
(business_id,name,@vNB,address,city,state,postal_code,latitude,longitude,stars,review_count,is_open,categories) 
SET neighborhood = nullif(@vNB, '');

load data INFILE '/var/lib/mysql-files/yelp_checkin.csv' 
into table Checkin fields terminated BY ',' IGNORE 1 LINES
(business_id,weekday,hour,checkins);

load data INFILE '/var/lib/mysql-files/yelp_user.csv' 
into table User fields terminated BY ',' IGNORE 1 LINES
(user_id,name,review_count,yelping_since,friends,useful,funny,cool,fans,elite,average_stars,@dummy,@dummy,@dummy,@dummy,@dummy,@dummy,@dummy,@dummy,@dummy,yelping_since)

load data INFILE '/var/lib/mysql-files/yelp_review.csv' 
into table Review fields terminated BY ',' IGNORE 1 LINES
(review_id,user_id,business_id,stars,date,text,useful,funny,cool)

load data INFILE '/var/lib/mysql-files/yelp_tip.csv' 
into table Tip fields terminated BY ',' IGNORE 1 LINES
(text,date,likes,business_id,user_id)

