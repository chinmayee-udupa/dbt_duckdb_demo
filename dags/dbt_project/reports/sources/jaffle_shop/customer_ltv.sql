select
  c.customer_id,
  count(distinct o.order_id) as orders_count,
  sum(o.amount) as total_spent,
  min(o.order_date) as first_order,
  max(o.order_date) as last_order
from marts.marts_customers c
left join marts.marts_orders o on c.customer_id = o.customer_id
group by c.customer_id
order by total_spent desc
limit 200;