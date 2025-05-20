# pipeline/training_pipeline.py

# Apne helper robots ko bulao
from src.data_processing import DataProcessing
from src.model_training import ModelTraining
# Diary Wala Robot import karne ki yahan seedha zarurat nahi hai
# Kyunki woh helper robots ke andar hi use ho raha hai

# Yeh code tabhi chalega jab aap seedha is file ko run karoge (jo hum karna chahte hain)
if __name__ == "__main__":
    print("Pipeline Started! 🚀") # Console par print karo ki shuru ho gaya

    # Data Cleaning Robot ka kaam shuru karo
    data_processor = DataProcessing("../DATA/data.csv") # Data Cleaning Robot banao aur raw data file batao
    data_processor.run() # Robot ko bolo apna kaam shuru kare (load, clean, split, save)

    print("Data Processing Done. ✨ Starting Model Training...") # Console par print karo next step shuru ho raha hai

    # Robot Trainer ka kaam shuru karo
    trainer =  ModelTraining() # Robot Trainer banao (yeh processed data khud dhund lega)
    trainer.run() # Robot ko bolo apna kaam shuru kare (load processed data, train, evaluate, save)

    print("Pipeline Finished Successfully! 🎉") # Console par print karo ki khatam ho gaya