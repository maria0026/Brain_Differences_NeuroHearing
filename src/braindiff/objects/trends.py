import numpy as np
import pandas as pd
from sklearn.linear_model import RANSACRegressor, LinearRegression
from sklearn.preprocessing import PolynomialFeatures, RobustScaler
from sklearn.pipeline import make_pipeline


class TrendCalculator:
    def __init__(self, df, df_hearing):
        self.df = df
        self.df_hearing = df_hearing

    def calculate_trends(self, sex='M'):
        if sex =='M':
            df_sel = self.df[self.df['male']==1]
            df_hearing = self.df_hearing[self.df_hearing['male']==1]
        else:
            df_sel = self.df[self.df['male']==0]
            df_hearing = self.df_hearing[self.df_hearing['male']==0]

        df_results = pd.DataFrame(columns=['feature_name', 'MAE_norm', 'mean'])
        
        #add huber regression    
        for column in df_sel.columns:
            if ('A2009' in column) or ('ASEG' in column):
                #scale features with robust scaler
                scaler = RobustScaler()
                y_norm_scaled = scaler.fit_transform(df_sel[[column]]).ravel()

                # Skalujemy słyszących tym samym scalerem
                df_hearing = df_hearing.dropna(subset=['age', column])
                if len(df_hearing) == 0:
                    continue
                y_hear_scaled = scaler.transform(df_hearing[[column]]).ravel()
                
                if len(np.unique(y_norm_scaled)) < 80:
                    continue


                ransac_norm = make_pipeline(
                PolynomialFeatures(degree=2, include_bias=False),
                RANSACRegressor(
                        estimator=LinearRegression(),
                        min_samples=0.5,
                        residual_threshold=None,
                        random_state=42
                    )
                )
                #print(column)
                #print(df_sel[['age']])
                #print(y_norm_scaled)
                ransac_norm.fit(df_sel[['age']], y_norm_scaled)
                ransac_step = ransac_norm.named_steps['ransacregressor']
                lin_est = ransac_step.estimator_

                mae_norm = np.mean(np.abs(y_norm_scaled - ransac_norm.predict(df_sel[['age']]))) #to jaka jest wartosc cech - jaka wynika z dopasowania
                mae_diff = np.mean(np.abs(y_hear_scaled - ransac_norm.predict(df_hearing[['age']]))) - mae_norm  
                #mean_diff = np.mean(np.abs(y_hear_scaled - y_norm))
                mae_diff_stand = mae_diff / (np.std(y_norm_scaled) * np.std(y_hear_scaled))


                df_results = pd.concat([
                    df_results,
                    pd.DataFrame([{
                        'feature_name': column,
                        'Norm_Coeff_age': lin_est.coef_[0],
                        'Norm_Coeff_age2': lin_est.coef_[1],
                        'Norm_Intercept': lin_est.intercept_,
                        'MAE_norm': mae_norm,
                        'mean': mae_diff_stand,
                        'Scaler_center': scaler.center_[0],
                        'Scaler_scale': scaler.scale_[0],
                    }])
                ], ignore_index=True)


        return df_results