/* Kartoteket: sortering, bläddring, filter, sökning och kort på måfå. Sajten fungerar utan skriptet. */
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

  /* Gemener utan accenter, men å, ä och ö behålls som egna bokstäver. */
  function normal(s) {
    return (s || '').toLowerCase()
      .replace(/å/g, '\u0001').replace(/ä/g, '\u0002').replace(/ö/g, '\u0003')
      .normalize('NFD').replace(/[̀-ͯ]/g, '')
      .replace(/\u0001/g, 'å').replace(/\u0002/g, 'ä').replace(/\u0003/g, 'ö');
  }
  function ordI(fraga) { return normal(fraga).split(/\s+/).filter(Boolean); }

  function el(tagg, klass, text) {
    var n = document.createElement(tagg);
    if (klass) n.className = klass;
    if (text !== undefined) n.textContent = text;
    return n;
  }

  /* Uppdaterar en role="status" först när skrivandet har stannat, så att skärmläsaren inte pratar i mun. */
  function meddelare(nod, ms) {
    var t;
    var sag = function (text) {
      clearTimeout(t);
      t = setTimeout(function () { if (nod) nod.textContent = text; }, ms);
    };
    sag.avbryt = function () { clearTimeout(t); };
    return sag;
  }

  function lagra(nyckel, varde) {
    try {
      if (varde === null) sessionStorage.removeItem(nyckel);
      else sessionStorage.setItem(nyckel, JSON.stringify(varde));
    } catch (e) { /* privat läge eller blockerad lagring: bläddringen följer då hemlådan */ }
  }
  function hamta(nyckel) {
    try { return JSON.parse(sessionStorage.getItem(nyckel) || 'null'); } catch (e) { return null; }
  }

  /* ---------- "/" går till sökfältet */
  document.addEventListener('keydown', function (ev) {
    if (ev.key !== '/' || ev.ctrlKey || ev.metaKey || ev.altKey) return;
    if (ev.target.closest && ev.target.closest('input, textarea, select, [contenteditable]')) return;
    var falt = document.getElementById('sok') || document.getElementById('toppsok');
    if (!falt) return;
    ev.preventDefault();
    falt.focus();
    falt.select();
  });

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

  /* ---------- lådor: visa en bit i taget, eller alla som matchar filtret */
  function radText(li) {
    if (li._h === undefined) {
      var t = li.querySelector('.rad-titel'), m = li.querySelector('.rad-meta');
      li._h = normal((t ? t.textContent : '') + ' ' + (m ? m.textContent : ''));
    }
    return li._h;
  }

  function visaBit(lista, antal) {
    var steg = parseInt(lista.getAttribute('data-visa'), 10) || 60;
    var rader = lista.children;
    var bladdra = lista.parentNode.querySelector('.bladdra');
    var ord = lista._filter || [];
    if (ord.length) {
      var traffar = 0;
      for (var j = 0; j < rader.length; j++) {
        var h = radText(rader[j]);
        var ja = ord.every(function (o) { return h.indexOf(o) !== -1; });
        rader[j].hidden = !ja;
        if (ja) traffar++;
      }
      if (bladdra) bladdra.hidden = true;
      lista.parentNode.hidden = traffar === 0;
      return traffar;
    }
    lista.parentNode.hidden = false;
    var visas = Math.max(antal || steg, steg);
    for (var i = 0; i < rader.length; i++) rader[i].hidden = i >= visas;
    if (!bladdra) return rader.length;
    var kvar = rader.length - Math.min(visas, rader.length);
    bladdra.hidden = kvar <= 0;
    bladdra.querySelector('span').textContent = kvar + ' kort till i lådan';
    lista.setAttribute('data-visas', Math.min(visas, rader.length));
    return rader.length;
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

    /* Ordningen sparas när ett kort öppnas, så att föregående och nästa kort följer den. */
    lista.addEventListener('click', function (ev) {
      if (!ev.target.closest('a')) return;
      var rader = [];
      Array.prototype.forEach.call(lista.children, function (li) {
        if (lista._filter && lista._filter.length && li.hidden) return;
        var a = li.querySelector('a');
        rader.push([a.pathname, li.querySelector('.rad-titel .t').textContent]);
      });
      lagra('kartoteket-ordning', rader);
    });
  });

  /* ---------- filter i stora lådor */
  var filter = document.getElementById('filter');
  if (filter) {
    var flista = document.querySelector('.kortlista[data-visa]');
    var fstatus = document.querySelector('.filter-status');
    var fsag = meddelare(fstatus, 400);
    var totalt = flista.children.length;
    var tal = function (n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ' '); };
    filter.addEventListener('input', function () {
      flista._filter = ordI(filter.value);
      var n = visaBit(flista);
      if (!flista._filter.length) { fsag.avbryt(); fstatus.hidden = true; fstatus.textContent = ''; return; }
      fstatus.hidden = false;
      if (n) {
        fsag(tal(n) + ' av ' + tal(totalt) + ' kort');
      } else {
        fsag.avbryt();
        fstatus.replaceChildren(
          document.createTextNode('Inga kort i lådan matchar ”' + filter.value + '”. '),
          (function () {
            var a = el('a', '', 'Sök i hela katalogen');
            a.href = filter.getAttribute('data-sok') + '?q=' + encodeURIComponent(filter.value);
            return a;
          })(),
          document.createTextNode('.')
        );
      }
    });
  }

  /* ---------- sortering */
  var jamfor = new Intl.Collator('sv').compare;
  document.querySelectorAll('.sortering').forEach(function (grupp) {
    var lista = grupp.closest('.lista').querySelector('.kortlista');
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

  /* ---------- föregående och nästa kort i den ordning lådan visades */
  var kortNav = document.querySelector('.kort-nav');
  if (kortNav) {
    var ordning = hamta('kartoteket-ordning');
    var plats = -1;
    if (ordning) {
      for (var p = 0; p < ordning.length; p++) if (ordning[p][0] === location.pathname) { plats = p; break; }
    }
    if (plats !== -1) {
      var byt = function (klass, rubrik, post) {
        var gammal = kortNav.querySelector('.' + klass);
        var ny;
        if (post) {
          ny = el('a', klass);
          ny.href = post[0];
          ny.appendChild(el('span', '', rubrik));
          ny.appendChild(el('span', 'kt', post[1]));
        } else {
          ny = el('span');
        }
        if (gammal) gammal.replaceWith(ny);
        else if (klass === 'fore') kortNav.replaceChild(ny, kortNav.firstElementChild);
        else kortNav.replaceChild(ny, kortNav.lastElementChild);
      };
      byt('fore', 'Föregående kort', ordning[plats - 1]);
      byt('nasta', 'Nästa kort', ordning[plats + 1]);
    }
  } else {
    lagra('kartoteket-ordning', null);
  }

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
    var sag = meddelare(document.querySelector('.vh[role="status"]'), 800);
    var tomt = document.querySelector('.sok-tomt');
    var ul = resultat.querySelector('.kortlista');
    var q = new URLSearchParams(location.search).get('q') || '';
    falt.value = q;

    /* Högst ett tecken fel, fattas eller för mycket. */
    var nara = function (a, b) {
      if (Math.abs(a.length - b.length) > 1) return false;
      var i = 0, j = 0, fel = 0;
      while (i < a.length && j < b.length) {
        if (a[i] === b[j]) { i++; j++; continue; }
        if (++fel > 1) return false;
        if (a.length > b.length) i++;
        else if (b.length > a.length) j++;
        else { i++; j++; }
      }
      return fel + (a.length - i) + (b.length - j) <= 1;
    };

    var resultatrad = function (k) {
      var li = el('li');
      var a = el('a');
      a.setAttribute('href', rot + k.u);
      var titel = el('span', 'rad-titel');
      titel.appendChild(el('span', 't', k.t));
      if (k.s) titel.appendChild(el('span', 'u', k.s));
      var mark = el('span', 'rad-mark');
      var betyg = el('span', 'betyg' + (k.r === k.x ? ' hog' : ''), k.r ? String(k.r) : '–');
      betyg.setAttribute('aria-hidden', 'true');
      mark.appendChild(el('span', 'vh', k.r ? 'Betyg ' + k.r + ' av ' + k.x : 'Inget betyg'));
      mark.appendChild(betyg);
      a.appendChild(titel);
      a.appendChild(el('span', 'rad-meta', [k.k, k.y, k.a].filter(Boolean).join(', ')));
      a.appendChild(mark);
      li.appendChild(a);
      return li;
    };

    var sok = function (fraga) {
      var ord = ordI(fraga);
      document.title = fraga ? '”' + fraga + '”, Sök | Kartoteket' : 'Sök | Kartoteket';
      if (!ord.length) {
        status.textContent = ''; sag(''); resultat.hidden = true; tomt.hidden = true; return;
      }
      hamtaIndex().then(function (lista) {
        lista.forEach(function (k) {
          if (!k._h) {
            k._h = normal([k.t, k.s, k.a, k.o, k.y, k.k, k.g, k.c].join(' '));
            k._w = k._h.split(/[\s,.;:()/–-]+/).filter(Boolean);
          }
        });
        var traffar = lista.filter(function (k) {
          return ord.every(function (o) { return k._h.indexOf(o) !== -1; });
        });
        /* Utan träffar: pröva ord med ett tecken fel. Den stavning som flest kort har kommer först. */
        var ungefar = '';
        var stavning = {};
        if (!traffar.length) {
          traffar = lista.filter(function (k) {
            k._nara = '';
            return ord.every(function (o) {
              if (k._h.indexOf(o) !== -1) return true;
              if (o.length < 4) return false;
              var w = k._w.filter(function (w) { return nara(o, w); })[0];
              if (w && !k._nara) k._nara = w;
              return !!w;
            });
          });
          traffar.forEach(function (k) { stavning[k._nara] = (stavning[k._nara] || 0) + 1; });
          ungefar = Object.keys(stavning).sort(function (a, b) { return stavning[b] - stavning[a]; })[0] || '';
        }
        traffar.sort(function (a, b) {
          var as = ungefar ? -stavning[a._nara] : 0, bs = ungefar ? -stavning[b._nara] : 0;
          var at = normal(a.t).indexOf(ord[0]) === 0 ? 0 : 1;
          var bt = normal(b.t).indexOf(ord[0]) === 0 ? 0 : 1;
          return (as - bs) || (at - bt) || (b.r / b.x - a.r / a.x) || jamfor(a.t, b.t);
        });
        var visade = traffar.slice(0, 200);
        var ny = document.createDocumentFragment();
        visade.forEach(function (k) { ny.appendChild(resultatrad(k)); });
        ul.replaceChildren(ny);
        resultat.hidden = !traffar.length;
        tomt.hidden = traffar.length > 0;
        var antal = traffar.length + ' kort' +
          (traffar.length > visade.length ? ', de första ' + visade.length + ' visas' : '');
        var text;
        if (ungefar) {
          text = 'Inga kort matchar ”' + fraga + '” exakt. ' + antal + ' med liknande stavning, först ”' + ungefar + '”.';
        }
        else if (traffar.length) text = antal;
        else text = 'Inga kort matchar ”' + fraga + '”. Pröva ett efternamn, en titel, en genre eller ett årtal.';
        status.textContent = text;
        sag(text);
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
