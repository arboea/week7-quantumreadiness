**Quantum Readiness Plan**

**Goal**: Prepare the organization to transition from classical public-key cryptography (e.g., RSA, ECC) to Post-Quantum Cryptography (PQC) in a controlled, auditable way.

**Inventory (where crypto is used)**
- **Databases**: encryption-at-rest (TDE, file-level, disk encryption), column-level encryption for PII, database TLS connections between app and DB.
- **Key Management**: HSMs, KMS (cloud), key rotation procedures, secret stores (Vault, Azure Key Vault, AWS KMS).
- **Transport**: TLS termination points (load balancers, ingress controllers), inter-service mTLS, VPNs and site-to-site tunnels.
- **Authentication**: SSH keys, user authentication tokens, password hashing, SSO/OAuth tokens, certificate-based logins.
- **Application Layer**: Data encrypted in application code (customer data, session tokens), JWTs signed with asymmetric keys.
- **Client Devices**: Mobile apps and IoT devices with embedded keys or certificates (over-the-air update signing).
- **Third-party Integrations**: External partners using certificates, API keys, or mutual TLS.
- **Backups & Archives**: Long-term encrypted backups that must remain readable after migration.
- **Compliance & Auditing**: Systems that log or store keys/crypto metadata for audits.

**PQC Migration Timeline (high-level)**
Note: adapt durations to organisation size and regulatory constraints.
- **Phase 0 — Awareness & Inventory (0–3 months)**: Complete inventory, identify high-risk assets (long-lived secrets, archived data), raise stakeholder awareness.
- **Phase 1 — Research & Pilot (3–9 months)**: Evaluate candidate PQC algorithms (Kyber, Dilithium, etc.), run pilots in isolated environments, update test suites and CI to exercise PQC algorithms.
- **Phase 2 — Controlled Deployments (9–18 months)**: Deploy hybrid crypto (classical + PQC) on public-facing TLS endpoints and internal services; validate interoperability and performance.
- **Phase 3 — Key Management & Rollout (18–30 months)**: Integrate PQC into KMS/HSMs or wrap PQC keys for storage; rotate keys for critical systems and update clients/devices.
- **Phase 4 — Verification & Decommissioning (30–48 months)**: Verify all clients and partners migrated, deprecate vulnerable algorithms, and ensure archives have been re-encrypted or noted as at-risk.

**Milestones & Metrics**
- **Milestone**: Inventory completed — metric: % of systems inventoried.
- **Milestone**: Hybrid TLS enabled on public endpoints — metric: % of public endpoints supporting PQC+classical.
- **Milestone**: KMS supports PQC-wrapped keys — metric: PQC keys issued and rotated.
- **Risk metric**: Count of long-lived secrets older than retention window.

**Ethical Rationale**
- **Protecting Trust**: Cryptography underpins customer privacy and trust. Proactively migrating to PQC prevents future mass-decryptions should a rapidly-scaling quantum capability appear.
- **Duty to Customers and Partners**: Organisations that hold long-lived sensitive data (medical, financial, intellectual property) have an ethical duty to mitigate foreseeable risks that could expose that data years later.
- **Against Unnecessary Panic**: Migration should be measured — avoid premature, disruptive changes that reduce security due to immature implementations.
- **Balance**: The ethical position favors deliberate, well-tested migration to PQC while maintaining current protections — not sudden emergency switches that harm availability or security.

**Leader’s Boardroom Talk Track**
- **Opening (15s)**: "Quantum computers are advancing; while immediate breakage of deployed cryptography isn't here yet, some encrypted data we hold today could be vulnerable in the future. We should act now to reduce that risk in a measured way."
- **Problem statement (30s)**: "Our current asymmetric cryptography (RSA/ECC) is widely used across our stack — in TLS, database encryption, device firmware signing, and backups. Several of these uses involve long-lived keys or archived data that could be harvested today and decrypted later when quantum capabilities arrive."
- **Proposed approach (45s)**: "We recommend a staged migration: inventory all crypto, pilot PQC in hybrid mode for critical endpoints, extend KMS/HSM support, then roll out PQC-wrapped keys and rotate. This minimizes operational disruption and preserves interoperability."
- **Benefits (20s)**: "This protects customer data, reduces long-term legal and reputational risk, and demonstrates responsible stewardship to regulators and partners."
- **Costs & Trade-offs (20s)**: "There are engineering and operational costs — testing, performance tuning, and possible hardware upgrades. But these are predictable, budgetable expenses compared to the open-ended risk of inaction."
- **Ask (15s)**: "Approve a 12-month pilot budget and a cross-functional steering team to deliver the inventory, pilots, and a board-facing progress report at the 9-month mark."

**Appendix: Actionable Next Steps**
- Start a short (4–6 week) discovery sprint to finalize inventory and classify data sensitivity.
- Select 1–2 public endpoints for hybrid PQC TLS pilot (low-risk traffic first).
- Engage KMS/HSM vendors about PQC support and timeline.
- Prepare communication for customers and partners about the transition (technical FAQs).

**References & Notes**
- NIST PQC standards (monitor releases)
- Vendor PQC announcements (Cloud KMS/HSM roadmaps)

**End**
