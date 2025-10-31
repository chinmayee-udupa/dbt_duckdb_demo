---
title: Sales Overview
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

## Revenue and Orders over Time

<BarChart data={series} x="day" y="orders" y2="revenue" xAxisTitle="Order Date" y2Fmt=usd />
<LineChart data={series} x="day" y="orders" y2="revenue" y2SeriesType=bar xAxisTitle="Order Date" y2Fmt=usd yAxisTitle="Total Orders" y2AxisTitle="Revenue" markers=true/>


```sql heatmap
select
  dayofmonth(cast(order_date as date)) as monthday,
  month(cast(order_date as date)) as month,
  count(*) as orders,
  sum(amount) as revenue
from jaffle_shop.orders
group by monthday, month
order by monthday, month
```

# Sales heatmap: Day of month vs monthly sales intensity

<Heatmap data={heatmap} 
    x="monthday" 
    y="month" 
    xSort="monthday"
    ySort="month"
    value="orders" 
    valueFmt=usd
    title="Orders Heatmap"
    subtitle="By Day vs Month"
    rightPadding=40
    cellHeight=25
/>
