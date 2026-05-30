# Phase 5: Add OAuth - Discussion Log

**Date:** 2026-05-30

This log records the discussion that produced `05-CONTEXT.md`. It is for human reference (audits, retrospectives) and is **not** consumed by downstream agents.

## Discussed Areas

### 1. Account Linking
**Options presented:** Auto-link them silently based on email / Require password login first to link the accounts / Send an email with a linking confirmation link.
**User selected:** Follow best practice.
**Resolution:** Auto-link them silently based on email (assuming Google and GitHub verify emails) for the best UX.

### 2. OAuth-only Users & Passwords
**Options presented:** Hide the password change form for OAuth-only users / Require OAuth users to set a password when they first log in / Allow them to set a password optionally from the settings page.
**User selected:** Follow best practice.
**Resolution:** Hide the "Change Password" form for OAuth-only users, but provide a "Set Password" option in settings as a fallback.

### 3. Provider Layout
**Options presented:** Place them directly on the main login and register forms / Place them on a separate 'Log in with SSO' page.
**User selected:** Place them directly on the main login and register forms (e.g. above/below the email/password fields).
**Resolution:** Proceed as requested for high visibility.

### 4. Missing Provider Emails
**Options presented:** Fail the login with an error / Prompt the user to manually enter their email address / Use a placeholder email.
**User selected:** Follow best practice.
**Resolution:** Prompt the user to manually enter their email address if the provider doesn't return one.

## Noted for Later
*(None)*
