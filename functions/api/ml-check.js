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

    // When ?lookup=<email>, fetch that subscriber and show which groups it's in.
    const lookup = url.searchParams.get('lookup');
    if (lookup) {
      try {
        const lr = await fetch('https://connect.mailerlite.com/api/subscribers/' + encodeURIComponent(lookup), {
          headers: { Authorization: 'Bearer ' + env.MAILERLITE_API_KEY, Accept: 'application/json' },
        });
        const lt = await lr.text();
        try {
          const j = JSON.parse(lt);
          const d = j.data || {};
          out.lookup = {
            email: d.email,
            status: lr.status,
            groups: (d.groups || []).map((g) => ({ id: g.id, name: g.name })),
            fields: d.fields ? { name: d.fields.name, source: d.fields.source } : null,
          };
        } catch (_) {
          out.lookup = { status: lr.status, body: lt.slice(0, 400) };
        }
      } catch (e) {
        out.lookup = { error: e && e.message };
      }
    }

    // When ?post=1, replicate the real subscriber write and surface the raw
    // MailerLite response so we can see exactly why it fails.
    if (url.searchParams.get('post') === '1') {
      const gid = String(env.ML_GROUP_GUIDE || '').match(/(\d{6,})(?!.*\d)/);
      const payload = {
        email: 'diag-' + Date.now() + '@example.com',
        status: 'active',
        groups: gid ? [gid[1]] : [],
      };
      try {
        const pr = await fetch('https://connect.mailerlite.com/api/subscribers', {
          method: 'POST',
          headers: {
            Authorization: 'Bearer ' + env.MAILERLITE_API_KEY,
            'Content-Type': 'application/json',
            Accept: 'application/json',
          },
          body: JSON.stringify(payload),
        });
        out.postTest = { sent: payload, status: pr.status, ok: pr.ok, body: (await pr.text()).slice(0, 800) };
      } catch (e) {
        out.postTest = { sent: payload, error: e && e.message };
      }
    }
  }

  return new Response(JSON.stringify(out, null, 2), {
    headers: { 'content-type': 'application/json' },
  });
}
