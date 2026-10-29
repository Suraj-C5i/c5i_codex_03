# Bounded task cards

## CART-T1: coupon calculation

- Repo: `cart_service`
- Requirements: CART-01, CART-02, CART-03
- Scope: add coupon calculation while preserving `calculate_total(items)` and numeric output.
- Before edit: inspect the existing contract; use full precision without rounding and timezone-aware UTC timestamps.
- Required evidence: valid code; case-insensitive match; activation boundary; exact-expiry and after-expiry eligibility; percentage bounds; full precision; cap; zero floor; regression on old API; no dependency change.
- Stop condition: timestamp interpretation is ambiguous or implementation requires a new public contract.
- Out of scope: tax, shipping, UI, database, payment provider.

## NOTIF-T1: bounded transient retry

- Repo: `notification_service`
- Requirements: NOTIF-01, NOTIF-02, NOTIF-03
- Scope: retry only the approved temporary exception, maximum three total sends, waits of one and two seconds between attempts.
- Required evidence: immediate success; temporary then success; three temporary failures; permanent 4xx once; exact delays; fake sender/sleeper; unchanged interface.
- Stop condition: error classification is not explicit or retry behavior would change the public sender contract.
- Out of scope: provider integration, persistence, production sending, distributed delivery guarantees.

## Independence check

These can run in parallel after requirements and cross-cutting review rules are agreed because they use separate repositories and do not modify a shared interface. If both tasks need a shared library, schema, or contract change, resolve that dependency first or serialize the work.
