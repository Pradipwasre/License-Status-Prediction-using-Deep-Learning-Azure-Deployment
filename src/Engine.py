from ML_Pipeline import Predict, Train_Model
from ML_Pipeline.Preprocess import apply
from ML_Pipeline.Utils import load_model, save_model
import pandas as pd
import subprocess

#input by the user 0 for training 1 for prediction and 2 for deployment
val = int(input("Train - 0\nPredict - 1\nDeploy - 2\nEnter your value: "))
if val == 0:
    #reading the data
    data = pd\
        .read_csv("../input/License_Data.csv", low_memory=False)\
        .drop_duplicates()\
        .reset_index(drop=True)

    print("Data loaded into pandas dataframe")

    processed_df = apply(data)
    ml_model, columns = Train_Model.fit(processed_df)
    model_path = save_model(ml_model, columns)
    print("Model saved in: ", "output/dnn-model")
elif val == 1:
    model_path = "../output/dnn-model"
    # model_path = input("Enter full model path: ")
    ml_model, columns = load_model(model_path) #loading model and features for the model
    test_data = pd \
        .read_csv("../input/test_data.csv", low_memory=False) \
        .drop_duplicates() \
        .reset_index(drop=True)
    # print(test_data.to_dict('dict'))
    processed_df = apply(test_data)
    prediction = Predict.init(processed_df, ml_model, columns)
    print(prediction)
else:
    # For prod deployment
    '''process = subprocess.Popen(['sh', 'ML_Pipeline/wsgi.sh'],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               universal_newlines=True
                               )'''

    # For dev deployment
    process = subprocess.Popen(['python', 'ML_Pipeline/deploy.py'],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               universal_newlines=True
                               )

    for stdout_line in process.stdout:
        print(stdout_line)

    stdout, stderr = process.communicate()
    print(stdout, stderr)
