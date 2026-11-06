# GIN SUSHI Restaurant OS

Separate public QR customer ordering and authenticated staff portals:

- `/ordine/?table=N&key=...`: QR customer menu and order history
- `/ordine/sala/`: waiter attendance, activation and movable room map
- `/ordine/cucina/?station=calda|frittura|sushi|maki|bar`: assigned kitchen stations
- `/ordine/uscita/`: quantities ready, service and undo
- `/ordine/cassa/`: authoritative menu/coperto or à-la-carte bill, externally received payment registration and closing
- `/ordine/admin/`: menu, service hours, accounts, orders/revenue reports, purchase/payroll records and QR codes

## Access

Sites supplies verified ChatGPT identity headers. `OWNER_EMAIL` is a secret runtime variable, configured in Sites rather than source. Each employee uses their own ChatGPT account; the owner enables the matching email, display name, role and stations. All write permissions and the scope of customer table tokens are enforced in the Worker. Changing client code cannot grant a role. Disabling an employee takes effect on their next API request. Customers do not need an account.

The public host serves menus/QR entry pages. Staff and business data require a recognized identity. Anonymous users do not receive staff, payroll, purchases, analytics, other tables or preparation instructions.

## Shared persistence

Cloudflare D1 binding `DB` holds normalized orders, receipts, purchases, payroll, operation IDs, audit entries and configuration. `BUCKET` holds uploaded images. The D1 migration is schema-only and included through Sites packaging. Initialization uses `OWNER_EMAIL` and starts with ordering disabled.

Mutations compare affected records, validate server-side rules, and use a versioned, conditional D1 batch to merge unrelated concurrent changes. Operation IDs make ordinary retries idempotent. Financial closing derives the total from stored attendance, menu rates and authoritative item prices; client totals are ignored. Receipt session IDs are unique. Open sessions are queried independently of calendar age. Completed records stay in their own tables for reports.

Clients poll shared state every 2 seconds. An unsuccessful network write is not confirmed. This version requires connectivity and does not queue offline orders.

## Required first configuration

The initial 18 dishes are the existing demonstration set, not a claim that the restaurant's complete menu has been entered. The owner must verify/import the complete current menu, enter adult/child lunch/dinner and coperto prices, enter à-la-carte dish prices, confirm real Europe/Rome service hours, add actual staff emails, and enable ordering. The default service hours are editable placeholders and are not confirmed opening times. Opening a table does not require rates; the customer then selects the menu allowed at the current server time. Dinner also supports à la carte.

Old device-local demo settings can be exported from the GitHub migration page and imported by the owner. Simulated historical orders/payments and accounts are not imported. Production databases are separate from the old localStorage demo.

Payroll is a private record of administrator-entered hours/amounts, not a payslip/tax contribution engine. Purchase records are not an automatic inventory valuation system. Cashier records externally received cash/POS/transfer payments; it does not charge cards, issue fiscal receipts, or integrate a fiscal register. Revenue reports count closed receipts, not net profit.

## Build and validation

`python3 scripts/build.py` embeds authored HTML, JS, CSS, the existing dish image payloads and vendored QR generator into a dependency-free Worker ESM at `dist/server/index.js`. The original menu images live in `worker/menu-source.json` so repeated builds are deterministic. `public/qr.js` vendors MIT-licensed qrcode-generator 2.0.4.

`node --test tests/*.test.mjs` checks role isolation, time windows, table activation, ingredient routing, shared order flow, partial completion/service, authoritative à-la-carte pricing, idempotent retry, independent concurrent updates, private records and UI workflows.

Deploy through the existing Sites project in `.openai/hosting.json`; never create a second project for this source. Source is synchronized through the Sites source workflow. Runtime values and credentials do not belong in this repository.
