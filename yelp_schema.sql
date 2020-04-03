drop database if exists YELP_DB;
create database YELP_DB;

use YELP_DB;

drop table if exists `BusinessTemp`;
create table `BusinessTemp` (
    `business_id` varchar(22) default null,
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
    `user_id` varchar(22) default null,
    `name` varchar(50) default null,
    `review_count` int unsigned default null,
    `yelping_since` varchar(10) default null,
    `friends` varchar(5000) default null,
    `useful` int unsigned default null,
    `funny` int unsigned default null,
    `cool` int unsigned default null,
    `fans` int unsigned default null,
    `average_stars` decimal(3,2) default null,
    `last_online` varchar(10) default null
);


-----------------------------------
-- New Tables                    --
-----------------------------------

drop table if exists `Business`;
create table `Business` (
    `business_id` varchar(22) default null,
    `name` varchar(255) default null,
    `latitude` varchar(255) default null,
    `longitude` varchar(255) default null,
    `stars` varchar(255) default null,
    `review_count` int default null,
    `is_open` int default null,
);

drop table if exists `BusinessCategories`;
create table `BusinessCategories` (
    `business_id` varchar(22) default null,
    `category` varchar(100) default null
);

drop table if exists `BusinessFollowers`;
create table `BusinessFollowers` (
    `business_id` varchar(30) default null,
    `user_id` varchar(30) default null
);

drop table if exists `AddressLocations`;
create table `AddressLocations` (
    `latitude` varchar(255) default null,
    `longitude` varchar(255) default null,
    `neighborhood` varchar(255) default null,
    `address_number` varchar(255) default null,    
    `address_name` varchar(255) default null,
    `city` varchar(255) default null,
    `state` varchar(255) default null,
    `postal_code` varchar(10) default null,
)

drop table if exists `Checkin`;
create table `Checkin` (
    `business_id` varchar(30) default null,
    `weekday` varchar(3) default null,
    `hour` varchar(5) default null,
    `checkins` int default null
);

drop table if exists `User`;
create table `User` (
    `user_id` varchar(22) default null,
    `name` varchar(50) default null,
    `review_count` int unsigned default null,
    `yelping_since` varchar(10) default null,
    `useful` int unsigned default null,
    `funny` int unsigned default null,
    `cool` int unsigned default null,
    `fans` int unsigned default null,
    `average_stars` decimal(3,2) default null,
    `last_online` varchar(10) default null
);

drop table if exists `UserFriends`;
create table `UserFriends` (
    `user_id` varchar(30) default null,
    `friend_id` varchar(30) default null
);

drop table if exists `Review`;
create table `Review` (
    `review_id` varchar(30) default null,
    `user_id` varchar(30) default null,
    `business_id` varchar(30) default null,
    `stars` int default null,
    `date` varchar(12) default null,
    `text` varchar(5000) default null,
    `useful` int default null,
    `funny` int default null,
    `cool` int default null
);

drop table if exists `Tip`;
create table `Tip` (
    `text` varchar(5000) default null,
    `date` varchar(10) default null,
    `likes` int default null,
    `business_id` varchar(30) default null,
    `user_id` varchar(30) default null
);