/**
 * TEMPORARY diagnostic endpoint — GET /api/ml-check?diag=ml7823
 * Reports whether the MailerLite env vars are present and whether the API key
 * works, without leaking the key. DELETE THIS FILE once capture is confirmed.
 */
export async function onRequestGet({ request, env }) {
  const url = new URL(request.url);
  if (url.searchParams.get('diag') !== 'ml7823') {
    return new Response('not found', { status: 404 });
  }

  const out = {
    env: {
      MAILERLITE_API_KEY: env.MAILERLITE_API_KEY ? 'set (' + String(env.MAILERLITE_API_KEY).length + ' chars)' : 'MISSING',
      ML_GROUP_GUIDE: env.ML_GROUP_GUIDE || 'MISSING',
      ML_GROUP_NEWSLETTER: env.ML_GROUP_NEWSLETTER || 'MISSING',
    },
    mailerlite: null,
    groups: null,
  };

  if (env.MAILERLITE_API_KEY) {
    try {
      const r = await fetch('https://connect.mailerlite.com/api/groups?limit=25', {
        headers: {
          Authorization: 'Bearer ' + env.MAILERLITE_API_KEY,
          Accept: 'application/json',
        },
      });
      out.mailerlite = { status: r.status, ok: r.ok };
      const text = await r.text();
      try {
        const j = JSON.parse(text);
        if (Array.isArray(j.data)) {
          out.groups = j.data.map((g) => ({ id: g.id, name: g.name, total: g.active_count }));
        } else {
          out.mailerlite.body = text.slice(0, 400);
        }
      } catch (_) {
        out.mailerlite.body = text.slice(0, 400);
      }
    } catch (e) {
      out.mailerlite = { error: e && e.message };
    }
  }

  return new Response(JSON.stringify(out, null, 2), {
    headers: { 'content-type': 'application/json' },
  });
}
