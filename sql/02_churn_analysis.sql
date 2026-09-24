
-- ==========================================================
-- Bank Customer Churn - Analysis 
-- ==========================================================

-- 1. Segmentacja wiekowa klientów 
WITH CustomerAgeGroups AS (
    SELECT 
        CustomerId,
        Age,
        CAST(Exited AS INTEGER) AS Exited,
        CASE 
            WHEN Age < 30 THEN '1. Below 30'
            WHEN Age BETWEEN 30 AND 45 THEN '2. 30-45'
            WHEN Age BETWEEN 46 AND 60 THEN '3. 46-60'
            ELSE '4. Over 60'
        END AS age_group
    FROM bank_churn
)
SELECT 
    age_group,
    COUNT(*) AS total_customers,
    SUM(Exited) AS churned_customers,
    ROUND(AVG(Exited) * 100, 2) AS churn_rate_pct
FROM CustomerAgeGroups
GROUP BY age_group
ORDER BY age_group;


-- 2. Porównanie salda klienta ze średnim saldem w jego kraju 
WITH CustomerBalanceComparison AS (
    SELECT 
        CustomerId,
        Geography,
        Balance,
        CAST(Exited AS INTEGER) AS Exited,
        ROUND(AVG(CAST(Balance AS REAL)) OVER (PARTITION BY Geography), 2) AS avg_country_balance
    FROM bank_churn
)
SELECT 
    Geography,
    Exited,
    COUNT(*) AS customer_count,
    ROUND(AVG(CAST(Balance AS REAL)), 2) AS avg_customer_balance,
    avg_country_balance
FROM CustomerBalanceComparison
GROUP BY Geography, Exited, avg_country_balance
ORDER BY Geography, Exited;


-- 3. Podział klientów na 4 grupy salda i ich wskaźnik odejść
WITH BalanceQuartiles AS (
    SELECT 
        CustomerId,
        CAST(Balance AS REAL) AS Balance,
        CAST(Exited AS INTEGER) AS Exited,
        NTILE(4) OVER (ORDER BY CAST(Balance AS REAL) ASC) AS balance_quartile
    FROM bank_churn
)
SELECT 
    balance_quartile,
    ROUND(MIN(Balance), 2) AS min_balance,
    ROUND(MAX(Balance), 2) AS max_balance,
    COUNT(*) AS total_customers,
    SUM(Exited) AS churned_customers,
    ROUND(AVG(Exited) * 100, 2) AS churn_rate_pct
FROM BalanceQuartiles
GROUP BY balance_quartile
ORDER BY balance_quartile;