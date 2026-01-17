CREATE table newest AS
  SELECT title, year from titles order by year DESC limit 10;


CREATE table dog_movies AS 
  SELECT title, character from titles join principals on titles.tconst = principals.tconst where character like "%dog%";


CREATE table leads AS 
  SELECT name, count(*) as lead_roles from principals join names on principals.nconst = names.nconst where ordering = '1' group by names.nconst HAVING count(*) > 10;


CREATE table long_movies AS 
  SELECT (year / 10 * 10) || "s" as decade, count(*) as count from titles where runtime > 180 group by decade;

