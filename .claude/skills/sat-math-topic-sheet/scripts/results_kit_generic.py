#!/usr/bin/env python3
"""LCC results kit, generic edition: autosave + "Results for your tutor" for the SAT sheets
that are NOT built on the SAT Math topic-sheet shell (those use results_kit.py).

One core (floating button, panel, report, autosave, welcome-back banner) plus a small
adapter per sheet family that says how to collect results and how to snapshot/restore state:

  verbal   SAT-Reading-1-Student-Notes, SAT-Grammar-1-Transitions, SAT-Grammar-2-Sentence-Boundaries
           (KEY/NQ, radio inputs q<n>, submitAll/resetAll, timer with elapsed/started)
  wic      SAT-Words-in-Context sets 1 to 3 (QD/N, radio inputs q<n>, doSubmit, flags, countdown)
  desmos   SAT-Desmos-Strategies (the GQ gauntlet in G.results, plus the FP fill-in format drill)

Usage:  python3 results_kit_generic.py <sheet.html> [...]     (family is detected from the file)
        python3 results_kit_generic.py --strip <sheet.html>    (remove the kit)
Re-running refreshes the kit in place; stripping restores the original byte for byte."""
import os, re, sys

MARK = '/* LCC results kit generic v1 */'

CSS = r'''/* rkg:begin */
/* LCC results kit (generic) v1: floating button, welcome-back banner, tutor report panel */
.rkg-fab { position: fixed; left: 16px; bottom: 16px; z-index: 450; display: inline-flex; align-items: center; gap: 8px; padding: 10px 16px; border-radius: 999px; border: 2px solid #DDA25E; background: #FFFCF6; color: #42260D; font-family: 'Inter', -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif; font-size: 13.5px; font-weight: 700; cursor: pointer; box-shadow: 0 6px 20px rgba(0,0,0,0.22); transition: transform 0.15s, background 0.2s; }
.rkg-fab:hover { background: #DDA25E; transform: translateY(-1px); }
.rkg-fab .n { background: #21442B; color: white; border-radius: 999px; padding: 1px 8px; font-size: 12px; }
.rkg-banner { background: #FFFCF6; border: 1.5px solid #E6BC84; border-left: 5px solid #DDA25E; border-radius: 8px; padding: 10px 16px; margin: 0 0 18px; font-family: 'Inter', -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif; font-size: 13.5px; line-height: 1.5; color: #2D2D2D; display: flex; gap: 10px 14px; align-items: center; flex-wrap: wrap; }
.rkg-card { background: white; border-radius: 8px; padding: 18px 20px; margin: 18px 0; border-left: 5px solid #39864E; box-shadow: 0 2px 8px rgba(0,0,0,0.08); font-family: 'Inter', -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif; color: #2D2D2D; }
.rkg-card h3 { margin: 0 0 6px; font-size: 17px; color: #42260D; }
.rkg-card p { margin: 0 0 10px; font-size: 14px; color: #555; line-height: 1.55; }
.rkg-b { display: inline-flex; align-items: center; gap: 6px; padding: 9px 16px; border-radius: 8px; border: 2px solid transparent; font-family: inherit; font-size: 14px; font-weight: 700; cursor: pointer; transition: background 0.2s; }
.rkg-b-gold { background: #DDA25E; color: #42260D; }
.rkg-b-gold:hover { background: #E6BC84; }
.rkg-b-ghost { background: transparent; color: #555; border-color: #E8E0D0; }
.rkg-b-ghost:hover { border-color: #DDA25E; color: #42260D; }
.rkg-b-sm { padding: 6px 12px; font-size: 13px; }
.rkg-overlay { position: fixed; inset: 0; background: rgba(39,20,4,0.45); z-index: 500; display: none; align-items: center; justify-content: center; padding: 16px; }
.rkg-overlay.open { display: flex; }
.rkg-modal { background: #FBF7EF; border-radius: 12px; max-width: 580px; width: 100%; max-height: 92vh; overflow: auto; padding: 22px 24px 18px; box-shadow: 0 12px 40px rgba(0,0,0,0.3); border-top: 6px solid #DDA25E; font-family: 'Inter', -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif; color: #2D2D2D; }
.rkg-modal h3 { color: #21442B; margin: 0 0 6px; font-size: 20px; }
.rkg-modal p { font-size: 14px; color: #555; margin: 0 0 10px; line-height: 1.55; }
.rkg-name { display: flex; align-items: center; gap: 10px; margin: 6px 0 14px; font-size: 13.5px; font-weight: 600; color: #42260D; }
.rkg-name input { flex: 1; min-width: 120px; padding: 8px 10px; border: 2px solid #E8E0D0; border-radius: 6px; font-size: 15px; font-family: inherit; background: white; }
.rkg-name input:focus { border-color: #21442B; outline: none; }
.rkg-stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(110px, 1fr)); gap: 8px; margin-bottom: 14px; }
.rkg-stat { background: white; border: 1.5px solid #E6BC84; border-radius: 8px; padding: 8px 6px; text-align: center; }
.rkg-stat b { display: block; font-size: 20px; color: #DDA25E; line-height: 1.2; }
.rkg-stat span { font-size: 10.5px; text-transform: uppercase; letter-spacing: 0.5px; color: #666; }
.rkg-actions { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
.rkg-status { font-size: 13px; color: #39864E; font-weight: 600; min-height: 20px; margin-top: 10px; }
.rkg-fine { font-size: 12.5px; color: #666; margin-top: 10px; }
.rkg-fine a { color: #BC6C26; font-weight: 600; cursor: pointer; }
@media (max-width: 600px) { .rkg-fab { padding: 8px 12px; font-size: 12.5px; } }
/* rkg:end */'''

OVERLAY = '''<!-- rkg:begin -->
<div class="rkg-overlay" id="rkgOverlay" onclick="if (event.target === this) rkgClose();" role="dialog" aria-modal="true" aria-labelledby="rkgTitle">
    <div class="rkg-modal">
        <h3 id="rkgTitle">Results for your tutor</h3>
        <p>Nothing is sent automatically. <strong>Download results</strong> makes one file with every answer on this sheet: text or email that file to your tutor. <strong>Copy summary</strong> gives a short version to paste into a message.</p>
        <label class="rkg-name">Your name <input type="text" id="rkgName" placeholder="so your tutor knows whose results these are" autocomplete="name" oninput="rkgSyncName()"></label>
        <div class="rkg-stats" id="rkgStats"></div>
        <div class="rkg-actions">
            <button class="rkg-b rkg-b-gold" onclick="rkgDownload()">&#8681; Download results</button>
            <button class="rkg-b rkg-b-ghost" onclick="rkgCopy()">Copy summary</button>
            <button class="rkg-b rkg-b-ghost" onclick="rkgEmail()">Email summary</button>
            <span style="flex:1"></span>
            <button class="rkg-b rkg-b-ghost" onclick="rkgClose()">Close</button>
        </div>
        <div class="rkg-status" id="rkgStatus"></div>
        <div class="rkg-fine">Your answers are saved in this browser automatically, so you can close the tab and come back. <a onclick="rkgReset()">Start fresh</a> clears them.</div>
    </div>
</div>
<!-- rkg:end -->
'''

# ----------------------------------------------------------------- adapters (JS)
ADAPTERS = {}

ADAPTERS['verbal'] = r'''
var RK_ADAPTER = {
    bannerHost: function() { return document.querySelector('.container'); },
    fabBottom: 16,
    hooks: ['submitAll', 'resetAll'],
    afterHook: function(name) { if (name === 'submitAll' && submitted) rkgMountCard(document.querySelector('#scoreBody .score-hero'), 'after'); },
    snapshot: function() {
        var ans = {}, flags = [], struck = [];
        for (var i = 1; i <= NQ; i++) { var sel = document.querySelector('input[name=q' + i + ']:checked'); if (sel) ans[i] = +sel.value; var q = document.getElementById('q' + i); if (q && q.classList.contains('flagged')) flags.push(i); }
        document.querySelectorAll('.choice.struck').forEach(function(c) { if (c.id) struck.push(c.id); });
        return { ans: ans, flags: flags, struck: struck, submitted: submitted, elapsed: elapsed, started: started };
    },
    restore: function(s) {
        Object.keys(s.ans || {}).forEach(function(n) { var r = document.querySelector('input[name=q' + n + '][value="' + s.ans[n] + '"]'); if (r) r.checked = true; });
        (s.flags || []).forEach(function(n) { var q = document.getElementById('q' + n); if (q) q.classList.add('flagged'); });
        (s.struck || []).forEach(function(id) { var c = document.getElementById(id); if (c) c.classList.add('struck'); });
        if (s.elapsed) elapsed = s.elapsed; if (s.started) started = true;
        if (typeof renderTimer === 'function') renderTimer();
        if (typeof onAnswer === 'function') onAnswer();
        if (s.submitted) { var c = window.confirm; window.confirm = function() { return true; }; try { submitAll(); } finally { window.confirm = c; } }
    },
    collect: function() {
        var items = [], answered = 0, correct = 0;
        KEY.forEach(function(k) {
            var sel = document.querySelector('input[name=q' + k.n + ']:checked'), you = sel ? +sel.value : -1, ok = you === k.ans;
            if (you >= 0) answered++; if (ok) correct++;
            var q = document.getElementById('q' + k.n), why = document.getElementById('why' + k.n);
            var txt = q ? Array.prototype.map.call(q.querySelectorAll('.txt, p.q-stem'), function(e) { return e.textContent.trim(); }).join(' ') : '';
            var choice = function(i) { var c = document.getElementById('c' + k.n + '_' + i); var t = c ? c.textContent.replace(/×\s*$/, '').replace(/\s+/g, ' ').trim() : ''; return t.replace(/^([A-D])\.\s*/, '$1. '); };
            items.push({ n: k.n, label: 'Q' + k.n, tag: k.skill + (k.place ? ' / ' + k.place : ''), q: txt, yours: you >= 0 ? choice(you) : '', correct: choice(k.ans), ok: ok, answered: you >= 0,
                flagged: !!(q && q.classList.contains('flagged')), note: why ? why.innerHTML.replace(/<span class="skill-tag"[^>]*>.*?<\/span>/g, '').trim() : '' });
        });
        return { sections: [{ key: 'practice', title: 'Practice section', total: NQ, attempted: answered, correct: correct, finished: !!submitted, time: started ? elapsed : 0, items: items }] };
    }
};
'''

ADAPTERS['wic'] = r'''
var RK_ADAPTER = {
    bannerHost: function() { return document.querySelector('.wrap'); },
    fabBottom: 84,
    hooks: ['doSubmit'],
    afterHook: function(name) { if (name === 'doSubmit' && submitted) rkgMountCard(document.querySelector('#results .card') || document.getElementById('results'), 'append'); },
    snapshot: function() {
        var ans = {}; QD.forEach(function(q) { var sel = document.querySelector('input[name="q' + q.n + '"]:checked'); if (sel) ans[q.n] = +sel.value; });
        return { ans: ans, flags: Object.keys(flags).filter(function(n) { return flags[n]; }), submitted: submitted, remaining: remaining, running: !!tid };
    },
    restore: function(s) {
        Object.keys(s.ans || {}).forEach(function(n) { var r = document.querySelector('input[name="q' + n + '"][value="' + s.ans[n] + '"]'); if (r) r.checked = true; });
        (s.flags || []).forEach(function(n) { flags[n] = true; var b = document.querySelector('.flag[data-n="' + n + '"]'); if (b) { b.classList.add('on'); var c = b.closest('.card'); if (c) c.classList.add('flagged'); } });
        if (typeof s.remaining === 'number') remaining = s.remaining;
        if (typeof updateProg === 'function') updateProg();
        if (s.submitted) { submitted = false; doSubmit(false); }
        else if (s.running) { var b = document.getElementById('timer-start'); if (b) b.click(); }
    },
    collect: function() {
        var items = [], answered = 0, correct = 0;
        QD.forEach(function(q) {
            var sel = document.querySelector('input[name="q' + q.n + '"]:checked'), g = sel ? +sel.value : -1, ok = g === q.answer;
            if (g >= 0) answered++; if (ok) correct++;
            var card = document.querySelector('.qcard[data-qid="' + q.n + '"]');
            var tag = card ? (card.querySelector('.q-tag') || {}).textContent || '' : '';
            var txt = card ? Array.prototype.map.call(card.querySelectorAll('.passage, .q-prompt'), function(e) { return e.textContent.trim(); }).join(' ') : '';
            items.push({ n: q.n, label: 'Q' + q.n, tag: tag, q: txt, yours: g >= 0 ? 'ABCD'[g] + '. ' + q.options[g] : '', correct: 'ABCD'[q.answer] + '. ' + q.options[q.answer], ok: ok, answered: g >= 0, flagged: !!flags[q.n], note: q.rationale || '' });
        });
        return { sections: [{ key: 'practice', title: 'Practice (' + N + ' questions)', total: N, attempted: answered, correct: correct, finished: !!submitted, time: 0, items: items }] };
    }
};
'''

ADAPTERS['desmos'] = r'''
var rkgFp = {};
var RK_ADAPTER = {
    bannerHost: function() { return document.querySelector('.container'); },
    fabBottom: 16,
    hooks: ['gFinish', 'gSubmit', 'gNext', 'gStart', 'gReset', 'fpGo'],
    beforeHook: function(name, args) { if (name === 'fpGo') { var i = args[0], e = document.getElementById('fpi' + i); if (e) rkgFp[i] = { v: e.value, ok: fpCheck(e.value, FP[i][1], FP[i][2])[0] }; } },
    afterHook: function(name) { if (name === 'gFinish') rkgMountCard(document.getElementById('g-summary'), 'append'); },
    snapshot: function() { return { G: { order: G.order, i: G.i, results: G.results, mode: G.mode, done: G.done }, fp: rkgFp }; },
    restore: function(s) {
        rkgFp = s.fp || {};
        Object.keys(rkgFp).forEach(function(i) { var e = document.getElementById('fpi' + i); if (e) { e.value = rkgFp[i].v; if (typeof fpLive === 'function') fpLive(+i); fpGo(+i); } });
        var g = s.G; if (!g || !g.order || !g.order.length) return;
        G.order = g.order; G.results = g.results || []; G.mode = g.mode || 'tier'; G.done = !!g.done;
        if (typeof gSetOrder === 'function') gSetOrder(G.mode);
        var intro = document.getElementById('g-intro'), stage = document.getElementById('g-stage');
        if (G.done) { if (intro) intro.style.display = 'none'; gFinish(); return; }
        G.i = Math.min(G.results.length, G.order.length - 1);
        if (G.results.length >= G.order.length) { G.i = G.order.length - 1; if (intro) intro.style.display = 'none'; gFinish(); return; }
        if (intro) intro.style.display = 'none'; if (stage) stage.style.display = '';
        gShow();
    },
    collect: function() {
        var items = [], correct = 0, secs = 0;
        (G.results || []).forEach(function(r, k) {
            var q = GQ[r.qi]; if (!q) return; if (r.ok) correct++; secs += r.secs || 0;
            var correctText = q.format === 'mc' ? 'ABCD'[q.answer] + '. ' + q.options[q.answer] : (q.accepted || []).join(' or ');
            var yours = q.format === 'mc' ? (r.given ? r.given + '. ' + (q.options['ABCD'.indexOf(r.given)] || '') : '') : r.given;
            items.push({ n: k + 1, label: 'Q' + (k + 1), tag: q.tier + (q.title ? ' / ' + q.title : ''), q: (q.prompt || '').replace(/\$\$[^$]*\$\$/g, ' [equations] '), yours: yours, correct: correctText, ok: !!r.ok, answered: true, note: (r.secs != null ? r.secs + 's. ' : '') + (q.desmos || '') });
        });
        var fpItems = [], fpOk = 0;
        Object.keys(rkgFp).sort(function(a, b) { return a - b; }).forEach(function(i) { var it = FP[i]; if (!it) return; if (rkgFp[i].ok) fpOk++; fpItems.push({ n: +i + 1, label: 'Item ' + (+i + 1), tag: it[2], q: it[0], yours: rkgFp[i].v, correct: fpDecimalString ? (it[1].q === 1 ? String(it[1].p) : it[1].p + '/' + it[1].q) : '', ok: !!rkgFp[i].ok, answered: true, note: '' }); });
        return { sections: [
            { key: 'gauntlet', title: 'SAT-Style Practice (timed set)', total: G.order && G.order.length ? G.order.length : GQ.length, attempted: items.length, correct: correct, finished: !!G.done, time: secs, items: items },
            { key: 'format', title: 'Formatting Your Answers drill', total: FP.length, attempted: fpItems.length, correct: fpOk, finished: fpItems.length === FP.length, time: 0, items: fpItems }
        ] };
    }
};
'''

# ----------------------------------------------------------------- core (JS)
CORE_JS = r'''
/* ================= LCC results kit (generic) v1: autosave + results report ================= */
/* LCC results kit generic v1 */
var RKG_TUTOR_EMAIL = '';
var rkg = { name: '', restoredAt: null, t: null, loading: false, mounted: false };
function rkgStore(k, v) { try { if (v == null) localStorage.removeItem(k); else localStorage.setItem(k, v); } catch (e) {} }
function rkgRead(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
function rkgSaveNow() { if (rkg.loading) return; try { rkgStore(RK_CFG.key, JSON.stringify({ v: 1, t: Date.now(), name: rkg.name, s: RK_ADAPTER.snapshot() })); } catch (e) {} }
function rkgSave() { if (rkg.t) clearTimeout(rkg.t); rkg.t = setTimeout(rkgSaveNow, 350); }
function rkgLoad() {
    var raw = rkgRead(RK_CFG.key); if (!raw) return;
    try { var s = JSON.parse(raw); if (!s || s.v !== 1) return; rkg.loading = true; rkg.name = s.name || ''; rkg.restoredAt = s.t || null; if (s.s) RK_ADAPTER.restore(s.s); }
    catch (e) {}
    rkg.loading = false;
}
/* wrap the host sheet's functions so the kit sees every submit / check */
(RK_ADAPTER.hooks || []).forEach(function(name) {
    var orig = window[name]; if (typeof orig !== 'function') return;
    window[name] = function() {
        if (RK_ADAPTER.beforeHook) { try { RK_ADAPTER.beforeHook(name, arguments); } catch (e) {} }
        var r = orig.apply(this, arguments);
        if (RK_ADAPTER.afterHook) { try { RK_ADAPTER.afterHook(name, arguments); } catch (e) {} }
        rkgSave();
        return r;
    };
});
function rkgFmtDate(ts) { try { return new Date(ts).toLocaleString([], { dateStyle: 'medium', timeStyle: 'short' }); } catch (e) { return new Date(ts).toLocaleString(); } }
function rkgFmtTime(s) { s = Math.round(s || 0); return Math.floor(s / 60) + ':' + String(s % 60).padStart(2, '0'); }
function rkgCardHtml() {
    return '<div class="rkg-card" id="rkgCard"><h3>Send these results to your tutor</h3>' +
        '<p>Nothing on this page is sent anywhere by itself, and nothing is lost either: your answers stay saved in this browser. To share them, download the results file (every question, your answer, the key, and the explanation) and text or email it, or copy a short summary into a message.</p>' +
        '<button class="rkg-b rkg-b-gold" onclick="rkgOpen()">&#8681; Download results for your tutor</button></div>';
}
function rkgMountCard(host, where) {
    if (!host) return; var old = document.getElementById('rkgCard'); if (old) old.remove();
    if (where === 'after') host.insertAdjacentHTML('afterend', rkgCardHtml()); else host.insertAdjacentHTML('beforeend', rkgCardHtml());
}
function rkgMountChrome() {
    if (rkg.mounted) return; rkg.mounted = true;
    var fab = document.createElement('button'); fab.className = 'rkg-fab'; fab.id = 'rkgFab'; fab.setAttribute('onclick', 'rkgOpen()'); fab.title = 'Download your results as a file you can text or email to your tutor';
    fab.innerHTML = '&#8681; Results for your tutor'; fab.style.bottom = (RK_ADAPTER.fabBottom || 16) + 'px'; document.body.appendChild(fab);
    if (rkg.restoredAt) {
        var host = (RK_ADAPTER.bannerHost && RK_ADAPTER.bannerHost()) || document.body;
        var b = document.createElement('div'); b.className = 'rkg-banner'; b.id = 'rkgBanner';
        b.innerHTML = '<span>&#128190; Welcome back: your answers from <strong>' + rkgFmtDate(rkg.restoredAt) + '</strong> are saved on this device and have been restored.</span>' +
            '<button class="rkg-b rkg-b-ghost rkg-b-sm" onclick="rkgOpen()">Results for your tutor</button><button class="rkg-b rkg-b-ghost rkg-b-sm" onclick="rkgReset()">Start fresh</button>';
        host.insertBefore(b, host.firstChild);
    }
}
function rkgReset() { if (!confirm('Clear every answer saved on this sheet and start fresh?')) return; rkg.loading = true; rkgStore(RK_CFG.key, null); location.reload(); }
/* ---- data ---- */
function rkgData() {
    var d = { kit: 'lcc-results-kit', version: 1, sheet: RK_CFG.sheet || document.title, url: location.href.split('#')[0], name: rkg.name, when: new Date().toISOString(), sections: [] };
    try { var c = RK_ADAPTER.collect(); d.sections = c.sections || []; if (c.takeaway) d.takeaway = c.takeaway; } catch (e) { d.error = String(e); }
    return d;
}
function rkgSummary(d) {
    var L = [d.sheet + (d.name ? ': results for ' + d.name : ': results') + ' (' + rkgFmtDate(Date.now()) + ')'];
    d.sections.forEach(function(s) {
        if (!s.attempted && !s.finished) { L.push(s.title + ': not started'); return; }
        var miss = s.items.filter(function(i) { return (i.answered || s.finished) && !i.ok; }).map(function(i) { return i.label || i.n; });
        L.push(s.title + ': ' + s.correct + '/' + (s.finished ? s.total : s.attempted) + (s.finished ? '' : ' so far (' + s.attempted + ' of ' + s.total + ' answered)') + (s.time ? ' in ' + rkgFmtTime(s.time) : '') + (miss.length ? '. Missed: ' + miss.join(', ') : ''));
    });
    if (d.takeaway) L.push('Takeaway: "' + d.takeaway + '"');
    L.push('Full report: ' + rkgFileName(d));
    return L.join('\n');
}
function rkgSlug(t) { return String(t || '').replace(/[^A-Za-z0-9]+/g, '-').replace(/^-+|-+$/g, ''); }
function rkgFileName(d) { return rkgSlug(d.sheet).slice(0, 60) + '-results' + (d.name ? '-' + rkgSlug(d.name) : '') + '-' + new Date().toISOString().slice(0, 10) + '.html'; }
function rkgReportHtml(d) {
    var esc = function(t) { return String(t == null ? '' : t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); };
    var mark = function(ok) { return ok ? '<span class="ok">&#10003;</span>' : '<span class="no">&#10007;</span>'; };
    var row = function(cells, cls) { return '<tr' + (cls ? ' class="' + cls + '"' : '') + '>' + cells.map(function(c) { return '<td>' + c + '</td>'; }).join('') + '</tr>'; };
    var table = function(head, rows) { return rows.length ? '<table><thead><tr>' + head.map(function(h) { return '<th>' + h + '</th>'; }).join('') + '</tr></thead><tbody>' + rows.join('') + '</tbody></table>' : '<p class="muted">Nothing attempted here yet.</p>'; };
    var h = '<div class="head"><div><div class="kicker">Learning Curve Collective &bull; results report</div><h1>' + esc(d.sheet) + '</h1></div>' +
        '<div class="meta"><div><b>Student:</b> ' + (d.name ? esc(d.name) : '<em>not given</em>') + '</div><div><b>Generated:</b> ' + rkgFmtDate(Date.parse(d.when)) + '</div><div><b>Sheet:</b> <a href="' + esc(d.url) + '">' + esc(d.url) + '</a></div></div></div>';
    h += '<div class="tiles">' + d.sections.map(function(s) { return '<div class="tile"><b>' + s.correct + '/' + (s.finished ? s.total : s.attempted) + '</b><span>' + esc(s.title) + (s.finished ? '' : ' (' + s.attempted + ' of ' + s.total + ' answered)') + (s.time ? ' &bull; ' + rkgFmtTime(s.time) : '') + '</span></div>'; }).join('') + '</div>';
    if (d.takeaway) h += '<div class="take"><b>Key takeaway (in the student\'s words):</b> ' + esc(d.takeaway) + '</div>';
    var review = [];
    d.sections.forEach(function(s) { s.items.forEach(function(i) { if ((i.answered || s.finished) && !i.ok) review.push({ s: s, i: i }); }); });
    if (review.length) {
        h += '<h2>Review list: the misses and the explanation for each</h2>';
        review.forEach(function(r) { h += '<div class="rev"><div class="rev-h">' + mark(false) + ' <b>' + esc(r.s.title) + ', ' + esc(r.i.label) + '</b>' + (r.i.tag ? '<span class="chip">' + esc(r.i.tag) + '</span>' : '') + (r.i.flagged ? '<span class="chip">flagged</span>' : '') + '<span class="ans">answered <b>' + (r.i.yours ? esc(r.i.yours) : '<em>nothing</em>') + '</b>, correct <b>' + esc(r.i.correct) + '</b></span></div>' + (r.i.q ? '<div class="stem">' + esc(r.i.q) + '</div>' : '') + (r.i.note ? '<div class="trap"><b>Explanation:</b> ' + r.i.note + '</div>' : '') + '</div>'; });
    }
    d.sections.forEach(function(s) {
        h += '<h2>' + esc(s.title) + (s.finished ? '' : ' (in progress)') + '</h2>' + table(['#', 'Type', 'Your answer', 'Correct', ''], s.items.map(function(i) { var counts = i.answered || s.finished; return row([esc(i.label) + (i.flagged ? ' &#9873;' : ''), esc(i.tag || ''), i.answered ? esc(i.yours) : '<em>no answer</em>', esc(i.correct), counts ? mark(i.ok) : ''], counts && !i.ok ? 'miss' : ''); }));
    });
    h += '<p class="muted foot">Generated by the sheet itself in the student\'s browser; nothing was sent to a server. The raw data is embedded in this file for import.</p>';
    return '<!DOCTYPE html>\n<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>' + esc(d.sheet) + ': results' + (d.name ? ' for ' + esc(d.name) : '') + '</title>' +
        '<script>window.MathJax = { tex: { inlineMath: [["$","$"]], displayMath: [["$$","$$"]] }, svg: { fontCache: "global" } };<\/script><script async src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.2/es5/tex-svg.min.js"><\/script>' +
        '<style>body{margin:0;background:#FBF7EF;color:#2D2D2D;font-family:Inter,-apple-system,Segoe UI,Helvetica,Arial,sans-serif;font-size:15px;line-height:1.5}.wrap{max-width:900px;margin:0 auto;padding:24px 20px 40px}.head{background:#21442B;color:white;border-radius:10px;padding:18px 22px;display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;border-bottom:4px solid #DDA25E}.kicker{font-size:11px;letter-spacing:1px;text-transform:uppercase;color:#E6BC84}h1{margin:4px 0 0;font-size:24px}.meta{font-size:13px;color:#F5E4CC}.meta a{color:#E6BC84;word-break:break-all}.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:18px 0}.tile{background:white;border:2px solid #E6BC84;border-radius:10px;padding:12px;text-align:center}.tile b{display:block;font-size:26px;color:#DDA25E}.tile span{font-size:11px;text-transform:uppercase;letter-spacing:.5px;color:#666}.take{background:white;border-left:5px solid #DDA25E;padding:12px 16px;border-radius:8px;margin:12px 0}h2{font-size:18px;color:#21442B;margin:26px 0 8px;border-bottom:2px solid #E8E0D0;padding-bottom:4px}table{width:100%;border-collapse:collapse;background:white;border-radius:8px;overflow:hidden;font-size:14px}th{background:#F5E4CC;color:#8B6914;font-size:11px;text-transform:uppercase;letter-spacing:.6px;text-align:left;padding:8px 10px}td{padding:8px 10px;border-top:1px solid #F1E6D2;vertical-align:top}tr.miss td{background:#FFF4F2}.ok{color:#39864E;font-weight:700}.no{color:#C0392B;font-weight:700}.muted{color:#777;font-size:13px}.foot{margin-top:28px}.rev{background:white;border-radius:8px;padding:12px 14px;margin:8px 0;border-left:5px solid #C0392B}.rev-h{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:6px}.chip{font-size:10.5px;text-transform:uppercase;letter-spacing:.5px;border-radius:99px;padding:2px 8px;background:#F5E4CC;color:#8B6914;font-weight:700}.ans{font-size:13px;color:#555}.stem{font-family:"Times New Roman",Georgia,serif;font-size:15.5px;margin:6px 0;color:#333}.trap{font-size:14px;color:#5A3E1B;background:#FFFCF6;border:1px solid #F1E6D2;border-radius:6px;padding:8px 10px}.trap .kbd{font-family:monospace;background:#eee;padding:0 4px;border-radius:3px}@media print{body{background:white}.head{-webkit-print-color-adjust:exact}}</style></head><body><div class="wrap">' + h + '</div>' +
        '<script type="application/json" id="lcc-results">' + JSON.stringify(d).replace(/</g, '\\u003c') + '<\/script></body></html>';
}
/* ---- the panel ---- */
function rkgStatus(t) { var el = document.getElementById('rkgStatus'); if (el) el.textContent = t; }
function rkgSyncName() { var inp = document.getElementById('rkgName'); if (!inp) return; rkg.name = inp.value.trim(); rkgStore('lcc:student-name', rkg.name || null); rkgSave(); }
function rkgOpen() {
    var ov = document.getElementById('rkgOverlay'); if (!ov) return;
    var d = rkgData();
    document.getElementById('rkgStats').innerHTML = d.sections.map(function(s) { return '<div class="rkg-stat"><b>' + s.correct + '/' + (s.finished ? s.total : s.attempted) + '</b><span>' + s.title.replace(/\(.*\)/, '').trim() + (s.finished ? '' : ', so far') + '</span></div>'; }).join('');
    var inp = document.getElementById('rkgName'); inp.value = rkg.name || rkgRead('lcc:student-name') || '';
    rkgStatus(''); ov.classList.add('open'); if (!inp.value) inp.focus();
}
function rkgClose() { var ov = document.getElementById('rkgOverlay'); if (ov) ov.classList.remove('open'); }
function rkgDownload() {
    rkgSyncName(); var d = rkgData(), name = rkgFileName(d);
    try { var blob = new Blob([rkgReportHtml(d)], { type: 'text/html' }); var a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = name; document.body.appendChild(a); a.click(); setTimeout(function() { URL.revokeObjectURL(a.href); a.remove(); }, 1500); rkgStatus('Downloaded ' + name + '. Now text or email that file to your tutor.'); }
    catch (e) { rkgStatus('The download could not start in this browser. Use Copy summary instead.'); }
}
function rkgCopyFallback(t) { var ta = document.createElement('textarea'); ta.value = t; ta.style.position = 'fixed'; ta.style.opacity = 0; document.body.appendChild(ta); ta.select(); try { document.execCommand('copy'); } catch (e) {} ta.remove(); }
function rkgCopy() { rkgSyncName(); var t = rkgSummary(rkgData()), done = function() { rkgStatus('Summary copied. Paste it into a text or an email.'); }; if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(t).then(done, function() { rkgCopyFallback(t); done(); }); else { rkgCopyFallback(t); done(); } }
function rkgEmail() { rkgSyncName(); var d = rkgData(); var body = rkgSummary(d) + '\n\n(The full report is the downloaded file ' + rkgFileName(d) + '; attach it to this email.)'; location.href = 'mailto:' + encodeURIComponent(RKG_TUTOR_EMAIL) + '?subject=' + encodeURIComponent(d.sheet + ': results' + (d.name ? ' for ' + d.name : '')) + '&body=' + encodeURIComponent(body); rkgStatus('Your email app should open with the summary filled in. Attach the downloaded report if you have it.'); }
document.addEventListener('keydown', function(e) { if (e.key === 'Escape') rkgClose(); if (e.key === 'Enter') rkgSave(); }, true);
document.addEventListener('click', function(e) { var t = e.target; if (t && t.closest && t.closest('button, label, .choice, .option, .g-opt, .flag, .lq-c')) rkgSave(); }, true);
document.addEventListener('input', function(e) { var t = e.target; if (t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA')) rkgSave(); }, true);
document.addEventListener('change', function() { rkgSave(); }, true);
window.addEventListener('beforeunload', rkgSaveNow);
setInterval(rkgSave, 20000);
function rkgBoot() { rkgLoad(); rkgMountChrome(); }
if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function() { setTimeout(rkgBoot, 0); }); else setTimeout(rkgBoot, 0);
'''

FAMILY_PATTERNS = [
    ('verbal', lambda h: 'function submitAll()' in h and 'var KEY = [' in h and 'var NQ = ' in h),
    ('wic', lambda h: 'const SETKEY=' in h and 'function doSubmit(' in h and 'const QD=[' in h),
    ('desmos', lambda h: 'var GQ = [' in h and 'function gFinish()' in h and 'var FP = [' in h),
]


def detect(html):
    for name, test in FAMILY_PATTERNS:
        if test(html):
            return name
    return None


def strip(html):
    html = re.sub(r'<!-- rkg:begin -->.*?<!-- rkg:end -->\n?', '', html, flags=re.S)
    html = re.sub(r'/\* rkg:begin \*/.*?/\* rkg:end \*/\n?', '', html, flags=re.S)
    html = re.sub(r'<script>/\* rkg:js:begin \*/.*?/\* rkg:js:end \*/</script>\n', '', html, flags=re.S)
    return html


def inject(html, family=None, sheet_title=None, key=None, path=None):
    if MARK in html:
        html = strip(html)
    family = family or detect(html)
    if family not in ADAPTERS:
        raise SystemExit('results_kit_generic: cannot detect the sheet family for %s' % (path or 'this sheet'))
    base = os.path.splitext(os.path.basename(path or 'sheet'))[0]
    key = key or ('lcc-rk:' + re.sub(r'[^A-Za-z0-9]+', '-', base).lower() + ':progress')
    if sheet_title is None:
        m = re.search(r'<title>(.*?)</title>', html, flags=re.S)
        sheet_title = re.sub(r'\s+', ' ', m.group(1)).strip() if m else base
        sheet_title = re.split(r'\s*(?:\||:\s*Interactive Worksheet|— Learning Curve)', sheet_title)[0].strip()
    cfg = "var RK_CFG = " + __import__('json').dumps({'key': key, 'sheet': sheet_title, 'family': family}) + ";"
    js = '<script>/* rkg:js:begin */\n' + cfg + '\n' + ADAPTERS[family].strip('\n') + '\n' + CORE_JS.strip('\n') + '\n/* rkg:js:end */</script>\n'
    # CSS before the first </style> inside <head>; overlay before </body>; JS right before </body>
    i = html.index('</style>')
    html = html[:i] + CSS + '\n' + html[i:]
    j = html.rindex('</body>')
    html = html[:j] + OVERLAY + js + html[j:]
    return html


if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    do_strip = args and args[0] == '--strip'
    if do_strip:
        args = args[1:]
    for p in args:
        src = open(p, encoding='utf-8').read()
        if do_strip:
            out = strip(src)
        else:
            out = inject(src, path=p)
        if out == src:
            print('up to date:', p)
        else:
            open(p, 'w', encoding='utf-8').write(out)
            print(('stripped:' if do_strip else ('refreshed:' if MARK in src else 'patched (%s):' % detect(src))), p, len(src), '->', len(out), 'bytes')
