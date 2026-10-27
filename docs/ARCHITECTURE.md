# Architecture

```
Angular SPA  --HTTP/JSON-->  FastAPI  -->  SQLite
(frontend/)                  (backend/)    (data/, git-ignored)
                                 |
                                 +--> Claude API (flyer / receipt extraction)
```

- **Contract-first:** FastAPI publishes an OpenAPI spec; the Angular client is generated from it.
- **Privacy:** receipts, flyer images and the database never leave the machine and are git-ignored.
- **Decision records** go in `docs/adr/` (one short file per decision).
