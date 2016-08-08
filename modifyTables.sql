create table PublishId as (select @rownum:=@rownum+1 id, publish from (select distinct publish from GamePublish) s , (select @rownum:=0) r);
alter table GamePublish add publishId int(11);
update GamePublish p set publishId=(select t.id from PublishId t where t.publish=p.publish);

create table GenreId as (select @rownum:=@rownum+1 id, genre from (select distinct genre from GameGenre) s , (select @rownum:=0) r);
alter table GameGenre add genreId int(11);
update GameGenre p set genreId=(select t.id from GenreId t where t.genre=p.genre);

create table MiscId as (select @rownum:=@rownum+1 id, misc from (select distinct misc from GameMisc) s , (select @rownum:=0) r);
alter table GameMisc add miscId int(11);
update GameMisc p set miscId=(select t.id from MiscId t where t.misc=p.misc);

create table NonSportId as (select @rownum:=@rownum+1 id, nonsport from (select distinct nonsport from GameNonSport) s , (select @rownum:=0) r);
alter table GameNonSport add nonsportId int(11);
update GameNonSport p set nonsportId=(select t.id from NonSportId t where t.nonsport=p.nonsport);

create table PerspectiveId as (select @rownum:=@rownum+1 id, perspective from (select distinct perspective from GamePerspective) s , (select @rownum:=0) r);
alter table GamePerspective add perspectiveId int(11);
update GamePerspective p set perspectiveId=(select t.id from PerspectiveId t where t.perspective=p.perspective);

create table PartGroupId as (select @rownum:=@rownum+1 id, partGroup from (select distinct partGroup from GamePartOfGroups) s , (select @rownum:=0) r);
alter table GamePartOfGroups add partGroupId int(11);
update GamePartOfGroups p set partGroupId=(select t.id from PartGroupId t where t.partGroup=p.partGroup);

create table PressId as (select @rownum:=@rownum+1 id, press from (select distinct press from GameRankScorePress) s , (select @rownum:=0) r);
alter table GameRankScorePress add pressId int(11);
alter table GamePressSaysMain add pressId int(11);
update GameRankScorePress p set pressId=(select t.id from PressId t where t.press=p.press);
update GamePressSaysMain p set pressId=(select t.id from PressId t where t.press=p.press);

create table RatingSysId as (select @rownum:=@rownum+1 id, system from (select distinct system from GameRatingSys) s , (select @rownum:=0) r);
alter table GameRatingSys add systemId int(11);
update GameRatingSys p set systemId=(select t.id from RatingSysId t where t.system=p.system);

alter table GameReleaseInfo add publishId int(11);
alter table GameReleaseInfo add developedId int(11);
update GameReleaseInfo p set publishId=(select t.id from PublishId t where t.publish=p.publish);
update GameReleaseInfo p set developedId=(select t.id from DevelopedId t where t.developed=p.developed);

