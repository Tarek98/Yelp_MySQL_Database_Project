create database YELP_DB;

use YELP_DB;

drop table if exists `Business`;
create table `Business` (
    `business_id` varchar(30) default null,
    `name` varchar(255) default null,
    `neighborhood` varchar(255) default null,
    `address` varchar(255) default null,
    `city` varchar(255) default null,
    `state` varchar(2) default null,
    `postal_code` varchar(10) default null,
    `latitude` decimal(20, 18) default null,
    `longitude` decimal(20, 17) default null,
    `stars` decimal(2,1) default null,
    `review_count` int default null,
    `is_open` boolean default null,
    `categories` varchar(1000) default null
);

drop table if exists `Checkin`;
create table `Checkin` (
    `business_id` varchar(30) default null,
    `weekday` varchar(3) default null,
    `hour` varchar(5) default null,
    `checkins` int default null
);

drop table if exists `User`;
create table `User` (
    `user_id` varchar(30) default null,
    `name` varchar(255) default null,
    `review_count` int default null,
    `yelping_since` varchar(10) default null,
    `friends` varchar(5000) default null,
    `useful` int default null,
    `funny` int default null,
    `cool` int default null,
    `fans` int default null,
    `elite` varchar(255) default null,
    `average_stars` decimal(3,2) default null,
    `last_online` varchar(10) default null
);

drop table if exists `BusinessFollowers`;
create table `BusinessFollowers` (
    `business_id` varchar(30) default null,
    `user_id` varchar(30) default null
);

drop table if exists `Review`;
create table `Review` (
    `review_id` varchar(30) default null,
    `user_id` varchar(30) default null,
    `business_id` varchar(30) default null,
    `stars` int default null,
    `date` varchar(10) default null,
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
