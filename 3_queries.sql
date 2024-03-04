
-- Query 1: Top 10 Fighters by Total Fights
-- This query returns the top 10 fighters with the highest number of fights.
SELECT Fighter_Name, COUNT(*) AS Total_Fights
FROM (
    SELECT R_fighter AS Fighter_Name FROM Fight
    UNION ALL
    SELECT B_fighter AS Fighter_Name FROM Fight
) AS All_Fights
GROUP BY Fighter_Name
ORDER BY Total_Fights DESC
LIMIT 10;

-- Query 2: Top 10 Average Significant Strike Percentages by Corner Color
-- This query provides the top 10 average significant strike percentages for each corner color (Red or Blue).
SELECT Color, AVG(SIG_STR_pct) AS Avg_SIG_STR_pct
FROM PerformanceMetrics
GROUP BY Color
ORDER BY Avg_SIG_STR_pct DESC
LIMIT 10;

-- Query 3: Top 10 Fighters with Most Wins
-- This query lists the top 10 fighters with the most wins.
SELECT Winner AS Fighter_Name, COUNT(*) AS Total_Wins
FROM Fight
WHERE Winner IS NOT NULL
GROUP BY Winner
ORDER BY Total_Wins DESC
LIMIT 10;

-- Query 4: Top 10 Fight Types by Average Last Round Duration
-- This query calculates the top 10 fight types with the longest average last round duration.
SELECT Fight_type, AVG(CAST(last_round_time AS FLOAT)) AS Avg_Last_Round_Duration
FROM Fight
GROUP BY Fight_type
ORDER BY Avg_Last_Round_Duration DESC
LIMIT 10;
