---
title: Customer lifetime value
description: LTV and recency-frequency charts
---

```sql ltv
select
  customer_id,
  orders_count,
  total_spent,
  first_order,
  last_order
from (select * from jaffle_shop.customer_ltv) t
```

<Grid columns={2}> 
<BarChart data={ltv} x="customer_id" y="total_spent" maxItems={10} rotateLabels={true} /> 
<ScatterPlot data={ltv} x="orders_count" y="total_spent" /> </Grid> 
<DataTable data={ltv} />
