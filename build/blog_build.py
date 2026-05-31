# -*- coding: utf-8 -*-
import os
ROOT   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets") + os.sep
BUILD  = os.path.join(ROOT, ".build") + os.sep
DISTD  = os.path.join(ROOT, "dist") + os.sep
os.makedirs(BUILD, exist_ok=True)

import json
from PIL import Image, ImageEnhance
import base64, io

OUT = BUILD
UP = ASSETS
SITE = 'https://duckwin.ru'

def proc(fn, w, q=82, save=None):
    im = Image.open(UP+fn).convert('RGB'); W,H = im.size
    if W > w: im = im.resize((w,int(H*w/W)), Image.LANCZOS)
    im = ImageEnhance.Brightness(im).enhance(1.03)
    b = io.BytesIO(); im.save(b,'JPEG',quality=q,optimize=True)
    data = b.getvalue()
    if save: open(OUT+save,'wb').write(data)
    return 'data:image/jpeg;base64,'+base64.b64encode(data).decode()

# cover source per article (chosen from uploads)
IMG = {
 'kak-sostavit-menyu-kofejni':'1780253212.png',
 'sebestoimost-napitka':'1780253299.png',
 'sezonnoe-menyu':'1780253424.png',
 'avtorskie-napitki-idei':'1780253467.png',
 'tehnologicheskaya-karta':'1780253595.png',
 'srednij-chek-kofejni':'1780253639.png',
}
THUMB = {}

# ---------------- shared head/style ----------------
STYLE = """
:root{--bg:#f5f1e8;--card:#fffdf8;--ink:#171310;--ink2:#4c453b;--soft:#857a6a;--line:#e6dcc9;--acc:#ff5a1f;--acc-soft:#ffe2d3;--acc2:#21564f;--dot:#e1d7c3;--disp:'Bricolage Grotesque',sans-serif;--body:'Hanken Grotesk',system-ui,sans-serif;}
*{margin:0;padding:0;box-sizing:border-box;}
html{scroll-behavior:smooth;}
body{background:var(--bg);color:var(--ink);font-family:var(--body);line-height:1.6;-webkit-font-smoothing:antialiased;position:relative;}
body:after{content:"";position:fixed;inset:0;z-index:-1;pointer-events:none;background-image:radial-gradient(var(--dot) 1.2px,transparent 1.2px);background-size:28px 28px;opacity:.55;}
a{color:inherit;}
.wrap{max-width:1080px;margin:0 auto;padding:0 24px;}
.col{max-width:720px;margin:0 auto;padding:0 24px;}

header.nav{position:sticky;top:0;z-index:50;background:rgba(245,241,232,.82);backdrop-filter:blur(12px);border-bottom:1px solid var(--line);}
.nav-in{display:flex;align-items:center;justify-content:space-between;height:66px;}
.brand{display:flex;align-items:center;gap:10px;font-family:var(--disp);font-weight:800;font-size:22px;letter-spacing:-.02em;text-decoration:none;}
.brand .lk{display:inline-flex;align-items:baseline;gap:6px;}
.brand .d{color:var(--ink2);font-weight:700;}
.brand .x{color:var(--acc);font-weight:600;font-size:.82em;}
.brand .v{color:var(--ink);font-weight:800;}
.brand svg{width:26px;height:26px;}
.brand svg circle{fill:none;stroke:var(--acc);stroke-width:5;}
.nav-links{display:flex;gap:22px;font-weight:600;font-size:14.5px;}
.nav-links a{text-decoration:none;color:var(--ink2);transition:color .2s;}
.nav-links a:hover{color:var(--acc);}

.kicker{display:inline-flex;align-items:center;gap:9px;font-weight:700;font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--acc);}
.kicker:before{content:"";width:22px;height:2px;background:var(--acc);border-radius:2px;}

footer{border-top:1px solid var(--line);margin-top:70px;}
.foot{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:14px;padding:30px 0;font-size:13.5px;color:var(--soft);}
.foot a{color:var(--ink);font-weight:600;text-decoration:none;}
.foot .ll{display:flex;gap:16px;}

/* ===== INDEX ===== */
.bloghero{padding:clamp(46px,7vw,88px) 0 30px;}
.bloghero h1{font-family:var(--disp);font-weight:800;font-size:clamp(38px,6vw,68px);line-height:1.0;letter-spacing:-.03em;margin:14px 0 16px;}
.bloghero p{font-size:18px;color:var(--ink2);max-width:60ch;}
.grid{display:grid;grid-template-columns:repeat(2,1fr);gap:20px;padding-bottom:30px;}
@media(max-width:760px){.grid{grid-template-columns:1fr;}}
.post{position:relative;overflow:hidden;isolation:isolate;display:flex;flex-direction:column;background:linear-gradient(165deg,#fffdf8 0%,#f6efe1 100%);border:1.5px solid var(--line);border-radius:22px;padding:26px;text-decoration:none;transition:transform .3s,box-shadow .3s,border-color .3s;}
.post:hover{transform:translateY(-5px);box-shadow:0 24px 50px -34px rgba(40,20,8,.35);border-color:var(--acc);}
.post>*{position:relative;z-index:1;}
.post .rings{position:absolute;z-index:0;right:-52px;bottom:-52px;width:200px;height:200px;opacity:.08;pointer-events:none;transition:opacity .45s ease,transform .6s cubic-bezier(.2,.7,.2,1);}
.post .rings circle{fill:none;stroke:var(--acc);stroke-width:2.5;}
.post:hover .rings{opacity:.2;transform:rotate(-24deg) scale(1.07);}
.post .idx{position:absolute;z-index:0;left:16px;bottom:-6px;font-family:var(--disp);font-weight:800;font-size:108px;line-height:1;letter-spacing:-.05em;color:transparent;-webkit-text-stroke:1.5px var(--acc);opacity:.07;pointer-events:none;transition:opacity .45s ease;}
.post:hover .idx{opacity:.15;}
.post .cat{display:inline-flex;align-items:center;gap:7px;font-weight:700;font-size:11.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--acc2);}
.post .cat:before{content:"✦";color:var(--acc);font-size:11px;}
.post h2{font-family:var(--disp);font-weight:700;font-size:23px;line-height:1.12;letter-spacing:-.01em;margin:10px 0 9px;}
.post p{font-size:14.5px;color:var(--ink2);flex:1;}
.post .meta{margin-top:16px;font-size:12.5px;color:var(--soft);font-weight:600;}
.post .cardfoot{display:flex;align-items:center;justify-content:space-between;margin-top:16px;padding-top:14px;border-top:1px solid var(--line);}
.post .cardfoot .meta{margin-top:0;}
.post .rd{display:inline-flex;align-items:center;gap:5px;font-weight:700;font-size:13px;color:var(--acc);}
.post .rd svg{width:15px;height:15px;transition:transform .3s;}
.post:hover .rd svg{transform:translateX(4px);}

/* ===== ARTICLE ===== */
.crumb{padding:26px 0 0;font-size:13px;color:var(--soft);}
.crumb a{color:var(--soft);text-decoration:none;}.crumb a:hover{color:var(--acc);}
article{padding:18px 0 0;}
article h1{font-family:var(--disp);font-weight:800;font-size:clamp(30px,4.6vw,50px);line-height:1.05;letter-spacing:-.025em;margin:14px 0 16px;}
.amETA{display:flex;gap:16px;font-size:13px;color:var(--soft);font-weight:600;border-bottom:1px solid var(--line);padding-bottom:22px;margin-bottom:30px;}
article h2{font-family:var(--disp);font-weight:700;font-size:clamp(22px,3vw,30px);line-height:1.15;letter-spacing:-.01em;margin:38px 0 12px;}
article h3{font-family:var(--disp);font-weight:700;font-size:19px;margin:24px 0 8px;}
article p{font-size:17px;color:#2b2620;margin:0 0 16px;}
article ul,article ol{margin:0 0 18px;padding-left:22px;}
article li{font-size:17px;color:#2b2620;margin:7px 0;}
article strong{color:var(--ink);}
article a.inl{color:var(--acc);font-weight:600;text-decoration:underline;text-underline-offset:2px;}
.lead{font-size:20px!important;color:var(--ink2)!important;}
.callout{background:var(--acc-soft);border-radius:18px;padding:22px 24px;margin:26px 0;}
.callout b{font-family:var(--disp);}
.callout ul{margin:10px 0 0;}
.formula{background:var(--ink);color:#f3ede2;border-radius:16px;padding:20px 24px;margin:22px 0;font-family:'JetBrains Mono',ui-monospace,monospace;font-size:15px;line-height:1.7;overflow-x:auto;}
.formula .v{color:#ffb38a;}
.endcta{background:var(--acc);color:#2a0e02;border-radius:26px;padding:34px;margin:46px 0 0;text-align:center;}
.endcta h3{font-family:var(--disp);font-weight:800;font-size:26px;margin-bottom:8px;}
.endcta p{font-size:15.5px;margin-bottom:18px;opacity:.85;}
.endcta .btn{display:inline-flex;align-items:center;gap:8px;background:var(--ink);color:var(--bg);font-weight:700;padding:13px 26px;border-radius:99px;text-decoration:none;transition:transform .2s;}
.endcta .btn:hover{transform:translateY(-2px);}
.more{margin-top:30px;}
.more .kicker{margin-bottom:14px;}
.more a{display:block;text-decoration:none;border-top:1px solid var(--line);padding:14px 0;font-family:var(--disp);font-weight:700;font-size:18px;color:var(--ink);transition:color .2s;}
.more a:hover{color:var(--acc);}
.more a span{color:var(--soft);font-family:var(--body);font-weight:600;font-size:13px;display:block;}
"""

STYLE += """
.cover{width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:18px;border:1.5px solid var(--line);margin:8px 0 30px;display:block;}
.post .thumb{width:100%;aspect-ratio:3/2;object-fit:cover;border-radius:14px;margin-bottom:16px;display:block;}
.idxhero{width:100%;aspect-ratio:24/9;object-fit:cover;border-radius:22px;border:1.5px solid var(--line);margin-top:26px;display:block;}
.fig{margin:32px 0;background:var(--card);border:1.5px solid var(--line);border-radius:20px;padding:24px 22px 18px;}
.fig svg{width:100%;height:auto;display:block;}
.fig figcaption{font-size:13px;color:var(--soft);margin-top:14px;text-align:center;line-height:1.4;}
"""

RINGS = '<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="46"/><circle cx="50" cy="50" r="30"/><circle cx="50" cy="50" r="14"/></svg>'

def head(title, desc, canonical, extra_ld="", ogimg=""):
    ogtag = f'<meta property="og:image" content="{ogimg}">\n' if ogimg else ''
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="article">
<meta property="og:url" content="{canonical}">
{ogtag}<link rel="canonical" href="{canonical}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,600;12..96,700;12..96,800&family=Hanken+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>{STYLE}</style>
{extra_ld}
</head>"""

NAV = f"""<header class="nav"><div class="wrap nav-in">
<a class="brand" href="/">{RINGS}<span class="lk"><span class="d">Duckwin</span><span class="x">×</span><span class="v">VLOZ</span></span></a>
<nav class="nav-links">
<a href="/blog/">Блог</a>
<a href="/#products">Услуги</a>
<a href="/#contact">Связаться</a>
</nav></div></header>"""

FOOT = f"""<footer><div class="wrap foot">
<div>© 2026 VLOZ · сезонное и авторское меню для кофеен · duckwin.ru</div>
<div class="ll"><a href="https://t.me/kryanton">Telegram</a><a href="https://max.ru/u/f9LHodD0cOIvYeSSomMV090N8qMvxtqD9VBvgUE7WqJQgWUf4hlujvKCu1s">MAX</a><a href="mailto:ad@duckwin.ru">Почта</a></div>
</div></footer>"""

ENDCTA = """<div class="endcta">
<h3>Нужно меню, которое окупается?</h3>
<p>VLOZ собирает сезонные и авторские напитки под ключ — с рецептурами, техкартами и расчётом себестоимости.</p>
<a class="btn" href="vloz.html#products">Смотреть форматы и цены →</a>
</div>"""

# ---------------- articles ----------------
ARTS = [
{
"slug":"kak-sostavit-menyu-kofejni",
"cat":"Меню","kw":"как составить меню кофейни",
"title":"Как составить меню для кофейни: пошаговый гайд 2026 — VLOZ",
"h1":"Как составить меню для кофейни: пошаговый гайд",
"desc":"Пошагово: с чего начать, как собрать структуру меню кофейни, сколько позиций нужно, как посчитать экономику каждой и не уйти в минус.",
"read":"7 мин",
"body":"""
<p class="lead">Меню — это не список напитков, а инструмент продаж. От него зависит средний чек, скорость отдачи и то, вернётся ли гость. Разберём, как собрать его осознанно, а не «как у всех».</p>

<h2>Шаг 1. Начните с концепции и гостя</h2>
<p>Прежде чем придумывать напитки, ответьте на три вопроса: кто ваш гость, зачем он приходит и что у вас за формат. Меню кофейни у бизнес-центра, спешелти-бара и точки в спальном районе — это три разных меню, даже если кофе один и тот же.</p>
<p>Зафиксируйте: средний возраст и привычки гостя, пиковые часы, формат потребления (с собой или в зале), ценовой сегмент. Это рамка, в которой вы дальше принимаете решения.</p>

<h2>Шаг 2. Соберите структуру: ядро, сезон, сигнатура</h2>
<p>Рабочее меню удобно делить на три слоя:</p>
<ul>
<li><strong>Ядро</strong> — классика, которую заказывают всегда: эспрессо, американо, капучино, латте, раф. Это 60–70% продаж, и оно почти не меняется.</li>
<li><strong>Сезонные позиции</strong> — 4–8 напитков, которые вы обновляете под время года. Они создают повод вернуться и оживляют витрину.</li>
<li><strong>Сигнатура</strong> — 1–3 авторских напитка, которые есть только у вас. Они работают на узнаваемость и средний чек.</li>
</ul>
[[DIAGRAM]]

<h2>Шаг 3. Не раздувайте количество позиций</h2>
<p>Частая ошибка новичков — огромное меню. Большой список замедляет выбор, усложняет работу бариста и повышает списания. Для небольшой кофейни обычно достаточно <strong>12–18 напитков</strong> в активном меню. Лучше меньше, но каждый продаётся и считается.</p>

<h2>Шаг 4. Посчитайте экономику каждой позиции</h2>
<p>Каждый напиток в меню должен зарабатывать. До того как поставить позицию в витрину, посчитайте её себестоимость и наценку. Если фудкост напитка выше 25–30%, либо пересмотрите рецептуру, либо поднимите цену. Подробно про расчёт — в отдельной статье про <a class="inl" href="blog-sebestoimost-napitka.html">себестоимость напитка</a>.</p>

<h2>Шаг 5. Оформление и описания</h2>
<p>Название и короткое описание продают напиток сильнее, чем фото. «Тыквенный латте» — это позиция. «Тыквенный латте на топлёном молоке с корицей» — это уже история, за которую платят охотнее. Группируйте логично, выделяйте новинки, не прячьте маржинальные позиции в конец.</p>

<div class="callout"><b>Коротко — что должно получиться:</b>
<ul>
<li>понятная концепция и портрет гостя;</li>
<li>3 слоя: ядро + сезон + сигнатура;</li>
<li>12–18 активных позиций, не больше;</li>
<li>посчитанная себестоимость по каждой;</li>
<li>описания, которые продают.</li>
</ul></div>

<h2>Частые ошибки</h2>
<ul>
<li>Копировать меню у соседа — вы получаете те же напитки без уникальности.</li>
<li>Ставить позиции «на вкус», без расчёта себестоимости.</li>
<li>Не обновлять меню месяцами — гостю нет повода возвращаться.</li>
<li>Зависеть от одного бариста, который держит рецепты в голове, а не в техкартах.</li>
</ul>
"""
},
{
"slug":"sebestoimost-napitka",
"cat":"Экономика","kw":"себестоимость напитка кофейня",
"title":"Как рассчитать себестоимость напитка в кофейне (формула + пример) — VLOZ",
"h1":"Как рассчитать себестоимость напитка в кофейне",
"desc":"Формула себестоимости напитка, разбор на примере капучино с цифрами, нормальный фудкост и как не уйти в минус на сезонных позициях.",
"read":"6 мин",
"body":"""
<p class="lead">Если себестоимость не посчитана, вы не управляете прибылью — вы угадываете. Разберём по шагам, как считать, и сделаем расчёт на реальном примере.</p>

<h2>Что входит в себестоимость напитка</h2>
<p>Себестоимость (фудкост) — это стоимость продуктов в одной порции. В неё входят:</p>
<ul>
<li>кофе (зерно на порцию);</li>
<li>молоко или альтернатива;</li>
<li>сиропы, топпинги, специи;</li>
<li>стакан, крышка, трубочка, если «с собой».</li>
</ul>
<p>Аренда, зарплаты и оборудование — это уже операционные расходы, в фудкост они не входят, но их закрывает наценка.</p>

<h2>Формула</h2>
<div class="formula">Себестоимость порции = сумма (расход ингредиента × цена за грамм/мл)<br>
Фудкост, % = <span class="v">Себестоимость ÷ Цена продажи × 100</span><br>
Наценка, % = <span class="v">(Цена − Себестоимость) ÷ Себестоимость × 100</span></div>

<h2>Пример: капучино 250 мл</h2>
<p>Допустим, цены такие: зерно 1 800 ₽/кг (1,8 ₽/г), молоко 80 ₽/л (0,08 ₽/мл), стакан с крышкой 9 ₽.</p>
<ul>
<li>Зерно: 18 г × 1,8 ₽ = <strong>32,4 ₽</strong></li>
<li>Молоко: 150 мл × 0,08 ₽ = <strong>12 ₽</strong></li>
<li>Стакан с крышкой: <strong>9 ₽</strong></li>
</ul>
<p>Итого себестоимость ≈ <strong>53,4 ₽</strong>. При цене продажи 220 ₽ фудкост = 53,4 ÷ 220 × 100 ≈ <strong>24%</strong> — это здоровый показатель.</p>
[[DIAGRAM]]

<h2>Какой фудкост считается нормальным</h2>
<p>Ориентир для напитков — <strong>20–30%</strong>. Ниже 20% — отлично, выше 30% — позиция съедает прибыль, и её нужно либо переработать, либо поднять в цене. У сезонных и авторских напитков фудкост часто выше из-за дорогих ингредиентов — это нормально, если цена продажи учитывает наценку.</p>

<div class="callout"><b>Почему сезонные напитки уходят в минус:</b> топпинги, сиропы и редкие ингредиенты считают «на глаз», а порцию наливают щедро. Зафиксируйте граммовки в техкарте и пересчитайте цену — иначе хит по продажам может работать в убыток.</div>

<h2>Чем считать</h2>
<p>На старте достаточно таблицы в Excel или Google Sheets: ингредиенты, расход, цена за единицу, автоподсчёт себестоимости и фудкоста. Главное — обновлять цены закупки, потому что себестоимость плавает вместе с рынком.</p>
"""
},
{
"slug":"sezonnoe-menyu",
"cat":"Меню","kw":"сезонное меню кофейни",
"title":"Сезонное меню для кофейни: зачем нужно и как обновлять — VLOZ",
"h1":"Сезонное меню для кофейни: зачем и как обновлять",
"desc":"Почему сезонность повышает выручку, календарь обновлений на 4 сезона, что менять и что оставлять, как тестировать новинки.",
"read":"5 мин",
"body":"""
<p class="lead">Сезонное меню — это не дань моде, а механика повторных визитов. Новинки дают гостю повод вернуться, а вам — поднять средний чек без скидок.</p>

<h2>Почему сезонность продаёт</h2>
<p>Гость, который пьёт один и тот же латте, ходит по привычке. Гость, который ждёт «а что нового в этом сезоне», ходит за впечатлением — и тратит больше. Сезонные напитки также отлично работают в соцсетях: новинка — это инфоповод, классика — нет.</p>

<h2>Календарь на 4 сезона</h2>
<ul>
<li><strong>Весна</strong> — лёгкие, цветочные и ягодные профили, матча, первые холодные напитки.</li>
<li><strong>Лето</strong> — холодная линейка: колд брю, тоники, лимонады, фраппе. Это пик спроса на «освежающее».</li>
<li><strong>Осень</strong> — пряные и согревающие: тыква, груша, корица, карамель. Самый «продающий» сезон новинок.</li>
<li><strong>Зима</strong> — десертные и согревающие: какао, пряный латте, имбирь, цитрус.</li>
</ul>
[[DIAGRAM]]
<p>Оптимальная частота — 4 обновления в год, по числу сезонов. Можно добавить точечные новинки под праздники.</p>

<h2>Что менять, а что оставлять</h2>
<p>Не трогайте ядро меню — классику, которая даёт основную выручку. Меняйте только сезонный слой: 4–8 позиций. Так вы освежаете витрину, не ломая привычки постоянных гостей и не перегружая бариста.</p>

<h2>Как тестировать новинки</h2>
<p>Запускайте сезонную линейку небольшим набором, отслеживайте продажи первые 1–2 недели и оставляйте лидеров. Слабые позиции убирайте без сожаления. Считайте себестоимость заранее — щедрая порция сиропа способна превратить хит в убыточную позицию.</p>

<div class="callout"><b>Главное:</b> ядро не трогаем, сезон обновляем 4 раза в год набором из 4–8 позиций, каждую считаем по себестоимости и оставляем только то, что продаётся.</div>
"""
},
{
"slug":"avtorskie-napitki-idei",
"cat":"Идеи","kw":"авторские напитки для кофейни идеи",
"title":"Идеи авторских напитков для кофейни по сезонам — VLOZ",
"h1":"Идеи авторских напитков для кофейни по сезонам",
"desc":"Что делает напиток авторским, концепты под весну, лето, осень и зиму, как адаптировать идею под себестоимость и придумать название.",
"read":"6 мин",
"body":"""
<p class="lead">Авторский напиток — это то, за чем приходят именно к вам. Ниже — направления для идей по сезонам и принцип, как превратить идею в рабочую позицию меню.</p>

<h2>Что делает напиток авторским</h2>
<p>Не экзотика ради экзотики, а узнаваемое сочетание, которое сложно скопировать из меню: связка вкуса, подачи и названия. Авторский напиток должен быть воспроизводим на вашем оборудовании и укладываться в адекватную себестоимость.</p>

<h2>Весна</h2>
<ul>
<li>матча-латте с цветочным сиропом (бузина, лаванда);</li>
<li>раф на ягодном пюре;</li>
<li>эспрессо-тоник с цитрусом — первый «холодный» напиток сезона.</li>
</ul>

<h2>Лето</h2>
<ul>
<li>колд брю с тоником и сезонными ягодами;</li>
<li>кофейный лимонад на эспрессо;</li>
<li>фраппе на растительном молоке.</li>
</ul>

<h2>Осень</h2>
<ul>
<li>тыквенный латте на топлёном молоке с корицей;</li>
<li>грушевый раф с карамелью;</li>
<li>пряный какао с имбирём.</li>
</ul>

<h2>Зима</h2>
<ul>
<li>цитрусовый согревающий напиток с пряностями;</li>
<li>десертный латте (печёное яблоко, халва, миндаль);</li>
<li>горячий шоколад на тёмном шоколаде с солью.</li>
</ul>

<h2>Как адаптировать под себестоимость</h2>
<p>Любую идею проверяйте калькулятором: посчитайте <a class="inl" href="blog-sebestoimost-napitka.html">себестоимость</a> и держите фудкост в пределах 25–30%. Дорогой ингредиент можно оставить, но тогда корректно отразите его в цене.</p>

<h2>Нейминг</h2>
<p>Название должно подсказывать вкус и вызывать желание попробовать. Сравните: «напиток №3» против «грушевый раф с солёной карамелью». Второй продаёт сам себя.</p>
"""
},
{
"slug":"tehnologicheskaya-karta",
"cat":"Документы","kw":"технологическая карта на напиток",
"title":"Технологическая карта на напиток: что это и как составить (шаблон) — VLOZ",
"h1":"Технологическая карта на напиток: что это и как составить",
"desc":"Зачем нужна ТТК на напиток, что в ней должно быть, чем отличается от рецепта, готовый шаблон и как внедрить в смену.",
"read":"5 мин",
"body":"""
<p class="lead">Технологическая карта (ТТК) — это стандарт, по которому любой бариста повторит напиток одинаково. Без неё качество плавает от смены к смене, а рецепты уходят вместе с сотрудником.</p>

<h2>Зачем нужна техкарта</h2>
<ul>
<li>стабильный вкус независимо от того, кто за стойкой;</li>
<li>контроль себестоимости — точные граммовки вместо «на глаз»;</li>
<li>быстрое обучение новых бариста;</li>
<li>рецепт остаётся у заведения, а не в голове одного человека.</li>
</ul>

<h2>Что должно быть в карте</h2>
<ul>
<li>название напитка и объём порции;</li>
<li>список ингредиентов с точными граммовками/миллилитрами;</li>
<li>последовательность приготовления по шагам;</li>
<li>температуры и параметры (экстракция, взбивание молока);</li>
<li>посуда и подача;</li>
<li>себестоимость и цена продажи.</li>
</ul>
[[DIAGRAM]]

<h2>Шаблон</h2>
<div class="formula">НАПИТОК: Грушевый раф · 300 мл<br>
ИНГРЕДИЕНТЫ:<br>
— эспрессо <span class="v">18 г / 36 мл</span><br>
— сливки 11% <span class="v">150 мл</span><br>
— грушевое пюре <span class="v">30 г</span><br>
— сахар/сироп <span class="v">10 г</span><br>
ПРИГОТОВЛЕНИЕ: 1) сварить эспрессо 2) прогреть и взбить сливки с пюре и сиропом 3) соединить, подать в стекле<br>
СЕБЕСТОИМОСТЬ: <span class="v">61 ₽</span> · ЦЕНА: <span class="v">260 ₽</span> · ФУДКОСТ: <span class="v">23%</span></div>

<h2>Чем ТТК отличается от рецепта</h2>
<p>Рецепт отвечает на вопрос «что положить», техкарта — «как стабильно повторить и сколько это стоит». Рецепт — для дома, техкарта — для бизнеса.</p>

<h2>Как внедрить в смену</h2>
<p>Соберите карты в одну папку (бумажную или в облаке), проведите прогон с командой и сделайте их обязательным стандартом. Обновляйте при смене поставщика или цен — иначе себестоимость в карте перестанет соответствовать реальности.</p>
"""
},
{
"slug":"srednij-chek-kofejni",
"cat":"Экономика","kw":"как увеличить средний чек кофейни",
"title":"Как поднять средний чек в кофейне через меню — VLOZ",
"h1":"Как поднять средний чек в кофейне через меню",
"desc":"Рабочие способы увеличить средний чек кофейни: допродажи, апгрейды, сигнатура как якорь, психология цен и сезонные новинки.",
"read":"6 мин",
"body":"""
<p class="lead">Поднять средний чек можно без агрессивных скидок и роста трафика — за счёт грамотно собранного меню и простых допродаж. Вот что работает.</p>

<h2>Что вообще влияет на чек</h2>
<p>Средний чек растёт двумя путями: гость берёт более дорогую позицию или добавляет к заказу что-то ещё. Меню должно мягко подталкивать к обоим сценариям.</p>
[[DIAGRAM]]

<h2>Допродажи через меню</h2>
<ul>
<li><strong>Апгрейд молока и объёма:</strong> альтернативное молоко, увеличенный размер — небольшая доплата, высокая маржа.</li>
<li><strong>Сиропы и топпинги:</strong> предлагаются как осознанная опция, а не прячутся.</li>
<li><strong>Фуд-пейринг:</strong> к напитку — десерт или выпечка. Связка «кофе + к нему» заметно поднимает чек.</li>
</ul>

<h2>Сигнатура как якорь</h2>
<p>Авторский напиток с более высокой ценой делает остальное меню «доступным» на контрасте и одновременно сам приносит хорошую маржу. Один-два таких якоря меняют восприятие всего прайса.</p>

<h2>Психология меню</h2>
<ul>
<li>не выстраивайте позиции строго по росту цены — выделяйте маржинальные;</li>
<li>используйте описания, которые оправдывают цену;</li>
<li>не ставьте «₽» навязчиво и не делайте прайс пугающим столбиком.</li>
</ul>

<h2>Сезонные новинки как повод</h2>
<p>Новинка — это законный повод заплатить больше: гость пробует что-то новое и не сравнивает напрямую с привычным латте. Поэтому <a class="inl" href="blog-sezonnoe-menyu.html">сезонное меню</a> — один из самых мягких способов поднять чек.</p>

<div class="callout"><b>Быстрый чек-лист:</b>
<ul>
<li>есть апгрейды (молоко, объём, сиропы);</li>
<li>есть фуд-пейринг к напиткам;</li>
<li>есть 1–2 сигнатуры-якоря;</li>
<li>описания оправдывают цену;</li>
<li>раз в сезон — новинки как повод.</li>
</ul></div>
"""
},
]

# ---------------- inline SVG diagrams ----------------
DIAGRAMS = {
"kak-sostavit-menyu-kofejni": """<figure class="fig"><svg viewBox="0 0 720 470" xmlns="http://www.w3.org/2000/svg" font-family="Hanken Grotesk, sans-serif">
<circle cx="215" cy="235" r="178" fill="#fffdf8" stroke="#e6dcc9" stroke-width="1.5"/>
<circle cx="215" cy="235" r="128" fill="rgba(33,86,79,.12)" stroke="#e6dcc9" stroke-width="1.5"/>
<circle cx="215" cy="235" r="74" fill="#ffe2d3" stroke="#ff5a1f" stroke-width="2"/>
<text x="215" y="90" text-anchor="middle" font-weight="700" font-size="14" fill="#21564f" font-family="Bricolage Grotesque, sans-serif" letter-spacing="1.5">СИГНАТУРА</text>
<text x="215" y="148" text-anchor="middle" font-weight="700" font-size="14" fill="#21564f" font-family="Bricolage Grotesque, sans-serif" letter-spacing="1.5">СЕЗОН</text>
<text x="215" y="232" text-anchor="middle" font-weight="800" font-size="24" fill="#171310" font-family="Bricolage Grotesque, sans-serif">ЯДРО</text>
<text x="215" y="254" text-anchor="middle" font-size="12" fill="#857a6a">60–70% продаж</text>
<g transform="translate(440,128)">
<rect x="0" y="-14" width="18" height="18" rx="5" fill="#ffe2d3" stroke="#ff5a1f" stroke-width="2"/>
<text x="30" y="0" font-weight="700" font-size="17" fill="#171310" font-family="Bricolage Grotesque, sans-serif">Ядро</text>
<text x="30" y="22" font-size="13.5" fill="#4c453b">Классика: эспрессо, латте, раф.</text>
<text x="30" y="40" font-size="13.5" fill="#857a6a">Почти не меняется.</text></g>
<g transform="translate(440,228)">
<rect x="0" y="-14" width="18" height="18" rx="5" fill="rgba(33,86,79,.16)" stroke="#21564f" stroke-width="2"/>
<text x="30" y="0" font-weight="700" font-size="17" fill="#171310" font-family="Bricolage Grotesque, sans-serif">Сезон</text>
<text x="30" y="22" font-size="13.5" fill="#4c453b">4–8 позиций, обновляем раз в сезон.</text>
<text x="30" y="40" font-size="13.5" fill="#857a6a">Повод вернуться.</text></g>
<g transform="translate(440,328)">
<rect x="0" y="-14" width="18" height="18" rx="5" fill="#fffdf8" stroke="#e6dcc9" stroke-width="2"/>
<text x="30" y="0" font-weight="700" font-size="17" fill="#171310" font-family="Bricolage Grotesque, sans-serif">Сигнатура</text>
<text x="30" y="22" font-size="13.5" fill="#4c453b">1–3 авторских напитка.</text>
<text x="30" y="40" font-size="13.5" fill="#857a6a">Уникальность — только у вас.</text></g>
</svg><figcaption>Структура меню: ядро держит выручку, сезон даёт повод вернуться, сигнатура — уникальность.</figcaption></figure>""",

"sebestoimost-napitka": """<figure class="fig"><svg viewBox="0 0 720 360" xmlns="http://www.w3.org/2000/svg" font-family="Hanken Grotesk, sans-serif">
<text x="40" y="60" font-size="13.5" font-weight="700" fill="#171310">Цена продажи — 220 ₽</text>
<rect x="40" y="72" width="430" height="42" rx="10" fill="#ffe2d3"/>
<text x="40" y="150" font-size="13.5" font-weight="700" fill="#171310">Себестоимость — 53,4 ₽</text>
<rect x="40" y="162" width="63" height="42" fill="#ff5a1f"/>
<rect x="103" y="162" width="23" height="42" fill="#21564f"/>
<rect x="126" y="162" width="18" height="42" fill="#857a6a"/>
<rect x="40" y="162" width="104" height="42" rx="10" fill="none" stroke="#171310" stroke-width="1" opacity="0"/>
<g font-size="13" fill="#4c453b" transform="translate(40,250)">
<rect x="0" y="-11" width="14" height="14" rx="4" fill="#ff5a1f"/><text x="22" y="0">зерно 32,4 ₽</text>
<rect x="150" y="-11" width="14" height="14" rx="4" fill="#21564f"/><text x="172" y="0">молоко 12 ₽</text>
<rect x="300" y="-11" width="14" height="14" rx="4" fill="#857a6a"/><text x="322" y="0">стакан 9 ₽</text></g>
<text x="40" y="312" font-size="14" fill="#857a6a" font-family="JetBrains Mono, monospace">53,4 ₽ ÷ 220 ₽ × 100 = 24%</text>
<circle cx="600" cy="150" r="66" fill="none" stroke="#e6dcc9" stroke-width="20"/>
<circle cx="600" cy="150" r="66" fill="none" stroke="#ff5a1f" stroke-width="20" stroke-linecap="round" stroke-dasharray="99.5 315.2" transform="rotate(-90 600 150)"/>
<text x="600" y="146" text-anchor="middle" font-weight="800" font-size="30" fill="#171310" font-family="Bricolage Grotesque, sans-serif">24%</text>
<text x="600" y="168" text-anchor="middle" font-size="12" fill="#857a6a">фудкост</text>
<text x="600" y="252" text-anchor="middle" font-size="12.5" fill="#21564f" font-weight="700">норма 20–30%</text>
</svg><figcaption>Себестоимость капучино — 53,4 ₽ при цене 220 ₽: фудкост 24%, здоровая зона.</figcaption></figure>""",

"sezonnoe-menyu": """<figure class="fig"><svg viewBox="0 0 720 420" xmlns="http://www.w3.org/2000/svg" font-family="Hanken Grotesk, sans-serif">
<path d="M230 210 L230 60 A150 150 0 0 1 380 210 Z" fill="rgba(242,160,12,.18)" stroke="#fffdf8" stroke-width="3"/>
<path d="M230 210 L380 210 A150 150 0 0 1 230 360 Z" fill="rgba(255,90,31,.16)" stroke="#fffdf8" stroke-width="3"/>
<path d="M230 210 L230 360 A150 150 0 0 1 80 210 Z" fill="rgba(47,108,240,.15)" stroke="#fffdf8" stroke-width="3"/>
<path d="M230 210 L80 210 A150 150 0 0 1 230 60 Z" fill="rgba(27,163,91,.16)" stroke="#fffdf8" stroke-width="3"/>
<text x="293" y="150" text-anchor="middle" font-weight="700" font-size="15" fill="#b9780a" font-family="Bricolage Grotesque, sans-serif">Лето</text>
<text x="293" y="278" text-anchor="middle" font-weight="700" font-size="15" fill="#ff5a1f" font-family="Bricolage Grotesque, sans-serif">Осень</text>
<text x="166" y="278" text-anchor="middle" font-weight="700" font-size="15" fill="#2f6cf0" font-family="Bricolage Grotesque, sans-serif">Зима</text>
<text x="166" y="150" text-anchor="middle" font-weight="700" font-size="15" fill="#1ba35b" font-family="Bricolage Grotesque, sans-serif">Весна</text>
<circle cx="230" cy="210" r="52" fill="#fffdf8" stroke="#e6dcc9" stroke-width="1.5"/>
<text x="230" y="205" text-anchor="middle" font-weight="800" font-size="18" fill="#171310" font-family="Bricolage Grotesque, sans-serif">4×</text>
<text x="230" y="224" text-anchor="middle" font-size="10.5" fill="#857a6a">в год</text>
<g font-family="Hanken Grotesk, sans-serif">
<g transform="translate(440,118)"><circle cx="6" cy="-4" r="6" fill="#1ba35b"/><text x="22" y="0" font-weight="700" font-size="15" fill="#171310">Весна</text><text x="22" y="20" font-size="13" fill="#857a6a">цветочное, ягодное, матча</text></g>
<g transform="translate(440,188)"><circle cx="6" cy="-4" r="6" fill="#f2a00c"/><text x="22" y="0" font-weight="700" font-size="15" fill="#171310">Лето</text><text x="22" y="20" font-size="13" fill="#857a6a">колд брю, тоники, фраппе</text></g>
<g transform="translate(440,258)"><circle cx="6" cy="-4" r="6" fill="#ff5a1f"/><text x="22" y="0" font-weight="700" font-size="15" fill="#171310">Осень</text><text x="22" y="20" font-size="13" fill="#857a6a">тыква, корица, карамель</text></g>
<g transform="translate(440,328)"><circle cx="6" cy="-4" r="6" fill="#2f6cf0"/><text x="22" y="0" font-weight="700" font-size="15" fill="#171310">Зима</text><text x="22" y="20" font-size="13" fill="#857a6a">какао, имбирь, цитрус</text></g>
</g></svg><figcaption>Сезонный круг: 4 обновления в год под вкусовые профили каждого сезона.</figcaption></figure>""",

"srednij-chek-kofejni": """<figure class="fig"><svg viewBox="0 0 720 340" xmlns="http://www.w3.org/2000/svg" font-family="Hanken Grotesk, sans-serif">
<line x1="70" y1="290" x2="700" y2="290" stroke="#e6dcc9" stroke-width="1.5"/>
<text x="58" y="180" font-size="12" fill="#857a6a" transform="rotate(-90 58 180)" text-anchor="middle">средний чек</text>
<rect x="120" y="190" width="78" height="100" rx="8" fill="#857a6a"/>
<rect x="285" y="150" width="78" height="140" rx="8" fill="#8aa9a4"/>
<rect x="450" y="110" width="78" height="180" rx="8" fill="#21564f"/>
<rect x="615" y="65" width="78" height="225" rx="8" fill="#ff5a1f"/>
<polyline points="159,190 324,150 489,110 654,65" fill="none" stroke="#171310" stroke-width="2" stroke-dasharray="4 5"/>
<path d="M654 65 l-9 2 l5 8 z" fill="#171310"/>
<g font-size="13" font-weight="700" fill="#171310" text-anchor="middle" font-family="Bricolage Grotesque, sans-serif">
<text x="159" y="312">База</text><text x="324" y="312">+Апгрейды</text><text x="489" y="312">+Пейринг</text><text x="654" y="312">+Сигнатура</text></g>
</svg><figcaption>Каждый рычаг меню — плюс к среднему чеку, без роста трафика.</figcaption></figure>""",
"tehnologicheskaya-karta": """<figure class="fig"><svg viewBox="0 0 720 452" xmlns="http://www.w3.org/2000/svg" font-family="Hanken Grotesk, sans-serif">
<rect x="60" y="20" width="600" height="416" rx="18" fill="#fffdf8" stroke="#e6dcc9" stroke-width="1.5"/>
<path d="M60 38 a18 18 0 0 1 18 -18 h564 a18 18 0 0 1 18 18 v46 h-600 z" fill="#ff5a1f"/>
<text x="84" y="59" font-size="20" font-weight="800" fill="#fff" font-family="Bricolage Grotesque, sans-serif">ГРУШЕВЫЙ РАФ</text>
<text x="636" y="59" text-anchor="end" font-size="15" font-weight="700" fill="#fff">300 мл</text>
<text x="84" y="118" font-size="12" font-weight="700" letter-spacing="1.2" fill="#21564f">ИНГРЕДИЕНТЫ</text>
<text x="96" y="146" font-size="14.5" fill="#2b2620">Эспрессо</text><text x="636" y="146" text-anchor="end" font-size="14.5" font-weight="700" fill="#ff5a1f">18 г / 36 мл</text>
<text x="96" y="173" font-size="14.5" fill="#2b2620">Сливки 11%</text><text x="636" y="173" text-anchor="end" font-size="14.5" font-weight="700" fill="#ff5a1f">150 мл</text>
<text x="96" y="200" font-size="14.5" fill="#2b2620">Грушевое пюре</text><text x="636" y="200" text-anchor="end" font-size="14.5" font-weight="700" fill="#ff5a1f">30 г</text>
<line x1="84" y1="222" x2="636" y2="222" stroke="#e6dcc9" stroke-width="1.5"/>
<text x="84" y="250" font-size="12" font-weight="700" letter-spacing="1.2" fill="#21564f">ПРИГОТОВЛЕНИЕ</text>
<circle cx="95" cy="278" r="11" fill="#ffe2d3" stroke="#ff5a1f" stroke-width="1.5"/><text x="95" y="282" text-anchor="middle" font-size="12" font-weight="700" fill="#ff5a1f">1</text><text x="118" y="282" font-size="14.5" fill="#2b2620">Сварить эспрессо</text>
<circle cx="95" cy="308" r="11" fill="#ffe2d3" stroke="#ff5a1f" stroke-width="1.5"/><text x="95" y="312" text-anchor="middle" font-size="12" font-weight="700" fill="#ff5a1f">2</text><text x="118" y="312" font-size="14.5" fill="#2b2620">Прогреть и взбить сливки с пюре и сиропом</text>
<circle cx="95" cy="338" r="11" fill="#ffe2d3" stroke="#ff5a1f" stroke-width="1.5"/><text x="95" y="342" text-anchor="middle" font-size="12" font-weight="700" fill="#ff5a1f">3</text><text x="118" y="342" font-size="14.5" fill="#2b2620">Соединить, подать в стекле</text>
<line x1="84" y1="362" x2="636" y2="362" stroke="#e6dcc9" stroke-width="1.5"/>
<rect x="84" y="378" width="172" height="46" rx="10" fill="rgba(33,86,79,.12)"/>
<text x="98" y="397" font-size="11.5" fill="#857a6a">Себестоимость</text><text x="98" y="416" font-size="16" font-weight="800" fill="#171310" font-family="Bricolage Grotesque, sans-serif">61 ₽</text>
<rect x="274" y="378" width="172" height="46" rx="10" fill="rgba(33,86,79,.12)"/>
<text x="288" y="397" font-size="11.5" fill="#857a6a">Цена</text><text x="288" y="416" font-size="16" font-weight="800" fill="#171310" font-family="Bricolage Grotesque, sans-serif">260 ₽</text>
<rect x="464" y="378" width="172" height="46" rx="10" fill="#ffe2d3"/>
<text x="478" y="397" font-size="11.5" fill="#857a6a">Фудкост</text><text x="478" y="416" font-size="16" font-weight="800" fill="#ff5a1f" font-family="Bricolage Grotesque, sans-serif">23%</text>
</svg><figcaption>Технологическая карта: название и объём, ингредиенты с граммовками, шаги, себестоимость и цена — всё на одном листе.</figcaption></figure>""",
}

# ---------------- render articles ----------------
bySlug = {a["slug"]: a for a in ARTS}
def url(slug): return f"{SITE}/blog/{slug}/"

for i, a in enumerate(ARTS):
    canonical = url(a["slug"])
    ld = {"@context":"https://schema.org","@graph":[
        {"@type":"Article","headline":a["h1"],"description":a["desc"],
         "inLanguage":"ru-RU","author":{"@type":"Person","name":"Антон Кряквин"},
         "publisher":{"@type":"Organization","name":"VLOZ","url":SITE},
         "mainEntityOfPage":canonical,"keywords":a["kw"]},
        {"@type":"BreadcrumbList","itemListElement":[
            {"@type":"ListItem","position":1,"name":"Главная","item":SITE},
            {"@type":"ListItem","position":2,"name":"Блог","item":f"{SITE}/blog/"},
            {"@type":"ListItem","position":3,"name":a["h1"],"item":canonical}]}
    ]}
    ldtag = '<script type="application/ld+json">\n'+json.dumps(ld,ensure_ascii=False,indent=1)+'\n</script>'
    # cover images
    cover = proc(IMG[a["slug"]], 1100, 82, save=f'cover-{a["slug"]}.jpg')
    THUMB[a["slug"]] = proc(IMG[a["slug"]], 680, 80)
    ogimg = f'{SITE}/blog/cover-{a["slug"]}.jpg'
    # related = next two
    rel = [ARTS[(i+1)%len(ARTS)], ARTS[(i+2)%len(ARTS)]]
    more = '<div class="more"><span class="kicker">Читать дальше</span>'
    for r in rel:
        more += f'<a href="blog-{r["slug"]}.html">{r["h1"]}<span>{r["cat"]} · {r["read"]}</span></a>'
    more += '</div>'

    body = a["body"].replace("[[DIAGRAM]]", DIAGRAMS.get(a["slug"], ""))
    html = head(a["title"], a["desc"], canonical, ldtag, ogimg) + f"""
<body>
{NAV}
<div class="col crumb"><a href="blog.html">Блог</a> → {a["cat"]}</div>
<main class="col">
<article>
<span class="kicker">{a["cat"]}</span>
<h1>{a["h1"]}</h1>
<div class="amETA"><span>{a["read"]} чтения</span><span>Автор: Антон Кряквин</span></div>
<img class="cover" src="{cover}" alt="{a['h1']}" loading="lazy">
{body}
{ENDCTA}
{more}
</article>
</main>
{FOOT}
</body>
</html>"""
    open(OUT+f'blog-{a["slug"]}.html','w',encoding='utf-8').write(html)
    print('article:', a["slug"])

# ---------------- render index ----------------
cards = ""
for n, a in enumerate(ARTS, 1):
    cards += f'''<a class="post" href="blog-{a["slug"]}.html">
<span class="idx" aria-hidden="true">{n:02d}</span>
<svg class="rings" viewBox="0 0 100 100" aria-hidden="true"><circle cx="50" cy="50" r="46"/><circle cx="50" cy="50" r="33"/><circle cx="50" cy="50" r="20"/><circle cx="50" cy="50" r="7"/></svg>
<img class="thumb" src="{THUMB[a["slug"]]}" alt="{a["h1"]}" loading="lazy">
<span class="cat">{a["cat"]}</span>
<h2>{a["h1"]}</h2>
<p>{a["desc"]}</p>
<div class="cardfoot"><span class="meta">{a["read"]} чтения</span><span class="rd">Читать<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span></div>
</a>'''

idx_ld = {"@context":"https://schema.org","@type":"Blog","name":"Блог VLOZ","url":f"{SITE}/blog/",
          "description":"Статьи о создании меню для кофеен: рецептуры, себестоимость, сезонность, авторские напитки.",
          "blogPost":[{"@type":"BlogPosting","headline":a["h1"],"url":url(a["slug"]),"keywords":a["kw"]} for a in ARTS]}
idx_ldtag = '<script type="application/ld+json">\n'+json.dumps(idx_ld,ensure_ascii=False,indent=1)+'\n</script>'
idxhero = proc('1780253743.png', 1500, 82, save='cover-blog.jpg')

index = head("Блог VLOZ — про меню, себестоимость и напитки для кофеен",
             "Практичные статьи о создании меню для кофейни: как составить меню, посчитать себестоимость напитка, собрать сезонную линейку и поднять средний чек.",
             f"{SITE}/blog/", idx_ldtag, f"{SITE}/blog/cover-blog.jpg") + f"""
<body>
{NAV}
<section class="bloghero"><div class="wrap">
<span class="kicker">Блог</span>
<h1>Про меню, себестоимость<br>и напитки для кофеен</h1>
<p>Практичные разборы для владельцев и управляющих кофеен — как собрать меню, которое продаёт и считается. Без воды.</p>
<img class="idxhero" src="{idxhero}" alt="Напитки специальной обжарки на светлой стойке — блог VLOZ" loading="lazy">
</div></section>
<div class="wrap"><div class="grid">
{cards}
</div></div>
{FOOT}
</body>
</html>"""
open(OUT+'blog.html','w',encoding='utf-8').write(index)
print('index: blog.html')

# sitemap with all blog URLs
urls = [f"{SITE}/", f"{SITE}/blog/"] + [url(a["slug"]) for a in ARTS]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for u in urls:
    sm += f'  <url><loc>{u}</loc><lastmod>2026-05-31</lastmod><changefreq>monthly</changefreq><priority>{"1.0" if u==SITE+"/" else "0.8"}</priority></url>\n'
sm += '</urlset>\n'
open(OUT+'sitemap.xml','w',encoding='utf-8').write(sm)
print('sitemap: %d urls' % len(urls))
print('done')
