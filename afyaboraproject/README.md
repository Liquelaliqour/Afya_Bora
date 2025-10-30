# Afya Bora — MVP Technical Features & System Design

**Version:** 0.1

**Purpose:** Build the Afya Bora MVP — a global marketplace connecting patients with credentialed Lifestyle Medicine practitioners for remote care (teleconsultation, messaging, file sharing, scheduling, payments). This document outlines product pages, user experiences, architecture, data model, APIs, integrations (including Paystack), security/compliance, deployment, and an implementation roadmap.

---

## 1) High-level goals (MVP scope)

* Enable verified lifestyle medicine practitioners (ACLM/IBLM/ILM/LMGA, etc.) to list services.
* Allow patients to find, book, pay, and consult with verified practitioners remotely.
* Provide secure messaging, file-sharing, and video teleconsultation (one‑to‑one).
* Offer practitioner verification workflows and admin moderation.
* Collect core metrics: practitioners onboarded (by credential), consultations by region, partnerships, growth & retention.

---

## 2) User Personas & Journeys

### Personas

* **Patient (Primary)** — age 25–65, health-conscious or early-stage chronic disease; looks for evidence-based lifestyle medicine care.
* **Practitioner (Secondary)** — credentialed clinician wanting remote clients; needs profile, schedule, teleconsultation tools, payments, client notes.
* **Admin / Verifier** — platform staff who review credentials, manage partnerships, dispute resolution.

### Key Journeys (MVP)

1. Patient signs up → searches practitioners → views profiles → books appointment → pays → receives teleconsult link → has consultation → receives notes & follow-up plan → rates provider.
2. Practitioner signs up → submits credentials → admin verifies → sets services & availability → receives booking → conducts consultation → logs notes and follow-up.
3. Admin verifies credentials, manages disputes, sees platform metrics.

---

## 3) Pages / Experiences

(Design UI as responsive web app; mobile-first. Native apps later.)

### Public

* Home / value proposition
* Search / discovery (filters: language, specialty, credential type, region, price, availability)
* Practitioner profile (photo, bio, credentials, verified badge, services, reviews, pricing, calendar)
* About / partnerships / institution pages
* Sign up / login

### Patient dashboard

* Upcoming appointments
* Message inbox (threads with practitioners)
* Medical file repository (uploads: PDFs, CSV from wearables, photos)
* Consultation history and notes
* Payment & invoices

### Practitioner dashboard

* Profile & credentials management
* Availability & scheduling
* Upcoming appointments + patient context
* Messaging & file exchange
* Session notes & care plans
* Earnings, payouts, tax docs

### Admin dashboard

* Practitioner verification queue
* Partnership management
* Platform metrics & analytics
* User support & moderation tools

---

## 4) Core Features (MVP)

* **Auth & identity:** email/password, OAuth (Google), 2FA (optional). Role-based access control (patient, practitioner, admin).
* **Practitioner verification:** file upload + manual review workflow; store verification status & cert metadata.
* **Discovery & matching:** search + filters + sorting; simple recommendation using tags and geography.
* **Scheduling / Booking:** calendar-based availability, time zone handling, buffer times, automatic timezone display.
* **Payments:** Paystack (primary for Africa)
* **Teleconsultation:** WebRTC-based video calls (peer-to-peer or SFU) with authenticated session links and access control.
* **Messaging:** real-time messaging with attachments, read receipts, and persisted history.
* **File Storage / Sharing:** secure uploads (documents, images) stored in encrypted object storage with signed URLs.
* **Session notes:** practitioner-only notes (private) and patient-facing after session (shared summary).
* **Ratings & reviews** for transparency.
* **Notifications:** email + in-app + optional SMS (via Twilio or Africa SMS provider).
* **Analytics & metrics dashboard** (practitioners onboarded, consultations/region, retention)

---

## 5) Technical Architecture (high level)

**Recommended stack (revised for Django):**

* **Frontend:** React (Next.js) — server-side rendered for SEO and performant dashboards; consumes REST/GraphQL APIs from Django / Django Rest Framework backend.
* **Backend:** Django + Django REST Framework (DRF) for REST APIs; Django Channels for WebSockets (real-time messaging, notifications, signaling for video calls).
* **Realtime Communication:** Django Channels (ASGI) + Redis as message broker. WebRTC for teleconsultations (integrated via signaling handled by Django Channels).

* **Video Conferencing:**

  * For MVP: integrate with **Daily.co** SDK or **Jitsi Meet API** to enable secure, browser-based teleconsultations with minimal infrastructure overhead. Both provide free tiers (≈10,000 participant-minutes/month) that do **not require credit cards**, ideal for rapid testing and iteration.
  
  * Django backend (via **Django Channels** + **Redis**) handles:
    * Authentication and token generation for each consultation session.
    * Room creation and participant access control.
    * WebSocket signaling for chat, presence, and in-call status updates.
  
  * For scalability: migrate to **Agora SDK** (for lower per-minute cost and global edge presence) or self-hosted **Jitsi** / **mediasoup** clusters.  
    This enables long-term cost optimization, data residency control, and compliance with **HIPAA/GDPR** standards as Afya Bora scales regionally.
  
  * All consultations are encrypted end-to-end, with optional recording stored securely in **S3-compatible** storage (encrypted at rest).  
    Access control, audit logging, and retention policies align with healthcare data protection standards.

* **Database:** PostgreSQL — relational database for all structured data (users, appointments, credentials, payments, etc.).
* **Caching & Queues:** Redis for caching, async tasks (Celery + Redis), and WebSocket pub/sub.
* **File Storage:** AWS S3 (or DigitalOcean Spaces/MinIO) with presigned URL access; server-side encryption enabled.
* **Payments:** Paystack SDK integrated into Django backend with webhook handling; fallback Stripe integration for global reach.
* **Authentication:** Django Allauth (for email + social OAuth) + JWT tokens (via SimpleJWT) for API authentication. Role-based permissions (patient, practitioner, admin) managed through Django’s built-in auth.
* **Search & Filtering:** PostgreSQL full-text search for MVP; optional ElasticSearch for advanced search later.
* **Deployment:**

  * Django app containerized (Docker) running via ASGI (Daphne or Uvicorn) for Channels compatibility.
  * Reverse proxy (Nginx) serving static/media assets and proxying WebSocket and API requests.
  * Hosting on vercel for the frontend and AWS (ECS / Elastic Beanstalk) or DigitalOcean App Platform; CI/CD via GitHub Actions.
* **Monitoring & Logging:** Sentry for error tracking, Prometheus + Grafana for metrics, Loki or CloudWatch for structured logs.

**Architecture diagram (conceptual):**

``` text
[Client (Web/Mobile)]
     ↓  HTTPS / WSS
[Next.js Frontend App]
     ↓
[Django API Server (ASGI)] — REST/GraphQL + WebSockets (Channels)
     ↓
[PostgreSQL] — data persistence
[Redis] — caching, queues, channels layer
[S3/MinIO] — secure file storage
[Paystack] — payments + webhooks
[Video (Jitsi/Daily)] — external teleconsultation service
```

**Key Django Apps (suggested modular design):**

* `users` — auth, roles, profiles, verification
* `practitioners` — credential management, services, availability
* `patients` — records, preferences
* `appointments` — booking, calendar, scheduling logic
* `messaging` — chat threads, attachments (WebSockets)
* `payments` — Paystack/Stripe integration, transactions, webhooks
* `telehealth` — video room generation, token management
* `reviews` — ratings & comments
* `analytics` — metrics collection for KPIs
* `admin_portal` — credential verification, moderation, reports

**Scalability & Future-readiness:**

* Stateless Django app containers with shared Redis and database.
* Horizontal scaling at ASGI layer for WebSockets.
* CDN (CloudFront or Cloudflare) for static assets and caching.
* Decouple real-time signaling service (if scaling WebRTC) later.

---

*This section now reflects a Django-based architecture optimized for scalability, compliance, and MVP speed while maintaining flexibility for future expansion.*

---

## 6) Data Model (core tables)

* **users** (id, email, name, role, phone, time_zone, created_at)
* **practitioners** (user_id FK, headline, bio, specializations[], credentials[], verified_status, verification_docs[], rating_avg, languages[])
* **credentials** (id, practitioner_id, authority, cert_id, issued_date, expires_date, doc_url, status)
* **services** (id, practitioner_id, title, description, duration_minutes, price_currency, price_amount, cancellation_policy)
* **availability_slots** (id, practitioner_id, start_ts, end_ts, recurring_rule)
* **appointments** (id, patient_id, practitioner_id, service_id, start_ts, end_ts, status (booked/cancelled/completed), price, payment_status, video_room_id)
* **messages** (id, thread_id, sender_id, body, attachments[], created_at)
* **threads** (id, patient_id, practitioner_id, last_message_at)
* **files** (id, owner_id, s3_key, content_type, size, access_level)
* **payments** (id, appointment_id, provider, provider_payment_id, amount, currency, status, created_at)
* **reviews** (id, appointment_id, patient_id, rating, comment)
* **audit_logs** (id, actor_id, action, object_type, object_id, timestamp)

---

## 7) API Surface (examples)

* `POST /auth/signup` — create account
* `POST /auth/login` — obtain JWT
* `GET /practitioners?filters...` — search
* `GET /practitioners/:id` — profile
* `POST /practitioners/:id/verify` — upload credentials
* `GET /availability/:practitionerId` — fetch slots
* `POST /appointments` — create booking (triggers payment intent)
* `POST /payments/paystack/init` — create Paystack transaction
* `POST /webhooks/paystack` — handle Paystack events
* `POST /video/rooms` — create video session (creates room in SFU)
* `GET /messages/:threadId` — paginate messages
* `POST /messages` — send message (websocket + persist)

Authentication via `Authorization: Bearer <JWT>`.

---

## 8) Teleconsultation (implementation choices)

### WebRTC options

* **Use a managed API (Daily.co, Twilio Video)**

  * Pros: fast integration, reliability, recording, scaling handled.
  * Cons: cost; provider lock-in.
* **Open-source SFU (mediasoup / Jitsi / Janus)**

  * Pros: control, lower long-term cost, GDPR-friendly self-hosting.
  * Cons: operational complexity; needs expertise to scale.

**MVP recommendation:** Start with Daily.co or Jitsi hosted for quick MVP (Daily has simpler API and good browser support). If budget constrained and engineering capacity exists, run a small Jitsi instance or mediasoup.

**Implementation details:**

* Authenticated ephemeral room tokens.
* Generate room ID when appointment status becomes `confirmed`.
* Provide pre-joined context (appointment id, patient profile summary) to practitioner client.
* Recordings optional — store in encrypted S3 with explicit consent.

---

## 9) Messaging & File Sharing

* Real-time messaging via WebSockets (Socket.IO) with messages persisted to DB and attachments to S3 (signed upload URLs).
* For large medical files, support chunked uploads + virus/malware scanning (ClamAV) in background job.
* Access control: signed URLs expire; only participants + admin can access files.

---

## 10) Payments: Paystack integration (suggested flow)

* **Why Paystack?** Strong African coverage (cards, mobile money), developer SDKs and webhooks.

### Flow (simplified)

1. Patient initiates booking → frontend calls `POST /payments/paystack/init` → backend creates a transaction with Paystack API (amount, metadata: appointment_id, user_id) and returns authorization URL/client token.
2. Patient completes payment on Paystack modal or redirect (Paystack inline/checkout).
3. Paystack sends webhook to `/webhooks/paystack` with transaction status.
4. Backend verifies webhook signature, updates `payments` and `appointments.payment_status` accordingly, then emits socket/email notifications.
5. On successful payment, appointment status becomes `paid` and a video room token is provisioned.

### Implementation notes

* Secure webhook endpoint (use Paystack signature header).
* Support refunds via Paystack API.
* Payouts to practitioners: maintain earnings ledger; use Transfer systems supported by Paystack or integrate local payout partners—initially manual payouts (bank transfer initiated by admin) to reduce complexity.

---

## 11) Security & Compliance

* **Encryption:** TLS everywhere; S3 server-side encryption; encrypt sensitive DB fields.
* **Data minimization:** store only necessary PHI; pseudonymize where possible.
* **Access controls:** RBAC; audit logging for record access.
* **Backups:** encrypted snapshots of DB; tested recovery plan.
* **Regulatory:** design for GDPR (data subject requests), and HIPAA principles if supporting US patients (BAA required if using third-party hosted services). Clearly document where data lives (region) and acquire consents.
* **Penetration testing** before public launch.

---

## 12) Non-functional requirements

* Availability: 99.9% for core booking & payments; video best-effort.
* Latency: API P95 < 300ms.
* Scalability: design stateless APIs + autoscaling; SFU scales separately.

---

## 13) Monitoring & Observability

* Error tracking: Sentry.
* Metrics: Prometheus + Grafana (requests, payments, bookings, active sessions).
* Logs: centralized (Loki/ELK) with structured logs.
* Alerts: PagerDuty or similar for outages.

---

## 14) DevOps & Deployment

* Infrastructure as Code: Terraform.
* CI/CD: GitHub Actions — run tests, lint, build containers, deploy to staging and production.
* Containerization: Docker; orchestrate with ECS / EKS.
* Secrets: Secrets Manager / Vault.

---

## 15) Roadmap (first 6 months)

**Phase 0 — Planning (weeks 0–2):** requirements, wireframes, partner outreach.
**Phase 1 — Core MVP (weeks 3–12):** auth, practitioner onboarding + verification, search & profiles, booking, Paystack payment flow, simple messaging, video via hosted provider, dashboards.
**Phase 2 — Harden (weeks 13–20):** analytics, reviews, refunds, admin workflows, security hardening, monitoring.
**Phase 3 — Scale & polish (weeks 21–36):** mobile apps, multi-currency support, payouts automation, advanced search, recommendations, integrations with wearables & EMRs.

---

## 16) Metrics & Instrumentation

* Practitioners onboarded (by credential authority)
* Consultations per region / per practitioner
* Conversion: profile view → booking
* Retention: repeat bookings per patient
* Revenue / ARPU
* Verification throughput & verification acceptance rate

---

## 17) Risks & Mitigations

* **Verification fraud:** require multiple verification artifacts, manual review, and spot-checks.
* **Payment disputes:** clear cancellation/refund policies and receipts; use webhooks and signed logs.
* **Video quality:** allow fallback to phone calls; provide pre-check tool for users.
* **Compliance overhead for US/HIPAA:** if targeting US patients, prepare to sign BAAs or avoid storing PHI on third-party services without BAA.

---

## 18) Cost Estimate (very rough)

* Initial engineering (3–4 engineers) 3 months: dev costs vary by region.
* Hosting: small (below $500/mo) at launch if using hosted video; increases with usage.
* Third-party (Daily/Jitsi paid tier): depends on minutes/month.
* Paystack fees: per their pricing for transactions.

---

## 19) Deliverables I can produce next (choose)

* Detailed API spec (OpenAPI) for the endpoints above.
* ERD diagram & SQL schema migrations for PostgreSQL.
* Component-level frontend wireframes for patient & practitioner flows (Next.js pages).
* CI/CD Terraform templates and deployment scripts.

---

*Document prepared as a technical MVP blueprint for Afya Bora. Use this to guide engineering sprints, vendor selection, and partnership outreach.*
