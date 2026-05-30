# Requirements: FlaskStuct

**Defined:** 2026-05-30
**Core Value:** Developers get a production-ready, organized Flask foundation with auth and responsive UI out of the box.

## v1 Requirements

### Authentication

- [ ] **AUTH-01**: User can register with email and password
- [ ] **AUTH-02**: User can log in and session persists across browser refresh
- [ ] **AUTH-03**: User can log out from any page
- [ ] **AUTH-04**: User can request password reset via email
- [ ] **AUTH-05**: User has a role (admin or user) assigned
- [x] **AUTH-06**: Admin users see admin-only items in sidebar

### Main Pages

- [x] **MAIN-01**: Homepage shows "Flask app is running" placeholder
- [x] **MAIN-02**: Authenticated users see dashboard after login
- [x] **MAIN-03**: Sidebar renders Dashboard and Settings links

### Layout & Design

- [x] **LAYOUT-01**: base.html provides consistent layout with Bootstrap 5
- [x] **LAYOUT-02**: Error pages exist and are styled (403, 404, 500)

### Mobile

- [x] **MOB-01**: Sidebar collapses to hamburger menu on screens < 768px
- [x] **MOB-02**: All pages are readable and functional on 320px+ viewports
- [x] **MOB-03**: Login/register forms are full-width and touch-friendly on mobile
- [x] **MOB-04**: Dashboard layout stacks vertically on mobile

## v2 Requirements

### Authentication

- **AUTH-07**: User verifies email after registration
- **AUTH-08**: User can log in via OAuth (Google, GitHub)
- **AUTH-09**: User can update profile (display name, avatar)

### Admin

- **ADMN-01**: Admin can view all registered users
- **ADMN-02**: Admin can change user roles
- **ADMN-03**: Admin can disable user accounts

### Features

- **FEAT-01**: User can upload avatar image
- **FEAT-02**: REST API for authentication

## Out of Scope

| Feature | Reason |
|---------|--------|
| REST API | Scaffold is server-rendered; API is separate concern |
| OAuth / Social login | Third-party dependency; defer to v2 |
| Email verification | Requires real email infrastructure |
| User profile editing | Not core scaffold; easy to add later |
| Admin user management | Not core scaffold; easy to add later |
| File uploads (avatars) | Storage complexity; defer to v2 |
| JS framework (React, Vue) | User chose pure server-rendered |
| Real-time features (WebSockets) | Different architecture requirement |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| AUTH-01 | Phase 2 | Pending |
| AUTH-02 | Phase 2 | Pending |
| AUTH-03 | Phase 2 | Pending |
| AUTH-04 | Phase 2 | Pending |
| AUTH-05 | Phase 2 | Pending |
| AUTH-06 | Phase 3 | Complete |
| MAIN-01 | Phase 1 | Complete |
| MAIN-02 | Phase 3 | Complete |
| MAIN-03 | Phase 3 | Complete |
| LAYOUT-01 | Phase 1 | Complete |
| LAYOUT-02 | Phase 1 | Complete |
| MOB-01 | Phase 1 | Complete |
| MOB-02 | Phase 3 | Complete |
| MOB-03 | Phase 1 | Complete |
| MOB-04 | Phase 3 | Complete |

**Coverage:**

- v1 requirements: 15 total
- Mapped to phases: 15
- Unmapped: 0 ✓

---
*Requirements defined: 2026-05-30*
*Last updated: 2026-05-30T03:08:25Z (Plan 01-02 executed)*
