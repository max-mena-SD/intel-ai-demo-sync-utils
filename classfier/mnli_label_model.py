from transformers import TFBartForSequenceClassification, BartTokenizer, pipeline
import tensorflow as tf


class MnliLabelModel:
    def __init__(self):  # , num_labels, hidden_size):
        self.classification_labels = {
            "industry": [
                "Healthcare",
                "Finance",
                "Manufacturing",
                "Retail",
                "Transportation",
                "Education",
                "Customer Service",
                "Entertainment",
                "Agriculture",
                "Cybersecurity",
            ],
            "type": [
                "Robotics",
                "Recommendation Systems",
                "Generative AI",
                "Anomaly Detection",
                "Speech Recognition",
                "Computer Vision",
                "Natural Language Processing",
            ],
            "technology": [
                "Machine Learning",
                "Deep Learning",
                "Computer Vision",
                "Natural Language Processing",
                "Reinforcement Learning",
                "Edge Computing",
                "Transformers",
                "Neural Networks",
            ],
            "complexity_level": ["Beginner", "Intermediate", "Advanced", "Expert"],
            "platform_tools": [
                "TensorFlow",
                "PyTorch",
                "OpenVINO",
                "Hugging Face",
                "Keras",
                "Scikit-learn",
                "AWS SageMaker",
                "Google Cloud AI",
            ],
            "use_case_functionality": [
                "Real-time Video Processing",
                "Predictive Maintenance",
                "Fraud Detection",
                "Speech-to-Text",
                "Recommendation Engine",
                "Chatbots",
                "Autonomous Systems",
                "Image Recognition",
                "Sentiment Analysis",
            ],
        }
        # Cargar el modelo de clasificación de secuencias BART
        self.model = TFBartForSequenceClassification.from_pretrained(
            "facebook/bart-large-mnli"
        )
        # Cargar el tokenizador correspondiente a BART
        self.tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-mnli")
        # Inicializar el pipeline con el modelo y el tokenizador
        self.classifier = pipeline(
            "zero-shot-classification",
            model=self.model,
            tokenizer=self.tokenizer,
            device=0 if tf.config.list_physical_devices("GPU") else -1,
        )

    def clasify_all_labels(self, summary: str) -> dict:
        dict_labels = {}
        for label, options in self.classification_labels.items():
            try:
                result_zero_shot = self.classifier(summary, options)
                dict_labels[label] = result_zero_shot["labels"][:3]
                # self.logger(f"{label}: Classify successful")
                print(f"{label}: Classify successful")
            except Exception as e:
                # self.logger(f"Error: {e} - Classify not successful")
                print(f"Error: {e} - Classify not successful")
        return dict_labels

    def insert_label_info(self, dict_premap: list) -> dict:

        dict_classification = self.clasify_all_labels(dict_premap[5])

        return dict_classification
