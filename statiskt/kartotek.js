/* Kartoteket: sortering, bläddring, sökning och kort på måfå. Sajten fungerar utan skriptet. */
(function () {
  'use strict';
  var html = document.documentElement;
  html.classList.add('js');
  var rot = html.getAttribute('data-rot') || '';
  var index = null;

  function hamtaIndex() {
    if (!index) {
      index = fetch(rot + 'sok.json').then(function (r) { return r.json(); });
    }
    return index;
  }

  /* ---------- kort på måfå */
  document.addEventListener('click', function (ev) {
    var a = ev.target.closest('[data-slump]');
    if (!a) return;
    ev.preventDefault();
    hamtaIndex().then(function (lista) {
      var k = lista[Math.floor(Math.random() * lista.length)];
      location.href = rot + k.u;
    }).catch(function () { location.href = a.href; });
  });

  /* ---------- lådor: visa en bit i taget */
  function visaBit(lista, antal) {
    var steg = parseInt(lista.getAttribute('data-visa'), 10) || 60;
    var rader = lista.children;
    var visas = Math.max(antal || steg, steg);
    for (var i = 0; i < rader.length; i++) rader[i].hidden = i >= visas;
    var bladdra = lista.parentNode.querySelector('.bladdra');
    if (!bladdra) return;
    var kvar = rader.length - Math.min(visas, rader.length);
    bladdra.hidden = kvar <= 0;
    bladdra.querySelector('span').textContent = kvar + ' kort till i lådan';
    lista.setAttribute('data-visas', Math.min(visas, rader.length));
  }

  document.querySelectorAll('.kortlista[data-visa]').forEach(function (lista) {
    visaBit(lista);
    var knapp = lista.parentNode.querySelector('.bladdra button');
    if (knapp) knapp.addEventListener('click', function () {
      var forsta = parseInt(lista.getAttribute('data-visas'), 10);
      visaBit(lista, forsta + (parseInt(lista.getAttribute('data-visa'), 10) || 60));
      var ny = lista.children[forsta];
      if (ny) ny.querySelector('a').focus();
    });
  });

  /* ---------- sortering */
  var jamfor = new Intl.Collator('sv').compare;
  document.querySelectorAll('.sortering').forEach(function (grupp) {
    var lista = grupp.parentNode.querySelector('.kortlista');
    grupp.addEventListener('click', function (ev) {
      var knapp = ev.target.closest('button[data-sort]');
      if (!knapp) return;
      var hur = knapp.getAttribute('data-sort');
      var rader = Array.prototype.slice.call(lista.children);
      rader.sort(function (a, b) {
        var ta = a.getAttribute('data-t'), tb = b.getAttribute('data-t');
        if (hur === 'y') return (a.getAttribute('data-y') - b.getAttribute('data-y')) || jamfor(ta, tb);
        if (hur === 'r') return (b.getAttribute('data-r') - a.getAttribute('data-r')) || jamfor(ta, tb);
        return jamfor(ta, tb);
      });
      rader.forEach(function (r) { lista.appendChild(r); });
      grupp.querySelectorAll('button').forEach(function (b) {
        b.setAttribute('aria-pressed', b === knapp ? 'true' : 'false');
      });
      visaBit(lista);
    });
  });

  /* ---------- sidokolumnen fälls ihop på smala skärmar */
  var smal = window.matchMedia('(max-width: 760px)');
  var sidokolumner = document.querySelectorAll('details.sidokolumn');
  var anpassa = function () {
    sidokolumner.forEach(function (d) { d.open = !smal.matches; });
  };
  anpassa();
  if (smal.addEventListener) smal.addEventListener('change', anpassa);

  /* ---------- sökning */
  var resultat = document.querySelector('.sok-resultat');
  if (resultat) {
    var falt = document.getElementById('sok');
    var status = document.querySelector('.sok-status');
    var ul = resultat.querySelector('.kortlista');
    var q = new URLSearchParams(location.search).get('q') || '';
    falt.value = q;

    var normal = function (s) {
      return (s || '').toLowerCase()
        .replace(/å/g, '\u0001').replace(/ä/g, '\u0002').replace(/ö/g, '\u0003')
        .normalize('NFD').replace(/[̀-ͯ]/g, '')
        .replace(/\u0001/g, 'å').replace(/\u0002/g, 'ä').replace(/\u0003/g, 'ö');
    };
    var el = function (tagg, klass, text) {
      var n = document.createElement(tagg);
      if (klass) n.className = klass;
      if (text !== undefined) n.textContent = text;
      return n;
    };
    var resultatrad = function (k) {
      var li = el('li');
      var a = el('a');
      a.setAttribute('href', rot + k.u);
      var titel = el('span', 'rad-titel');
      titel.appendChild(el('span', 't', k.t));
      if (k.s) titel.appendChild(el('span', 'u', k.s));
      var mark = el('span', 'rad-mark');
      var betyg = el('span', 'betyg' + (k.r === k.x ? ' hog' : ''), String(k.r));
      betyg.setAttribute('aria-label', 'Betyg ' + k.r + ' av ' + k.x);
      mark.appendChild(betyg);
      a.appendChild(titel);
      a.appendChild(el('span', 'rad-meta', [k.k, k.y, k.a].filter(Boolean).join(', ')));
      a.appendChild(mark);
      li.appendChild(a);
      return li;
    };

    var sok = function (fraga) {
      var ord = normal(fraga).split(/\s+/).filter(Boolean);
      if (!ord.length) { status.textContent = ''; resultat.hidden = true; return; }
      hamtaIndex().then(function (lista) {
        var traffar = lista.filter(function (k) {
          if (!k._h) k._h = normal([k.t, k.s, k.a, k.o, k.y, k.k].join(' '));
          return ord.every(function (o) { return k._h.indexOf(o) !== -1; });
        });
        traffar.sort(function (a, b) {
          var at = normal(a.t).indexOf(ord[0]) === 0 ? 0 : 1;
          var bt = normal(b.t).indexOf(ord[0]) === 0 ? 0 : 1;
          return (at - bt) || (b.r / b.x - a.r / a.x) || jamfor(a.t, b.t);
        });
        var visade = traffar.slice(0, 200);
        var ny = document.createDocumentFragment();
        visade.forEach(function (k) { ny.appendChild(resultatrad(k)); });
        ul.replaceChildren(ny);
        resultat.hidden = !traffar.length;
        status.textContent = traffar.length
          ? traffar.length + ' kort' + (traffar.length > visade.length ? ', de första ' + visade.length + ' visas' : '')
          : 'Inga kort matchar ”' + fraga + '”. Pröva ett efternamn, en titel eller ett årtal.';
      }).catch(function () {
        status.textContent = 'Sökindexet gick inte att läsa in. Ladda om sidan och försök igen.';
      });
    };

    sok(q);
    var timer;
    falt.addEventListener('input', function () {
      clearTimeout(timer);
      timer = setTimeout(function () {
        var url = new URL(location.href);
        if (falt.value) url.searchParams.set('q', falt.value); else url.searchParams.delete('q');
        history.replaceState(null, '', url);
        sok(falt.value);
      }, 150);
    });
  }
})();
