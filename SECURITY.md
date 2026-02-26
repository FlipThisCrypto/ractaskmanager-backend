# Security Policy

## Reporting Vulnerabilities

If you discover a security vulnerability, please email security@flipthiscrypto.com instead of using the issue tracker.

## Security Best Practices

### Environment Configuration
- **NEVER commit .env files** to version control
- Always use `.env.example` to document required variables
- In production, set all sensitive values via environment variables or secrets management
- Rotate `FLASK_SECRET_KEY` regularly in production

### Firebase Configuration
- Service account keys must be kept in `.env` (ignored by git)
- API keys should be restricted to specific Firebase services
- Use Firebase Security Rules to limit access

### Deployment
- Always set `FLASK_ENV=production` in production
- Set `FLASK_DEBUG=False` in production
- Use HTTPS only in production
- Enable `SESSION_COOKIE_SECURE` and `SESSION_COOKIE_HTTPONLY`
- Implement rate limiting on API endpoints
- Use a production WSGI server (gunicorn, uwsgi, etc.) not Flask dev server

### Dependency Management
- Keep dependencies updated with security patches
- Regularly run `pip-audit` to check for known vulnerabilities
- Use pinned versions in requirements.txt for production

### Content Security Policy
Firebase Hosting is configured with strict CSP headers:
- `default-src 'self'` restricts all content to same origin
- External resources limited to Firebase domains only
- Inline scripts evaluated only from trusted sources
- Frame embedding blocked entirely

## Vulnerable Patterns (Do Not Use)

❌ Hardcoded API endpoints, ngrok URLs, or tunnels in code
❌ Exposing service account keys in repositories
❌ Using `Flask_DEBUG=True` in production
❌ Committing `.env` files with secrets
❌ Making API calls without HTTPS in production
❌ Allowing cross-origin requests from `*`

## Security Checklist for Releases

- [ ] All environment variables are documented in `.env.example`
- [ ] No `.env`, `.key`, or `secrets` files are committed
- [ ] Dependencies are updated and audited (`pip-audit`)
- [ ] Security headers are enabled in production config
- [ ] HTTPS is enforced for all API calls
- [ ] Rate limiting is configured for API endpoints
- [ ] Session cookies are marked Secure + HttpOnly + SameSite=Strict
- [ ] Firebase rules have been reviewed for proper access control
- [ ] No sensitive data is logged (API keys, tokens, passwords)
- [ ] Error messages don't expose system information

## Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Flask Security](https://flask.palletsprojects.com/security/)
- [Firebase Security Rules](https://firebase.google.com/docs/firestore/security/start)
- [pip-audit](https://github.com/pypa/pip-audit)

---

Last Updated: 2026-02-26
