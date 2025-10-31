---
title: Creative Sales Overview
description: KPIs, multi-series area chart and revenue distribution widgets
---

```sql kpi
select
  sum(amount) as total_revenue,
  count(distinct order_id) as total_orders,
  count(distinct customer_id) as active_customers,
  avg(amount) as avg_order_value
from jaffle_shop.orders
```

```sql series
select
  order_date::date as day,
  sum(amount) as revenue,
  count(*) as orders
from jaffle_shop.orders
group by day
order by day
```

## Revenue and Orders (Area + Line)

<AreaChart data={series} x="day" y="revenue" stacked={false} />
<LineChart data={series} x="day" y="orders" />
