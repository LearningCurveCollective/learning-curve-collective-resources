/* Open Learning by Learning Curve Collective: shared script for the hub pages.
   Everything renders from catalog.js. index.html is the home page (data-page="home");
   each subject page carries data-page="area" and data-area="<area key>". */
(function () {
    var C = window.OPEN_LEARNING_CATALOG;
    if (!C) return;
    var BASE = C.site.base;
    var R = C.resources.slice().sort(function (a, b) { return a.subject === b.subject ? a.order - b.order : 0; });
    var BYID = {}; R.forEach(function (r) { BYID[r.id] = r; });
    var SUBJ = {}; C.subjects.forEach(function (s) { SUBJ[s.key] = s; });
    var AREA = {}; C.areas.forEach(function (a) { AREA[a.key] = a; });
    var EXAMS = ['SAT', 'PSAT', 'ACT', 'GRE'];
    var CONTENT = {}; C.content_types.forEach(function (c) { CONTENT[c.key] = c; });
    var LEADS = {}; R.forEach(function (r) { (r.builds_on || []).forEach(function (d) { (LEADS[d] = LEADS[d] || []).push(r.id); }); });
    var PAGE = document.body.getAttribute('data-page') || 'home';
    var HOME = PAGE === 'home' ? '' : 'index.html';

    function enc(p) { return BASE + p.split('/').map(encodeURIComponent).join('/'); }
    function el(tag, attrs, children) {
        var e = document.createElement(tag);
        if (attrs) Object.keys(attrs).forEach(function (k) {
            if (attrs[k] === null || attrs[k] === undefined) return;
            if (k === 'text') e.textContent = attrs[k];
            else if (k === 'html') e.innerHTML = attrs[k];
            else e.setAttribute(k, attrs[k]);
        });
        (children || []).forEach(function (c) { if (c) e.appendChild(c); });
        return e;
    }
    function count(fn) { return R.filter(fn).length; }
    function slug(s) { return s.toLowerCase().replace(/&/g, 'and').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, ''); }
    function subjectsIn(areaKey) { return C.subjects.filter(function (s) { return s.area === areaKey; }); }
    function subjectHref(s) {
        var a = AREA[s.area];
        return subjectsIn(s.area).length > 1 ? a.page + '#' + s.key : a.page;
    }
    function listNames(names) {
        if (names.length <= 1) return names.join('');
        return names.slice(0, -1).join(', ') + ' and ' + names[names.length - 1];
    }

    /* ---------- the learning curve (logistic), shared by the hero and the level glyphs ---------- */
    function logistic(t, k) { k = k || 7; var f = function (x) { return 1 / (1 + Math.exp(-k * (x - 0.5))); }; return (f(t) - f(0)) / (f(1) - f(0)); }
    function curvePath(x0, y0, w, h, n) {
        var d = '';
        for (var i = 0; i <= n; i++) { var t = i / n; var x = x0 + t * w, y = y0 - logistic(t) * h; d += (i ? ' L' : 'M') + x.toFixed(1) + ' ' + y.toFixed(1); }
        return d;
    }
    function drawHeroCurve() {
        var svg = document.getElementById('curve'); if (!svg) return;
        var NS = 'http://www.w3.org/2000/svg';
        var x0 = 44, y0 = 252, w = 380, h = 206, n = 120;
        var defs = document.createElementNS(NS, 'defs');
        defs.innerHTML = '<linearGradient id="curveFill" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#DDA25E" stop-opacity=".22"/><stop offset="1" stop-color="#DDA25E" stop-opacity="0"/></linearGradient>';
        svg.appendChild(defs);
        var g = document.createElementNS(NS, 'g'); g.setAttribute('class', 'grid');
        for (var i = 0; i <= 4; i++) { var l = document.createElementNS(NS, 'line'); var y = y0 - i * (h / 4); l.setAttribute('x1', x0 - 4); l.setAttribute('x2', x0 + w + 16); l.setAttribute('y1', y); l.setAttribute('y2', y); g.appendChild(l); }
        svg.appendChild(g);
        var fill = document.createElementNS(NS, 'path'); fill.setAttribute('class', 'fill');
        fill.setAttribute('d', curvePath(x0, y0, w, h, n) + ' L' + (x0 + w) + ' ' + y0 + ' Z'); svg.appendChild(fill);
        var path = document.createElementNS(NS, 'path'); path.setAttribute('class', 'path'); path.setAttribute('pathLength', '1');
        path.setAttribute('d', curvePath(x0, y0, w, h, n)); svg.appendChild(path);
        var labels = C.levels;
        labels.forEach(function (name, i) {
            var t = i / (labels.length - 1), x = x0 + t * w, y = y0 - logistic(t) * h;
            var dot = document.createElementNS(NS, 'circle'); dot.setAttribute('class', 'dot'); dot.setAttribute('cx', x); dot.setAttribute('cy', y); dot.setAttribute('r', 5);
            dot.style.animationDelay = (0.3 + 1.6 * t) + 's'; svg.appendChild(dot);
            var tx = document.createElementNS(NS, 'text');
            // labels: the first two sit below the flat start, the last sits above the top, the rest hang to the left of their dot
            if (i === 0) { tx.setAttribute('x', x); tx.setAttribute('y', y + 22); tx.setAttribute('text-anchor', 'start'); }
            else if (i === 1) { tx.setAttribute('x', x + 10); tx.setAttribute('y', y + 18); tx.setAttribute('text-anchor', 'start'); }
            else if (i === labels.length - 1) { tx.setAttribute('x', x); tx.setAttribute('y', y - 14); tx.setAttribute('text-anchor', 'end'); }
            else { tx.setAttribute('x', x - 12); tx.setAttribute('y', y + 4); tx.setAttribute('text-anchor', 'end'); }
            tx.textContent = name; svg.appendChild(tx);
        });
    }
    function levelGlyph(i) {  // small curve with a dot at this level's position, 26 x 12
        var n = C.levels.length - 1, t = i / n, x0 = 2, y0 = 10.5, w = 22, h = 9;
        var x = x0 + t * w, y = y0 - logistic(t) * h;
        return '<svg viewBox="0 0 26 12" aria-hidden="true"><path d="' + curvePath(x0, y0, w, h, 24) + '" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" opacity=".55"/><circle class="d" cx="' + x.toFixed(1) + '" cy="' + y.toFixed(1) + '" r="2.6" fill="currentColor"/></svg>';
    }
    var ICON = {
        theory: '<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 5h7a3 3 0 0 1 3 3v12a2 2 0 0 0-2-2H2z"/><path d="M22 5h-7a3 3 0 0 0-3 3v12a2 2 0 0 1 2-2h8z"/></svg>',
        practice: '<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 20l4-1 11-11-3-3L5 16z"/><path d="M13 7l3 3"/></svg>',
        reference: '<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 10h18M9 10v10"/></svg>'
    };
    ICON['theory+practice'] = ICON.theory + ICON.practice;
    var AREA_ICON = {
        'math': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="5.5" r="1.8" fill="currentColor" stroke="none"/><path d="M4 12h16"/><circle cx="12" cy="18.5" r="1.8" fill="currentColor" stroke="none"/></svg>',
        'test-prep': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 20l4-1 11-11-3-3L5 16z"/><path d="M13 7l3 3"/></svg>',
        'econ': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 20h16"/><rect x="5" y="12" width="3.5" height="8" rx=".5"/><rect x="10.25" y="8" width="3.5" height="12" rx=".5"/><rect x="15.5" y="4" width="3.5" height="16" rx=".5"/></svg>',
        'science': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 3h6"/><path d="M10 3v6l-5.2 9.1A1.8 1.8 0 0 0 6.4 21h11.2a1.8 1.8 0 0 0 1.6-2.9L14 9V3"/><path d="M7.5 15h9"/></svg>',
        'ml': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="6" cy="6" r="2.5"/><circle cx="18" cy="6" r="2.5"/><circle cx="12" cy="18" r="2.5"/><path d="M7.5 8l3 8M16.5 8l-3 8M8.5 6h7"/></svg>',
        'social': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="9" cy="8" r="3.2"/><path d="M3 20a6 6 0 0 1 12 0"/><circle cx="17" cy="9" r="2.5"/><path d="M15.5 14.2A5 5 0 0 1 22 19"/></svg>'
    };
    var DEFAULT_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="8"/></svg>';

    /* ---------- explore pills: one per area, drawn into every [data-pills] on the page ---------- */
    function renderPills() {
        document.querySelectorAll('[data-pills]').forEach(function (box) {
            var current = box.getAttribute('data-current') || '';
            box.innerHTML = '';
            C.areas.forEach(function (a) {
                var n = count(function (r) { return SUBJ[r.subject].area === a.key; });
                if (!n) return;
                var li = el('li');
                li.appendChild(el('a', { 'class': 'pill-link' + (a.key === current ? ' current' : ''), href: a.page, 'aria-current': a.key === current ? 'page' : null }, [
                    el('span', { 'class': 'p-ic', html: AREA_ICON[a.key] || DEFAULT_ICON }),
                    el('span', null, [el('span', { 'class': 'p-name', text: a.name }), el('span', { 'class': 'p-count', text: n + (n === 1 ? ' resource' : ' resources') })])
                ]));
                box.appendChild(li);
            });
        });
        document.querySelectorAll('[data-quick]').forEach(function (q) {
            q.innerHTML = '';
            q.appendChild(el('span', { text: 'Or jump straight to a subject:' }));
            C.subjects.forEach(function (s) {
                var n = count(function (r) { return r.subject === s.key; });
                if (!n) return;
                q.appendChild(el('a', { href: subjectHref(s), text: s.name }));
            });
        });
    }
    /* ---------- cards (featured and search results) ---------- */
    function relLink(id) {
        var t = BYID[id]; if (!t) return null;
        var a = el('a', { href: HOME + '#r=' + id, text: t.title });
        if (PAGE === 'home') a.addEventListener('click', function (e) { e.preventDefault(); jumpTo(id); });
        return a;
    }
    function relRow(label, ids) {
        var row = el('div', null, [el('span', { text: label })]);
        ids.forEach(function (id, i) { if (i) row.appendChild(el('i', { 'class': 'sep', text: '|' })); row.appendChild(relLink(id)); });
        return row;
    }
    function card(r, extra) {
        var meta = el('div', { 'class': 'meta' });
        r.levels.forEach(function (l) { meta.appendChild(el('span', { 'class': 'pill pill-level', html: levelGlyph(C.levels.indexOf(l)) + '<span>' + l + '</span>' })); });
        if (r.content && CONTENT[r.content]) meta.appendChild(el('span', { 'class': 'pill pill-content', html: ICON[r.content] + '<span>' + CONTENT[r.content].label + '</span>' }));
        meta.appendChild(el('span', { 'class': 'pill pill-format', text: r.format }));
        if (extra && extra.topic) meta.appendChild(el('span', { 'class': 'pill-topic', text: r.topic }));
        var h = el('h4', null, [el('a', { href: enc(r.path), text: r.title })]);
        var kids = [];
        if (extra && extra.subject) kids.push(el('span', { 'class': 'subj' }, [el('a', { href: subjectHref(SUBJ[r.subject]), text: SUBJ[r.subject].name })]));
        kids.push(h, el('p', { text: r.description }), meta);
        var bo = (r.builds_on || []).filter(function (id) { return BYID[id]; }), lt = (LEADS[r.id] || []);
        if (bo.length || lt.length) {
            var rel = el('div', { 'class': 'rel' });
            if (bo.length) rel.appendChild(relRow('Builds on', bo));
            if (lt.length) rel.appendChild(relRow('Leads to', lt));
            kids.push(rel);
        }
        var node = el('article', { 'class': 'card' + (extra && extra.featured ? ' featured-card' : ''), id: 'r-' + r.id, 'data-id': r.id }, kids);
        node.addEventListener('click', function (e) {
            if (e.target.closest('a') || e.defaultPrevented) return;
            if (e.metaKey || e.ctrlKey) window.open(enc(r.path), '_blank'); else location.href = enc(r.path);
        });
        return node;
    }
    function renderFeatured() {
        var g = document.getElementById('featured-grid'); if (!g) return;
        R.filter(function (r) { return r.featured; }).sort(function (a, b) { return a.featured - b.featured; })
         .forEach(function (r) { g.appendChild(card(r, { featured: true, subject: true })); });
    }

    /* =====================================================================
       HOME: search
       ===================================================================== */
    var state = { q: '', levels: [], exams: [], content: [] };
    var view = 'home';   // 'home' | 'search' | 'all'

    function readHash() {
        var h = location.hash.replace(/^#/, '');
        if (h === 'all') { state = { q: '', levels: [], exams: [], content: [] }; view = 'all'; return true; }
        var m = h.match(/^(search|browse)(\?(.*))?$/);
        if (!m) return false;
        var ps = new URLSearchParams(m[3] || '');
        // links from the previous site version: a subject filter is now a subject page
        if (m[1] === 'browse' && ps.get('subject')) {
            var key = ps.get('subject'), s = SUBJ[key], a = AREA[key] || (s && AREA[s.area]);
            if (a) { location.replace(s ? subjectHref(s) : a.page); return true; }
        }
        state.q = ps.get('q') || '';
        state.levels = ps.get('level') ? ps.get('level').split(',') : [];
        state.exams = ps.get('exam') ? ps.get('exam').split(',') : [];
        state.content = ps.get('inside') ? ps.get('inside').split(',') : [];
        view = (state.q.trim() || state.levels.length || state.exams.length || state.content.length) ? 'search' : 'all';
        return true;
    }
    function writeHash() {
        var target;
        if (view === 'home') target = location.pathname + location.search;
        else if (view === 'all' && !filtering()) target = '#all';
        else {
            var ps = new URLSearchParams();
            if (state.q.trim()) ps.set('q', state.q.trim());
            if (state.levels.length) ps.set('level', state.levels.join(','));
            if (state.exams.length) ps.set('exam', state.exams.join(','));
            if (state.content.length) ps.set('inside', state.content.join(','));
            var s = ps.toString();
            target = s ? '#search?' + s : '#all';
        }
        if (view === 'home') { if (location.hash) history.replaceState(null, '', target); }
        else if (location.hash !== target) history.replaceState(null, '', target);
    }
    function filtering() { return !!(state.q.trim() || state.levels.length || state.exams.length || state.content.length); }

    /* The page-content index (search-index.js) is fetched the first time someone searches,
       so the first paint never waits for it. Until it arrives, search works on the catalog
       text alone and re-runs by itself once the index lands. */
    var IDX = null, idxState = 'idle';
    function ensureIndex() {
        if (idxState !== 'idle') return;
        idxState = 'loading';
        var s = document.createElement('script');
        s.src = 'search-index.js';
        s.onload = function () { IDX = window.SEARCH_INDEX || {}; idxState = 'ready'; if (state.q) renderResults(); };
        s.onerror = function () { idxState = 'failed'; if (state.q) renderResults(); };   // keep searching the catalog text
        document.head.appendChild(s);
    }
    function queryTerms() { return state.q.trim().toLowerCase().split(/\s+/).filter(Boolean); }
    function wordHit(hay, term) {
        if (!hay) return false;
        var i = hay.indexOf(term);
        while (i !== -1) { if (i === 0 || hay.charAt(i - 1) === ' ') return true; i = hay.indexOf(term, i + 1); }
        return false;
    }
    /* 0 means "not a result". Higher is a better match: the title beats the catalog text,
       which beats a heading inside the page, which beats ordinary prose. */
    function score(r) {
        if (state.levels.length && !state.levels.some(function (l) { return r.levels.indexOf(l) !== -1; })) return 0;
        if (state.content.length && state.content.indexOf(r.content) === -1) return 0;
        if (state.exams.length && !(r.exams || []).some(function (x) { return state.exams.indexOf(x) !== -1; })) return 0;
        var terms = queryTerms();
        if (!terms.length) return 1;
        var title = r.title.toLowerCase();
        var meta = (r.description + ' ' + r.topic + ' ' + r.tags.join(' ') + ' ' + SUBJ[r.subject].name + ' '
                    + r.levels.join(' ') + ' ' + r.format + ' ' + (r.exams || []).join(' ')).toLowerCase();
        var doc = (IDX && IDX[r.id]) || null;
        var total = 0, deep = false;
        for (var i = 0; i < terms.length; i++) {
            var term = terms[i], s = 0;
            if (title.indexOf(term) !== -1) s += 100;
            if (meta.indexOf(term) !== -1) s += 40;
            if (doc) {
                if (wordHit(doc.k, term)) s += 20;
                else if (wordHit(doc.b, term)) { s += 6; deep = true; }
            }
            if (!s) return 0;                 // every word in the query has to land somewhere
            total += s;
        }
        return deep && total <= 6 * terms.length ? total : total + 1;   // nudge non-content matches ahead of ties
    }
    function matches(r) { return score(r) > 0; }

    function jumpTo(id) {
        var t = BYID[id]; if (!t) return;
        if (view === 'home' || !matches(t)) { state = { q: '', levels: [], exams: [], content: [] }; view = 'all'; }
        update();
        var node = document.getElementById('r-' + id);
        if (!node) return;
        node.scrollIntoView({ block: 'center' });
        node.classList.add('flash'); setTimeout(function () { node.classList.remove('flash'); }, 2200);
        var link = node.querySelector('h4 a'); if (link) link.focus({ preventScroll: true });
    }

    function toggle(arr, v) { var i = arr.indexOf(v); if (i === -1) arr.push(v); else arr.splice(i, 1); }
    function renderChips() {
        var lc = document.getElementById('level-chips'); if (!lc) return;
        C.levels.forEach(function (l, i) {
            var b = el('button', { type: 'button', 'class': 'chip', 'aria-pressed': 'false', 'data-level': l, html: levelGlyph(i) + '<span>' + l + '</span>' });
            b.addEventListener('click', function () { toggle(state.levels, l); update(); });
            lc.appendChild(b);
        });
        var cc = document.getElementById('content-chips');
        C.content_types.forEach(function (c) {
            var b = el('button', { type: 'button', 'class': 'chip', 'aria-pressed': 'false', 'data-content': c.key, title: c.blurb, html: ICON[c.key] + '<span>' + c.label + '</span>' });
            b.addEventListener('click', function () { toggle(state.content, c.key); update(); });
            cc.appendChild(b);
        });
        var ec = document.getElementById('exam-chips');
        EXAMS.forEach(function (x) {
            var b = el('button', { type: 'button', 'class': 'chip', 'aria-pressed': 'false', 'data-exam': x, text: x });
            b.addEventListener('click', function () { toggle(state.exams, x); update(); });
            ec.appendChild(b);
        });
        var key = document.getElementById('key');
        key.appendChild(el('b', { text: 'Tag key' }));
        key.appendChild(el('span', { 'class': 'k', html: levelGlyph(1) + 'the dot marks the academic level on the curve, from Foundations to Graduate' }));
        C.content_types.forEach(function (c) { key.appendChild(el('span', { 'class': 'k', html: ICON[c.key] + c.label + ': ' + c.blurb.toLowerCase() })); });
    }
    function syncChips() {
        var hqi = document.getElementById('hq');
        /* Never write back into the box being typed in: doing so used to eat spaces. */
        if (hqi && document.activeElement !== hqi) hqi.value = state.q;
        document.querySelectorAll('[data-level]').forEach(function (b) { b.setAttribute('aria-pressed', state.levels.indexOf(b.getAttribute('data-level')) !== -1 ? 'true' : 'false'); });
        document.querySelectorAll('[data-content]').forEach(function (b) { b.setAttribute('aria-pressed', state.content.indexOf(b.getAttribute('data-content')) !== -1 ? 'true' : 'false'); });
        document.querySelectorAll('[data-exam]').forEach(function (b) { b.setAttribute('aria-pressed', state.exams.indexOf(b.getAttribute('data-exam')) !== -1 ? 'true' : 'false'); });
    }

    function renderResults() {
        var sec = document.getElementById('results'); if (!sec) return;
        var showing = view !== 'home';
        sec.hidden = !showing;
        document.querySelectorAll('.home-only').forEach(function (n) { n.hidden = showing; });
        if (!showing) return;
        var root = document.getElementById('result-list'); root.innerHTML = '';
        var hits = R.filter(matches), total = hits.length;
        var examRelevant = hits.some(function (r) { return (r.exams || []).length; }) || state.exams.length;
        document.getElementById('exam-chips').hidden = !examRelevant;
        document.getElementById('result-title').textContent = state.q.trim() ? 'Results for “' + state.q.trim() + '”' : 'All resources';
        document.getElementById('result-count').textContent = filtering()
            ? 'Showing ' + total + ' of ' + R.length + ' resources'
            : R.length + ' resources across ' + C.subjects.filter(function (s) { return count(function (r) { return r.subject === s.key; }); }).length + ' subjects';
        renderBest(hits);
        if (!total) { root.appendChild(el('div', { 'class': 'empty', text: 'No resources match that search. Try a broader term, or clear the filters.' })); return; }
        C.areas.forEach(function (a) {
            var subs = subjectsIn(a.key);
            var areaHits = hits.filter(function (r) { return SUBJ[r.subject].area === a.key; });
            if (!areaHits.length) return;
            subs.forEach(function (s) {
                var sh = areaHits.filter(function (r) { return r.subject === s.key; });
                if (!sh.length) return;
                var label = subs.length > 1 ? a.name + ': ' + s.name : s.name;
                root.appendChild(el('div', { 'class': 'group-label' }, [el('a', { href: subjectHref(s), text: label }), el('span', { 'class': 'n', text: sh.length })]));
                var grid = el('div', { 'class': 'cards' });
                sh.forEach(function (r) { grid.appendChild(card(r, { topic: true })); });
                root.appendChild(grid);
            });
        });
    }
    /* With a search term, lead with the strongest matches so a concept turns up a page even
       when its title says nothing about that concept. */
    function renderBest(hits) {
        var box = document.getElementById('best'); box.innerHTML = '';
        if (!state.q.trim() || !hits.length) return;
        var ranked = hits.map(function (r) { return { r: r, s: score(r) }; })
                         .sort(function (a, b) { return b.s - a.s || a.r.title.localeCompare(b.r.title); });
        var note = idxState === 'ready'
            ? 'Searching titles, tags and the text inside every sheet.'
            : (idxState === 'failed' ? 'Searching titles and tags.' : 'Searching titles and tags; loading page text…');
        var kids = [el('div', { 'class': 'best-head' }, [
            el('span', { 'class': 'best-title', text: hits.length > 4 ? 'Best matches' : 'Matches' }),
            el('span', { 'class': 'best-note', text: note })
        ])];
        /* Four or fewer hits are all visible in the list below, so showing them again here
           would just be noise: the note alone explains why they turned up. */
        if (hits.length > 4) {
            var grid = el('div', { 'class': 'cards' });
            ranked.slice(0, 4).forEach(function (x) { grid.appendChild(card(x.r, { subject: true })); });
            kids.push(grid);
        }
        box.appendChild(el('div', { 'class': 'best', id: 'best-box' }, kids));
    }
    function update(hash) {
        if (view !== 'home' && !filtering()) view = 'all';
        if (state.q.trim()) ensureIndex();
        syncChips(); if (hash !== false) writeHash(); renderResults();
    }
    function initHome() {
        renderFeatured(); renderChips();
        var hf = document.getElementById('hero-search'), hq = document.getElementById('hq');
        hq.addEventListener('input', function (e) {
            state.q = e.target.value;
            if (state.q.trim()) view = 'search'; else if (view === 'search') view = 'home';
            update();
        });
        hf.addEventListener('submit', function (e) {
            e.preventDefault(); state.q = hq.value; view = state.q.trim() ? 'search' : 'all'; update();
            document.getElementById('results').scrollIntoView();
        });
        document.getElementById('clear-search').addEventListener('click', function () {
            state = { q: '', levels: [], exams: [], content: [] }; view = 'home'; update();
            window.scrollTo({ top: 0 });
        });
        function route() {
            var rm = location.hash.match(/^#r=(.+)$/);
            if (rm) { jumpTo(decodeURIComponent(rm[1])); return; }
            if (readHash()) { update(); document.getElementById('results').scrollIntoView(); }
            else { view = 'home'; update(false); }
        }
        route();
        window.addEventListener('hashchange', route);
    }

    /* =====================================================================
       SUBJECT PAGES: one card per course, every sheet listed in course order
       ===================================================================== */
    function sheetItem(r) {
        var tip = r.levels.join(' / ') + ' · ' + r.format + (r.description ? '\n' + r.description : '');
        var a = el('a', { href: enc(r.path), title: tip, html: r.levels.length ? levelGlyph(C.levels.indexOf(r.levels[0])) : '' });
        a.appendChild(el('span', { text: r.title }));
        if (r.topic === 'Recently added') a.appendChild(el('span', { 'class': 'new', text: 'New' }));
        return el('li', null, [a]);
    }
    function unit(label, rs) {
        var u = el('div', { 'class': 'unit' });
        if (label) u.appendChild(el('div', { 'class': 'unit-label', text: label }));
        var ul = el('ul', { 'class': 'sheets' });
        rs.forEach(function (r) { ul.appendChild(sheetItem(r)); });
        u.appendChild(ul);
        return u;
    }
    function topicsOf(rs) { var t = []; rs.forEach(function (r) { if (t.indexOf(r.topic) === -1) t.push(r.topic); }); return t; }
    function renderArea(key) {
        var a = AREA[key]; if (!a) return;
        var subs = subjectsIn(key);
        var rs = R.filter(function (r) { return SUBJ[r.subject].area === key; });
        var meta = document.getElementById('band-meta');
        var courses = [];   // { id, name, blurb, rs, grouped }
        if (subs.length > 1) {
            subs.forEach(function (s) {
                var sr = rs.filter(function (r) { return r.subject === s.key; });
                if (sr.length) courses.push({ id: s.key, name: s.name, blurb: s.blurb, rs: sr, grouped: true });
            });
        } else {
            topicsOf(rs).forEach(function (t) {
                courses.push({ id: slug(t), name: t, blurb: '', rs: rs.filter(function (r) { return r.topic === t; }), grouped: false });
            });
        }
        if (meta) meta.textContent = rs.length + ' free resources'
            + (subs.length > 1 ? ' across ' + listNames(courses.map(function (c) { return c.name; })) : (courses.length > 1 ? ' in ' + courses.length + ' groups' : ''));
        var nav = document.getElementById('subnav-links');
        if (nav) {
            nav.innerHTML = '';
            courses.forEach(function (c) { nav.appendChild(el('a', { href: '#' + c.id, html: c.name + '<span class="n">' + c.rs.length + '</span>' })); });
        }
        var root = document.getElementById('courses'); root.innerHTML = '';
        courses.forEach(function (c) {
            var sec = el('section', { 'class': 'course', id: c.id, 'aria-labelledby': 'h-' + c.id });
            sec.appendChild(el('div', { 'class': 'course-head' }, [el('h2', { id: 'h-' + c.id, text: c.name }), el('span', { 'class': 'n', text: c.rs.length + (c.rs.length === 1 ? ' resource' : ' resources') })]));
            if (c.blurb) sec.appendChild(el('p', { 'class': 'blurb', text: c.blurb }));
            if (c.grouped) topicsOf(c.rs).forEach(function (t) { sec.appendChild(unit(t, c.rs.filter(function (r) { return r.topic === t; }))); });
            else sec.appendChild(unit('', c.rs));
            root.appendChild(sec);
        });
        var key = document.getElementById('key');
        if (key && !key.childNodes.length) {
            key.appendChild(el('span', { 'class': 'k', html: levelGlyph(1) + 'the dot marks each sheet’s academic level on the curve, from Foundations to Graduate. Hover a title for details.' }));
        }
    }
    function initArea() {
        var key = document.body.getAttribute('data-area');
        renderArea(key);
        var f = document.getElementById('band-search');
        if (f) f.addEventListener('submit', function (e) {
            e.preventDefault();
            var q = document.getElementById('bq').value.trim();
            location.href = 'index.html#search?q=' + encodeURIComponent(q);
        });
        if (location.hash) { var t = document.getElementById(location.hash.slice(1)); if (t) setTimeout(function () { t.scrollIntoView(); }, 50); }
    }

    /* ---------- boot ---------- */
    drawHeroCurve(); renderPills();
    if (PAGE === 'home') initHome(); else initArea();

    /* ---------- safety net: list any published .html not yet in the catalog ---------- */
    (function () {
        var API = 'https://api.github.com/repos/LearningCurveCollective/learning-curve-collective-resources/git/trees/main?recursive=1';
        var known = {}; R.forEach(function (r) { known[r.path] = true; });
        var folderToSubject = { 'medical study sheets': 'medicine', 'test-prep': 'sat' };
        fetch(API).then(function (r) { return r.ok ? r.json() : null; }).then(function (data) {
            if (!data || !data.tree) return;
            var extra = [];
            data.tree.forEach(function (n) {
                var p = n.path;
                if (n.type !== 'blob' || !/\.html$/i.test(p) || p.indexOf('/') === -1 || known[p] || p.charAt(0) === '_') return;
                var folder = p.split('/')[0];
                var key = p.indexOf('test-prep/act/') === 0 ? 'act' : (folderToSubject[folder] || folder);
                if (!SUBJ[key]) return;
                var name = p.split('/').pop().replace(/\.html$/, '').replace(/[-_]+/g, ' ');
                extra.push({ id: 'new--' + p, path: p, title: name, description: 'Just published. A catalog entry is on its way.', subject: key, topic: 'Recently added', order: 999, levels: [], format: 'New', tags: [], builds_on: [] });
            });
            if (!extra.length) return;
            R = R.concat(extra); extra.forEach(function (x) { BYID[x.id] = x; });
            if (PAGE === 'home') { if (view !== 'home') renderResults(); }
            else { var key = document.body.getAttribute('data-area'); if (extra.some(function (x) { return SUBJ[x.subject].area === key; })) renderArea(key); }
        }).catch(function () {});
    })();
})();
