from datetime import date, datetime

import responder
import yaml

from src.english.ipa_phonetics import IPA
from src.japanese.kana_phonetics import Furigana

api = responder.API(
    templates_dir='static/templates',
    auto_escape=True,
)


class JapaneseAPI:
    def __init__(self) -> None:
        self.furigana = Furigana()

    async def on_post(self, req, resp) -> None:
        data: object = await req.media()
        resp.media["success"] = "ok"
        resp.media["text"] = data['raw-text']
        resp.media["html"] = self.furigana.export_html(data['raw-text'])


class EnglishAPI:
    def __init__(self) -> None:
        self.ipa = IPA()

    async def on_post(self, req, resp) -> None:
        data: object = await req.media()
        resp.media["success"] = "ok"
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
        data: object = await req.media(format='form')
        raw_text: str = data['raw-text'].replace("<", "&lt").replace(">", "&gt")
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


api.add_route('', JapaneseWeb())
api.add_route('/japanese/furigana', JapaneseWeb())
api.add_route('/english/ipa', EnglishWeb())

api.add_route('/v1/japanese', JapaneseAPI())  # api.add_route('/v1/english', EnglishAPI())

if __name__ == '__main__':
    from config import setting
    with open(f'./config/{setting.MODE}.yaml') as settings:
        mode = yaml.load(settings, Loader=yaml.FullLoader)
        ENV = mode['ENV']
        SERVER = mode['SERVER']
        PORT = mode['PORT']

    print(f"Start in {ENV} mode...")
    api.run(address=SERVER, port=PORT)
