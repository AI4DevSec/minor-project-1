# src/model_training.py

import joblib # Cheezein save aur load karne wala tool
import os # Folders aur files manage karne wala tool
from sklearn.tree import DecisionTreeClassifier # Decision Tree Robot banane wala tool
# Robot ke test marks check karne wale tools
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,confusion_matrix
import matplotlib.pyplot as plt # Pictures (graphs) banane wala tool
import seaborn as sns # Sundar pictures banane wala tool
import numpy as np # Numbers wala tool
from src.logger import get_logger # Diary Wala Robot import kiya
from src.custom_exception import CustomException # Error Reporter Robot import kiya

# Diary Wala Robot ka ek instance (copy) banate hain is file ke liye
logger = get_logger(__name__)

# Robot Trainer ka blueprint (Class)
class ModelTraining:
    # Jab yeh robot banega, sabse pehle yeh steps honge
    def __init__(self):
        self.processed_data_path = "artifacts/processed" # Saaf data kahan hai, woh path yaad rakho
        self.model_path = "artifacts/models" # Train kiya hua robot kahan save karna hai, woh path yaad rakho
        os.makedirs(self.model_path , exist_ok=True) # Woh folder bana do agar nahi hai
        # Apna Decision Tree robot banao aur uski settings set karo
        self.model = DecisionTreeClassifier(criterion="gini" , max_depth=30 , random_state=42)
        logger.info("Model Training Robot Ready! 🤖") # Diary mein likho robot ready hai

    # Saaf data ko special boxes se load karne ka kaam
    def load_data(self):
        try:
            logger.info("Loading processed data...") # Diary mein likho shuru ho gaya
            # joblib.load use karke saare data files load karo
            X_train = joblib.load(os.path.join(self.processed_data_path , "X_train.pkl"))
            X_test = joblib.load(os.path.join(self.processed_data_path , "X_test.pkl"))
            y_train = joblib.load(os.path.join(self.processed_data_path , "y_train.pkl"))
            y_test = joblib.load(os.path.join(self.processed_data_path , "y_test.pkl"))
            logger.info("Processed data loaded successfully.") # Diary mein likho load ho gaya

            return X_train,X_test,y_train,y_test # Saara data wapas bhej do use karne ke liye

        except Exception as e:
            logger.error(f"Error while loading processed data: {e}") # Diary mein galti likho
            raise CustomException("Error while loading processed data", e) # Loud Error Reporter ko bolo detail report de

    # Decision Tree robot ko data se sikhane ka kaam
    def train_model(self, X_train, y_train): # Sikhane wala data lo
        try:
            logger.info("Starting model training...") # Diary mein likho shuru ho gaya
            self.model.fit(X_train,y_train) # Robot ko sikhao! Yeh hai training ka main step
            # Train kiye hue robot ko special box mein pack karke save karo
            joblib.dump(self.model, os.path.join(self.model_path, "model.pkl"))
            logger.info("Model trained and saved successfully in %s", self.model_path) # Diary mein likho train aur save ho gaya

        except Exception as e:
            logger.error(f"Error during model training: {e}") # Diary mein galti likho
            raise CustomException("Error during model training", e) # Loud Error Reporter ko bolo detail report de

    # Train kiye hue robot ka test lene aur report banane ka kaam
    def evaluate_model(self, X_test, y_test): # Test wala data aur asli answers lo
        try:
            logger.info("Starting model evaluation...") # Diary mein likho shuru ho gaya
            y_pred = self.model.predict(X_test) # Robot se test data par predictions karwao

            # Robot ke test marks calculate karo (Accuracy, Precision, Recall, F1)
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred, average="weighted")
            recall = recall_score(y_test, y_pred, average="weighted")
            f1 = f1_score(y_test, y_pred, average="weighted")

            # Robot ke marks Diary mein likho
            logger.info(f"Accuracy Score: {accuracy}")
            logger.info(f"Precision Score: {precision}")
            logger.info(f"Recall Score: {recall}")
            logger.info(f"F1 Score: {f1}")

            # Robot ki galatiyon ki picture (Confusion Matrix) banao
            cm = confusion_matrix(y_test, y_pred)
            logger.info("Confusion Matrix calculated.") # Diary mein entry

            # Confusion Matrix ko sundar graph mein dikhao aur save karo
            plt.figure(figsize=(8, 6)) # Picture ka size set karo
            sns.heatmap(cm, annot=True, cmap="Blues", xticklabels=np.unique(y_test), yticklabels=np.unique(y_test))
            plt.title("Confusion Matrix")
            plt.xlabel("Predicted Label") # Neeche likho yeh robot ke answers hain
            plt.ylabel("Actual Label") # Side mein likho yeh asli answers hain
            confusion_matrix_path = os.path.join(self.model_path, "confusion_matrix.png") # Picture kahan save karni hai
            plt.savefig(confusion_matrix_path) # Picture save karo
            plt.close() # Picture window band karo

            logger.info("Confusion Matrix saved successfully to %s", confusion_matrix_path) # Diary mein likho picture save ho gayi
            logger.info("Model Evaluation Finished Successfully.") # Diary entry

        except Exception as e:
            logger.error(f"Error during model evaluation: {e}") # Diary mein galti likho
            raise CustomException("Error during model evaluation", e) # Loud Error Reporter ko bolo detail report de

    # Robot Trainer ka main kaam (to-do list)
    def run(self):
        logger.info("Model Training Pipeline Step Started.") # Diary entry
        # Pehla kaam: Saaf data load karo
        X_train, X_test, y_train, y_test = self.load_data()
        self.train_model(X_train,y_train) # Doosra kaam: Robot ko sikhao
        self.evaluate_model(X_test,y_test) # Teesra kaam: Robot ka test lo
        logger.info("Model Training Pipeline Step Finished Successfully.") # Diary entry


# Yeh code tabhi chalega jab aap seedha is file ko run karoge
# Agar is file ko pipeline/training_pipeline.py se chalayenge, toh yeh hissa nahi chalega
if __name__ == "__main__":
    # Sirf testing ke liye, aap seedha model training chala sakte ho
    # Note: Iske liye data_processing pehle chalaya hua hona chahiye taki files exist karein
    trainer = ModelTraining() # Robot trainer banao
    trainer.run() # Trainer ka kaam shuru karo