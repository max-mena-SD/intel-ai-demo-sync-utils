from transformers import pipeline


class LLMModel:
    def __init__(self):
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
            "ai_techniques": [  # "technology": [
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
            "ai_framework": [  # "platform_tools": [
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
        self.summarizer = pipeline(
            "summarization",
            model="facebook/bart-large-cnn",
            batch_size=1,
            device=-1,
            use_fast=True,
        )
        self.classifier = pipeline(
            "zero-shot-classification", model="facebook/bart-large-mnli", batch_size=1
        )

    def to_sumarize(self, article):
        try:
            summary = self.summarizer(
                article, max_length=130, min_length=30, do_sample=False
            )
            # self.logger("Summarize successful")
            print("Summarize successful")
            return summary[0]["summary_text"]
        except Exception as e:
            # self.logger(f"Error: {e} - Summarize not successful")
            print(f"Error: {e} - Summarize not successful")
            return None

    def to_clasify(self, summary, label):
        try:
            result_zero_shot = self.classifier(
                summary, self.classification_labels[label]
            )
            # self.logger("Classify successful")
            print("Classify successful")
            return result_zero_shot
        except Exception as e:
            # self.logger(f"Error: {e} - Classify not successful")
            print(f"Error: {e} - Classify not successful")
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
                # self.logger(f"{label}: Classify successful")
                print(f"{label}: Classify successful")
            except Exception as e:
                # self.logger(f"Error: {e} - Classify not successful")
                print(f"Error: {e} - Classify not successful")
                return None
        return dict_labels
