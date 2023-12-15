import os
import sys
from dataclasses import dataclass

from catboost import CatBoostRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from sklearn.ensemble import (AdaBoostRegressor,GradientBoostingRegressor,RandomForestRegressor)

from src.exception import CustomException
from src.logger import logging

from src.utils import save_object,evaluate_model

@dataclass
class Modeltrainerconfig:
    trained_model_file_path = os.path.join("artifacts","model.pkl")

class Modeltrainer:
    def __init__(self):
        self.model_trainer_config = Modeltrainerconfig()

    def initiate_model_trainer(self,train_array,test_array):
        try:
            logging.info("splitting traininig and testing data")
            x_train,y_train,x_test,y_test=(
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )

            models = {
                "Random_forest" :RandomForestRegressor(),
                "Decision_tree" :DecisionTreeRegressor(),
                "Gradient_boosting":GradientBoostingRegressor(),
                "Linear_regressor" :LinearRegression(),
                "K-neighbourClassifier":KNeighborsRegressor(),
                "Xgbclassifier":XGBRegressor(),
                "CatboostingClassifier":CatBoostRegressor(verbose=False),
                "AdaboostClassifier":AdaBoostRegressor()
            }

            model_report :dict= evaluate_model(x_train=x_train,y_train=y_train,x_test=x_test,y_test=y_test,models = models)

            best_model_score  =max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ] 

            best_model = models[best_model_name]

            if best_model_score < 0.6:
                raise CustomException("no best model")
            logging.info("best modle found on training and testing dataset")

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )

            predicted=  best_model.predict(x_test)
            r2Score = r2_score(y_test,predicted)
            return r2Score
        
        except Exception as e:
            raise CustomException(e,sys)




