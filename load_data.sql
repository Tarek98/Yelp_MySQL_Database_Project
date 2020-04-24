use YELP_DB;

-- ------------------------------------------
-- Insert raw data into temp tables        --
-- ------------------------------------------
load data INFILE '/var/lib/mysql-files/yelp_business.csv' 
into table BusinessTemp fields terminated BY ',' ENCLOSED BY '"' IGNORE 1 LINES
(business_id,name,@vNB,address,city,state,postal_code,latitude,longitude,stars,review_count,is_open,@vCategories) 
SET neighborhood = nullif(@vNB, ''), categories = left(@vCategories, length(@vCategories) - 1);

-- followers is VARCHAR(255) --> limit max 10 followers per user to make processing easier (see below 238 < 255 [varchar length])
-- user_id = '0njfJmB-7n84DlIgUByCNw'
-- 238 = len(user_id+', '+ 8*(user_id+', ') + user_id) 
load data INFILE '/var/lib/mysql-files/yelp_user.csv' 
into table UserTemp 
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY "\r\n" IGNORE 1 LINES 
(user_id,name,@vRC,@vYsince,@vFollowers,@vUseful,@vFunny,@vCool,@vFans,@dummy,average_stars,@dummy,@dummy,@dummy,@dummy,@dummy,@dummy,@dummy,@dummy,@dummy, @dummy, @dummy)
SET review_count = cast(@vRC as unsigned), useful = cast(@vUseful as unsigned), 
funny = cast(@vFunny as unsigned), cool = cast(@vCool as unsigned),
followers = left(@vFollowers, 238), yelping_since = @vYsince, last_online = @vYsince;

-- -------------------------------------------------------------------------
-- Move User & Business data from temp tables to normalized tables        --
-- -------------------------------------------------------------------------

-- Delete businesses that don't have a latitude or longitude value 
--   (only 1 exists --> business_id = 'W1x0rlzGUrMBbK3Hq5bk2Q') 
delete from BusinessTemp where latitude = '' or longitude = '';

-- Insert all distinct pairs of latitude and longitude, 
--   with their corresponding location details into AddressLocations table
insert into AddressLocations
select latitude, longitude, ANY_VALUE(neighborhood), ANY_VALUE(address), 
ANY_VALUE(city), ANY_VALUE(state), ANY_VALUE(postal_code)
from BusinessTemp
group by latitude, longitude;

insert into Business
select business_id, name, latitude, longitude, stars, review_count, is_open
from BusinessTemp;

-- "insert ignore" in stored procedure below, ensures we avoid issue (skip to next insert)
--   when there is a category list with repeated (duplicate) categories for the same business
drop procedure if exists split_categories;
delimiter ;;
create procedure split_categories()
begin
    DECLARE done int default FALSE; DECLARE x int default 0;
    DECLARE num_businesses int default 0; DECLARE num_categories int default 0;
    DECLARE bId varchar(23) default NULL; DECLARE category_list varchar(5000) default NULL;
    
    DECLARE cur1 CURSOR FOR 
        select business_id, 
        categories, length(categories) - length(replace(categories, ';', '')) + 1
        from BusinessTemp order by business_id;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    START TRANSACTION;
    OPEN cur1;

    business_loop: LOOP   
        FETCH cur1 INTO bId, category_list, num_categories;   
        IF done THEN
            LEAVE business_loop;
        END IF;

        SET x = 1;
        WHILE x <= num_categories DO
            insert ignore into BusinessCategories
            select bId, substring_index(substring_index(category_list, ';', x), ';', -1);
            
            set x = x + 1;
        END WHILE;
    END LOOP;

    CLOSE cur1;
    COMMIT;
end;;
delimiter ;

call split_categories();

-- BusinessTemp no longer needed, drop it
drop table BusinessTemp;

insert into User
select user_id, name, review_count, yelping_since, useful, funny, cool, average_stars, last_online
from UserTemp;

-- "insert ignore" in stored procedure below, ensures we avoid issue (skip to next insert)
--   when there is a follower user_id that doesn't exist in the user table
--   (e.g. a follower has deleted their account but that follower hasn't been removed) 
drop procedure if exists split_followers;
delimiter ;;
create procedure split_followers()
begin
    DECLARE done int default FALSE; DECLARE x int default 0;
    DECLARE num_users int default 0; DECLARE num_followers int default 0;
    DECLARE pId varchar(23) default NULL; DECLARE follower_list varchar(255) default NULL;
    
    DECLARE cur1 CURSOR FOR 
        select user_id, 
        followers, length(followers) - length(replace(followers, ',', '')) + 1
        from UserTemp where followers <> 'None';
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    START TRANSACTION;
    OPEN cur1;

    user_loop: LOOP   
        FETCH cur1 INTO pId, follower_list, num_followers;   
        IF done THEN
            LEAVE user_loop;
        END IF;

        SET x = 1;
        WHILE x <= num_followers DO
            insert ignore into UserFollowers
            select pId, substring_index(substring_index(follower_list, ', ', x), ', ', -1);
            
            set x = x + 1;
        END WHILE;
    END LOOP;

    CLOSE cur1;
    COMMIT;
end;;
delimiter ;

call split_followers();

-- UserTemp no longer needed, drop it
drop table UserTemp;
-- -----------------------------------------------------------------------------
-- Checkin, Review, and Tip tables are already normalized... Insert raw data  --
-- -----------------------------------------------------------------------------
load data INFILE '/var/lib/mysql-files/yelp_checkin.csv' ignore
into table Checkin fields terminated BY ',' IGNORE 1 LINES
(business_id,weekday,hour,checkins);

load data INFILE '/var/lib/mysql-files/yelp_review.csv' ignore
into table Review 
fields terminated BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES
(@rId,user_id,business_id,@vStars,date,@vText,@vUseful,@vFunny,@vCool)
SET stars  = cast(@vStars as unsigned), useful  = cast(@vUseful as unsigned),
text = left(@vText, 5000), funny = cast(@vFunny as unsigned), cool  = cast(@vCool as unsigned),
review_id = default;

load data INFILE '/var/lib/mysql-files/yelp_tip.csv' 
into table Tip 
fields terminated BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES
(text,date,likes,business_id,user_id);

