from transformers import pipeline
import log_progress as lp


class SummaryClassify:
    def __init__(self):
        self.path = "./docs/log/"
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
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        self.classifier = pipeline(
            "zero-shot-classification", model="facebook/bart-large-mnli"
        )
        self.logger = lp.LogProcess(self.path).log

    def to_sumarize(self, article):
        try:
            summary = self.summarizer(
                article, max_length=130, min_length=30, do_sample=False
            )
            self.logger("Summarize successful")
            return summary[0]["summary_text"]
        except Exception as e:
            self.logger(f"Error: {e} - Summarize not successful")
            return None

    def to_clasify(self, summary, label):
        try:
            result_zero_shot = self.classifier(
                summary, self.classification_labels[label]
            )
            self.logger("Classify successful")
            return result_zero_shot
        except Exception as e:
            self.logger(f"Error: {e} - Classify not successful")
            return None

    def clasify_all(self, summary):
        dict_labels = {}
        for label, options in self.classification_labels.items():
            try:
                result_zero_shot = self.classifier(summary, options)
                dict_labels[label] = {
                    "labels": result_zero_shot["labels"][:3],
                    "scores": result_zero_shot["scores"][:3],
                }
                self.logger(f"{label}: Classify successful")
            except Exception as e:
                self.logger(f"Error: {e} - Classify not successful")
        return dict_labels
