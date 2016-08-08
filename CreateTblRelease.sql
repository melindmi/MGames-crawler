create table ReleaseIdGamePlatform(relId integer, gameId integer, platformId integer, primary key(relId));
create table ReleasePublish(relId integer, publishId integer, primary key(relId, publishId));
create table ReleaseDeveloped(relId integer, developedId integer, primary key(relId, developedId));
create table ReleaseCountry(relId integer, country varchar(25), primary key(relId, country));
create table ReleaseDate(relId integer, date varchar(20), primary key(relId, date));

update table set email=replace(email,char(160),'');

-- if the tables are UTF 8
update PublishId set publish=replace(publish,char(49824),' ');
