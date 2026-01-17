-- Pizza Time 
CREATE TABLE pizzas (name TEXT, open INTEGER, close INTEGER);

INSERT INTO pizzas VALUES
  ("Artichoke", 12, 15),
  ("La Val's", 11, 22),
  ("Sliver", 11, 20),
  ("Cheeseboard", 16, 23),
  ("Emilia's", 13, 18);

CREATE TABLE meals (meal TEXT, time INTEGER);

INSERT INTO meals VALUES
  ("breakfast", 11),
  ("lunch", 13),
  ("dinner", 19),
  ("snack", 22);

-- Pizza places that open before 1pm in alphabetical order
SELECT name from pizzas where open < 13 order by name DESC;

-- Pizza places and the duration of a study break that ends at 14 o'clock
SELECT name, max(14 - open, 0) as duration from pizzas order by duration DESC;

-- Pizza places that are open for late-night-snack time and when they close
  SELECT p.name || " closes at " || p.close AS status
  FROM pizzas p, meals m
  WHERE m.meal = "snack" and p.close >= m.time;

-- Two meals at the same place
  SELECT m1.meal AS first, m2.meal AS second, name
  FROM meals m1, meals m2, pizzas
  WHERE m1.meal < m2.meal
  AND m2.time - m1.time > 6
  AND pizzas.open <= m1.time AND pizzas.close >= m1.time
  AND pizzas.open <= m2.time AND pizzas.close >= m2.time;

--A Final Exam About Final Exams
CREATE TABLE finals AS
  SELECT "RSF" AS hall, "61A" as course UNION
  SELECT "Wheeler"    , "61A"           UNION
  SELECT "Pimentel"   , "61A"           UNION
  SELECT "Li Ka Shing", "61A"           UNION
  SELECT "RSF"        , "61B"           UNION
  SELECT "Wheeler"    , "61B"           UNION
  SELECT "Morgan"     , "61B"           UNION
  SELECT "Wheeler"    , "61C"           UNION
  SELECT "Pimentel"   , "61C"           UNION
  SELECT "Soda 306"   , "10"            UNION
  SELECT "RSF"        , "70";

CREATE TABLE sizes AS
  SELECT "RSF" AS room, 900 as seats    UNION
  SELECT "Wheeler"    , 700             UNION
  SELECT "Pimentel"   , 500             UNION
  SELECT "Li Ka Shing", 300             UNION
  SELECT "Morgan"     , 100             UNION
  SELECT "Soda 306"   , 80              UNION
  SELECT "Soda 310"   , 40              UNION
  SELECT "Soda 320"   , 30;

SELECT course, sum(seats) AS total
  FROM finals join sizes ON hall = room
  GROUP BY course HAVING count(room) >= 2;

SELECT f1.course, COUNT(DISTINCT f1.hall) AS shared
  FROM finals AS f1, finals AS f2
  WHERE f1.hall = f2.hall AND f1.course <> f2.course
  GROUP BY f1.course;