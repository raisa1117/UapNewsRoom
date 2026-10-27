(function () {
  const $ = (s, r = document) => r.querySelector(s);```javascript
(function () { 
  // Initialize DOM selector helpers for selecting single and multiple elements.
  const $ = (s, r = document) => r.querySelector(s); 
  const $$ = (s, r = document) => [...r.querySelectorAll(s)]; 

  // Read the CSRF token from the browser cookies for secure POST requests.
  const csrf = (document.cookie.match(/csrftoken=([^;]+)/) || [])[1]; 
 
  // Display temporary notification messages on the page.
  const toast = msg => { 
    const t = document.createElement('div'); t.className = 'toast'; t.textContent = msg; 
    $('#toasts').appendChild(t); setTimeout(() => t.remove(), 3200); 
  }; 

  // Send POST requests with form data and the CSRF token.
  async function send(url, data = {}) { 
    const r = await fetch(url, { method: 'POST', headers: { 'X-CSRFToken': csrf, 'Content-Type': 'application/x-www-form-urlencoded' }, body: new URLSearchParams(data) }); 
    if (!r.ok) throw new Error(r.status); 
    return r.json(); 
  } 

  // Apply a CSS class and remove the element after the transition delay.
  const fade = (el, cls = 'gone') => { el.classList.add(cls); setTimeout(() => el.remove(), 300); }; 
 
  // Display today's date in the front-page date section.
  $('#today').textContent = new Date().toLocaleDateString(undefined, { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' }); 

  // Toggle between light and dark themes and save the selected preference.
  $('#theme').addEventListener('click', () => { 
    const n = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark'; 
    document.documentElement.dataset.theme = n; 
    try { localStorage.setItem('uap-theme', n); } catch (e) {} 
  }); 

  // Convert existing flash messages into toast notifications.
  $$('.flash').forEach(f => { toast(f.textContent); f.remove(); }); 
 
  // ---- Front page: sections, kind, search, layout, follow ---- 
  // Initialize the story container and its filtering controls.
  const box = $('#stories'); 
  if ($('#sections')) { 
    const st = { sec: '', kind: '', q: '' }, cards = $$('.story', box); 

    // Filter stories using the selected section, type, and search query.
    const apply = () => { 
      let n = 0, lead = null; 
      cards.forEach(c => { 
        const ok = (!st.sec || c.dataset.sec === st.sec) && (!st.kind || c.dataset.kind === st.kind) && (!st.q || c.dataset.text.includes(st.q)); 
        c.classList.toggle('hide', !ok); c.classList.remove('lead'); 
        if (ok) { n++; lead = lead || c; } 
      }); 
      if (lead && !box.classList.contains('list')) lead.classList.add('lead'); 
      $('#blank').hidden = n > 0; 
      $('#count').textContent = cards.length ? `${n} of ${cards.length} stories` : ''; 
    }; 

    // Handle selection buttons for sections, story types, and layouts.
    const pick = (root, fn) => root.addEventListener('click', e => { 
      const b = e.target.closest('button[data-v]'); if (!b) return; 
      $$('button[data-v]', root).forEach(x => x.classList.toggle('on', x === b)); fn(b.dataset.v); 
    }); 

    // Register the story filtering and layout controls.
    pick($('#sections'), v => { st.sec = v; apply(); }); 
    pick($('#kinds'), v => { st.kind = v; apply(); }); 
    pick($('#layout'), v => { box.classList.toggle('list', v === 'list'); apply(); }); 

    // Update the visible stories whenever the search input changes.
    $('#q').addEventListener('input', e => { st.q = e.target.value.trim().toLowerCase(); apply(); }); 

    // Follow or unfollow the selected item and show the result.
    $$('.follow').forEach(b => b.addEventListener('click', async () => { 
      try { const d = await send(b.dataset.url); b.classList.toggle('on', d.on); toast(d.on ? `Following ${d.name}` : `Unfollowed ${d.name}`); } 
      catch (e) { toast('Could not update. Try again.'); } 
    })); 

    // Apply the initial story filtering state.
    apply(); 
  } 
 
  // ---- Write form counter ---- 
  // Update the character count as the user writes a story.
  const body = $('textarea[name=body]'); 
  if (body && $('#chars')) { const u = () => $('#chars').textContent = body.value.length; body.addEventListener('input', u); u(); } 
 
  // ---- Reading page: progress bar, favourite, flag ---- 
  // Calculate the reading progress and update the progress bar on scroll.
  const bar = $('#progress'); 
  if (bar) addEventListener('scroll', () => { 
    const h = document.documentElement; bar.style.width = (h.scrollTop / Math.max(1, h.scrollHeight - h.clientHeight) * 100) + '%'; 
  }, { passive: true }); 

  // Handle the favourite button and update its label and count.
  const fav = $('#fav'); 
  if (fav) fav.addEventListener('click', async () => { 
    try { const d = await send(fav.dataset.url); $('#fav-label').textContent = d.on ? '★ Favourited' : '☆ Favourite'; $('#fav-count').textContent = d.count; } 
    catch (e) { toast('Could not update. Try again.'); } 
  }); 

  // Open the reporting dialog and submit the selected flag reason.
  const dlg = $('#flag-dlg'); 
  if (dlg) { 
    $('#flag-open').addEventListener('click', () => dlg.showModal()); 
    $('#flag-send').addEventListener('click', async () => { 
      try { const d = await send($('#flag-send').dataset.url, { reason: $('#flag-reason').value }); toast(d.new ? 'Sent to the editors' : 'You already flagged this'); } 
      catch (e) { toast('Could not send the flag.'); } 
    }); 
  } 
 
  // ---- Editor desk: pick, approve, reject, close flags ---- 
  // Initialize the editor queue and select the first available item.
  const queue = $('#queue'); 

  // Show the first queue item or display the empty-sta
```

  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const csrf = (document.cookie.match(/csrftoken=([^;]+)/) || [])[1];

  const toast = msg => {
    const t = document.createElement('div'); t.className = 'toast'; t.textContent = msg;
    $('#toasts').appendChild(t); setTimeout(() => t.remove(), 3200);
  };
  async function send(url, data = {}) {
    const r = await fetch(url, { method: 'POST', headers: { 'X-CSRFToken': csrf, 'Content-Type': 'application/x-www-form-urlencoded' }, body: new URLSearchParams(data) });
    if (!r.ok) throw new Error(r.status);
    return r.json();
  }
  const fade = (el, cls = 'gone') => { el.classList.add(cls); setTimeout(() => el.remove(), 300); };

  $('#today').textContent = new Date().toLocaleDateString(undefined, { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' });
  $('#theme').addEventListener('click', () => {
    const n = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
    document.documentElement.dataset.theme = n;
    try { localStorage.setItem('uap-theme', n); } catch (e) {}
  });
  $$('.flash').forEach(f => { toast(f.textContent); f.remove(); });

  // ---- Front page: sections, kind, search, layout, follow ----
  const box = $('#stories');
  if ($('#sections')) {
    const st = { sec: '', kind: '', q: '' }, cards = $$('.story', box);
    const apply = () => {
      let n = 0, lead = null;
      cards.forEach(c => {
        const ok = (!st.sec || c.dataset.sec === st.sec) && (!st.kind || c.dataset.kind === st.kind) && (!st.q || c.dataset.text.includes(st.q));
        c.classList.toggle('hide', !ok); c.classList.remove('lead');
        if (ok) { n++; lead = lead || c; }
      });
      if (lead && !box.classList.contains('list')) lead.classList.add('lead');
      $('#blank').hidden = n > 0;
      $('#count').textContent = cards.length ? `${n} of ${cards.length} stories` : '';
    };
    const pick = (root, fn) => root.addEventListener('click', e => {
      const b = e.target.closest('button[data-v]'); if (!b) return;
      $$('button[data-v]', root).forEach(x => x.classList.toggle('on', x === b)); fn(b.dataset.v);
    });
    pick($('#sections'), v => { st.sec = v; apply(); });
    pick($('#kinds'), v => { st.kind = v; apply(); });
    pick($('#layout'), v => { box.classList.toggle('list', v === 'list'); apply(); });
    $('#q').addEventListener('input', e => { st.q = e.target.value.trim().toLowerCase(); apply(); });
    $$('.follow').forEach(b => b.addEventListener('click', async () => {
      try { const d = await send(b.dataset.url); b.classList.toggle('on', d.on); toast(d.on ? `Following ${d.name}` : `Unfollowed ${d.name}`); }
      catch (e) { toast('Could not update. Try again.'); }
    }));
    apply();
  }

  // ---- Write form counter ----
  const body = $('textarea[name=body]');
  if (body && $('#chars')) { const u = () => $('#chars').textContent = body.value.length; body.addEventListener('input', u); u(); }

  // ---- Reading page: progress bar, favourite, flag ----
  const bar = $('#progress');
  if (bar) addEventListener('scroll', () => {
    const h = document.documentElement; bar.style.width = (h.scrollTop / Math.max(1, h.scrollHeight - h.clientHeight) * 100) + '%';
  }, { passive: true });
  const fav = $('#fav');
  if (fav) fav.addEventListener('click', async () => {
    try { const d = await send(fav.dataset.url); $('#fav-label').textContent = d.on ? '★ Favourited' : '☆ Favourite'; $('#fav-count').textContent = d.count; }
    catch (e) { toast('Could not update. Try again.'); }
  });
  const dlg = $('#flag-dlg');
  if (dlg) {
    $('#flag-open').addEventListener('click', () => dlg.showModal());
    $('#flag-send').addEventListener('click', async () => {
      try { const d = await send($('#flag-send').dataset.url, { reason: $('#flag-reason').value }); toast(d.new ? 'Sent to the editors' : 'You already flagged this'); }
      catch (e) { toast('Could not send the flag.'); }
    });
  }

  // ---- Editor desk: pick, approve, reject, close flags ----
  const queue = $('#queue');
  const showFirst = () => {
    const first = $('.qitem', queue);
    if (first) { first.classList.add('on'); $('#' + first.dataset.pane).hidden = false; }
    else { $('#deskwrap').hidden = true; $('#desk-empty').hidden = false; }
  };
  if (queue) queue.addEventListener('click', e => {
    const q = e.target.closest('.qitem'); if (!q) return;
    $$('.qitem', queue).forEach(x => x.classList.toggle('on', x === q));
    $$('.pane').forEach(p => p.hidden = p.id !== q.dataset.pane);
  });
  document.addEventListener('click', async e => {
    const b = e.target.closest('button[data-act], button[data-close]'); if (!b) return;
    b.disabled = true;
    try {
      if (b.dataset.close) { await send(b.dataset.url); fade(b.closest('.line-item')); toast('Flag closed'); return; }
      const pane = b.closest('.pane'), note = $('textarea', pane).value;
      const d = await send(b.dataset.url, { note });
      const item = $(`.qitem[data-pane="${pane.id}"]`);
      pane.remove(); item.remove(); showFirst();
      $('#left').textContent = d.left;
      const nav = $('#nav-queue'); if (nav) nav.textContent = d.left;
      toast(b.dataset.act === 'approve' ? 'Published' : 'Rejected');
    } catch (err) { b.disabled = false; toast('Something went wrong. Try again.'); }
  });
})();
