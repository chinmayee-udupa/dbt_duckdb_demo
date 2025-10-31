---
title: Payments Overview
---

## Payment Type by Spend over Month
```sql payment_mix
SELECT
  date_trunc('month', CAST(order_date AS DATE)) AS month,
  SUM(credit_card_amount) AS credit_card,
  SUM(coupon_amount) AS coupon,
  SUM(bank_transfer_amount) AS bank_transfer,
  SUM(gift_card_amount) AS gift_card,
  SUM(amount) AS total
FROM jaffle_shop.orders
GROUP BY 1
ORDER BY 1
```

<Chart data={payment_mix}>
  <Bubble 
      y=credit_card
      size=total
  />
  <Bubble 
      y=coupon
      size=total
  />
  <Bubble 
      y=bank_transfer
      size=total
  />
  <Bubble 
      y=gift_card
      size=total
  />
</Chart>
