from langchain.llms import Ollama
from translate import Translator as translator
from gtts import gTTS as tts


class Interface:

    def __init__(self, language: str):
        """ Initialise the translator objects
        :param language: a 2-letter language code
        """

        self.en_to_lang = translator(from_lang='en', to_lang=language)
        self.lang_to_en = translator(from_lang=language, to_lang='en')
        self.llm = Ollama(model='llama2')

    def get_response(self, context: str, query: str, language: str) -> (str, str):
        """
        Creates a reply in two languages. Generates a language voice
        in the file 'voice.mp3'
        :param context:  the setting in which the speaker is placed
        :param query:    the information that needs to be generated
        :param language: a 2-letter language code
        :return:         (English, [Language]) string tuple.
        """

        response = self.llm.invoke(f'[{context}] {query} in beginner English')

        lang_text = self.en_to_lang.translate(response)
        en_text = self.lang_to_en.translate(lang_text)

        speech = tts(lang_text, lang=language)
        speech.save('voice.mp3')

        return en_text, lang_text
