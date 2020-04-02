use YELP_DB;

load data INFILE '/var/lib/mysql-files/yelp_business.csv' 
into table Business fields terminated BY ',' IGNORE 1 LINES
(business_id,name,@vNB,address,lgID,G,@vAB,@vR,@vH,@v2B,@v3B,@vHR,@vRBI,@vSB,@vCS,@vBB,@vSO,@vIBB,@vHBP,@vSH,@vSF,GIDP) 
SET AB = nullif(@vAB, ''), R = nullif(@vR, ''), H = nullif(@vH, ''),
    SB = nullif(@vSB, ''), CS = nullif(@vCS, ''), IBB = nullif(@vIBB,''),
    HBP = nullif(@vHBP, ''),SH = nullif(@vSH, ''),SF = nullif(@vSF, ''),
    2B = nullif(@v2B, ''), 3B = nullif(@v3B, ''), HR = nullif(@vHR, ''),
    RBI = nullif(@vRBI, ''), SO = nullif(@vSO, ''), BB = nullif(@vBB, '');

