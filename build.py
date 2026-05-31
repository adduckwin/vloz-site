#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Полная пересборка сайта VLOZ: лендинг -> блог -> dist/.
Запуск:  python3 build.py   (нужен Python 3 + Pillow)
Результат: папка dist/ — готова к заливке в корень хостинга.
"""
import subprocess, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.join(HERE, "build")
for step in ("patch.py", "blog_build.py", "deploy_build.py"):
    print(f"\n=== {step} ===")
    r = subprocess.run([sys.executable, os.path.join(B, step)])
    if r.returncode:
        sys.exit(f"Ошибка на шаге {step}")
print("\nГотово. Содержимое dist/ — заливай в корень хостинга.")
