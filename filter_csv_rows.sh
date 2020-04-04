#REASON for filtering rows is that some text values at the end
#  contain many unescaped characters such as neseted quotation marks

#Delete all lines after 2,000,000 till end of yelp_review.csv file (line 17746269)
#  and backup original file to yelp_review.csv.bak
sed -i.bak -e '2000001,17746269d' /var/lib/mysql-files/yelp_review.csv

#Delete all lines after 10,000 till end of yelp_tip.csv file (line 1140054)
#  and backup original file to yelp_tip.csv.bak
sed -i.bak -e '10001,1140054d' /var/lib/mysql-files/yelp_tip.csv
