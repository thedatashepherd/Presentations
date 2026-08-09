# Contoso10K — Sales Analytics Project

## Overview

This project delivers a suite of sales performance reports and KPIs for the Contoso retail business using the **Contoso10K** SQL Server database. The database covers 10,000 orders across multiple store locations, product categories, and customer segments.

---

## Database

| Property | Value |
|---|---|
| Server | localhost (Docker) |
| Database | Contoso10K |
| Schema | `[Data]` |
| Auth | SQL Server Authentication |

---

## Tables

| Table | Type | Description |
|---|---|---|
| `[Data].[Orders]` | Fact | Header-level order records |
| `[Data].[OrderRows]` | Fact | Line-item detail per order |
| `[Data].[Customer]` | Dimension | Customer profile and location |
| `[Data].[Product]` | Dimension | Product catalog with category hierarchy |
| `[Data].[Store]` | Dimension | Store locations and metadata |
| `[Data].[Date]` | Dimension | Calendar table for time intelligence |
| `[Data].[GeoLocations]` | Dimension | City, state, country lookup |
| `[Data].[CurrencyExchange]` | Reference | Daily exchange rates for multi-currency orders |

---

## Report Requirements

### REQ-001 — Sales Summary by Month
- Total revenue, total orders, and average order value by month
- Compare current year vs prior year
- Filter by store, product category, and channel

### REQ-002 — Top Products Report
- Top 20 products by revenue for a given date range
- Include units sold, revenue, and margin %
- Highlight products where margin % is below 15%

### REQ-003 — Customer Segmentation
- Group customers by total lifetime spend: Bronze / Silver / Gold / Platinum
- Include order frequency and average order value per segment
- Geographic breakdown by country and state

### REQ-004 — Store Performance Dashboard
- Revenue per store with month-over-month trend
- Revenue per square foot (where available)
- Flag stores with declining revenue for 3+ consecutive months

### REQ-005 — Currency Exposure Report
- Orders broken down by currency
- Apply `[Data].[CurrencyExchange]` rates to normalize to USD
- Show impact of exchange rate fluctuations on reported revenue

---

## Key Metrics

```sql
-- Total Revenue
SUM(OrderRows.TotalAmount)

-- Average Order Value
SUM(OrderRows.TotalAmount) / COUNT(DISTINCT Orders.OrderKey)

-- Gross Margin %
(SUM(OrderRows.TotalAmount) - SUM(OrderRows.UnitCost * OrderRows.Quantity)) 
    / SUM(OrderRows.TotalAmount)
```

---

## Notes

- The `[Data].[Date]` table should be used for **all** date filtering — do not filter directly on `OrderDate`
- Currency normalization should always reference the exchange rate on the **order date**, not today's rate
- `[Data].[GeoLocations]` is shared between `Customer` and `Store` — join carefully to avoid fan traps

---

## Status

| Report | Owner | Status |
|---|---|---|
| REQ-001 Sales Summary | TBD | 🔴 Not Started |
| REQ-002 Top Products | TBD | 🔴 Not Started |
| REQ-003 Customer Segmentation | TBD | 🟡 In Progress |
| REQ-004 Store Performance | TBD | 🔴 Not Started |
| REQ-005 Currency Exposure | TBD | 🟡 In Progress |
