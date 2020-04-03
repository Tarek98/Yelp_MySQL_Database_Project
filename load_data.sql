use YELP_DB;

load data INFILE '/var/lib/mysql-files/yelp_business.csv' 
into table Business fields terminated BY ',' ENCLOSED BY '"' IGNORE 1 LINES
(business_id,name,@vNB,address,city,state,postal_code,latitude,longitude,stars,review_count,is_open,categories) 
SET neighborhood = nullif(@vNB, '');

load data INFILE '/var/lib/mysql-files/yelp_checkin.csv' 
into table Checkin fields terminated BY ',' IGNORE 1 LINES
(business_id,weekday,hour,checkins);

-- friends is VARCHAR(5000) --> can fit max 200 IDs in variable (see below: 4798 < 5000)
-- user_id = '0njfJmB-7n84DlIgUByCNw'
-- 4798 = len(user_id+', '+ 198*(user_id+', ') + user_id) 
load data INFILE '/var/lib/mysql-files/yelp_user.csv' 
into table User 
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY "\r\n" IGNORE 1 LINES 
(user_id,name,@vRC,@vYsince,@vFriends,@vUseful,@vFunny,@vCool,@vFans,@dummy,average_stars,@dummy,@dummy,@dummy,@dummy,@dummy,@dummy,@dummy,@dummy,@dummy, @dummy, @dummy)
SET review_count = cast(@vRC as unsigned), useful = cast(@vUseful as unsigned), 
funny = cast(@vFunny as unsigned), cool = cast(@vCool as unsigned),
friends = left(@vFriends, 4798), yelping_since = @vYsince, last_online = @vYsince;

-- REASON for deleting lines is that descriptions of review and text
--   contain many unescaped characters such as neseted quotation marks

-- delete all lines after 2,000,000 till end of yelp_review.csv file (line 17746269)
-- run command below on linux terminal (backs up file to yelp_review.csv.bak then deletes lines)
sed -i.bak -e '2000001,17746269d' /var/lib/mysql-files/yelp_review.csv
-- run command below on mysql shell

load data INFILE '/var/lib/mysql-files/yelp_review.csv' 
into table Review 
fields terminated BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES
(review_id,user_id,business_id,@vStars,date,@vText,@vUseful,@vFunny,@vCool)
SET stars  = cast(@vStars as unsigned), useful  = cast(@vUseful as unsigned),
text = left(@vText, 5000), funny = cast(@vFunny as unsigned), cool  = cast(@vCool as unsigned);

-- delete all lines after 10,000 till end of yelp_tip.csv file (line 1140054)
-- run command below on linux terminal (backs up file to yelp_tip.csv.bak then deletes lines)
sed -i.bak -e '10001,1140054d' /var/lib/mysql-files/yelp_tip.csv
-- run command below on mysql shell

load data INFILE '/var/lib/mysql-files/yelp_tip.csv' 
into table Tip 
fields terminated BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES
(text,date,likes,business_id,user_id);

