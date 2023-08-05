<h1>Переводчик текста</h1>

```python
from yandex_translate_api import translate

en_text = 'Hello, world'
ru_text = translate(en_text, 'en', 'ru')

print(ru_text) #Привет, мир
```

```python
from yandex_translate_api import async_translate
import asyncio

async def main():
    en_text = 'Hello, world'
    ru_text = await async_translate(en_text, 'en', 'ru')

    print(ru_text) #Привет, мир

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```
