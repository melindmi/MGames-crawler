create table Games(id integer, title varchar(200), releaseDate varchar(20), primary key(id));
alter table Games convert to character set utf8 collate utf8_general_ci;

create table Platform(id integer auto_increment, name varchar(50) unique, primary key(id));
alter table Platform convert to character set utf8 collate utf8_general_ci;

create table GamePlatformRankScore(id integer auto_increment, gameId integer, platformId integer, rank float, score float, primary key(id), CONSTRAINT uniquekey UNIQUE(gameId, platformId), foreign key(gameId) references Games(id), foreign key(platformId) references Platform(id));
alter table GamePlatformRankScore convert to character set utf8 collate utf8_general_ci;

create table GamePublish(id integer auto_increment, gameId integer, publish varchar(100), primary key(id), CONSTRAINT uniquekey UNIQUE(gameId, publish), foreign key(gameId) references Games(id));
alter table GamePublish convert to character set utf8 collate utf8_general_ci;

create table GameDeveloped(id integer auto_increment, gameId integer, developed varchar(100), primary key(id), CONSTRAINT uniquekey UNIQUE(gameId, developed), foreign key(gameId) references Games(id));
alter table GameDeveloped convert to character set utf8 collate utf8_general_ci;

create table GameGenre(id integer auto_increment, gameId integer, genre varchar(50), primary key(id), CONSTRAINT uniquekey UNIQUE(gameId, genre), foreign key(gameId) references Games(id));
alter table GameGenre convert to character set utf8 collate utf8_general_ci;

create table GamePerspective(id integer auto_increment, gameId integer, perspective varchar(100), primary key(id), CONSTRAINT uniquekey UNIQUE(gameId, perspective), foreign key(gameId) references Games(id));
alter table GamePerspective convert to character set utf8 collate utf8_general_ci;

create table GameSport(id integer auto_increment, gameId integer, sport varchar(50), primary key(id), CONSTRAINT uniquekey UNIQUE(gameId, sport), foreign key(gameId) references Games(id));
alter table GameSport convert to character set utf8 collate utf8_general_ci;

create table GameNonSport(id integer auto_increment, gameId integer, nonsport varchar(50), primary key(id), CONSTRAINT uniquekey UNIQUE(gameId, nonsport), foreign key(gameId) references Games(id));
alter table GameNonSport convert to character set utf8 collate utf8_general_ci;

create table GameMisc(id integer auto_increment, gameId integer, misc varchar(100), primary key(id), CONSTRAINT uniquekey UNIQUE(gameId, misc), foreign key(gameId) references Games(id));
alter table GameMisc convert to character set utf8 collate utf8_general_ci;

create table GameAlternateTitle(id integer auto_increment, gameId integer, altTitle varchar(200), primary key(id), CONSTRAINT uniquekey UNIQUE(gameId, altTitle), foreign key(gameId) references Games(id));
alter table GameAlternateTitle convert to character set utf8 collate utf8_general_ci;

create table GamePartOfGroups(id integer auto_increment, gameId integer, partGroup varchar(200), primary key(id), CONSTRAINT uniquekey UNIQUE(gameId, partGroup), foreign key(gameId) references Games(id));
alter table GamePartOfGroups convert to character set utf8 collate utf8_general_ci;

create table GamePressSaysMain(id integer auto_increment, gameId integer, platformId integer, press varchar(200), score float, primary key(id), CONSTRAINT uniquekey UNIQUE(gameId, platformId, press, score), foreign key(gameId) references Games(id), foreign key(platformId) references Platform(id));
alter table GamePressSaysMain convert to character set utf8 collate utf8_general_ci;

create table GameReleaseInfo(id integer auto_increment, gameId integer, platformId integer, publish varchar(100), developed varchar(100), country varchar(25), releaseDate varchar(20), primary key(id), CONSTRAINT uniquekey UNIQUE(gameId, platformId, publish, developed, country, releaseDate), foreign key(gameId) references Games(id), foreign key(platformId) references Platform(id));
alter table GameReleaseInfo convert to character set utf8 collate utf8_general_ci;

create table GameRatingSys(id integer auto_increment, gameId integer, platformId integer, system varchar(100), value varchar(200), primary key(id), CONSTRAINT uniquekey UNIQUE(gameId, platformId, system), foreign key(gameId) references Games(id), foreign key(platformId) references Platform(id));
alter table GameRatingSys convert to character set utf8 collate utf8_general_ci;

create table GameRankScorePress(id integer auto_increment, gameId integer, platformId integer, press varchar(100), rankscore float, primary key(id), CONSTRAINT uniquekey UNIQUE(gameId, platformId, press), foreign key(gameId) references Games(id), foreign key(platformId) references Platform(id));
alter table GameRankScorePress convert to character set utf8 collate utf8_general_ci;

create table GameRankScoreUsers(id integer auto_increment, gameId integer, platformId integer, category varchar(100), score float, primary key(id), CONSTRAINT uniquekey UNIQUE(gameId, platformId, category), foreign key(gameId) references Games(id), foreign key(platformId) references Platform(id));
alter table GameRankScoreUsers convert to character set utf8 collate utf8_general_ci;
