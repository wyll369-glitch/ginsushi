CREATE TABLE restaurant_state (id INTEGER PRIMARY KEY CHECK(id=1), version INTEGER NOT NULL DEFAULT 0, last_commit TEXT NOT NULL DEFAULT '', payload TEXT NOT NULL);
--> statement-breakpoint
CREATE TABLE order_records (id TEXT PRIMARY KEY, business_date TEXT NOT NULL, table_no INTEGER NOT NULL, session_id TEXT NOT NULL, closed INTEGER NOT NULL DEFAULT 0, created_ms INTEGER NOT NULL, payload TEXT NOT NULL);
--> statement-breakpoint
CREATE INDEX order_records_open_date ON order_records(closed,business_date);
--> statement-breakpoint
CREATE TABLE receipt_records (id TEXT PRIMARY KEY, business_date TEXT NOT NULL, session_id TEXT NOT NULL UNIQUE, created_ms INTEGER NOT NULL, payload TEXT NOT NULL);
--> statement-breakpoint
CREATE INDEX receipt_records_date ON receipt_records(business_date);
--> statement-breakpoint
CREATE TABLE purchase_records (id TEXT PRIMARY KEY, business_date TEXT NOT NULL, created_ms INTEGER NOT NULL, payload TEXT NOT NULL);
--> statement-breakpoint
CREATE TABLE payroll_records (id TEXT PRIMARY KEY, business_date TEXT NOT NULL, created_ms INTEGER NOT NULL, payload TEXT NOT NULL);
--> statement-breakpoint
CREATE TABLE operation_requests (id TEXT PRIMARY KEY, created_ms INTEGER NOT NULL);
--> statement-breakpoint
CREATE TABLE audit_log (id TEXT PRIMARY KEY, actor TEXT NOT NULL, role TEXT NOT NULL, action TEXT NOT NULL, created_ms INTEGER NOT NULL);
