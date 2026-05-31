# -*- coding: utf-8 -*-
from PIL import Image, ImageEnhance
import base64, io, re, json
import os
ROOT   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets") + os.sep
BUILD  = os.path.join(ROOT, ".build") + os.sep
DISTD  = os.path.join(ROOT, "dist") + os.sep
os.makedirs(BUILD, exist_ok=True)


T = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'template2.html')
html = open(T, encoding='utf-8').read()

def rep(old, new, label, n=1):
    global html
    c = html.count(old)
    assert c >= n and c > 0, f'NOT FOUND [{label}] count={c}'
    html = html.replace(old, new, n)
    print('ok:', label)

# ---------- CSS additions ----------
CSS = """
/* ===== graphic system ===== */
html{counter-reset:sec;}
body{position:relative;}
body:after{content:"";position:fixed;inset:0;z-index:-1;pointer-events:none;background-image:radial-gradient(var(--dot) 1.2px,transparent 1.2px);background-size:28px 28px;opacity:.6;}
:root{--dot:#e1d7c3;}
html[data-season="winter"]{--dot:#d3d2cd;}
html[data-season="spring"]{--dot:#d6dcc6;}
html[data-season="summer"]{--dot:#e7dab9;}

.masthead{display:flex;justify-content:space-between;align-items:center;gap:14px;padding-bottom:14px;border-bottom:1.5px solid var(--ink);margin-bottom:38px;font-weight:700;font-size:11.5px;letter-spacing:.16em;text-transform:uppercase;}
.masthead .r{color:var(--soft);}

.S{counter-increment:sec;}
.S .eyebrow{display:flex;align-items:center;gap:14px;width:100%;}
.S .eyebrow:before{content:counter(sec,decimal-leading-zero);width:auto;height:auto;background:none;border-radius:0;font-family:var(--disp);font-weight:700;font-size:14px;color:var(--acc);}
.S .eyebrow:after{content:"";flex:1;height:1.5px;background:var(--line);}

.rings{position:absolute;pointer-events:none;}
.rings circle{fill:none;stroke:var(--acc);stroke-width:1.1;transition:stroke .5s;}
.hero-art{position:relative;}
.hero-art .rings.big{width:64%;right:-12%;bottom:-14%;z-index:1;}
.hero-art .rings.big circle{stroke:var(--ink);opacity:.13;stroke-width:1;}
.hero-art .rings.sm{width:23%;left:-7%;top:5%;z-index:3;}
.hero-art .rings.sm circle{stroke:var(--acc);stroke-width:1.7;}

.sticker{transform:none;border-radius:9px;font-weight:700;letter-spacing:.01em;background:var(--card);color:var(--ink);border:1.5px solid var(--acc);}

.mark{position:relative;white-space:nowrap;z-index:0;}
.mark:before{content:"";position:absolute;left:-3px;right:-3px;bottom:.05em;height:.32em;background:var(--acc-soft);z-index:-1;border-radius:3px;transition:background .5s;}

.dcard .ic{display:inline-flex;align-items:center;justify-content:center;width:48px;height:48px;border-radius:15px;background:var(--acc-soft);color:var(--acc);transition:.5s;}
.dcard .ic svg{width:25px;height:25px;}

.step{border-top:2px solid var(--ink);padding-top:16px;}

.seasons .g{display:inline-flex;}
.seasons .g svg{width:14px;height:14px;}
.seasons button[data-s=winter] .g{color:#2f6cf0;}
.seasons button[data-s=spring] .g{color:#1ba35b;}
.seasons button[data-s=summer] .g{color:#f2a00c;}
.seasons button[data-s=autumn] .g{color:#ff5a1f;}
.seasons button.on .g{color:var(--bg);}

.about .pic .pring{position:absolute;inset:-24px;width:auto;height:auto;z-index:1;}
.about .pic .pring circle{stroke:var(--acc);stroke-width:.8;opacity:.5;}

.footmark{display:flex;align-items:center;gap:12px;}
.footmark .fr{width:44px;height:44px;flex:0 0 auto;}
.footmark .fr circle{fill:none;stroke:var(--acc);stroke-width:2.4;}
</style>"""
rep('</style>', CSS, 'css block')

# ---------- numbered sections ----------
for old, new, lab in [
    ('<section class="prob" id="problem">', '<section class="prob S" id="problem">', 'S problem'),
    ('<section id="products">', '<section class="S" id="products">', 'S products'),
    ('<section id="deliverables">', '<section class="S" id="deliverables">', 'S deliverables'),
    ('<section id="process">', '<section class="S" id="process">', 'S process'),
    ('<section id="payback">', '<section class="S" id="payback">', 'S payback'),
    ('<section id="cases">', '<section class="S" id="cases">', 'S cases'),
    ('<section id="about">', '<section class="S" id="about">', 'S about'),
    ('<section id="faq">', '<section class="S" id="faq">', 'S faq'),
]:
    rep(old, new, lab)

# ---------- hero masthead (wrap restructure) ----------
rep('<section class="hero">\n  <div class="wrap hero-grid">',
    '<section class="hero">\n  <div class="wrap">\n    <div class="masthead"><span>Сезон — студия меню для кофеен</span><span class="r">Москва · с 2026</span></div>\n    <div class="hero-grid">',
    'hero open')
rep('  </div>\n</section>\n\n<!-- MARQUEE -->',
    '  </div>\n  </div>\n</section>\n\n<!-- MARQUEE -->',
    'hero close')

# ---------- hero rings (replace blob) ----------
rings_big = '<svg class="rings big draw" viewBox="0 0 100 100"><circle pathLength="1" cx="50" cy="50" r="48"/><circle pathLength="1" cx="50" cy="50" r="38"/><circle pathLength="1" cx="50" cy="50" r="28"/><circle pathLength="1" cx="50" cy="50" r="18"/><circle pathLength="1" cx="50" cy="50" r="8"/></svg>'
rings_sm = '<svg class="rings sm" viewBox="0 0 100 100"><circle cx="50" cy="50" r="46"/><circle cx="50" cy="50" r="31"/><circle cx="50" cy="50" r="16"/></svg>'
rep('<div class="blob"></div>', rings_big + rings_sm, 'hero rings')

# ---------- squiggle -> highlight ----------
rep('<span class="squiggle">окупается<svg viewBox="0 0 300 12" preserveAspectRatio="none"><path d="M3 8 C 60 2, 120 2, 160 6 S 250 11, 297 4"/></svg></span>',
    '<span class="mark">окупается</span>', 'hero mark')

# ---------- season glyphs ----------
GLY = {
 'winter':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M12 3v18M4.2 7.5l15.6 9M19.8 7.5 4.2 16.5"/></svg>',
 'spring':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21v-8"/><path d="M12 13c-3 0-5-2-5-5 3 0 5 2 5 5z"/><path d="M12 11c0-2.6 2-4.5 5-4.5 0 2.6-2 4.5-5 4.5z"/></svg>',
 'summer':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="3.6"/><path d="M12 3v2M12 19v2M3 12h2M19 12h2M5.6 5.6 7 7M17 17l1.4 1.4M18.4 5.6 17 7M7 17l-1.4 1.4"/></svg>',
 'autumn':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M6 18C6 10 12 5 19 5c0 8-6 13-13 13z"/><path d="M6 18 14.5 9.5"/></svg>',
}
for s, lab, on in [('winter','Зима',''),('spring','Весна',''),('summer','Лето',''),('autumn','Осень',' class="on"')]:
    old = f'<button data-s="{s}"{on} onclick="setSeason(\'{s}\',this)"><span class="d"></span><span>{lab}</span></button>'
    new = f'<button data-s="{s}"{on} onclick="setSeason(\'{s}\',this)"><span class="g">{GLY[s]}</span><span>{lab}</span></button>'
    rep(old, new, 'season '+s)

# ---------- deliverable icons ----------
IC = {
 '1':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4"/><path d="M9 12h6M9 15.5h6"/></svg>',
 '2':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="4.5" width="14" height="16" rx="2"/><path d="M9 3.5h6v3H9z"/><path d="M8.5 11h7M8.5 14.5h7"/></svg>',
 '3':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"><circle cx="12" cy="12" r="8.5"/><path d="M8.6 15.4 15.4 8.6"/><circle cx="9.4" cy="9.4" r="1"/><circle cx="14.6" cy="14.6" r="1"/></svg>',
 '4':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M6.5 8h11l-1 12.5h-9z"/><path d="M9 8a3 3 0 0 1 6 0"/></svg>',
 '5':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="9" r="2.6"/><path d="M4.5 18.5a4.5 4.5 0 0 1 9 0"/><path d="M15.6 7a2.6 2.6 0 0 1 0 5"/><path d="M16 18.5a4.5 4.5 0 0 0-1.3-3.2"/></svg>',
 '6':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M4 8h9M4 12h6"/><path d="M14.5 17 19 12.5l2 2-4.5 4.5-2.5.5z"/></svg>',
}
for k in '123456':
    rep(f'<span class="n">{k}</span>', f'<span class="ic">{IC[k]}</span>', 'icon '+k)

# ---------- about ring -> concentric ----------
rep('      <div class="ring"></div>',
    '      <svg class="rings pring draw" viewBox="0 0 100 100"><circle pathLength="1" cx="50" cy="50" r="48"/><circle pathLength="1" cx="50" cy="50" r="40"/><circle pathLength="1" cx="50" cy="50" r="32"/></svg>',
    'about rings')

# ---------- footer mark ----------
rep('    <div class="brand"><span class="o" style="display:inline-block;width:17px;height:17px"></span> Сезон</div>',
    '    <div class="footmark"><svg class="fr" viewBox="0 0 100 100"><circle cx="50" cy="50" r="46"/><circle cx="50" cy="50" r="33"/><circle cx="50" cy="50" r="20"/><circle cx="50" cy="50" r="8"/></svg><span class="brand">Сезон</span></div>',
    'footer mark')

# ---------- enhancements: secondary color, ring animation, big season word ----------
CSS2 = """
:root{--acc2:#21564f;}
.masthead{border-bottom-color:var(--acc2);}
.S .eyebrow:after{background:var(--acc2);opacity:.4;}
.step{border-top-color:var(--acc2);}
.hero-art .rings.big circle{stroke:var(--acc2);opacity:.5;}
.about .pic .pring circle{stroke:var(--acc2);opacity:.5;}
.footmark .fr circle{stroke:var(--acc2);}
.marq{background:var(--acc2);}

.draw circle{stroke-dasharray:1;stroke-dashoffset:1;}
.draw.in circle{animation:draw 1.5s cubic-bezier(.4,0,.2,1) forwards;}
.draw.in circle:nth-child(2){animation-delay:.12s;}
.draw.in circle:nth-child(3){animation-delay:.24s;}
.draw.in circle:nth-child(4){animation-delay:.36s;}
.draw.in circle:nth-child(5){animation-delay:.48s;}
@keyframes draw{to{stroke-dashoffset:0;}}

.hero-art .rings.sm{animation:spin 26s linear infinite;transform-origin:50% 50%;}
.hero-art .rings.sm circle{stroke-dasharray:3 4;}
@keyframes spin{to{transform:rotate(360deg);}}

.bigband{padding:clamp(26px,5vw,56px) 0;overflow:hidden;text-align:center;}
.bigword:before{font-family:var(--disp);font-weight:800;font-size:clamp(74px,21vw,250px);letter-spacing:-.04em;color:transparent;-webkit-text-stroke:2px var(--acc2);opacity:.45;display:block;white-space:nowrap;line-height:.85;transition:-webkit-text-stroke-color .5s;}
html[data-season=autumn] .bigword:before{content:"ОСЕНЬ";}
html[data-season=winter] .bigword:before{content:"ЗИМА";}
html[data-season=spring] .bigword:before{content:"ВЕСНА";}
html[data-season=summer] .bigword:before{content:"ЛЕТО";}
</style>"""
rep('</style>', CSS2, 'css2')

rep("document.querySelectorAll('.reveal').forEach(el=>io.observe(el));",
    "document.querySelectorAll('.reveal,.draw').forEach(el=>io.observe(el));",
    'observe draws')

rep('<!-- FINAL -->',
    '<div class="bigband"><div class="bigword reveal"></div></div>\n\n<!-- FINAL -->',
    'bigband')

# ---------- MAX graphics layer ----------
CSS3 = """
.grain{position:fixed;inset:0;z-index:400;pointer-events:none;opacity:.045;mix-blend-mode:multiply;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");}
.progress{position:fixed;top:0;left:0;height:3px;width:0;background:linear-gradient(90deg,var(--acc),var(--acc2));z-index:500;}
.scrollring{position:fixed;right:22px;bottom:22px;width:54px;height:54px;z-index:450;cursor:pointer;background:var(--card);border:1.5px solid var(--line);border-radius:50%;box-shadow:0 10px 24px -10px rgba(0,0,0,.3);opacity:0;transform:scale(.5);transition:opacity .35s,transform .35s;}
.scrollring.show{opacity:1;transform:scale(1);}
.scrollring svg{position:absolute;inset:0;width:100%;height:100%;transform:rotate(-90deg);}
.scrollring .bar{fill:none;stroke:var(--acc);stroke-width:3.5;stroke-linecap:round;transition:stroke .5s;}
.scrollring .arrow{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-family:var(--disp);font-weight:700;color:var(--ink);font-size:17px;}
.secnav{position:fixed;right:24px;top:50%;transform:translateY(-50%);z-index:120;display:flex;flex-direction:column;gap:14px;}
.secnav a{display:flex;align-items:center;gap:9px;justify-content:flex-end;text-decoration:none;color:var(--soft);font-weight:700;font-size:11px;letter-spacing:.06em;font-variant-numeric:tabular-nums;}
.secnav a .ln{width:16px;height:2px;background:var(--line);border-radius:2px;transition:.3s;}
.secnav a .tx{opacity:0;transform:translateX(6px);transition:.3s;}
.secnav a:hover .tx,.secnav a.active .tx{opacity:1;transform:none;}
.secnav a:hover .ln,.secnav a.active .ln{width:32px;background:var(--acc);}
.secnav a.active{color:var(--ink);}
@media(max-width:1180px){.secnav{display:none;}}
.wrap{position:relative;z-index:1;}
.hasbg{position:relative;overflow:hidden;}
.bgword{position:absolute;top:16%;z-index:0;pointer-events:none;font-family:var(--disp);font-weight:800;letter-spacing:-.05em;color:transparent;-webkit-text-stroke:1.5px var(--line);font-size:clamp(96px,19vw,250px);line-height:.8;white-space:nowrap;opacity:.85;user-select:none;}
.bgword.bgw-right{right:-3%;}
.bgword.bgw-left{left:-5%;}
.S .eyebrow:after{transform:scaleX(0);transform-origin:left;transition:transform .9s cubic-bezier(.2,.7,.2,1) .1s;}
.S .eyebrow.in:after{transform:scaleX(1);}
.mark:before{transform:scaleX(0);transform-origin:left;transition:transform .6s cubic-bezier(.2,.7,.2,1) .55s;}
.loaded .mark:before{transform:scaleX(1);}
.final{position:relative;overflow:hidden;}
.final .mesh{position:absolute;inset:0;z-index:0;pointer-events:none;}
.final .mesh i{position:absolute;border-radius:50%;filter:blur(55px);}
.final .mesh .m1{width:42%;aspect-ratio:1;background:rgba(255,255,255,.4);left:-6%;top:-22%;animation:flo1 15s ease-in-out infinite;}
.final .mesh .m2{width:36%;aspect-ratio:1;background:rgba(0,0,0,.14);right:-5%;bottom:-26%;animation:flo2 19s ease-in-out infinite;}
.final .spot{position:absolute;width:360px;height:360px;border-radius:50%;background:radial-gradient(circle,rgba(255,255,255,.45),transparent 68%);transform:translate(-50%,-50%);pointer-events:none;z-index:1;opacity:0;transition:opacity .3s;}
.final .wrap{z-index:2;}
@keyframes flo1{0%,100%{transform:translate(0,0)}50%{transform:translate(10%,14%)}}
@keyframes flo2{0%,100%{transform:translate(0,0)}50%{transform:translate(-9%,-12%)}}
@media (prefers-reduced-motion: reduce){.hero-art .rings.sm,.final .mesh i{animation:none!important;}}
</style>"""
rep('</style>', CSS3, 'css3')

TOPUI = '''<body>
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-KS3V5PKD"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->
<div class="grain"></div>
<div class="progress"></div>
<nav class="secnav" aria-hidden="true">
  <a href="#problem"><span class="tx">01</span><span class="ln"></span></a>
  <a href="#products"><span class="tx">02</span><span class="ln"></span></a>
  <a href="#deliverables"><span class="tx">03</span><span class="ln"></span></a>
  <a href="#process"><span class="tx">04</span><span class="ln"></span></a>
  <a href="#payback"><span class="tx">05</span><span class="ln"></span></a>
  <a href="#cases"><span class="tx">06</span><span class="ln"></span></a>
  <a href="#about"><span class="tx">07</span><span class="ln"></span></a>
  <a href="#faq"><span class="tx">08</span><span class="ln"></span></a>
</nav>
<div class="scrollring" title="Наверх"><svg viewBox="0 0 54 54"><circle class="bar" cx="27" cy="27" r="23"/></svg><span class="arrow">↑</span></div>'''
rep('<body>', TOPUI, 'top ui')

rep('<section class="S" id="process">\n  <div class="wrap">',
    '<section class="S hasbg" id="process">\n  <div class="bgword bgw-right">МЕНЮ</div>\n  <div class="wrap">', 'bgword process')
rep('<section class="S" id="payback">\n  <div class="wrap">',
    '<section class="S hasbg" id="payback">\n  <div class="bgword bgw-left">ВКУС</div>\n  <div class="wrap">', 'bgword payback')

rep('<section class="final" id="contact">',
    '<section class="final" id="contact">\n  <div class="mesh"><i class="m1"></i><i class="m2"></i></div>\n  <div class="spot"></div>', 'final fx')

SCRIPT = '''<script>
(function(){
  var rm=matchMedia('(prefers-reduced-motion: reduce)').matches;
  var bar=document.querySelector('.progress');
  var ring=document.querySelector('.scrollring'), rb=ring&&ring.querySelector('.bar');
  var len=rb?rb.getTotalLength():0; if(rb){rb.style.strokeDasharray=len;rb.style.strokeDashoffset=len;}
  if(ring) ring.addEventListener('click',function(){window.scrollTo({top:0,behavior:'smooth'});});
  var links={}; document.querySelectorAll('.secnav a').forEach(function(a){links[a.getAttribute('href').slice(1)]=a;});
  var ids=['problem','products','deliverables','process','payback','cases','about','faq'];
  var so=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){for(var k in links)links[k].classList.remove('active');if(links[e.target.id])links[e.target.id].classList.add('active');}});},{rootMargin:'-45% 0px -45% 0px'});
  ids.forEach(function(id){var s=document.getElementById(id);if(s)so.observe(s);});
  var bgw=[].slice.call(document.querySelectorAll('.bgword')), hero=document.querySelector('.hero-art');
  function onScroll(){
    var h=document.documentElement,max=h.scrollHeight-h.clientHeight,p=max>0?h.scrollTop/max:0;
    if(bar)bar.style.width=(p*100)+'%';
    if(rb)rb.style.strokeDashoffset=len*(1-p);
    if(ring)ring.classList.toggle('show',h.scrollTop>500);
    if(rm)return;
    var vh=window.innerHeight;
    bgw.forEach(function(el){var r=el.getBoundingClientRect();var prog=(vh-r.top)/(vh+r.height);el.style.transform='translateX('+((prog-.5)*130)+'px)';});
    if(hero)hero.style.transform='translateY('+(window.scrollY*0.06)+'px)';
  }
  window.addEventListener('scroll',onScroll,{passive:true}); window.addEventListener('resize',onScroll); onScroll();
  var fmt=function(n){return new Intl.NumberFormat('ru-RU').format(n);};
  function animM(el){
    var t=el.textContent.trim();
    var fi=-1; for(var a=0;a<t.length;a++){if(t[a]>='0'&&t[a]<='9'){fi=a;break;}}
    if(fi<0)return;
    var li=fi; for(var b=t.length-1;b>=0;b--){if(t[b]>='0'&&t[b]<='9'){li=b;break;}}
    var pre=t.slice(0,fi), suf=t.slice(li+1);
    var tg=parseInt(t.slice(fi,li+1).replace(/[^0-9]/g,''),10); if(isNaN(tg))return;
    var st=34,i=0; var tm=setInterval(function(){i++;var c=Math.round(tg/st*i);if(i>=st){c=tg;clearInterval(tm);}el.textContent=pre+fmt(c)+suf;},26);
  }
  var mo=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){animM(e.target);mo.unobserve(e.target);}});},{threshold:.6});
  document.querySelectorAll('.case .metric').forEach(function(el){mo.observe(el);});
  if(matchMedia('(pointer:fine)').matches&&!rm){
    document.querySelectorAll('.prod,.case').forEach(function(c){
      c.addEventListener('pointermove',function(e){var r=c.getBoundingClientRect();var x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;c.style.transform='perspective(820px) translateY(-6px) rotateX('+(-y*5)+'deg) rotateY('+(x*5)+'deg)';});
      c.addEventListener('pointerleave',function(){c.style.transform='';});
    });
  }
  var fin=document.querySelector('.final'), spot=document.querySelector('.final .spot');
  if(fin&&spot){fin.addEventListener('pointermove',function(e){var r=fin.getBoundingClientRect();spot.style.left=(e.clientX-r.left)+'px';spot.style.top=(e.clientY-r.top)+'px';spot.style.opacity=1;});fin.addEventListener('pointerleave',function(){spot.style.opacity=0;});}
})();
</script>
</body>'''
rep('</body>', SCRIPT, 'advanced js')

# ---------- WebGL living hero background ----------
CSS4 = """
.hero{position:relative;}
.hero-fx{position:absolute;inset:0;width:100%;height:100%;z-index:0;display:block;pointer-events:none;}
</style>"""
rep('</style>', CSS4, 'css4')

rep('<section class="hero">\n  <div class="wrap">',
    '<section class="hero">\n  <canvas class="hero-fx"></canvas>\n  <div class="wrap">', 'hero canvas')

WEBGL = '''<script>
(function(){
  var cv=document.querySelector('.hero-fx'); if(!cv) return;
  var gl; try{gl=cv.getContext('webgl')||cv.getContext('experimental-webgl');}catch(e){}
  if(!gl){cv.remove();return;}
  var rm=matchMedia('(prefers-reduced-motion: reduce)').matches;
  var vs='attribute vec2 p;void main(){gl_Position=vec4(p,0.,1.);}';
  var fs='precision highp float;uniform float u_time;uniform vec2 u_res;uniform vec3 c1;uniform vec3 c2;uniform vec3 c3;'+
   'float hash(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}'+
   'float noise(vec2 p){vec2 i=floor(p),f=fract(p);vec2 u=f*f*(3.-2.*f);return mix(mix(hash(i),hash(i+vec2(1.,0.)),u.x),mix(hash(i+vec2(0.,1.)),hash(i+vec2(1.,1.)),u.x),u.y);}'+
   'float fbm(vec2 p){float v=0.,a=.5;for(int i=0;i<5;i++){v+=a*noise(p);p*=2.02;a*=.5;}return v;}'+
   'void main(){vec2 uv=gl_FragCoord.xy/u_res.xy;vec2 p=uv*vec2(u_res.x/u_res.y,1.0)*2.2;float t=u_time*0.05;'+
   'vec2 q=vec2(fbm(p+vec2(0.,t)),fbm(p+vec2(5.2,1.3-t)));'+
   'vec2 r=vec2(fbm(p+4.0*q+vec2(1.7,9.2)+t),fbm(p+4.0*q+vec2(8.3,2.8)-t));'+
   'float f=fbm(p+4.0*r);'+
   'vec3 col=mix(c1,mix(c1,c3,0.6),smoothstep(0.0,0.7,f));'+
   'col=mix(col,c2,smoothstep(0.55,0.95,r.x)*0.18);'+
   'col=mix(col,c1,0.5);'+
   'gl_FragColor=vec4(col,1.0);}';
  function sh(t,s){var o=gl.createShader(t);gl.shaderSource(o,s);gl.compileShader(o);return o;}
  var pr=gl.createProgram();gl.attachShader(pr,sh(gl.VERTEX_SHADER,vs));gl.attachShader(pr,sh(gl.FRAGMENT_SHADER,fs));gl.linkProgram(pr);
  if(!gl.getProgramParameter(pr,gl.LINK_STATUS)){cv.remove();return;}
  gl.useProgram(pr);
  var buf=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,buf);
  gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,3,-1,-1,3]),gl.STATIC_DRAW);
  var loc=gl.getAttribLocation(pr,'p');gl.enableVertexAttribArray(loc);gl.vertexAttribPointer(loc,2,gl.FLOAT,false,0,0);
  var uT=gl.getUniformLocation(pr,'u_time'),uR=gl.getUniformLocation(pr,'u_res'),uC1=gl.getUniformLocation(pr,'c1'),uC2=gl.getUniformLocation(pr,'c2'),uC3=gl.getUniformLocation(pr,'c3');
  function hex(v){v=(v||'').trim();if(v.charAt(0)==='#'){if(v.length===4)v='#'+v[1]+v[1]+v[2]+v[2]+v[3]+v[3];return [parseInt(v.substr(1,2),16)/255,parseInt(v.substr(3,2),16)/255,parseInt(v.substr(5,2),16)/255];}return [0.95,0.92,0.86];}
  function colors(){var s=getComputedStyle(document.documentElement);gl.uniform3fv(uC1,hex(s.getPropertyValue('--paper')));gl.uniform3fv(uC2,hex(s.getPropertyValue('--acc')));gl.uniform3fv(uC3,hex(s.getPropertyValue('--acc-soft')));}
  function size(){var d=Math.min(window.devicePixelRatio||1,2);cv.width=Math.max(1,cv.clientWidth*d);cv.height=Math.max(1,cv.clientHeight*d);gl.viewport(0,0,cv.width,cv.height);gl.uniform2f(uR,cv.width,cv.height);}
  window.addEventListener('resize',size);
  new MutationObserver(colors).observe(document.documentElement,{attributes:true,attributeFilter:['data-season']});
  size();colors();
  var start=Date.now();
  function frame(){gl.uniform1f(uT,(Date.now()-start)/1000);gl.drawArrays(gl.TRIANGLES,0,3);if(!rm)requestAnimationFrame(frame);}
  frame();
})();
</script>
</body>'''
rep('</body>', WEBGL, 'webgl')

# ---------- REAL CONTENT: VLOZ ----------
# brand renames (only standalone brand "Сезон", not the word сезон in copy)
rep('<div class="brand"><span class="o"></span>Сезон</div>',
    '<div class="brand"><span class="o"></span><span class="lk"><span class="d">Duckwin</span><span class="x">×</span><span class="v">VLOZ</span></span></div>', 'nav brand')
rep('    <a href="#contact" class="nav-cta"><svg viewBox="0 0 24 24" width="15" height="15" fill="currentColor"><path d="M22 3 2 11l5 2 2 6 3-4 5 4 5-16Z"/></svg><span>Telegram</span></a>',
    '    <a href="blog.html" class="nav-blog">Блог</a>\n    <a href="https://max.ru/u/ВАШ_ХЕШ" class="nav-max"><svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 5h16v11H8l-4 4z"/></svg><span>MAX</span></a>\n    <a href="#contact" class="nav-cta"><svg viewBox="0 0 24 24" width="15" height="15" fill="currentColor"><path d="M22 3 2 11l5 2 2 6 3-4 5 4 5-16Z"/></svg><span>Telegram</span></a>', 'nav blog link')
rep('</style>', '.nav-blog{font-weight:700;font-size:14px;color:var(--ink2);text-decoration:none;transition:color .2s;margin-right:4px;}\n.nav-blog:hover{color:var(--acc);}\n.nav-max{display:inline-flex;align-items:center;gap:6px;border:1.6px solid var(--line);color:var(--ink);padding:9px 15px;border-radius:99px;font-weight:700;font-size:14px;text-decoration:none;transition:border-color .2s,color .2s,transform .2s;}\n.nav-max:hover{border-color:var(--acc);color:var(--acc);transform:translateY(-2px);}\n.nav-max svg{width:15px;height:15px;}\n.brand .lk{display:inline-flex;align-items:baseline;gap:6px;}\n.brand .d{color:var(--ink2);font-weight:700;}\n.brand .x{color:var(--acc);font-weight:600;font-size:.82em;}\n.brand .v{font-weight:800;}\n@media(max-width:540px){.nav-max span{display:none;}}\n</style>', 'nav blog css')
rep('<span class="brand">Сезон</span>', '<span class="brand">VLOZ</span>', 'footer brand')
rep('<div class="masthead"><span>Сезон — студия меню для кофеен</span><span class="r">Москва · с 2026</span></div>',
    '<div class="masthead"><span>VLOZ — весна · лето · осень · зима</span><span class="r">Москва · duckwin.ru</span></div>', 'masthead')

# title + meta/OG
rep('<title>Сезон — студия меню для кофеен</title>',
    '<title>VLOZ — студия сезонного и авторского меню для кофеен</title>\n'
    '<meta name="description" content="VLOZ — студия сезонного и авторского меню для кофеен. Рецептуры, техкарты, расчёт себестоимости. Москва и онлайн.">\n'
    '<meta property="og:title" content="VLOZ — сезонное и авторское меню для кофеен">\n'
    '<meta property="og:description" content="Меню, которое окупается с первой недели.">\n'
    '<meta property="og:type" content="website">\n'
    '<meta property="og:url" content="https://duckwin.ru">\n'
    '<link rel="canonical" href="https://duckwin.ru">', 'title+meta')

# remove CASES section entirely (no real cases yet)
html = re.sub(r'<!-- CASES -->.*?<!-- ABOUT -->', '<!-- ABOUT -->', html, flags=re.S)
print('ok: removed cases')

# rebuild secnav (7 links, renumbered)
rep('''<nav class="secnav" aria-hidden="true">
  <a href="#problem"><span class="tx">01</span><span class="ln"></span></a>
  <a href="#products"><span class="tx">02</span><span class="ln"></span></a>
  <a href="#deliverables"><span class="tx">03</span><span class="ln"></span></a>
  <a href="#process"><span class="tx">04</span><span class="ln"></span></a>
  <a href="#payback"><span class="tx">05</span><span class="ln"></span></a>
  <a href="#cases"><span class="tx">06</span><span class="ln"></span></a>
  <a href="#about"><span class="tx">07</span><span class="ln"></span></a>
  <a href="#faq"><span class="tx">08</span><span class="ln"></span></a>
</nav>''',
'''<nav class="secnav" aria-hidden="true">
  <a href="#problem"><span class="tx">01</span><span class="ln"></span></a>
  <a href="#products"><span class="tx">02</span><span class="ln"></span></a>
  <a href="#deliverables"><span class="tx">03</span><span class="ln"></span></a>
  <a href="#process"><span class="tx">04</span><span class="ln"></span></a>
  <a href="#payback"><span class="tx">05</span><span class="ln"></span></a>
  <a href="#about"><span class="tx">06</span><span class="ln"></span></a>
  <a href="#faq"><span class="tx">07</span><span class="ln"></span></a>
</nav>''', 'secnav 7')

# JS ids array without cases
rep("var ids=['problem','products','deliverables','process','payback','cases','about','faq'];",
    "var ids=['problem','products','deliverables','process','payback','about','faq'];", 'js ids')

# hero chips -> honest (10 лет, Москва+онлайн, 4 сезона)
rep('''<div class="hero-chips">
        <span class="chip"><b><span class="num" data-to="8">0</span>+</b> лет в спешелти</span>
        <span class="chip"><b><span class="num" data-to="40">0</span>+</b> кофеен</span>
        <span class="chip"><b>4</b> сезона в год</span>
      </div>''',
'''<div class="hero-chips">
        <span class="chip"><b><span class="num" data-to="10">0</span></b> лет в спешелти</span>
        <span class="chip"><b>Москва</b> + онлайн</span>
        <span class="chip"><b>4</b> сезона в год</span>
      </div>''', 'hero chips')

# about lead
rep('<p class="lead reveal">[Имя]. Не маркетолог, нагенеривший «трендовые напитки», а человек, который годами варил, считал и запускал меню в реальных кофейнях.</p>',
    '<p class="lead reveal">Антон, 10 лет в спешелти-кофе. Не маркетолог, нагенеривший «трендовые напитки», а человек, который сам варил, считал себестоимость и запускал меню в реальных кофейнях.</p>', 'about lead')

# Telegram -> @kryanton (all occurrences)
html = html.replace('https://t.me/username', 'https://t.me/kryanton')
print('ok: telegram kryanton')

# final CTA: Telegram + MAX buttons + phone/email
rep('<a href="https://t.me/kryanton" class="btn reveal"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M22 3 2 11l5 2 2 6 3-4 5 4 5-16Z"/></svg>Написать в Telegram</a>\n    <div class="alt reveal">или почта <a href="mailto:hello@example.ru">hello@example.ru</a></div>',
'''<div class="cta-row reveal">
      <a href="https://t.me/kryanton" class="btn"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M22 3 2 11l5 2 2 6 3-4 5 4 5-16Z"/></svg>Telegram</a>
      <a href="https://max.ru/u/ВАШ_ХЕШ" class="btn btn-max"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 5h16v11H8l-4 4z"/></svg>MAX</a>
    </div>
    <div class="alt reveal">тел. / MAX <a href="tel:+79958861838">8 995 886 18 38</a> · почта <a href="mailto:ad@duckwin.ru">ad@duckwin.ru</a></div>''', 'final cta')

# footer text + links
rep('<div>© 2026 · Студия сезонного и авторского меню для кофеен</div>',
    '<div>© 2026 VLOZ · сезонное и авторское меню для кофеен · duckwin.ru</div>', 'footer copy')
rep('<div><a href="https://t.me/kryanton" style="color:var(--ink);font-weight:600">Telegram</a></div>',
    '<div style="display:flex;gap:16px"><a href="https://t.me/kryanton" style="color:var(--ink);font-weight:600">Telegram</a><a href="https://max.ru/u/ВАШ_ХЕШ" style="color:var(--ink);font-weight:600">MAX</a><a href="mailto:ad@duckwin.ru" style="color:var(--ink);font-weight:600">Почта</a></div>', 'footer links')

# real MAX link (decoded from QR)
html = html.replace('https://max.ru/u/ВАШ_ХЕШ',
    'https://max.ru/u/f9LHodD0cOIvYeSSomMV090N8qMvxtqD9VBvgUE7WqJQgWUf4hlujvKCu1s')
print('ok: max link')

# CSS for cta-row + MAX button
CSS5 = """
.cta-row{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;}
.final .btn-max{background:transparent;color:var(--ink);}
.final .btn-max:hover{background:var(--ink);color:var(--bg);}
</style>"""
rep('</style>', CSS5, 'css5')

# analytics (placeholders to fill in)
ANALYTICS = '''<!-- Yandex.Metrika counter -->
<script type="text/javascript">
(function(m,e,t,r,i,k,a){
m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};
m[i].l=1*new Date();
for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}
k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)
})(window,document,"script","https://mc.yandex.ru/metrika/tag.js?id=109550359","ym");
ym(109550359,"init",{ssr:true,webvisor:true,clickmap:true,ecommerce:"dataLayer",referrer:document.referrer,url:location.href,accurateTrackBounce:true,trackLinks:true});
</script>
<noscript><div><img src="https://mc.yandex.ru/watch/109550359" style="position:absolute;left:-9999px" alt=""></div></noscript>
<!-- /Yandex.Metrika counter -->
<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-KS3V5PKD');</script>
<!-- End Google Tag Manager -->'''
rep('</head>', ANALYTICS + '\n</head>', 'analytics')

# ---------- SEO ----------
rep('<p>Обсуждаем в Telegram после брифа. Работаю официально, по договору. [Уточните условия под себя.]</p>',
    '<p>Обсуждаем в Telegram после брифа. Работаю официально, по договору.</p>', 'faq5 clean')

rep('src="__HERO__" alt="Эксперт за работой"',
    'src="__HERO__" alt="Бариста готовит авторский напиток — студия меню VLOZ"', 'alt hero')
rep('src="__ABOUT__" alt="Эксперт за работой"',
    'src="__ABOUT__" alt="Антон Кряквин — основатель студии меню VLOZ"', 'alt about')

rep('<link rel="canonical" href="https://duckwin.ru">',
    '<meta property="og:image" content="https://duckwin.ru/og.jpg">\n<link rel="canonical" href="https://duckwin.ru">', 'og image')

faq=[
 ("Сколько правок входит в цену?","В каждый проект включено 2 круга правок — этого хватает в подавляющем большинстве случаев. Дополнительные оплачиваются по прайсу. Так проект не растягивается на месяцы, а вы заранее понимаете итоговую стоимость."),
 ("Что значит «гео-эксклюзив»?","Для пакета «Сигнатура»: разработанные для вас авторские напитки я не передаю другой кофейне в вашем районе. Вы получаете уникальность, которую сосед не скопирует из меню."),
 ("Работаете только по Москве?","Физическая проработка с дегустациями — да, по Москве. Но пакет «Сезонная коллекция» полностью удалённый и подходит для кофейни в любом городе."),
 ("Какие сроки?","Удалённая коллекция — обычно несколько дней. Авторская проработка с дегустациями дольше, обсуждаем под объём на брифе."),
 ("Как происходит оплата?","Обсуждаем в Telegram после брифа. Работаю официально, по договору."),
]
ld={"@context":"https://schema.org","@graph":[
 {"@type":"ProfessionalService","@id":"https://duckwin.ru/#org","name":"VLOZ",
  "description":"Студия сезонного и авторского меню для кофеен: рецептуры, технологические карты, расчёт себестоимости.",
  "url":"https://duckwin.ru","email":"ad@duckwin.ru","telephone":"+79958861838",
  "areaServed":["Москва","Россия"],
  "address":{"@type":"PostalAddress","addressLocality":"Москва","addressCountry":"RU"},
  "sameAs":["https://t.me/kryanton","https://max.ru/u/f9LHodD0cOIvYeSSomMV090N8qMvxtqD9VBvgUE7WqJQgWUf4hlujvKCu1s"]},
 {"@type":"Service","name":"Сезонная коллекция","provider":{"@id":"https://duckwin.ru/#org"},
  "areaServed":"Россия","description":"Готовая сезонная линейка напитков под ваше оборудование: рецептуры, техкарты, себестоимость, лист закупки.",
  "offers":{"@type":"Offer","price":"9000","priceCurrency":"RUB"}},
 {"@type":"Service","name":"Сигнатура","provider":{"@id":"https://duckwin.ru/#org"},
  "areaServed":"Москва","description":"Авторская разработка напитков под ключ с дегустациями и гео-эксклюзивом.",
  "offers":{"@type":"Offer","price":"60000","priceCurrency":"RUB"}},
 {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]}
]}
JSONLD='<script type="application/ld+json">\n'+json.dumps(ld,ensure_ascii=False,indent=1)+'\n</script>'
rep('</head>', JSONLD+'\n</head>', 'jsonld')

# ---------- inject images ----------
U = ASSETS
def d(fn, maxw, q=82, b=1.10, c=0.93, s=0.90, square=False):
    im = Image.open(U+fn).convert('RGB'); w,h = im.size
    if square:
        m=min(w,h); l=(w-m)//2; t=int((h-m)*0.35)
        im=im.crop((l,t,l+m,t+m)); w,h=im.size
    if w > maxw: im = im.resize((maxw,int(h*maxw/w)), Image.LANCZOS)
    im = ImageEnhance.Brightness(im).enhance(b)
    im = ImageEnhance.Contrast(im).enhance(c)
    im = ImageEnhance.Color(im).enhance(s)
    b2 = io.BytesIO(); im.save(b2,'JPEG',quality=q,optimize=True)
    return 'data:image/jpeg;base64,'+base64.b64encode(b2.getvalue()).decode()

# HERO = barista pour; ABOUT = real photo of Anton (sunglasses portrait)
html = html.replace('__HERO__', d('generated-image__16_.png',820,82))
html = html.replace('__ABOUT__', d('IMG_0237.jpeg',720,88, b=1.03, c=1.01, s=1.02, square=True))

out = BUILD + 'vloz.html'
open(out, 'w', encoding='utf-8').write(html)
print('\nWritten', out, len(html)//1024, 'KB')
