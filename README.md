# Takealot API Pagination Issues

This repository contains reproducible examples of pagination issues encountered in the Takealot Seller API.

Each example includes:

* A clear reproduction script
* Steps to replicate
* Expected vs actual behaviour
* Real-world impact

---

# 🐞 Returns API Pagination Issue

## Steps to Reproduce

1. Add a valid API key to the request.
2. Execute a request to the Returns endpoint with filters that yield more than 50 results (e.g. using `return_date__gte` / `return_date__lte` with `limit=50`).
3. Capture the `continuation_token` from the initial response.
4. Make a follow-up request using the `continuation_token`.

---

## Expected Behaviour

The API should return the next page of results and continue pagination until all results are retrieved, without errors.

---

## Current Behaviour

The API returns a **500 Internal Server Error** when a request is made using the `continuation_token`.

---

## Additional Context

* Endpoint: `/v1/returns`
* Pagination Method: `continuation_token`
* Initial request succeeds
* Failure only occurs when using the continuation token

---

## Impact

This prevents reliable pagination and makes it impossible to retrieve complete datasets when results exceed the page limit.

---

# 🐞 Offers API Pagination Issue

## Steps to Reproduce

1. Add a valid API key to the request.
2. Execute the `fetch_offers.py` script.
3. The script performs:

   * Initial request with:

     * `limit=100`
     * `include_count=true`
     * `expands=takealot_warehouse_stock`
   * Subsequent requests using `continuation_token`
4. Observe pagination behaviour across pages.

---

## Expected Behaviour

The API should:

* Return a `continuation_token` on each page
* Continue pagination until **all results have been retrieved**

---

## Current Behaviour

* Page 1:

  * ✅ Returns results
  * ✅ Returns `continuation_token`

* Page 2:

  * ✅ Returns results
  * ❌ Does **NOT** return a `continuation_token`

* Pagination stops prematurely despite more data existing.

---

## Proof of Issue

The API returns a total count (via `include_count=true`) that is significantly higher than the number of items actually retrieved.

Example:

* Reported total: ~1000 offers
* Retrieved via pagination: ~200 offers (2 pages only)

This confirms that pagination terminates early and results are incomplete.

---

## Additional Context

* Endpoint: `/v1/offers`
* Pagination Method: `continuation_token`
* Page size: 100
* Script compares:

  * API reported `count`
  * Total fetched records

This is not a failure of the second request — it succeeds, but **pagination stops incorrectly**.

---

## Impact

* Incomplete offer data retrieval
* Broken integrations relying on full datasets
* Inaccurate reporting and analytics
* Reduced trust in API reliability

---

## 🎯 Summary

Both issues relate to incorrect handling of `continuation_token` pagination:

* **Returns API** → Hard failure (500 error)
* **Offers API** → Silent failure (early termination)

These issues make it impossible to reliably retrieve complete datasets from the API.

---

## 👤 Author

Jeremy Quinton
Cape Town, South Africa

