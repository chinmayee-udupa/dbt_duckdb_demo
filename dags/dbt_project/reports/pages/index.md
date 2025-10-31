---
title: Ecommerce Overview
---

## KPIs
```sql kpis
WITH base AS (
  SELECT
    date_trunc('month', CAST(order_date AS DATE)) AS month,
    COUNT(*) AS orders,
    SUM(CASE WHEN status = 'completed' THEN amount ELSE 0 END) AS revenue
  FROM jaffle_shop.orders
  GROUP BY 1
)
SELECT
  SUM(orders) AS total_orders,
  SUM(revenue) AS total_revenue,
  AVG(CASE WHEN orders > 0 THEN revenue * 1.0 / orders ELSE NULL END) AS avg_order_value
FROM base
```

<BigValue 
  data={kpis} 
  value=total_revenue 
  fmt=usd
/>
<BigValue 
  data={kpis} 
  value=total_orders 
/>
<BigValue 
  data={kpis} 
  value=avg_order_value 
  fmt=usd
/>

---

## Daily Orders and Revenue
```sql daily
SELECT
  CAST(order_date AS DATE) AS order_date,
  COUNT(*) AS orders,
  SUM(CASE WHEN status = 'completed' THEN amount ELSE 0 END) AS revenue
FROM jaffle_shop.orders
GROUP BY 1
ORDER BY 1
```

<LineChart data={daily} x=order_date y=orders y2=revenue type=line />

## Top Customers by LTV
```sql top_customers
SELECT
  c.customer_id,
  c.first_name || ' ' || c.last_name AS customer_name,
  c.number_of_orders,
  c.customer_lifetime_value AS ltv,
  c.first_order,
  c.most_recent_order
FROM jaffle_shop.customers c
ORDER BY ltv DESC
LIMIT 20
```

<DataTable data={top_customers} />
