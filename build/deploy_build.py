# -*- coding: utf-8 -*-
import os, re, shutil, base64
from PIL import Image
import os
ROOT   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets") + os.sep
BUILD  = os.path.join(ROOT, ".build") + os.sep
DISTD  = os.path.join(ROOT, "dist") + os.sep
os.makedirs(BUILD, exist_ok=True)


OUT  = BUILD
UP   = ASSETS
DIST = DISTD
SITE = 'https://duckwin.ru'
slugs = ['kak-sostavit-menyu-kofejni','sebestoimost-napitka','sezonnoe-menyu',
         'avtorskie-napitki-idei','tehnologicheskaya-karta','srednij-chek-kofejni']

FAV = '<link rel="icon" href="/favicon.svg" type="image/svg+xml">'
FAVSVG = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
          '<rect width="100" height="100" rx="22" fill="#f5f1e8"/>'
          '<g fill="none" stroke="#ff5a1f" stroke-width="6">'
          '<circle cx="50" cy="50" r="34"/><circle cx="50" cy="50" r="20"/><circle cx="50" cy="50" r="7"/>'
          '</g></svg>')

def jpeg_uris(h):
    return re.findall(r'data:image/jpeg;base64,[A-Za-z0-9+/=]+', h)

def writebytes(path, datauri):
    open(path,'wb').write(base64.b64decode(datauri.split(',',1)[1]))

def blog_links(h):
    h = h.replace('href="vloz.html#products"','href="/#products"')
    h = h.replace('href="vloz.html#contact"','href="/#contact"')
    h = h.replace('href="blog.html"','href="/blog/"')
    h = re.sub(r'href="blog-([a-z0-9-]+)\.html"', r'href="/blog/\1/"', h)
    return h

# fresh dist
shutil.rmtree(DIST, ignore_errors=True)
os.makedirs(DIST+'img', exist_ok=True)
os.makedirs(DIST+'blog', exist_ok=True)
for s in slugs:
    os.makedirs(DIST+'blog/'+s, exist_ok=True)

# ---- main landing ----
h = open(OUT+'vloz.html',encoding='utf-8').read()
u = jpeg_uris(h)
assert len(u) == 2, ('main jpeg count', len(u))
writebytes(DIST+'img/hero.jpg', u[0])
writebytes(DIST+'img/about.jpg', u[1])
h = h.replace(u[0],'/img/hero.jpg').replace(u[1],'/img/about.jpg')
h = h.replace('href="blog.html"','href="/blog/"')
h = h.replace('</head>', FAV+'\n</head>', 1)
open(DIST+'index.html','w',encoding='utf-8').write(h)
print('index.html', len(h)//1024,'KB  (был ~285KB)')

# ---- blog index ----
h = open(OUT+'blog.html',encoding='utf-8').read()
u = jpeg_uris(h)
assert len(u) == 1+len(slugs), ('blog index jpeg count', len(u))
h = h.replace(u[0],'/blog/cover-blog.jpg')
for i,s in enumerate(slugs):
    h = h.replace(u[1+i], f'/blog/cover-{s}.jpg')
h = blog_links(h)
h = h.replace('</head>', FAV+'\n</head>', 1)
open(DIST+'blog/index.html','w',encoding='utf-8').write(h)
print('blog/index.html', len(h)//1024,'KB')

# ---- articles ----
for s in slugs:
    h = open(OUT+f'blog-{s}.html',encoding='utf-8').read()
    u = jpeg_uris(h)
    if u: h = h.replace(u[0], f'/blog/cover-{s}.jpg')
    h = blog_links(h)
    h = h.replace('</head>', FAV+'\n</head>', 1)
    open(DIST+f'blog/{s}/index.html','w',encoding='utf-8').write(h)
print('articles:', len(slugs))

# ---- copy covers ----
for f in os.listdir(OUT):
    if f.startswith('cover-') and f.endswith('.jpg'):
        shutil.copy(OUT+f, DIST+'blog/'+f)

# ---- robots + sitemap ----
shutil.copy(UP+'robots.txt', DIST+'robots.txt')
shutil.copy(OUT+'sitemap.xml', DIST+'sitemap.xml')

# ---- favicon ----
open(DIST+'favicon.svg','w',encoding='utf-8').write(FAVSVG)

# ---- og.jpg 1200x630 ----
im = Image.open(UP+'1780253743.png').convert('RGB')
tw,th = 1200,630
w,h = im.size
scale = max(tw/w, th/h)
im = im.resize((int(w*scale), int(h*scale)), Image.LANCZOS)
w,h = im.size
im = im.crop(((w-tw)//2,(h-th)//2,(w-tw)//2+tw,(h-th)//2+th))
im.save(DIST+'og.jpg','JPEG',quality=85,optimize=True)

# ---- 404 ----
open(DIST+'404.html','w',encoding='utf-8').write(
'<!DOCTYPE html><html lang="ru"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
'<title>Страница не найдена — VLOZ</title>'+FAV+
'<style>body{margin:0;min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;'
'background:#f5f1e8;color:#171310;font-family:system-ui,-apple-system,sans-serif;text-align:center;padding:24px}'
'h1{font-size:72px;margin:0;letter-spacing:-.03em}p{color:#857a6a;font-size:18px}'
'a{display:inline-block;margin-top:20px;background:#ff5a1f;color:#2a0e02;text-decoration:none;font-weight:700;padding:14px 28px;border-radius:99px}</style>'
'</head><body><h1>404</h1><p>Такой страницы нет — но кофе ещё остался.</p><a href="/">На главную</a></body></html>')

# ---- README ----
readme = """# VLOZ — сайт для деплоя

Готовый статический сайт. Залейте содержимое этой папки в корень хостинга
(чтобы index.html открывался по адресу duckwin.ru/).

## Структура
- index.html              — главная (лендинг)
- 404.html                — страница «не найдено»
- favicon.svg             — иконка вкладки
- og.jpg                  — превью при шеринге главной (1200×630)
- robots.txt, sitemap.xml — для поисковиков (в корень)
- img/hero.jpg, img/about.jpg — фото лендинга
- blog/index.html         — блог (открывается по /blog/)
- blog/<статья>/index.html — статьи (чистые URL /blog/<статья>/)
- blog/cover-*.jpg         — обложки статей

Чистые URL (/blog/, /blog/название/) работают на любом статическом хостинге,
который отдаёт index.html из папки (Netlify, Vercel, GitHub Pages, nginx, Beget и т.п.).

## Что заменить перед запуском (3 пункта)
1. Метрики — в index.html в <head>:
   - 00000000  -> номер счётчика Яндекс.Метрики
   - G-XXXXXXXXXX -> Measurement ID Google Analytics
2. og.jpg — при желании замените на свой баннер 1200×630 (для красивого превью).
3. Фото в блоке «Эксперт» (img/about.jpg) — можно заменить на своё.

Уже готово: VLOZ, цены, Telegram @kryanton, кнопка MAX (реальная ссылка),
телефон, почта ad@duckwin.ru, SEO-разметка, sitemap, 6 статей блога со схемами.

## После заливки
1. Подключите домен duckwin.ru и SSL (https).
2. Добавьте сайт в Яндекс.Вебмастер и Google Search Console, подтвердите,
   скормите https://duckwin.ru/sitemap.xml — это запускает индексацию.
3. Заведите карточку в Яндекс.Бизнес (бесплатная видимость по Москве).
"""
open(DIST+'README.md','w',encoding='utf-8').write(readme)

# ---- zip ----
zip_path = shutil.make_archive(os.path.join(ROOT,'vloz-site'),'zip', DIST)
print('ZIP:', zip_path, os.path.getsize(zip_path)//1024,'KB')

# tree
print('\n--- dist tree ---')
for root,dirs,files in os.walk(DIST):
    lvl = root.replace(DIST,'').count('/')
    print('  '*lvl + (root.replace(DIST,'') or '.') + '/')
    for f in sorted(files):
        print('  '*(lvl+1) + f)
