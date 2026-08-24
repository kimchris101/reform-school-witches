✝ THE REFORM SCHOOL FOR WITCHES — OFFICIAL READER PORTAL & EXECUTIVE TERMINAL

A production-ready web platform and interactive digital companion for The Reform School for Witches novel series (rsfwseries.com). Built on a modern Python backend with lightweight, fast-loading frontend architecture, this portal serves reader intake diagnostics, subscriber-gated personnel dossiers, streaming cinematic cutscenes, and an HTMX-gated executive pitch deck.

---

⚡ TECH STACK

• Backend: Python 3.11+, FastAPI, Pydantic v2, Uvicorn
• Frontend: HTMX 1.9+, Jinja2 Templates, Tailwind CSS (CDN)
• Email Service: Brevo REST API v3 (Async transactional HTML emails)
• Design Aesthetic: Southern Gothic Sacramental Noir / Dark Academia (Custom typography with Cinzel, EB Garamond, and JetBrains Mono)

---

🏛 SYSTEM ARCHITECTURE & FEATURES

1. Academy Diagnostic Protocol (/intake)
• Scoring Engine: Algorithmic evaluation mapping initiate responses to canonical character archetypes (Co-Link Partner, Perimeter Guard, Sacramental Scholar).
• Automated Disciplinary Letters: Asynchronous background tasks dispatch custom HTML assessment letters with dark academia styling via Brevo's REST API.
• Cutscene Triggers: Automated HTMX headers (HX-Trigger) launch full-screen modal cutscenes upon specific archetype results.
2. Personnel Dossiers & Classified Files (/dossiers)
• Interactive Archives: Personnel records for Roman De La Croix, Kimbra, Damian Boudreaux, and Father Manuel.
• Gated Content & Easter Eggs: Level-restricted dossier notes, audio recordings, and secret routes accessible through lore interactions.
3. Surveillance Vault & Cinematics (/media)
• Video Streaming: HTML5 video playback for animated cutscenes (The Sacramental Bond, Library Awakening).
• Subscriber Access Guardrail: Registration modal unlocks full streaming access and downloadable lore samples.
4. Executive Producer Terminal (/industry)
• Gated Pitch Deck: Accessible via a restricted clearance passkey form embedded inside the Cinematics vault.
• Multi-Season Arc Trajectory: Detailed breakdown of market analytics, genre hybrid positioning, and Damian Boudreaux's 3-season transformation arc.
5. Interactive Script Engine (/interactive)
• Visual Novel Terminal: Real-time story choice nodes rendered dynamically via HTMX partial swaps without full page reloads.
6. Book Vault & Commerce (/vault)
• Digital Storefront: Direct integration with Amazon Kindle store links and free sample PDF distribution.

---

🚀 QUICKSTART & LOCAL SETUP

1. Clone & Setup Virtual Environment:
git clone [https://github.com/your-username/rsfw-portal.git](https://www.google.com/search?q=https://github.com/your-username/rsfw-portal.git)
cd rsfw-portal

python3 -m venv venv
source venv/bin/activate  (On Windows: venv\Scripts\activate)
pip install -r requirements.txt

2. Configure Environment Variables (.env):
BREVO_API_KEY=xkeysib-your-validated-brevo-api-key
SENDER_EMAIL=hello@rsfwseries.com
SENDER_NAME="Our Lady of Tears Academy"
INDUSTRY_PASSKEY=SACRAMENTAL2026

Note: Ensure your IP address is whitelisted in your Brevo dashboard under SMTP & API > Authorized IP Addresses if running locally.

3. Launch Development Server:
uvicorn app.main:app --reload

Navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

📁 REPOSITORY STRUCTURE

├── app/
│   ├── main.py                  (FastAPI entry point, middleware & route registrations)
│   ├── models/                  (Pydantic validation schemas & archetype enums)
│   ├── routes/                  (Feature routers: intake, dossiers, media, industry, etc.)
│   ├── services/                (Business logic: scoring engine, Brevo email dispatch)
│   ├── templates/               (Jinja2 templates & HTMX components)
│   │   ├── base.html            (Global gothic layout & header/footer navigation)
│   │   ├── components/          (Reusable HTMX fragments: story nodes, email templates, modals)
│   │   └── pages/               (Main route views: intake, dossiers, media, industry, vault)
│   └── static/                  (Static assets: media, audio clips, PDFs)
├── .env.example                 (Environment template)
├── requirements.txt             (Python dependencies)
└── README.md                    (System documentation)

---

🌐 PRODUCTION DEPLOYMENT CHECKLIST

1. Domain Authentication: Publish DKIM and SPF TXT records in your DNS host for rsfwseries.com via Brevo.
2. IP Whitelisting: Update Brevo security settings to include your production server IP address.
3. SSL/TLS: Serve via HTTPS using Nginx, Caddy, or Cloudflare edge SSL.

---



Phase 2: RSFW Archival Engine & Interactive System

🏰 Catholic Noir World Alignment

* Canon Precision: Cleaned up character profiles to enforce strict role separation—defining Roman as a student initiate/sponsor, Ignatius as a penitent sentry, and Father Manuel as the sole ordained rector.
* Narrative Accuracy: Resolved role confusion across all story nodes, ensuring backstory details (like New Orleans high-society roots) stay strictly tied to Roman.

📚 Standalone Manuscript Lore Search

* PDF Ingestion: Engine ingests Book I: The Blood Lily Contract, breaking text into searchable chunks with page-level attribution.
* Multi-Tier Retrieval: Implemented a hybrid lookup that prioritizes curated canonical character cards before searching raw manuscript passages.
* Offline Efficiency: Decommissioned external LLM dependencies to eliminate API costs, latency, and decommissioned model errors.

🖥️ Interactive Engine & UI Integration

* Archival Modal Overlay: Renamed character interrogation modals to "Consult Archival Index" to match the new lookup functionality.
* Clean HTMX Rendering: Updated HTMX targets (`/interactive/lore-search`) and templates (`lore_results.html`) for seamless modal updates.
* Future-Proofing: Built a scalable data pipeline ready to index future book releases (Book II, Book III) and new canon entries seamlessly.

🚀 Phase 3: Production Hardening, Containerization & Staging Preparation


🛠️ Resolved Pylance and Type Security Warnings
We updated app/config.py and app/routes/interactive.py with strict type hints for cookie security. Cleaned up code structure so VS Code runs with zero errors.

📦 Configured Container Infrastructure
Built a production-ready Dockerfile and docker-compose.yml setup. This guarantees identical performance across local development and cloud hosting servers.

⚡ Implemented Startup PDF Index Caching
Updated app/services/lore_engine.py and app/main.py with FastAPI lifespan handlers. The manuscript PDF now indexes straight into server memory on boot for lightning-fast search responses.

🛡️ Added Custom Error Fallbacks
Integrated thematic 404 and 500 error handlers to catch unexpected anomalies gracefully without exposing raw backend stack traces to readers.

🔍 Aligned HTMX Search Templates
Fixed data key mismatches between app/routes/interactive.py and components/lore_results.html. Searching terms like Roman or Kimbra now instantly returns manuscript excerpts in the terminal modal.


© 2026 Red Candle Digital. All Diocesan Records Reserved.
