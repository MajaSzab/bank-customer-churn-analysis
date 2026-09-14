
-- 1. Ogólna liczba klientów, liczba odejść i wskaźnik Churn Rate (%)
SELECT 
    COUNT(*) AS total_customers,
    SUM(CAST(Exited AS INTEGER)) AS churned_customers,
    ROUND(AVG(CAST(Exited AS REAL)) * 100, 2) AS churn_rate_pct
FROM bank_churn;

-- 2. Churn Rate według kraju (Geography)
SELECT 
    Geography,
    COUNT(*) AS total_customers,
    SUM(CAST(Exited AS INTEGER)) AS churned_customers,
    ROUND(AVG(CAST(Exited AS REAL)) * 100, 2) AS churn_rate_pct
FROM bank_churn
GROUP BY Geography
ORDER BY churn_rate_pct DESC;

-- 3. Churn Rate według płci (Gender)
SELECT 
    Gender,
    COUNT(*) AS total_customers,
    SUM(CAST(Exited AS INTEGER)) AS churned_customers,
    ROUND(AVG(CAST(Exited AS REAL)) * 100, 2) AS churn_rate_pct
FROM bank_churn
GROUP BY Gender
ORDER BY churn_rate_pct DESC;