# AI planner verification — 19/11/2026

## Delivered behavior

`POST /products/planner/` now calls the configured AI provider. Gemini uses
`PLANNER_GEMINI_MODEL` (default `gemini-3.1-flash-lite`); Groq uses `GROQ_MODEL`.
The request includes the user's wish, budget, household size, number of days,
preference and up to 120 available catalog items with price, unit and description.
No account profile, order history, address or credentials are included in the prompt.

AI returns JSON containing product IDs, integer quantities, reasons, meal ideas
and assumptions. The server rejects unknown/duplicate IDs, invalid quantities,
unavailable stock, inactive products and totals exceeding the budget including
shipping. Prices and stock are read again after the API call. Sentences containing
monetary amounts in AI explanations are omitted; the server computes displayed totals.
The existing signed proposal and cart validation remain in use.

The interface distinguishes AI suggestions from rule-based fallback, shows reasons
and meal ideas, and disables repeated submission while waiting. Provider errors,
timeouts and malformed results fall back with an explicit warning. When request
rate limiting is enabled, planner POSTs are limited to five per IP per minute.

## Verification results

| Check | Result | Evidence |
| --- | --- | --- |
| Django check / Python syntax | PASS | No Django system-check issues; changed Python parses successfully |
| Migration consistency | PASS | `makemigrations --check --dry-run`: no changes |
| Lint, changed Python | PASS | Ruff: ai_planner, discovery_views, rate_limit, new tests, settings |
| Lint, whole working directory | FAIL | 274 findings, including skill/tool scripts; 89 under application/tests paths |
| Types, whole working directory | FAIL | Pyright: 1,282 errors and 1 warning across 272 files |
| Types, four affected Python modules/tests | FAIL | 22 errors, including Django dynamic ORM managers, existing response and decorator typing |
| Full regression suite | PASS | 162/162 tests; `logs/planner-final-tests.log` |
| Overall branch-inclusive coverage | PASS | 82.22%, excluding tests/migrations; `logs/planner-final-coverage.json` |
| New AI planner coverage | PASS | 87.80% |
| Security review of changes | PASS (limited scope) | No key-pattern matches in five reviewed Python files; keys in headers, no raw provider error logging; escaped template output |
| Real Gemini request | VERIFIED | `gemini-3.1-flash-lite` returned generated content and a valid catalog proposal |
| Browser form submission | VERIFIED | 4 people, 1 day, budget 500,000 VND: AI meal ideas, 8 product rows, server total 357,000 VND including delivery, remaining 143,000 VND |
| Production deployment | NOT PERFORMED | Only local server at 127.0.0.1:8000 |

The 13 new tests cover provider transports, missing credentials, timeout fallback,
displayed AI/fallback status, escaping, server totals, misleading AI monetary text,
invalid IDs/quantities/duplicates, budget including delivery, and changed price/stock.
The existing cart, order and concurrency regressions also pass.

## Live provider findings

- Existing chatbot model `gemini-2.5-flash` returns HTTP 404: unavailable to new users.
  The planner has a separate verified model setting; chatbot settings were not changed.
- `gemini-flash-latest` and `gemini-3.8-flash` timed out in probes. They are not used
  by the delivered planner.
- Groq returned HTTP 401 `invalid_api_key`. Its transport is unit-tested, but real
  Groq acceptance is FAIL until credentials are replaced locally.
- A first successful Gemini proposal contained incorrect arithmetic in its prose.
  A regression and server-side explanation filtering were added before the final run.
  Final browser output displayed server-computed totals without that arithmetic claim.

## Limits and follow-up

- Overall status: local Gemini feature works; repository-wide quality gates are NOT READY.
  Resolve the recorded type/lint errors before declaring the whole repository clean.
- AI meal/portion quality is not clinically or nutritionally validated. Product units
  are integer sale units, some bundle weights are absent, and the catalog lacks meat,
  fish and eggs. The live response explicitly identified missing protein sources.
- Human review of portions, allergies, substitutions and real package weights remains
  necessary. API use does not establish complete or nutritionally accurate meal plans.
- The chatbot's budget shortcut still uses its existing rule-based basket function;
  this change integrates AI into the planner page requested in the screenshot.
- Provider availability, future quotas, load testing, mobile browser behavior and a
  logged-in browser checkout were not verified in this change. Cart validation is
  covered by the regression suite; no real order was placed during browser verification.
- Browser tool export of screenshots/JSON to the workspace was denied by that tool's
  configured roots. The result was inspected in the live browser; no screenshot file
  is claimed as a saved artifact.

## Reproduce

```powershell
.venv/Scripts/python.exe manage.py check
.venv/Scripts/python.exe manage.py makemigrations --check --dry-run
.venv/Scripts/python.exe -m ruff check apps/products/ai_planner.py apps/products/discovery_views.py apps/accounts/rate_limit.py apps/products/tests/test_ai_planner.py nongsan_project/settings.py
.venv/Scripts/python.exe -m coverage run --data-file=logs/planner-final.coverage --branch --source=apps,nongsan_project --omit="*/tests/*,*/migrations/*" manage.py test --settings=nongsan_project.test_settings --noinput
.venv/Scripts/python.exe -m coverage report --data-file=logs/planner-final.coverage --precision=2
```

Test settings leave both API keys empty: automated tests cannot charge the real API.
Live verification uses the existing local Gemini credential, never stored in this report.
