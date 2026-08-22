import pandas as pd 
import pickle 
import json 
from pathlib import Path 
from .preprocessing import cols


def load_models():
    try : 

        paths = Path(__file__).resolve().parents[1]/"models"
        with open(paths/"model.pkl", 'rb') as f : 
            model = pickle.load(f)

        with open(paths/"oe.pkl", 'rb') as f : 
            oe = pickle.load(f)

        with open(paths/"trf.pkl", 'rb') as f : 
            trf = pickle.load(f)

        with open(paths/"le_pkl.pkl", 'rb') as f : 
            le = pickle.load(f)

        return model , oe ,trf ,le 

    except Exception as e : 
        raise e 



def predict_output(user_input : dict) : 

    model , oe ,trf ,le =load_models()
    df = pd.DataFrame([user_input])

    cate_cols, nums_cols = cols()
    df[nums_cols] = trf.transform(df[nums_cols])
    df[cate_cols] = oe.transform(df[cate_cols])

    pred = model.predict(df)
    prob = model.predict_proba(df)
    
    prediction_label = le.inverse_transform(pred)
    
    return {
            "prediction": prediction_label[0],
            "probability": float(prob[0].max())
}





# import pandas as pd
# import pickle
# from pathlib import Path
# from .preprocessing import cols


# def load_models():
#     try:
#         paths = Path(__file__).resolve().parents[1] / "models"

#         with open(paths / "model.pkl", "rb") as f:
#             model = pickle.load(f)

#         with open(paths / "oe.pkl", "rb") as f:
#             oe = pickle.load(f)

#         with open(paths / "trf.pkl", "rb") as f:
#             trf = pickle.load(f)

#         with open(paths / "le.pkl", "rb") as f:
#             le = pickle.load(f)

#         return model, oe, trf, le

#     except Exception as e:
#         raise e


# def predict_output(user_input: dict):
#     model, oe, trf, le = load_models()

#     df = pd.DataFrame([user_input])

#     cate_cols, nums_cols = cols()

#     df[nums_cols] = trf.transform(df[nums_cols])
#     df[cate_cols] = oe.transform(df[cate_cols])

#     pred = model.predict(df)
#     prob = model.predict_proba(df)

#     prediction_label = le.inverse_transform(pred)[0]

#     class_probabilities = {
#         le.inverse_transform([int(class_index)])[0]: float(prob[0][i])
#         for i, class_index in enumerate(model.classes_)
#     }

#     return {
#         "predicted_category": {
#             "predicted_category": prediction_label,
#             "confidence": float(prob[0].max()),
#             "class_probabilities": class_probabilities
#         }
#     }