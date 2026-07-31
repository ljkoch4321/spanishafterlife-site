/**
 * POST /api/subscribe
 * Receives a site signup form, adds the subscriber to the right MailerLite
 * group (which fires the automation), then redirects to a thank-you page.
 *
 * Required Cloudflare Pages environment variables (Settings -> Environment
 * variables, Production + Preview):
 *   MAILERLITE_API_KEY   - MailerLite API token (kept server-side)
 *   ML_GROUP_GUIDE       - MailerLite group id for guide / prospect signups
 *   ML_GROUP_NEWSLETTER  - MailerLite group id for blog / newsletter signups
 *
 * Forms post application/x-www-form-urlencoded with:
 *   EMAIL      - the email address (required)
 *   intent     - "guide" (default) or "newsletter"  -> chooses group + redirect
 *   source     - free-text origin label, stored as a MailerLite field
 *   website    - honeypot; if filled we treat it as a bot and no-op
 *   consent    - consent checkbox (presence expected; not stored)
 */

const EMAIL_RE = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;

function seeOther(origin, path) {
  return new Response(null, { status: 303, headers: { Location: origin + path } });
}

export async function onRequestPost({ request, env }) {
  const origin = new URL(request.url).origin;

  // Parse the submission (form-encoded or JSON).
  let form = {};
  try {
    const ct = request.headers.get('content-type') || '';
    if (ct.includes('application/json')) {
      form = await request.json();
    } else {
      const fd = await request.formData();
      form = Object.fromEntries(fd.entries());
    }
  } catch (_) {
    return seeOther(origin, '/');
  }

  const email = String(form.EMAIL || form.email || '').trim().toLowerCase();
  const name = String(form.FNAME || form.name || '').trim().slice(0, 80);
  const honeypot = String(form.website || '').trim();
  const intent = form.intent === 'newsletter' ? 'newsletter' : 'guide';
  const source = String(form.source || '').slice(0, 100);
  const redirectTo = intent === 'newsletter' ? '/subscribed' : '/thank-you';

  // Bot caught by honeypot: pretend success, do nothing.
  if (honeypot) return seeOther(origin, redirectTo);

  // Bad email: still send them onward (the thank-you/guide is harmless), but
  // tag the URL so we could surface a message later if we want.
  if (!EMAIL_RE.test(email)) return seeOther(origin, redirectTo + '?e=email');

  const groupId = intent === 'newsletter' ? env.ML_GROUP_NEWSLETTER : env.ML_GROUP_GUIDE;
  const payload = { email, status: 'active' };
  const fields = {};
  if (name) fields.name = name;
  if (source) fields.source = source;
  if (Object.keys(fields).length) payload.fields = fields;
  if (groupId) payload.groups = [String(groupId)];

  // Add / upsert the subscriber. Joining the group fires the MailerLite
  // automation. We never block the visitor on MailerLite being reachable.
  if (env.MAILERLITE_API_KEY) {
    try {
      const r = await fetch('https://connect.mailerlite.com/api/subscribers', {
        method: 'POST',
        headers: {
          Authorization: 'Bearer ' + env.MAILERLITE_API_KEY,
          'Content-Type': 'application/json',
          Accept: 'application/json',
        },
        body: JSON.stringify(payload),
      });
      if (!r.ok && r.status !== 422) {
        console.log('MailerLite error', r.status, await r.text());
      }
    } catch (e) {
      console.log('MailerLite request failed:', e && e.message);
    }
  } else {
    console.log('MAILERLITE_API_KEY not set — skipping capture for', email);
  }

  return seeOther(origin, redirectTo);
}

// Anything that isn't a POST just goes home.
export async function onRequestGet({ request }) {
  return seeOther(new URL(request.url).origin, '/');
}
