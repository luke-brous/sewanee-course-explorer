# Project Context: Sewanee Course Explorer

## Tech Stack
* **Framework:** Next.js 16 (App Router)
* **Language:** TypeScript
* **Styling:** Tailwind CSS v4
* **Database ORM:** Prisma
* **Database:** PostgreSQL (Neon)
* **Data Pipeline:** Python (Pandas, Psycopg2)

## Architectural Rules (Twelve-Factor App)
1.  **Strict Directory Structure:** All application code MUST reside in the `src/` directory. Next.js routing uses `src/app/`.
2.  **API Routes:** Data services are isolated in `src/app/api/...` using standard Next.js Route Handlers.
3.  **Database Connection:** Always use the Prisma singleton pattern located at `src/lib/prisma.ts`. Do not instantiate a new PrismaClient in individual components.
4.  **Admin Processes:** One-off scripts (like database seeding or data extraction) must live in the `scripts/` directory, separate from the core web application.

## Coding Standards
* Prefer Server Components for data fetching.
* Only use Client Components (`"use client"`) when interactivity (e.g., hooks, state, browser APIs) is strictly required.
* Write explicit interfaces for all component props and API responses.
* Never hardcode configuration variables; always read from `process.env`.