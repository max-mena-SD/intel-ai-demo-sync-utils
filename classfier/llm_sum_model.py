# from transformers import pipeline


# class LLMSumModel:
#     def __init__(self):
#         # self.model = TFBartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")
#         self.summarizer = pipeline(
#             "summarization",
#             model="facebook/bart-large-cnn",
#             batch_size=1,
#             device=-1,
#             use_fast=True,
#         )

from transformers import TFBartForConditionalGeneration, BartTokenizer, pipeline


class LLMSumModel:
    def __init__(self):
        # Cargar el modelo BART para generación condicional
        self.model = TFBartForConditionalGeneration.from_pretrained(
            "facebook/bart-large-cnn"
        )

        # Cargar el tokenizador correspondiente a BART
        self.tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")

        # Inicializar el pipeline con el modelo y el tokenizador
        self.summarizer = pipeline(
            "summarization",
            model=self.model,
            tokenizer=self.tokenizer,  # Agregar el tokenizador aquí
            batch_size=1,
            device=-1,  # Usar CPU
            use_fast=True,
        )

    def to_sumarize(self, article):
        try:
            summary = self.summarizer(
                article,
                max_length=130,
                min_length=30,
                do_sample=False,  # , framework="pt"
            )
            # self.logger("Summarize successful")
            print("Summarize successful")
            return summary[0]["summary_text"]
        except Exception as e:
            # self.logger(f"Error: {e} - Summarize not successful")
            print(f"Error: {e} - Summarize not successful")
            return None
