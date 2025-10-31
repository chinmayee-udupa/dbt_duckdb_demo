---
title: Customers & Retention
---

## Customer Growth (Monthly New Customers)
```sql new_customers
SELECT
  date_trunc('month', CAST(first_order AS DATE)) AS month,
  COUNT(*) AS new_customers
FROM jaffle_shop.customers
GROUP BY 1
ORDER BY 1
```

<LineChart data={new_customers} x=month y=new_customers />

## Active Customers by Month
```sql active_customers
SELECT
  date_trunc('month', CAST(most_recent_order AS DATE)) AS month,
  COUNT(*) AS active_customers
FROM jaffle_shop.customers
GROUP BY 1
ORDER BY 1
```

<LineChart data={active_customers} x=month y=active_customers />
