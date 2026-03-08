# Database

PostgreSQL schema for IRIDIUM. The current API uses in-memory state; this schema is for future persistence and migrations. To initialise a local database:

```bash
psql -U postgres -d iridium -f infrastructure/db/schema.sql
```

PostGIS can be enabled for spatial queries on nodes and segments. See docs/deployment.md for connection configuration.
