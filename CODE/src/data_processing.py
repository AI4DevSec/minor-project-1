# src/data_processing.py

import pandas as pd # Smart table wala tool
import numpy as np # Numbers wala tool
import joblib # Cheezein save aur load karne wala tool
from sklearn.model_selection import train_test_split # Data divide karne wala tool
import os # Folders aur files manage karne wala tool
from src.logger import get_logger # Diary Wala Robot import kiya
from src.custom_exception import CustomException # Error Reporter Robot import kiya

# Diary Wala Robot ka ek instance (copy) banate hain is file ke liye
logger = get_logger(__name__)

# Data Cleaning Robot ka blueprint (Class)
class DataProcessing:
    # Jab yeh robot banega, sabse pehle yeh steps honge
    def __init__(self,file_path):
        self.file_path = file_path # Kacche data file ka path yaad rakho
        self.df = None # Abhi table empty hai
        self.processed_data_path = "artifacts/processed" # Saaf data kahan save karna hai, woh path yaad rakho
        os.makedirs(self.processed_data_path , exist_ok=True) # Woh folder bana do agar nahi hai
        logger.info("Data Processing Robot Ready! 🛠️") # Diary mein likho ki robot ready hai

    # Data ko kacche file se load karne ka kaam
    def load_data(self):
        try: # Yeh kaam try karo, agar galti ho toh catch karna
            self.df = pd.read_csv(self.file_path) # Data read karke table mein daalo
            logger.info("Raw data successfully loaded from %s", self.file_path) # Diary mein likho load ho gaya
        except Exception as e: # Agar galti hui
            logger.error(f"Error while reading data: {e}") # Diary mein galti likho
            raise CustomException("Failed to read data", e) # Loud Error Reporter ko bolo detail report de

    # Shararti numbers (outliers) ko theek karne ka kaam
    def handle_outliers(self, column): # Kis column ke outliers theek karne hain, yeh batao
        try:
            logger.info(f"Starting outlier handling for column: {column}") # Diary mein likho shuru ho gaya
            Q1 = self.df[column].quantile(0.25) # Data ka 25% point
            Q3 = self.df[column].quantile(0.75) # Data ka 75% point

            IQR = Q3 - Q1 # Beech ka range

            Lower_value = Q1 - 1.5 * IQR # Outlier ki lower limit
            Upper_value = Q3 + 1.5 * IQR # Outlier ki upper limit

            sepal_median = np.median(self.df[column]) # Jis value se replace karna hai (median)

            # Har number ko check karo aur agar outlier hai toh replace karo
            for i in self.df[column]:
                if i > Upper_value or i < Lower_value:
                    self.df[column] = self.df[column].replace(i, sepal_median)

            logger.info("Outliers handled successfully for column: %s", column) # Diary mein likho ho gaya
        except Exception as e:
            logger.error(f"Error while handling outliers for column {column}: {e}") # Diary mein galti likho
            raise CustomException(f"Failed to handle outliers for column {column}", e) # Loud Error Reporter ko bolo detail report de

    # Data ko train aur test sets mein divide karne ka kaam
    def split_data(self):
        try:
            # Inputs (features) aur output (target) columns alag karo
            X = self.df[['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm']]
            Y = self.df["Species"]
            logger.info("Features (X) and Target (Y) separated.") # Diary entry

            # Data ko 80% train aur 20% test mein baanto
            X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
            logger.info("Data split into training (80%) and testing (20%) sets.") # Diary entry

            # Saaf aur divided data ko special boxes mein pack karke save karo
            joblib.dump(X_train, os.path.join(self.processed_data_path, "X_train.pkl"))
            joblib.dump(X_test, os.path.join(self.processed_data_path, "X_test.pkl"))
            joblib.dump(y_train, os.path.join(self.processed_data_path, "y_train.pkl"))
            joblib.dump(y_test, os.path.join(self.processed_data_path, "y_test.pkl"))
            logger.info("Processed data files saved successfully in %s", self.processed_data_path) # Diary entry

        except Exception as e:
            logger.error(f"Error while splitting and saving data: {e}") # Diary mein galti likho
            raise CustomException("Failed to split and save data", e) # Loud Error Reporter ko bolo detail report de

    # Data Cleaning Robot ka main kaam (to-do list)
    def run(self):
        logger.info("Data Processing Pipeline Step Started.") # Diary entry
        self.load_data() # Pehla kaam: Data load karo
        # Doosra kaam: SepalWidthCm ke outliers theek karo (pichhle notebook mein bhi yeh hi kiya tha)
        self.handle_outliers("SepalWidthCm")
        self.split_data() # Teesra kaam: Data ko divide karke save karo
        logger.info("Data Processing Pipeline Step Finished Successfully.") # Diary entry

# Yeh code tabhi chalega jab aap seedha is file ko run karoge
# Agar is file ko pipeline/training_pipeline.py se chalayenge, toh yeh hissa nahi chalega
if __name__ == "__main__":
    # Sirf testing ke liye, aap seedha data processing chala sakte ho
    data_processor = DataProcessing("../artifacts/raw/data.csv") # Robot banao
    data_processor.run() # Robot ka kaam shuru karo
