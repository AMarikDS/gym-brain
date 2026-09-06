"""
Модуль конфигурации Reflex-фронтенда.
Содержит настройки сборки и адреса API.
"""

# BSL License
# Copyright (c) 2025 RTA Technologies

import reflex as rx

config = rx.Config(
    app_name="web",
    backend_host="0.0.0.0",
    api_url="http://localhost:3001",
)
