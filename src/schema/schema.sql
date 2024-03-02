DROP TABLE trades;
CREATE TABLE trades (
    id serial primary key,
    docId varchar(20) not null,
    firstName varchar(30),
    lastName  varchar(30),
    filingType  varchar(10),
    stateDst  varchar(10),
    year  varchar(4),
    filingDate varchar(10),
    trades varchar(10240)
);