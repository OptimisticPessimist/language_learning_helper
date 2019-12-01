from datetime import date, datetime

import responder
import yaml

from src.add_japanese_ruby import Phonetic

api = responder.API(
    templates_dir='static/templates',
    auto_escape=True,
)


class JapaneseAPI:
    def __init__(self) -> None:
        self.p = Phonetic()

    async def on_post(self, req, resp) -> None:
        data: object = await req.media()

class JapaneseWeb:
    def __init__(self) -> None:
        self.p = Phonetic()

    def on_get(self, req, resp) -> None:
        raw_text = "樹木希林はFUJIカラーで写せない遠いお正月へ旅立ったよ。"
        converted_text = self.p.export_html(raw_text)
        resp.html = api.template('japanese.html',
                                 raw_text=raw_text,
                                 converted_text=converted_text)

    async def on_post(self, req, resp) -> None:
        data: object = await req.media()
        text: str = data['text'].replace("<", "&lt").replace(">", "&gt")
        html = self.p.export_html(text)

        resp.media["success"] = "ok"
        resp.media["date"] = str(datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
        resp.media["text"] = text
        resp.media["html"] = html


api.add_route('', JapaneseWeb())
api.add_route('/', JapaneseWeb())

api.add_route('/v1/japanese', JapaneseAPI())


if __name__ == '__main__':
    from config import setting
    with open(f'./config/{setting.MODE}.yaml') as settings:
        mode = yaml.load(settings)
        ENV = mode['ENV']
        SERVER = mode['SERVER']
        PORT = mode['PORT']

    print(f"Start in {ENV} mode...")
    api.run(address=SERVER, port=PORT)
