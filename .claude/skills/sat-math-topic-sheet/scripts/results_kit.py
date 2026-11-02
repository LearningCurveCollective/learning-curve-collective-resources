#!/usr/bin/env python3
"""LCC results kit: patches an SAT Math topic sheet so that
  1. every answer the student gives is autosaved in the browser (localStorage) and restored
     on the next visit, with a "Welcome back" banner and a Start fresh button;
  2. a "Results for your tutor" button (tab bar, practice-set results, exit ticket) opens a
     panel that downloads a self-contained HTML report of every tab (practice set, challenge,
     fluency, quick checks, exit ticket, takeaway), copies a short text summary for a text
     message, or opens a pre-filled email. Nothing is ever sent automatically.
The report embeds its data as JSON (<script id="lcc-results">) so a hub tool can import it.

Usage:  python3 results_kit.py <sheet.html> [...]      patches the files in place (idempotent)
        from results_kit import inject; html = inject(html)
The shell sheet (SAT-Math-1-Linear-Equations.html) carries the kit, so builders that copy the
shell inherit it; they retarget the storage key by replacing 'sat-linear-sheet:rule'."""
import sys

MARK = '/* LCC results kit v1 */'
KIT_VERSION = 'v1'

CSS = r'''/* rk:begin */
/* LCC results kit v1: autosave banner, tutor-results button, report panel */
.rk-btn { margin-left: auto; display: inline-flex; align-items: center; gap: 7px; padding: 7px 14px; border-radius: 8px; border: 2px solid var(--gold); background: var(--gold-pale); color: var(--brown-dark); font-family: 'Inter', sans-serif; font-size: 13px; font-weight: 700; cursor: pointer; transition: background 0.2s; }
.rk-btn:hover { background: var(--gold); }
.rk-banner { background: #FFFCF6; border: 1.5px solid var(--gold-light); border-left: 5px solid var(--gold); border-radius: 8px; padding: 10px 16px; margin-bottom: 18px; font-family: 'Inter', sans-serif; font-size: 13.5px; line-height: 1.5; display: flex; gap: 10px 14px; align-items: center; flex-wrap: wrap; }
.rk-overlay { position: fixed; inset: 0; background: rgba(39,20,4,0.45); z-index: 500; display: none; align-items: center; justify-content: center; padding: 16px; }
.rk-overlay.open { display: flex; }
.rk-modal { background: var(--cream); border-radius: 12px; max-width: 580px; width: 100%; max-height: 92vh; overflow: auto; padding: 22px 24px 18px; box-shadow: 0 12px 40px rgba(0,0,0,0.3); border-top: 6px solid var(--gold); }
.rk-modal h3 { font-family: 'Switzer', 'Space Grotesk', sans-serif; color: var(--green-dark); margin: 0 0 6px; font-size: 20px; }
.rk-modal p { font-size: 14px; color: var(--text-medium); margin: 0 0 10px; line-height: 1.55; }
.rk-name { display: flex; align-items: center; gap: 10px; margin: 6px 0 14px; font-family: 'Inter', sans-serif; font-size: 13.5px; font-weight: 600; color: var(--brown-dark); }
.rk-name input { flex: 1; min-width: 120px; padding: 8px 10px; border: 2px solid var(--cream-dark); border-radius: 6px; font-size: 15px; font-family: 'Inter', sans-serif; background: white; }
.rk-name input:focus { border-color: var(--green-dark); outline: none; }
.rk-stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(96px, 1fr)); gap: 8px; margin-bottom: 14px; }
.rk-stat { background: white; border: 1.5px solid var(--gold-light); border-radius: 8px; padding: 8px 6px; text-align: center; }
.rk-stat b { display: block; font-family: 'Switzer', 'Space Grotesk', sans-serif; font-size: 20px; color: var(--gold); line-height: 1.2; }
.rk-stat span { font-family: 'Inter', sans-serif; font-size: 10.5px; text-transform: uppercase; letter-spacing: 0.5px; color: var(--text-medium); }
.rk-actions { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
.rk-status { font-family: 'Inter', sans-serif; font-size: 13px; color: var(--green-light); font-weight: 600; min-height: 20px; margin-top: 10px; }
.rk-fine { font-size: 12.5px; color: var(--text-medium); margin-top: 10px; font-family: 'Inter', sans-serif; }
.rk-fine a { color: var(--copper); font-weight: 600; cursor: pointer; }
/* rk:end */'''

TAB_BUTTON = '''<!-- rk:begin -->
            <button class="rk-btn" onclick="rkOpen()" title="Download your results as a file you can text or email to your tutor"><span>&#8681;</span> Results for your tutor</button><!-- rk:end -->'''

BANNER = '''<!-- rk:begin --><div id="rkBanner"></div>

    <!-- rk:end -->'''

EXIT_CARD = '''<!-- rk:begin --><div class="card" style="border-left-color: var(--green-light);">
            <h3 style="font-family:'Switzer','Space Grotesk',sans-serif; color:var(--brown-dark); margin-bottom:6px;">Send your results to your tutor</h3>
            <p style="font-size:14px; color:var(--text-medium); margin-bottom:10px;">Nothing on this sheet is sent anywhere by itself, and nothing is lost either: your answers stay saved in this browser. To share them, download the results file (every tab, every answer, in one page) and text or email it, or copy a short summary into a message.</p>
            <div class="toolbar" style="margin-bottom:0;"><button class="btn btn-gold" onclick="rkOpen()">&#8681; Download results for your tutor</button></div>
        </div>
        <!-- rk:end -->'''

OVERLAY = '''<!-- rk:begin --><!-- Results kit: tutor report panel -->
<div class="rk-overlay" id="rkOverlay" onclick="if (event.target === this) rkClose();" role="dialog" aria-modal="true" aria-labelledby="rkTitle">
    <div class="rk-modal">
        <h3 id="rkTitle">Results for your tutor</h3>
        <p>Nothing is sent automatically. <strong>Download results</strong> makes one file with every answer on this sheet (the practice set, challenge questions, drills, quick checks, exit ticket, and your takeaway): text or email that file to your tutor. <strong>Copy summary</strong> gives a short version to paste into a message.</p>
        <label class="rk-name">Your name <input type="text" id="rkName" placeholder="so your tutor knows whose results these are" autocomplete="name" oninput="rkSyncName()"></label>
        <div class="rk-stats" id="rkStats"></div>
        <div class="rk-actions">
            <button class="btn btn-gold" onclick="rkDownload()">&#8681; Download results</button>
            <button class="btn btn-ghost" onclick="rkCopy()">Copy summary</button>
            <button class="btn btn-ghost" onclick="rkEmail()">Email summary</button>
            <span style="flex:1"></span>
            <button class="btn btn-ghost" onclick="rkClose()">Close</button>
        </div>
        <div class="rk-status" id="rkStatus"></div>
        <div class="rk-fine">Your answers are saved in this browser automatically, so you can close the tab and come back. <a onclick="rkReset()">Start fresh</a> clears them.</div>
    </div>
</div>

<!-- rk:end -->'''

JS = r'''/* rk:begin */
/* ================= LCC results kit v1: autosave + results report ================= */
/* LCC results kit v1 */
var RK_RULE_KEY = 'sat-linear-sheet:rule';            /* builders retarget this string per sheet */
var RK_KEY = RK_RULE_KEY.replace(/:rule$/, ':progress');
var RK_TUTOR_EMAIL = '';                              /* optional: pre-addresses the email button */
var rk = { fl: {}, mc: {}, mic: {}, name: '', restoredAt: null, t: null, loading: false };
function rkStore(k, v) { try { if (v == null) localStorage.removeItem(k); else localStorage.setItem(k, v); } catch (e) {} }
function rkRead(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
function rkSnapshot() {
    return { v: 1, t: Date.now(), name: rk.name,
        g: { idx: gState.idx, answers: gState.answers, finished: gState.finished }, tG: timers.G.sec, tF: timers.F.sec,
        ch: chState, cx: cxState, cho: chExtraOpen, st: { idx: stepState.idx, done: stepState.done },
        fl: rk.fl, mc: rk.mc, mic: rk.mic };
}
function rkSaveNow() { if (rk.loading) return; rkStore(RK_KEY, JSON.stringify(rkSnapshot())); }
function rkSave() { if (rk.t) clearTimeout(rk.t); rk.t = setTimeout(rkSaveNow, 350); }
function rkLoad() {
    var raw = rkRead(RK_KEY); if (!raw) return;
    try {
        var s = JSON.parse(raw); if (!s || s.v !== 1) return;
        rk.loading = true;
        if (s.g) { gState.idx = s.g.idx || 0; gState.answers = s.g.answers || {}; gState.finished = !!s.g.finished; }
        if (s.tG) timers.G.sec = s.tG;
        if (s.tF) timers.F.sec = s.tF;
        if (s.ch) chState = s.ch;
        if (s.cx) cxState = s.cx;
        if (s.cho) chExtraOpen = s.cho;
        if (s.st) { stepState.idx = Math.min(s.st.idx || 0, STEPS.length - 1); stepState.done = s.st.done || {}; }
        rk.fl = s.fl || {}; rk.mc = s.mc || {}; rk.mic = s.mic || {}; rk.name = s.name || '';
        rk.restoredAt = s.t || null;
    } catch (e) {}
    rk.loading = false;
}
/* record every check the shell makes, then replay it after each render */
var _rkCheckExp = checkExp, _rkCheckMC = checkMC, _rkMicroExp = microExp, _rkMicroMC = microMC,
    _rkRenderStep = renderStep, _rkRenderFluency = renderFluency, _rkRenderExit = renderExit, _rkRenderGauntletResults = renderGauntletResults;
checkExp = function(id, si, ii) { _rkCheckExp(id, si, ii); var v = document.getElementById('in-' + id).value; rk.fl[id] = { v: v, ok: answerMatches(v, FLUENCY[si].items[ii].accept), si: si, ii: ii }; rkSave(); };
checkMC = function(id, chosen, correct) { _rkCheckMC(id, chosen, correct); rk.mc[id] = { c: chosen, ok: chosen === correct, k: correct }; rkSave(); };
microExp = function(i) { _rkMicroExp(i); var v = document.getElementById('in-micro' + i).value; rk.mic[i] = { v: v, ok: answerMatches(v, STEPS[i].micro.accept) }; rkSave(); };
microMC = function(i, chosen) { _rkMicroMC(i, chosen); rk.mic[i] = { c: chosen, ok: chosen === STEPS[i].micro.correct }; rkSave(); };
renderStep = function() { _rkRenderStep(); rkReplayMicro(); };
renderFluency = function() { _rkRenderFluency(); rkReplayFluency(); };
renderExit = function() { _rkRenderExit(); rkReplayExit(); };
renderGauntletResults = function(host) { _rkRenderGauntletResults(host); host.insertAdjacentHTML('beforeend', rkCardHtml()); };
function rkReplayMicro() {
    var i = stepState.idx, m = rk.mic[i]; if (!m) return;
    if (m.c != null) { if (document.getElementById('opts-micro' + i)) _rkMicroMC(i, m.c); }
    else { var inp = document.getElementById('in-micro' + i); if (inp) { inp.value = m.v; _rkMicroExp(i); } }
}
function rkReplayFluency() {
    Object.keys(rk.fl).forEach(function(id) { var r = rk.fl[id], inp = document.getElementById('in-' + id); if (inp && FLUENCY[r.si] && FLUENCY[r.si].items[r.ii]) { inp.value = r.v; _rkCheckExp(id, r.si, r.ii); } });
    Object.keys(rk.mc).forEach(function(id) { if (id.charAt(0) === 'f' && document.getElementById('opts-' + id)) _rkCheckMC(id, rk.mc[id].c, rk.mc[id].k); });
}
function rkReplayExit() { Object.keys(rk.mc).forEach(function(id) { if (id.charAt(0) === 'x' && document.getElementById('opts-' + id)) _rkCheckMC(id, rk.mc[id].c, rk.mc[id].k); }); }
function rkCardHtml() {
    return '<div class="card" style="border-left-color: var(--green-light); margin-top: 18px;">' +
        '<h3 style="font-family:\'Switzer\',\'Space Grotesk\',sans-serif; color:var(--brown-dark); margin-bottom:6px;">Send these results to your tutor</h3>' +
        '<p style="font-size:14px; color:var(--text-medium); margin-bottom:10px;">Nothing on this page is sent anywhere by itself, and nothing is lost either: your answers stay saved in this browser. To share them, download the results file (every tab, every answer) and text or email it, or copy a short summary into a message.</p>' +
        '<div class="toolbar" style="margin-bottom:0;"><button class="btn btn-gold" onclick="rkOpen()">&#8681; Download results for your tutor</button></div></div>';
}
function rkFmtDate(ts) { try { return new Date(ts).toLocaleString([], { dateStyle: 'medium', timeStyle: 'short' }); } catch (e) { return new Date(ts).toLocaleString(); } }
function rkBanner() {
    var el = document.getElementById('rkBanner'); if (!el || !rk.restoredAt) return;
    el.innerHTML = '<div class="rk-banner"><span>&#128190; Welcome back: your answers from <strong>' + rkFmtDate(rk.restoredAt) + '</strong> are saved on this device and have been restored.</span>' +
        '<button class="btn btn-ghost btn-sm" onclick="rkOpen()">Results for your tutor</button><button class="btn btn-ghost btn-sm" onclick="rkReset()">Start fresh</button></div>';
}
function rkReset() {
    if (!confirm('Clear every answer saved on this sheet and start fresh?')) return;
    rk.loading = true; rkStore(RK_KEY, null); location.reload();
}
/* ---- gathering the data ---- */
function rkText(html) { var d = document.createElement('div'); d.innerHTML = html; return (d.textContent || '').replace(/\s+/g, ' ').trim(); }
function rkData() {
    var d = { kit: 'lcc-results-kit', version: 1, sheet: document.title, url: location.href.split('#')[0], name: rk.name, when: new Date().toISOString(), sections: {} };
    var g = { finished: gState.finished, answered: 0, correct: 0, total: GAUNTLET.length, time: timers.G.sec, items: [] };
    GAUNTLET.forEach(function(p, i) {
        var has = gHasAns(i), ok = has && gGrade(i); if (has) g.answered++; if (ok) g.correct++;
        g.items.push({ n: i + 1, diff: p.diff || '', starred: !!p.ess, type: p.type, answered: has, ok: !!ok, yours: has ? gAnswerText(i) : '', correct: gCorrectText(i), stem: p.stem, trap: p.trap });
    });
    d.sections.practice = g;
    var c = { checked: 0, correct: 0, total: CHALLENGE.length, items: [], extras: [] };
    CHALLENGE.forEach(function(p, i) {
        var st = chState[i] || {}; if (st.checked) c.checked++; if (st.checked && st.ok) c.correct++;
        c.items.push({ n: i + 1, diff: p.diff || '', starred: !!p.ess, checked: !!st.checked, ok: !!(st.checked && st.ok),
            yours: st.checked ? (p.type === 'mc' ? LETTERS[st.pick] + '. ' + p.options[st.pick] : String(st.pick)) : '',
            correct: p.type === 'mc' ? LETTERS[p.correct] + '. ' + p.options[p.correct] : p.accept[0], stem: p.stem, trap: p.trap });
        (p.extras || []).forEach(function(x, j) { var xs = cxState[i + '_' + j]; if (xs && xs.checked) c.extras.push({ n: (i + 1) + String.fromCharCode(97 + j), ok: !!xs.ok, yours: String(xs.pick), correct: x.accept[0], q: x.q }); });
    });
    d.sections.challenge = c;
    var f = { attempted: 0, correct: 0, total: 0, items: [] }, n = 0;
    FLUENCY.forEach(function(sec, si) { sec.items.forEach(function(it, ii) {
        n++; f.total++; var id = 'f' + si + '_' + ii, r = it.mc ? rk.mc[id] : rk.fl[id];
        if (r) { f.attempted++; if (r.ok) f.correct++; f.items.push({ n: n, sec: sec.sec, ok: !!r.ok, yours: it.mc ? LETTERS[r.c] + '. ' + it.opts[r.c] : r.v, correct: it.mc ? LETTERS[it.correct] + '. ' + it.opts[it.correct] : it.accept[0], q: it.q }); }
    }); });
    d.sections.fluency = f;
    var m = { attempted: 0, correct: 0, total: STEPS.length, items: [] };
    STEPS.forEach(function(s, i) { var r = rk.mic[i]; if (r) { m.attempted++; if (r.ok) m.correct++; m.items.push({ n: i + 1, name: s.name, ok: !!r.ok }); } });
    d.sections.quick = m;
    var x = { attempted: 0, correct: 0, total: EXIT.length, items: [] };
    EXIT.forEach(function(it, i) { var r = rk.mc['x' + i]; if (r) { x.attempted++; if (r.ok) x.correct++; x.items.push({ n: i + 1, ok: !!r.ok, yours: LETTERS[r.c] + '. ' + it.opts[r.c], correct: LETTERS[it.correct] + '. ' + it.opts[it.correct], q: it.q }); } });
    d.sections.exit = x;
    var rb = document.getElementById('ruleBox'); d.takeaway = rb ? rb.value.trim() : '';
    return d;
}
function rkSummary(d) {
    var s = d.sections, L = [];
    var missed = function(items, test) { var m = items.filter(test).map(function(i) { return i.n; }); return m.length ? '. Missed: ' + m.join(', ') : ''; };
    L.push(d.sheet + (d.name ? ': results for ' + d.name : ': results') + ' (' + rkFmtDate(Date.now()) + ')');
    L.push('Practice set: ' + (s.practice.finished ? s.practice.correct + '/' + s.practice.total + (s.practice.time ? ' in ' + fmtTime(s.practice.time) : '') + missed(s.practice.items, function(i) { return !i.ok; })
        : 'not scored yet (' + s.practice.answered + ' of ' + s.practice.total + ' answered)'));
    L.push('Challenge: ' + s.challenge.correct + '/' + s.challenge.checked + ' checked (' + s.challenge.total + ' total)' + missed(s.challenge.items, function(i) { return i.checked && !i.ok; }) +
        (s.challenge.extras.length ? '. Extra reps: ' + s.challenge.extras.filter(function(e) { return e.ok; }).length + '/' + s.challenge.extras.length : ''));
    L.push('Fluency drills: ' + s.fluency.correct + '/' + s.fluency.attempted + ' tried (' + s.fluency.total + ' total)' + missed(s.fluency.items, function(i) { return !i.ok; }));
    L.push('Quick checks: ' + s.quick.correct + '/' + s.quick.attempted + ' tried (' + s.quick.total + ' total)' + missed(s.quick.items, function(i) { return !i.ok; }));
    L.push('Exit ticket: ' + s.exit.correct + '/' + s.exit.attempted + ' tried (' + s.exit.total + ' total)' + missed(s.exit.items, function(i) { return !i.ok; }));
    if (d.takeaway) L.push('Takeaway: "' + d.takeaway + '"');
    L.push('Full report: ' + rkFileName(d));
    return L.join('\n');
}
function rkSlug(t) { return String(t || '').replace(/[^A-Za-z0-9]+/g, '-').replace(/^-+|-+$/g, ''); }
function rkFileName(d) {
    var day = new Date().toISOString().slice(0, 10);
    return rkSlug(d.sheet) + '-results' + (d.name ? '-' + rkSlug(d.name) : '') + '-' + day + '.html';
}
function rkReportHtml(d) {
    var s = d.sections;
    var esc = function(t) { return String(t == null ? '' : t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); };
    var mark = function(ok) { return ok ? '<span class="ok">&#10003;</span>' : '<span class="no">&#10007;</span>'; };
    var tile = function(num, label) { return '<div class="tile"><b>' + num + '</b><span>' + label + '</span></div>'; };
    var row = function(cells, cls) { return '<tr' + (cls ? ' class="' + cls + '"' : '') + '>' + cells.map(function(c) { return '<td>' + c + '</td>'; }).join('') + '</tr>'; };
    var table = function(head, rows) { return rows.length ? '<table><thead><tr>' + head.map(function(h) { return '<th>' + h + '</th>'; }).join('') + '</tr></thead><tbody>' + rows.join('') + '</tbody></table>' : '<p class="muted">Nothing attempted here yet.</p>'; };
    var h = '';
    h += '<div class="head"><div><div class="kicker">Learning Curve Collective &bull; results report</div><h1>' + esc(d.sheet) + '</h1></div>' +
        '<div class="meta"><div><b>Student:</b> ' + (d.name ? esc(d.name) : '<em>not given</em>') + '</div><div><b>Generated:</b> ' + rkFmtDate(Date.parse(d.when)) + '</div><div><b>Sheet:</b> <a href="' + esc(d.url) + '">' + esc(d.url) + '</a></div></div></div>';
    h += '<div class="tiles">' +
        tile(s.practice.finished ? s.practice.correct + '/' + s.practice.total : s.practice.answered + '/' + s.practice.total, s.practice.finished ? 'practice set' + (s.practice.time ? ' &bull; ' + fmtTime(s.practice.time) : '') : 'practice answered, not scored') +
        tile(s.challenge.correct + '/' + s.challenge.checked, 'challenge (of ' + s.challenge.total + ')') +
        tile(s.fluency.correct + '/' + s.fluency.attempted, 'fluency (of ' + s.fluency.total + ')') +
        tile(s.quick.correct + '/' + s.quick.attempted, 'quick checks (of ' + s.quick.total + ')') +
        tile(s.exit.correct + '/' + s.exit.attempted, 'exit ticket (of ' + s.exit.total + ')') + '</div>';
    if (d.takeaway) h += '<div class="take"><b>Key takeaway (in the student\'s words):</b> ' + esc(d.takeaway) + '</div>';
    var review = s.practice.items.filter(function(i) { return (i.answered || s.practice.finished) && !i.ok; }).map(function(i) { return { tag: 'Practice Q' + i.n, i: i }; })
        .concat(s.challenge.items.filter(function(i) { return i.checked && !i.ok; }).map(function(i) { return { tag: 'Challenge ' + i.n, i: i }; }));
    if (review.length) {
        h += '<h2>Review list: the misses and the trap behind each</h2>';
        review.forEach(function(r) { h += '<div class="rev"><div class="rev-h">' + mark(false) + ' <b>' + r.tag + '</b> <span class="chip">' + esc(r.i.diff) + '</span>' + (r.i.starred ? '<span class="chip star">&#9733; starred rule</span>' : '') + '<span class="ans">answered <b>' + (r.i.yours ? esc(r.i.yours) : '<em>nothing</em>') + '</b>, correct <b>' + r.i.correct + '</b></span></div><div class="stem">' + r.i.stem + '</div><div class="trap"><b>The trap:</b> ' + r.i.trap + '</div></div>'; });
    }
    h += '<h2>Practice set' + (s.practice.finished ? '' : ' (not scored yet)') + '</h2>' + table(['#', 'Difficulty', 'Your answer', 'Correct', ''],
        s.practice.items.map(function(i) { var counts = i.answered || s.practice.finished; return row(['Q' + i.n + (i.starred ? ' &#9733;' : ''), esc(i.diff), i.answered ? esc(i.yours) : '<em>no answer</em>', i.correct, counts ? mark(i.ok) : ''], counts && !i.ok ? 'miss' : ''); }));
    h += '<h2>Challenge questions</h2>' + table(['#', 'Difficulty', 'Your answer', 'Correct', ''],
        s.challenge.items.filter(function(i) { return i.checked; }).map(function(i) { return row(['C' + i.n + (i.starred ? ' &#9733;' : ''), esc(i.diff), esc(i.yours), i.correct, mark(i.ok)], i.ok ? '' : 'miss'); }));
    if (s.challenge.extras.length) h += '<h3>Extra reps</h3>' + table(['#', 'Question', 'Your answer', 'Correct', ''], s.challenge.extras.map(function(e) { return row([e.n, e.q, esc(e.yours), e.correct, mark(e.ok)], e.ok ? '' : 'miss'); }));
    h += '<h2>Fluency drills</h2>' + table(['#', 'Section', 'Question', 'Your answer', 'Correct', ''], s.fluency.items.map(function(i) { return row([i.n, esc(i.sec), i.q, esc(i.yours), i.correct, mark(i.ok)], i.ok ? '' : 'miss'); }));
    h += '<h2>Quick checks (worked examples)</h2>' + table(['Step', 'Rule', ''], s.quick.items.map(function(i) { return row([i.n, i.name, mark(i.ok)], i.ok ? '' : 'miss'); }));
    h += '<h2>Exit ticket</h2>' + table(['#', 'Question', 'Your answer', 'Correct', ''], s.exit.items.map(function(i) { return row([i.n, i.q, esc(i.yours), i.correct, mark(i.ok)], i.ok ? '' : 'miss'); }));
    h += '<p class="muted foot">Generated by the sheet itself in the student\'s browser; nothing was sent to a server. The raw data is embedded in this file for import.</p>';
    return '<!DOCTYPE html>\n<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">' +
        '<title>' + esc(d.sheet) + ': results' + (d.name ? ' for ' + esc(d.name) : '') + '</title>' +
        '<script>window.MathJax = { tex: { inlineMath: [["$","$"]], displayMath: [["$$","$$"]] }, svg: { fontCache: "global" } };<\/script>' +
        '<script async src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.2/es5/tex-svg.min.js"><\/script>' +
        '<style>body{margin:0;background:#FBF7EF;color:#2D2D2D;font-family:Inter,-apple-system,Segoe UI,Helvetica,Arial,sans-serif;font-size:15px;line-height:1.5}' +
        '.wrap{max-width:900px;margin:0 auto;padding:24px 20px 40px}.head{background:#21442B;color:white;border-radius:10px;padding:18px 22px;display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;border-bottom:4px solid #DDA25E}' +
        '.kicker{font-size:11px;letter-spacing:1px;text-transform:uppercase;color:#E6BC84}h1{margin:4px 0 0;font-size:24px}.meta{font-size:13px;color:#F5E4CC}.meta a{color:#E6BC84;word-break:break-all}' +
        '.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:10px;margin:18px 0}.tile{background:white;border:2px solid #E6BC84;border-radius:10px;padding:12px;text-align:center}.tile b{display:block;font-size:26px;color:#DDA25E}.tile span{font-size:11px;text-transform:uppercase;letter-spacing:.5px;color:#666}' +
        '.take{background:white;border-left:5px solid #DDA25E;padding:12px 16px;border-radius:8px;margin:12px 0}h2{font-size:18px;color:#21442B;margin:26px 0 8px;border-bottom:2px solid #E8E0D0;padding-bottom:4px}h3{font-size:15px;color:#21442B;margin:16px 0 6px}' +
        'table{width:100%;border-collapse:collapse;background:white;border-radius:8px;overflow:hidden;font-size:14px}th{background:#F5E4CC;color:#8B6914;font-size:11px;text-transform:uppercase;letter-spacing:.6px;text-align:left;padding:8px 10px}td{padding:8px 10px;border-top:1px solid #F1E6D2;vertical-align:top}tr.miss td{background:#FFF4F2}' +
        '.ok{color:#39864E;font-weight:700}.no{color:#C0392B;font-weight:700}.muted{color:#777;font-size:13px}.foot{margin-top:28px}' +
        '.rev{background:white;border-radius:8px;padding:12px 14px;margin:8px 0;border-left:5px solid #C0392B}.rev-h{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:6px}.chip{font-size:10.5px;text-transform:uppercase;letter-spacing:.5px;border-radius:99px;padding:2px 8px;background:#F5E4CC;color:#8B6914;font-weight:700}.chip.star{background:#DDA25E;color:#42260D}.ans{font-size:13px;color:#555}' +
        '.stem{font-family:"Times New Roman",Georgia,serif;font-size:16px;margin:6px 0}.trap{font-size:14px;color:#5A3E1B;background:#FFFCF6;border:1px solid #F1E6D2;border-radius:6px;padding:8px 10px}' +
        '.nw{white-space:nowrap}table.vtab{width:auto;display:inline-table;margin:6px 0;font-size:14px}table.vtab th,table.vtab td{border:1px solid #D8CDB5;padding:4px 10px;text-align:center}table.vtab th{background:#F5E4CC}' +
        '@media print{body{background:white}.head{-webkit-print-color-adjust:exact}}</style></head><body><div class="wrap">' + h + '</div>' +
        '<script type="application/json" id="lcc-results">' + JSON.stringify(d).replace(/</g, '\\u003c') + '<\/script></body></html>';
}
/* ---- the panel ---- */
function rkStatus(t) { var el = document.getElementById('rkStatus'); if (el) el.textContent = t; }
function rkSyncName() { var inp = document.getElementById('rkName'); if (!inp) return; rk.name = inp.value.trim(); rkStore('lcc:student-name', rk.name || null); rkSave(); }
function rkOpen() {
    var ov = document.getElementById('rkOverlay'); if (!ov) return;
    var d = rkData(), s = d.sections;
    var tile = function(num, label) { return '<div class="rk-stat"><b>' + num + '</b><span>' + label + '</span></div>'; };
    document.getElementById('rkStats').innerHTML =
        tile(s.practice.finished ? s.practice.correct + '/' + s.practice.total : s.practice.answered + '/' + s.practice.total, s.practice.finished ? 'practice set' : 'practice answered') +
        tile(s.challenge.correct + '/' + s.challenge.checked, 'challenge') + tile(s.fluency.correct + '/' + s.fluency.attempted, 'fluency') +
        tile(s.quick.correct + '/' + s.quick.attempted, 'quick checks') + tile(s.exit.correct + '/' + s.exit.attempted, 'exit ticket');
    var inp = document.getElementById('rkName'); inp.value = rk.name || rkRead('lcc:student-name') || '';
    rkStatus('');
    ov.classList.add('open');
    if (!inp.value) inp.focus();
}
function rkClose() { var ov = document.getElementById('rkOverlay'); if (ov) ov.classList.remove('open'); }
function rkDownload() {
    rkSyncName();
    var d = rkData(), name = rkFileName(d);
    try {
        var blob = new Blob([rkReportHtml(d)], { type: 'text/html' });
        var a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = name; document.body.appendChild(a); a.click();
        setTimeout(function() { URL.revokeObjectURL(a.href); a.remove(); }, 1500);
        rkStatus('Downloaded ' + name + '. Now text or email that file to your tutor.');
    } catch (e) { rkStatus('The download could not start in this browser. Use Copy summary instead.'); }
}
function rkCopyFallback(t) { var ta = document.createElement('textarea'); ta.value = t; ta.style.position = 'fixed'; ta.style.opacity = 0; document.body.appendChild(ta); ta.select(); try { document.execCommand('copy'); } catch (e) {} ta.remove(); }
function rkCopy() {
    rkSyncName();
    var t = rkSummary(rkData()), done = function() { rkStatus('Summary copied. Paste it into a text or an email.'); };
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(t).then(done, function() { rkCopyFallback(t); done(); });
    else { rkCopyFallback(t); done(); }
}
function rkEmail() {
    rkSyncName();
    var d = rkData();
    var body = rkSummary(d) + '\n\n(The full report is the downloaded file ' + rkFileName(d) + '; attach it to this email.)';
    location.href = 'mailto:' + encodeURIComponent(RK_TUTOR_EMAIL) + '?subject=' + encodeURIComponent(d.sheet + ': results' + (d.name ? ' for ' + d.name : '')) + '&body=' + encodeURIComponent(body);
    rkStatus('Your email app should open with the summary filled in. Attach the downloaded report if you have it.');
}
document.addEventListener('keydown', function(e) { if (e.key === 'Escape') rkClose(); if (e.key === 'Enter') rkSave(); }, true);
document.addEventListener('click', function(e) { var t = e.target; if (t && t.closest && t.closest('button, .choice, .mc-opt, .qchip, .step-dot, .tog')) rkSave(); }, true);
document.addEventListener('input', function(e) { var t = e.target; if (t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA')) rkSave(); }, true);
window.addEventListener('beforeunload', rkSaveNow);
setInterval(function() { if (timers.G.on || timers.F.on) rkSave(); }, 15000);
rkLoad();
if (timers.F.sec && document.getElementById('timerF')) document.getElementById('timerF').textContent = fmtTime(timers.F.sec);
setTimeout(rkBanner, 0);
/* rk:end */
'''


def _once(src, old, new):
    if src.count(old) != 1:
        sys.exit('results_kit: expected exactly one occurrence (%d): %r' % (src.count(old), old[:90]))
    return src.replace(old, new)


def strip(html):
    """Remove every block a previous run injected (between rk:begin / rk:end markers)."""
    import re
    html = re.sub(r'<!-- rk:begin -->.*?<!-- rk:end -->', '', html, flags=re.S)
    html = re.sub(r'/\* rk:begin \*/.*?/\* rk:end \*/\n?', '', html, flags=re.S)
    return html


def inject(html, refresh=True):
    """Patch a topic sheet with the results kit. A sheet that already has it is refreshed
    (old blocks stripped, current version injected), so re-running is safe."""
    if MARK in html:
        if not refresh:
            return html
        html = strip(html)
    html = _once(html, '</style>', CSS + '</style>')
    html = _once(html, "6. Exit Ticket</button>\n        </div>", "6. Exit Ticket</button>" + TAB_BUTTON + "\n        </div>")
    html = _once(html, '    <!-- ============ TAB 1: RULES ============ -->', '    ' + BANNER + '<!-- ============ TAB 1: RULES ============ -->')
    html = _once(html, '        <div class="card" style="border-left-color:#8B5E3C;">', '        ' + EXIT_CARD + '<div class="card" style="border-left-color:#8B5E3C;">')
    html = _once(html, '<!-- Desmos floating calculator -->', OVERLAY + '<!-- Desmos floating calculator -->')
    html = _once(html, 'fillFigSlots();\nrenderStep();', JS + 'fillFigSlots();\nrenderStep();')
    return html


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for path in sys.argv[1:]:
        src = open(path, encoding='utf-8').read()
        out = inject(src)
        if out == src:
            print('up to date:', path)
        else:
            open(path, 'w', encoding='utf-8').write(out)
            print(('refreshed:' if MARK in src else 'patched:'), path, len(src), '->', len(out), 'bytes')
