
drop database if exists YELP_DB;
create database YELP_DB;

use YELP_DB;

drop table if exists `BusinessTemp`;
create table `BusinessTemp` (
    `business_id` varchar(23) default null,
    `name` varchar(255) default null,
    `neighborhood` varchar(255) default null,
    `address` varchar(255) default null,
    `city` varchar(255) default null,
    `state` varchar(255) default null,
    `postal_code` varchar(10) default null,
    `latitude` varchar(255) default null,
    `longitude` varchar(255) default null,
    `stars` varchar(255) default null,
    `review_count` int default null,
    `is_open` int default null,
    `categories` varchar(5000) default null
);

drop table if exists `UserTemp`;
create table `UserTemp` (
    `user_id` varchar(23) default null,
    `name` varchar(50) default null,
    `review_count` int unsigned default null,
    `yelping_since` varchar(10) default null,
    `followers` varchar(255) default null,
    `useful` int unsigned default null,
    `funny` int unsigned default null,
    `cool` int unsigned default null,
    `fans` int unsigned default null,
    `average_stars` decimal(3,2) default null,
    `last_online` varchar(10) default null
);

-- ---------------------------------
-- New Tables (Normalized)        --
-- ---------------------------------
drop table if exists `AddressLocations`;
create table `AddressLocations` (
    `latitude` decimal(16,13) not null,
    `longitude` decimal(16,13) not null,
    `neighborhood` varchar(50) default null,
    `address` varchar(255) default null,
    `city` varchar(50) default null,
    `state` varchar(3) default null,
    `postal_code` varchar(10) default null,
    primary key (latitude, longitude)
);

drop table if exists `Business`;
create table `Business` (
    `business_id` varchar(23) not null,
    `name` varchar(100) default null,
    `latitude` decimal(16,13) default null,
    `longitude` decimal(16,13) default null,
    `stars` decimal(2,1) default null,
    `review_count` int default null,
    `is_open` boolean default null,
    primary key (business_id),
    foreign key (latitude, longitude) references AddressLocations(latitude, longitude)
);

drop table if exists `BusinessCategories`;
create table `BusinessCategories` (
    `business_id` varchar(23) not null,
    `category` varchar(100) not null,
    primary key (category, business_id),
    foreign key (business_id) references Business(business_id)
);

drop table if exists `User`;
create table `User` (
    `user_id` varchar(23) not null,
    `name` varchar(50) default null,
    `review_count` smallint unsigned default null,
    `yelping_since` varchar(10) default null,
    `useful` int unsigned default null,
    `funny` int unsigned default null,
    `cool` int unsigned default null,
    `average_stars` decimal(3,2) default null,
    `last_online` varchar(10) default null,
    primary key (user_id)
);

drop table if exists `CategoryFollowers`;
create table `CategoryFollowers` (
    `category` varchar(100) not null,
    `user_id` varchar(23) not null,
    primary key (category, user_id),
    foreign key (category) references BusinessCategories(category),
    foreign key (user_id) references User(user_id)
);

drop table if exists `BusinessFollowers`;
create table `BusinessFollowers` (
    `business_id` varchar(23) not null,
    `user_id` varchar(23) not null,
    primary key (business_id, user_id),
    foreign key (business_id) references Business(business_id),
    foreign key (user_id) references User(user_id)
);

drop table if exists `Checkin`;
create table `Checkin` (
    `business_id` varchar(23) not null,
    `weekday` varchar(3) not null,
    `hour` varchar(5) not null,
    `checkins` int default null,
    primary key (business_id, weekday, hour),
    foreign key (business_id) references Business(business_id)
);

drop table if exists `UserFollowers`;
create table `UserFollowers` (
    `user_id` varchar(23) not null,
    `follower_id` varchar(23) not null,
    primary key (user_id, follower_id),
    foreign key (user_id) references User(user_id),
    foreign key (follower_id) references User(user_id)
);

drop table if exists `Review`;
create table `Review` (
    `review_id` varchar(23) not null,
    `user_id` varchar(23) default null,
    `business_id` varchar(23) default null,
    `stars` decimal(3,2) default null,
    `date` varchar(10) default null,
    `text` varchar(5000) default null,
    `useful` int unsigned default null,
    `funny` int unsigned default null,
    `cool` int unsigned default null,
    primary key (review_id),
    foreign key (user_id) references User(user_id),
    foreign key (business_id) references Business(business_id)
);

drop table if exists `Tip`;
create table `Tip` (
    `tip_id` int not null auto_increment,
    `text` varchar(500) default null,
    `date` varchar(10) default null,
    `likes` smallint default null,
    `business_id` varchar(23) default null,
    `user_id` varchar(23) default null,
    primary key (tip_id),
    foreign key (business_id) references Business(business_id),
    foreign key (user_id) references User(user_id)
);