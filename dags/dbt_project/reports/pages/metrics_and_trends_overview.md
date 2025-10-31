---
title: Revenue & Customers Overview
description: Key metrics and trends for revenue and customer behavior
---

## Daily Orders and Revenue
```sql daily_orders_revenue
WITH daily AS (
  SELECT
    CAST(order_date AS DATE) AS order_date,
    COUNT(*) AS orders,
    SUM(CASE WHEN status = 'completed' THEN amount ELSE 0 END) AS revenue
  FROM jaffle_shop.orders
  GROUP BY 1
)
SELECT order_date, orders, revenue
FROM daily
ORDER BY order_date
```

<BarChart data={daily_orders_revenue} x=order_date y=orders y2=revenue type=line />

## Revenue by Status (Weekly)
```sql revenue_by_status_week
SELECT
  DATE_TRUNC('week', CAST(order_date AS DATE)) AS week,
  status,
  SUM(amount) AS revenue
FROM jaffle_shop.orders
GROUP BY 1, 2
ORDER BY 1, 2
```

<BarChart data={revenue_by_status_week} x=week y=revenue series=status type=area stack=true />

## New vs Repeat Revenue (Monthly)
```sql new_vs_repeat
WITH firsts AS (
  SELECT customer_id, MIN(CAST(order_date AS DATE)) AS first_order_date
  FROM jaffle_shop.orders
  GROUP BY 1
), labeled AS (
  SELECT
    DATE_TRUNC('month', CAST(o.order_date AS DATE)) AS month,
    CASE WHEN CAST(o.order_date AS DATE) = f.first_order_date THEN 'new' ELSE 'repeat' END AS cust_type,
    SUM(o.amount) AS revenue
  FROM jaffle_shop.orders o
  JOIN firsts f USING (customer_id)
  GROUP BY 1, 2
)
SELECT month, cust_type, revenue
FROM labeled
ORDER BY month, cust_type
```

<BarChart data={new_vs_repeat} x=month y=revenue series=cust_type type=column stack=true />
