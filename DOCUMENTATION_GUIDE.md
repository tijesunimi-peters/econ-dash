# Documentation Guide

**Last Updated:** 2026-03-12
**Purpose:** Navigate the Econ Dashboard documentation suite

---

## Quick Start

### 👤 I'm a new developer
1. Read **[INDEX.md](INDEX.md)** — Get the big picture
2. Follow **[DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)** — Set up your environment
3. Check **[API_ENDPOINTS.md](API_ENDPOINTS.md)** — Understand the API

### 🏗️ I'm planning the next feature
1. Start with **[ROADMAP.md](ROADMAP.md)** — See what's next
2. Review **[STATUS.md](STATUS.md)** — Understand current architecture
3. Check **[DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)** — Understand patterns

### 🐛 I'm debugging something
1. Go to **[DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md#troubleshooting)** — Common issues
2. Check **[STATUS.md](STATUS.md#known-limitations)** — Known limitations
3. Review **[API_ENDPOINTS.md](API_ENDPOINTS.md)** — Verify expected behavior

### 📊 I need current status
1. See **[STATUS.md](STATUS.md)** — Feature checklist, architecture, data coverage
2. Check **[CHANGELOG.md](CHANGELOG.md)** — What changed recently

---

## Documentation Map

```
├── 🚀 GETTING STARTED
│   ├── INDEX.md .......................... Complete documentation hub
│   └── DEVELOPER_GUIDE.md ............... Setup, common tasks, troubleshooting
│
├── 📋 STATUS & PLANNING
│   ├── STATUS.md ........................ Current feature status, checklist
│   ├── ROADMAP.md ....................... Next steps, priorities, timeline
│   └── CHANGELOG.md ..................... Version history
│
├── 🔧 TECHNICAL REFERENCE
│   ├── API_ENDPOINTS.md ................. REST API documentation
│   ├── PROJECT.md ....................... Architecture, goals, design
│   └── STRATEGIC_CONTEXT_ROADMAP.md .... Phase 1-4 strategic context (reference)
│
└── 📚 ARCHIVES (Historical)
    ├── PLAN.md, PLAN-V2.md ............ Original architecture plans
    ├── PLAN-CAUSAL-FACTORS.md ........ Causal factors design (completed)
    ├── PLAN-COUNTRIES.md ............. Add JP, AU, DE design (completed)
    ├── PHASE3_*.md ................... Phase 3 progress tracking
    ├── WHATS_NEXT.md ................. Superseded by ROADMAP.md
    ├── HANDOFF.md .................... Superseded by DEVELOPER_GUIDE.md
    └── SESSION_5_FINAL.md ............ Session summary
```

---

## Documentation by Role

### Backend Engineer
**Essential:**
- [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) — Setup, common tasks, patterns
- [API_ENDPOINTS.md](API_ENDPOINTS.md) — Endpoint reference
- [STATUS.md](STATUS.md) — Current architecture, models, services

**Reference:**
- [PROJECT.md](PROJECT.md) — Design decisions
- [ROADMAP.md](ROADMAP.md) — What to build next

---

### Frontend Engineer
**Essential:**
- [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) — Frontend setup
- [API_ENDPOINTS.md](API_ENDPOINTS.md) — Available API calls
- [PROJECT.md](PROJECT.md) — Component architecture

**Reference:**
- [STATUS.md](STATUS.md) — Current UI status
- [ROADMAP.md](ROADMAP.md) — Planned features

---

### Project Manager / Product Lead
**Essential:**
- [STATUS.md](STATUS.md) — Feature checklist
- [ROADMAP.md](ROADMAP.md) — Next priorities, timeline, effort estimates
- [CHANGELOG.md](CHANGELOG.md) — Release history

**Reference:**
- [INDEX.md](INDEX.md) — Project overview
- [PROJECT.md](PROJECT.md) — Goals, architecture

---

### DevOps / Infrastructure
**Essential:**
- [PROJECT.md](PROJECT.md) — Infrastructure description
- [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) — Docker setup, environment variables

**Reference:**
- [STATUS.md](STATUS.md) — Performance metrics
- [CHANGELOG.md](CHANGELOG.md) — Infrastructure changes

---

## Key Documentation Sections

### Phase Status
All phases documented in [STATUS.md](STATUS.md):
- ✅ Phase 1: Policy Timeline
- ✅ Phase 2: Market Sentiment
- ✅ Phase 3: Structural Health
- ✅ Phase 4: Trade Flows & Supply Chain

### Next Steps
See [ROADMAP.md](ROADMAP.md) for:
- Tier 2: Quick wins (1-2 hours)
- Tier 3: Medium-term (3-4 weeks)
- Tier 4: Advanced features (Q2 2026+)

### API Reference
Complete in [API_ENDPOINTS.md](API_ENDPOINTS.md):
- 20+ endpoints documented
- Request/response examples
- Caching policies
- Error handling

### Development Workflow
See [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md):
- Installation & setup
- Common tasks (add endpoint, add country, etc.)
- Debugging guide
- Troubleshooting

---

## Document Purpose Summary

| Document | Purpose | Audience | Frequency |
|----------|---------|----------|-----------|
| INDEX.md | Navigation hub | All | Read once |
| STATUS.md | Current state checklist | Engineers, PMs | Weekly |
| ROADMAP.md | Next priorities | Engineers, PMs | Monthly |
| API_ENDPOINTS.md | API reference | Engineers | Daily |
| DEVELOPER_GUIDE.md | How to develop | Engineers | When needed |
| PROJECT.md | Architecture & goals | All | Monthly |
| CHANGELOG.md | What changed | All | Every release |

---

## Staying Current

### To understand what's being worked on:
→ Check [ROADMAP.md](ROADMAP.md)

### To understand what changed:
→ Check [CHANGELOG.md](CHANGELOG.md)

### To understand current status:
→ Check [STATUS.md](STATUS.md)

### To understand how to work on it:
→ Check [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)

### To understand why it works this way:
→ Check [PROJECT.md](PROJECT.md)

---

## Archive Notice

The following documents are kept for historical reference but are superseded by newer docs:

- **WHATS_NEXT.md** → Use [ROADMAP.md](ROADMAP.md) instead
- **PHASE3_*.md** → Consolidated into [STATUS.md](STATUS.md)
- **HANDOFF.md** → Use [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) instead
- **PLAN*.md** → Use [PROJECT.md](PROJECT.md) instead

These are kept in version control for historical tracking but should not be the primary reference.

---

## Contribution Notes

When updating documentation:

1. **Architecture changes** → Update [PROJECT.md](PROJECT.md)
2. **Feature completion** → Update [STATUS.md](STATUS.md) and [CHANGELOG.md](CHANGELOG.md)
3. **New priority** → Add to [ROADMAP.md](ROADMAP.md)
4. **API changes** → Update [API_ENDPOINTS.md](API_ENDPOINTS.md)
5. **Dev workflow changes** → Update [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)

---

## Questions?

- **"How do I...?"** → [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)
- **"What endpoints are available?"** → [API_ENDPOINTS.md](API_ENDPOINTS.md)
- **"What's the current status?"** → [STATUS.md](STATUS.md)
- **"What should we build next?"** → [ROADMAP.md](ROADMAP.md)
- **"How does it work?"** → [PROJECT.md](PROJECT.md)
- **"Where do I start?"** → [INDEX.md](INDEX.md)

---

*Last updated 2026-03-12. See [CHANGELOG.md](CHANGELOG.md) for recent changes.*
