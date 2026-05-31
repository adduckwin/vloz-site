# VLOZ — сайт студии сезонных и авторских меню для кофеен

Статический сайт (лендинг + блог) для **VLOZ** (Антон Кряквин, Москва).
Домен: **duckwin.ru**. Хостинг — свой, GitHub используется как хранилище кода.

## Что внутри

```
vloz-site/
├── build.py            ← единая команда пересборки (python3 build.py)
├── build/              ← движок сборки
│   ├── patch.py            лендинг: template2.html → .build/vloz.html
│   ├── blog_build.py       блог + обложки + sitemap.xml
│   ├── deploy_build.py     упаковка в dist/ (вынос картинок, чистые URL)
│   └── template2.html      шаблон лендинга
├── assets/             ← исходники (картинки, robots.txt) — НЕ заливаются на хостинг
├── dist/               ← ГОТОВЫЙ САЙТ — это содержимое заливается в корень хостинга
└── .build/             ← промежуточные файлы (в .gitignore)
```

## Деплой (заливка на хостинг)

Заливай **содержимое папки `dist/`** в корень хостинга так, чтобы
`dist/index.html` открывался по адресу `https://duckwin.ru/`.

Чистые URL (`/blog/`, `/blog/название/`) работают на любом статическом
хостинге, который отдаёт `index.html` из папки (nginx, Apache, Beget,
Netlify, Vercel, GitHub Pages и т. п.).

## Пересборка (если правил тексты/картинки)

Нужен Python 3 и Pillow (`pip install pillow`):

```bash
python3 build.py
```

Скрипт прогонит лендинг → блог → упаковку и обновит `dist/`.

- Тексты/блоки лендинга — в `build/template2.html` и `build/patch.py`.
- Статьи блога, обложки, схемы — в `build/blog_build.py`
  (словари `IMG`, `DIAGRAMS`, тела статей).
- Картинки hero/портрет — низ `build/patch.py`; обложки статей — `assets/`.

## Что заменить перед запуском (на стороне Антона)

1. **Метрики** в `dist/index.html` (`<head>`): `00000000` → счётчик
   Яндекс.Метрики, `G-XXXXXXXXXX` → Measurement ID Google Analytics.
   (Лучше править в шаблоне `build/template2.html` и пересобрать.)
2. **og.jpg** — при желании свой баннер 1200×630 для превью при шеринге.
3. **Фото «Эксперт»** (`assets/IMG_0237.jpeg`) — можно заменить.

## После заливки

1. Подключить домен `duckwin.ru` + SSL (https).
2. Добавить сайт в Яндекс.Вебмастер и Google Search Console,
   скормить `https://duckwin.ru/sitemap.xml`.
3. Завести карточку в Яндекс.Бизнес.

---

Уже готово: VLOZ-брендинг, цены, Telegram @kryanton, кнопка MAX (реальная
ссылка), телефон, почта `ad@duckwin.ru`, SEO-разметка, sitemap, блог из 6 статей.
