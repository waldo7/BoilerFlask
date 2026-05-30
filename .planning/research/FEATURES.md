# Features Research: Flask Scaffold

## Table Stakes (must have)

| Feature | Complexity | In Scope |
|---------|-----------|----------|
| User registration with email/password | Low | Yes — AUTH-01 |
| Login with session persistence | Low | Yes — AUTH-02 |
| Logout | Low | Yes — AUTH-03 |
| Password reset via email token | Medium | Yes — AUTH-04 |
| Role-based access (admin/user) | Low | Yes — AUTH-05 |
| Admin gating on sidebar items | Low | Yes — AUTH-06 |
| Consistent layout with template inheritance | Low | Yes — LAYOUT-01 |
| Error pages (403, 404, 500) | Low | Yes — LAYOUT-02 |
| Responsive/mobile-first layout | Medium | Yes — MOB-01 to MOB-04 |
| Homepage placeholder | Low | Yes — MAIN-01 |
| Post-login dashboard | Low | Yes — MAIN-02 |
| Sidebar navigation | Low | Yes — MAIN-03 |

## Differentiators (competitive advantage)

| Feature | Complexity | In Scope? |
|---------|-----------|-----------|
| Blueprint-based modular structure | Low | Yes (architecture choice) |
| App factory pattern | Low | Yes (architecture choice) |
| Easy DB migration path (SQLite → Postgres) | Low | Yes (config-only swap) |

## Anti-Features (deliberately NOT building)

| Feature | Reason |
|---------|--------|
| REST API | Scaffold is server-rendered; API is separate concern |
| OAuth / Social login | Adds third-party dependency complexity; defer to v2 |
| Email verification | Requires real email infra; defer to production setup |
| User profile editing | Not core to scaffold; easy to add later |
| Admin user management panel | Not core to scaffold; easy to add later |
| File uploads (avatars) | Storage complexity; defer to v2 |
| JS framework (React/Vue) | User chose server-rendered Jinja |

## Dependencies Between Features

- Auth features (AUTH-01 to AUTH-06) depend on Project Skeleton (LAYOUT-01, LAYOUT-02)
- Dashboard (MAIN-02) depends on Auth (login_required)
- Sidebar admin gating (AUTH-06) depends on roles (AUTH-05)
- Mobile features (MOB-01 to MOB-04) are layout concerns — built alongside their parent features
