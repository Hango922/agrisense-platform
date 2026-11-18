# Phase 1: reproducible local setup

Date: 2026-11-18 (Asia/Saigon).

## Scope and source plan

This implements phase 1 of the assessment agreed in the chat: make the existing
application installable, runnable and testable. Product expansion and the
business defects identified in phases 2-5 are outside this change.

The user requested ECC `tdd-workflow`. Journeys were derived from the chat,
not an external executable plan:

1. A developer can install the declared dependencies in a fresh Python 3.14
   virtualenv and initialize Django's MySQL backend and URL configuration.
2. A developer can run tests against MySQL without modifying the application
   database, writing test uploads into real media, or calling external AI.
3. A developer can migrate a fresh database, seed demo data, update segments,
   log in with the documented accounts and open the main demo pages.

## Changes

- `requirements.in` records pinned direct dependencies. `requirements.txt`
  resolves and pins 57 runtime distributions, including transitive packages.
- Django 6.1.2 and PyMySQL 1.2.3 replace the incompatible fresh-install pairing.
- `requirements-dev.txt` adds coverage tooling without making it a runtime
  dependency.
- `nongsan_project.test_settings` uses a unique MySQL test database per process,
  in-memory media, deterministic QR URLs, console logging and offline AI.
- `.env.example` documents blank AI keys, bank placeholders and the QR base URL.
  The unused `CHATBOT_MAX_TOKENS` example was removed; no model/token behavior
  was changed.
- README setup commands preserve an existing `.env`, consume committed
  migrations and describe the actual seed data and test configuration.

## RED/GREEN evidence

| Task | RED evidence | GREEN evidence | Checkpoints |
| --- | --- | --- | --- |
| Bootstrap dependency compatibility | The executed bootstrap test failed with `mysqlclient 2.2.1 or newer is required; you have 1.4.6` under PyMySQL 1.1.1. | The same final bootstrap test passes with the locked dependency set; `pip check` passes. | `95b3fe3`, `137f8a5` (RED); `f84c0dc` (GREEN) |
| Test environment isolation | Three executed tests failed because the requested local `test_settings` implementation did not exist. | All three tests pass after adding that settings module. | `86c5758` (RED); `dacc967` (GREEN) |

The initial bootstrap test ran the full Django system check with example
database credentials. Once dependency loading was fixed, this exposed an
unrelated authentication failure from those placeholders. The test was narrowed
to URL/bootstrap checks, which require no live database. Its final form was
rerun with PyMySQL 1.1.1 and failed for the original driver incompatibility
before restoring the fixed lock and verifying GREEN. Full system/model checks
were run separately with the configured MySQL credentials.

Commands actually run (from the repository root):

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_environment -v
.\.venv\Scripts\python.exe -m unittest tests.test_runtime -v
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
.\.venv\Scripts\python.exe manage.py test --settings=nongsan_project.test_settings --noinput
```

The first complete suite passed: `Ran 65 tests in 62.280s`, `OK`.
It includes the 60 pre-existing tests and five new tests.

## Test specification

| Guarantee | Test | Type |
| --- | --- | --- |
| Django initializes the MySQL backend and application URLs using the example configuration without requiring a migrated database | `tests.test_environment.EnvironmentTests.test_application_urls_boot_with_example_environment` | Bootstrap integration |
| Separate invocations choose distinct MySQL test databases and preserve the source database configuration | `tests.test_runtime.TestRuntimeTests.test_each_run_uses_a_distinct_mysql_test_database` | Process integration |
| Configured external API keys do not cause network calls in the test environment | `tests.test_runtime.TestRuntimeTests.test_ai_falls_back_even_when_real_keys_are_configured` | Process integration, network mocked |
| Test uploads can be read back without appearing in the real media directory | `tests.test_runtime.TestRuntimeTests.test_uploaded_test_files_do_not_touch_media_directory` | Storage integration |
| Freshly seeded data supports QR lookup, both demo logins, customer access restrictions, Dashboard and Excel export | `tests.test_bootstrap.DemoBootstrapTests.test_seeded_demo_supports_customer_and_admin_pages` | MySQL integration |

The seed smoke test verifies existing behavior and required setup commands;
it did not require a business-logic change or a manufactured RED failure.

## Clean environment verification

Final verification completed in a second temporary virtualenv with user site
packages disabled (`PYTHONNOUSERSITE=1`). It installed `requirements-dev.txt`,
which includes the complete runtime lock, without using global packages.

| Check | Observed result |
| --- | --- |
| Install locked runtime and development requirements | Exit 0 |
| `python -m pip check` | No broken requirements found |
| `python -m unittest tests.test_environment tests.test_runtime -v` | 4 tests, OK |
| `python manage.py check` | No issues |
| `python manage.py makemigrations --check --dry-run` | No changes detected |
| Full suite with the isolated test settings | 65 tests, OK, 63.953 seconds |
| Fresh MySQL migrations, seed, segment update and demo pages | Passed inside the full suite |

The test database and temporary validation virtualenv were removed afterwards.
The workspace `.venv` remains available.

## Coverage

The clean run collected branch coverage with:

```powershell
python -m coverage run --branch --source=apps,nongsan_project manage.py test --settings=nongsan_project.test_settings --noinput
python -m coverage json --data-file=tools/phase1-clean.coverage --omit="*/tests/*,*/migrations/*" -o tools/phase1-coverage.json
```

The orchestration set `COVERAGE_FILE=tools/phase1-clean.coverage` for the run.
The final report excludes test code and generated migrations. The README
equivalent omits them at collection time instead.

- Changed executable configuration, `nongsan_project/test_settings.py`: **100%**
  (11/11 statements; no branches).
- Application statements: **78.46%** (1650/2103).
- Application branches: **56.78%** (268/472).
- Combined application coverage: **74.49%**.

The ECC 80% aggregate target is not yet met across the existing application.
This is recorded as remaining regression work for phases 2-5, not reported as
a pass. Phase 1's new configuration is fully covered; changing unrelated
business flows merely to reach an aggregate percentage is outside the agreed
scope. No tests were skipped or disabled.

A separate development-server smoke check started `runserver --noreload` on a
free loopback port, fetched `/`, and verified HTTP 200 with AgriSense content.
The server was stopped afterwards. This is an HTTP smoke check, not browser
interaction or visual validation.

## Limits and preserved work

- The supported, verified setup here is Windows / Python 3.14.3 with the local
  MySQL server. A new test database is created; the MySQL service itself is not
  reinstalled. Other OS/Python combinations need their own verification.
- The test settings are opt-in via `--settings`; ordinary `manage.py test`
  still uses the original settings. Unique test database names are intended
  for disposable runs, not `--keepdb`.
- Real AI requests, bank settlement, browser flows, concurrency fixes and
  deployment hardening are not part of this phase.
- Existing untracked files under `docs/` and the user's `.env` were preserved.
  Only this new report is added from `docs/`.
- The new `.venv` is ignored by Git and remains available for local work.

## Checklist

- [x] Reproduce and fix the dependency bootstrap failure.
- [x] Pin direct and transitive runtime dependencies.
- [x] Document environment variables and local setup commands.
- [x] Add a repeatable, isolated MySQL test configuration.
- [x] Pass the original suite and new setup/isolation tests.
- [x] Verify seed commands and demo pages on a fresh test database.
- [x] Verify the development server responds over HTTP.
- [x] Complete second-clean-virtualenv verification and record coverage.
- [ ] Phase 2: authorization, CSRF and input/file validation.
- [ ] Phase 3: order status transitions, stock safety and repeated requests.
- [ ] Phase 4: QR consistency, AI deadlines, events, Excel safety and KPI rules.
- [ ] Phase 5: broader regression, browser/mobile verification, aggregate
  coverage of at least 80%, and handover.
