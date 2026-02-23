import pandas as pd

class DataPreprocessor:
    def __init__(self, path):
        self.data = pd.read_csv(path)  #Load data from the specified path

    def delete_features_from_wm(self, aseg_path):
        aseg_list =[]
        for column in self.data.columns:
            if 'ASEG' in column:
                aseg_list.append(column)

        df_aseg = pd.read_csv(aseg_path, sep=None, engine='python')
        aseg_list_diff = list(set(aseg_list) - set(df_aseg.columns))
        self.data = self.data.drop(columns=aseg_list_diff)


    def filter_data(self):
        cols_to_check = self.data.columns.difference(['L_HEARING_TYPE', 'P_HEARING_TYPE'])
        self.data = self.data.dropna(subset=cols_to_check).copy()
        self.data = self.data[self.data['IF_FIRST'] == 1] #only first examiation
        self.data['age'] = pd.to_numeric(self.data['age'], errors='coerce') 
        self.data = self.data[(self.data['age'] >= 0) & (self.data['age'] <= 100)]
    

    def choose_examinations_with_mri_after(self):
        self.data['DATA_BADANIA_MRI'] = pd.to_datetime(self.data['DATA_BADANIA_MRI'], format='%Y-%m-%d')
        self.data['DATA_BADANIA'] = pd.to_datetime(self.data['DATA_BADANIA'], dayfirst=True, errors='coerce')
        self.data = self.data[self.data['DATA_BADANIA_MRI'] > self.data['DATA_BADANIA']]
