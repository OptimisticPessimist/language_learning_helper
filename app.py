from datetime import date, datetime
from pathlib import Path

import responder
import yaml

from presenters import api

api = responder.API(
    templates_dir='static/templates',
    auto_escape=True,
)


class JapaneseAPI:
    def __init__(self) -> None:
        self.japanese_api = api.Japanese()

    def on_post(self, req, resp) -> None:
        self.japanese_api.post(req, resp)


class EnglishAPI:
    def __init__(self) -> None:
        self.ipa = IPA()

    async def on_post(self, req, resp) -> None:
        data = await req.media()
        resp.media["date"] = datetime.today()
        resp.media["text"] = data["raw-text"]
        resp.media["html"] = self.ipa.export_html(data["raw-text"])


class JapaneseWeb:
    def __init__(self) -> None:
        self.furigana = Furigana()

    def on_get(self, req, resp) -> None:
        raw_text = "樹木希林はFUJIカラーで写せない遠いお正月へ旅立ったよ。"
        converted_text = self.furigana.export_html(raw_text)
        resp.html = api.template('japanese.html',
                                 raw_text=raw_text,
                                 converted_text=converted_text)

    async def on_post(self, req, resp) -> None:
        data = await req.media(format='form')
        raw_text = data['raw-text'].replace("<", "&lt").replace(">", "&gt")
        converted_text = self.furigana.export_html(raw_text)

        @api.background.task
        def log():
            today = date.today()
            exec_time = datetime.today()
            raw = '-'.join(raw_text.splitlines())
            converted = '-'.join(converted_text.splitlines())
            with open(f'./logs/{today}.tsv', mode='a',
                      encoding='utf-8') as log:
                log.write(f"{exec_time}\t{raw}\t{converted}\n")

        log()
        resp.content = api.template('japanese.html',
                                    raw_text=raw_text,
                                    converted_text=converted_text)


class EnglishWeb:
    def __init__(self) -> None:
        self.ipa = IPA()

    def on_get(self, req, resp) -> None:
        raw_text = "I just read the article on the newspaper."
        converted_text = self.ipa.export_html(raw_text)
        resp.html = api.template('english.html',
                                 raw_text=raw_text,
                                 converted_text=converted_text)

    async def on_post(self, req, resp) -> None:
        data: object = await req.media(format='form')
        raw_text: str = data['raw-text'].replace("<", "&lt").replace(">", "&gt")
        converted_text = self.ipa.export_html(raw_text)

        @api.background.task
        def log():
            today = date.today()
            exec_time = datetime.today()
            raw = '-'.join(raw_text.splitlines())
            converted = '-'.join(converted_text.splitlines())
            with open(f'./logs/{today}.tsv', mode='a',
                      encoding='utf-8') as log:
                log.write(f"{exec_time}\t{raw}\t{converted}\n")

        log()
        resp.content = api.template('english.html',
                                    raw_text=raw_text,
                                    converted_text=converted_text)


api.add_route('/', JapaneseWeb)
api.add_route('/japanese/furigana', JapaneseWeb)
api.add_route('/english/ipa', EnglishWeb)


if __name__ == '__main__':
    from config import setting
    with open(f'./config/{setting.MODE}.yaml') as settings:
        mode = yaml.load(settings, Loader=yaml.FullLoader)
        ENV = mode['ENV']
        SERVER = mode['SERVER']
        PORT = mode['PORT']

    logs = Path('./logs')
    if not logs.exists():
        logs.mkdir(mode=0o644)

    print(f"Start in {ENV} mode...")
    api.run(address=SERVER, port=PORT)
