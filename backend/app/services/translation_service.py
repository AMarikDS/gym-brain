from transformers import MarianMTModel, MarianTokenizer
from functools import lru_cache
import logging
import os

logger = logging.getLogger(__name__)

class TranslationService:
    def __init__(self):
        self.model_name = "Helsinki-NLP/opus-mt-en-ru"
        self.tokenizer = None
        self.model = None
        self._is_loaded = False
        
        # Save the model locally in the 'models/translation' directory
        self.cache_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "..", "models", "translation")
        )
        os.makedirs(self.cache_dir, exist_ok=True)

    def load_model(self):
        if not self._is_loaded:
            try:
                logger.info(f"Loading translation model {self.model_name}...")
                self.tokenizer = MarianTokenizer.from_pretrained(
                    self.model_name, cache_dir=self.cache_dir
                )
                self.model = MarianMTModel.from_pretrained(
                    self.model_name, cache_dir=self.cache_dir
                )
                self._is_loaded = True
                logger.info("Translation model loaded successfully.")
            except Exception as e:
                logger.error(f"Failed to load translation model: {e}")
                self._is_loaded = False

    @lru_cache(maxsize=1024)
    def translate_en_to_ru(self, text: str) -> str:
        """
        Translates English text to Russian.
        Uses LRU Cache to instantly return previously translated strings (0ms delay).
        """
        import html
        text = html.unescape(text)
        
        if not text:
            return ""
        if not self._is_loaded:
            self.load_model()
        if not self._is_loaded:
            return text # Fallback to original text if model fails to load

        try:
            inputs = self.tokenizer(text, return_tensors="pt", padding=True)
            translated = self.model.generate(**inputs)
            res = self.tokenizer.decode(translated[0], skip_special_tokens=True)
            return res
        except Exception as e:
            logger.error(f"Translation error for text '{text}': {e}")
            return text

# Global singleton
translation_service = TranslationService()
