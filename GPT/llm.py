import logging
import pathlib
import time

from openai import OpenAI


class KimiService:
    moonshot_v1_8k = "moonshot-v1-8k"
    moonshot_v1_32k = "moonshot-v1-32k"
    moonshot_v1_128k = "moonshot-v1-128k"

    def __init__(self, args):
        logging.info('Initializing ChatGPT Service...')
        self.model = args.model if args.kimi_model else KimiService.moonshot_v1_32k
        self.kimi_key = args.kimi_key
        self.character = args.character
        self.tune = self.init_tune()

        self.client = OpenAI(
            api_key=self.kimi_key,
            base_url="https://api.moonshot.cn/v1",
        )

    def init_tune(self):
        with pathlib.Path(__file__).parent.joinpath(fr"prompts/{self.character}.txt").open() as f:
            return f.read()

    def answer(self, text: str) -> str:
        """
        Get llm answer content.
        """
        stime = time.time()
        data = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": self.tune
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        )
        logging.info('ChatGPT Response: %s, time used %.2f' % (data.choices[0].message.content, time.time() - stime))
        return data.choices[0].message.content
