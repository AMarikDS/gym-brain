"""
Модуль конфигурации Reflex-фронтенда.
Содержит настройки сборки и адреса API.
"""

import reflex as rx
from reflex_components_radix.plugin import RadixThemesPlugin

config = rx.Config(
    app_name="web",
    default_color_mode="dark",
    backend_host="0.0.0.0",
    api_url="http://localhost:3001",
    plugins=[
        RadixThemesPlugin(
            theme=rx.theme(
                appearance="dark",
                has_background=False,
                radius="large",
                accent_color="cyan",
                gray_color="slate",
            )
        )
    ],
)
