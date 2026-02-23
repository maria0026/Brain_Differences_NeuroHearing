import argparse
from braindiff.objects.preprocess_data import DataPreprocessor
from braindiff.objects.trends import TrendCalculator
from braindiff.common import tools
import os

def main(args):
    config = tools.load_config()
    path = config['mrihearingdata']
    file_normal = path + f"mri_audiometry_prawidlowy_{args.frequency}.csv"
    file = path + f"mri_audiometry_{args.degree}_{args.frequency}.csv"

    processor = DataPreprocessor(file)
    processor.delete_features_from_wm(config['asegfile']) 
    processor.filter_data()
    processor.choose_examinations_with_mri_after()

    processor_normal = DataPreprocessor(file_normal)
    processor_normal.delete_features_from_wm(config['asegfile']) 
    processor_normal.filter_data()

    normal_data = processor_normal.data
    pathology_data = processor.data

    print(pathology_data)
    pathology_data.to_csv("znaczny_2.csv")
    

    trend_calculator = TrendCalculator(normal_data, pathology_data)
    df_results = trend_calculator.calculate_trends(sex=args.sex)
    print(df_results)

    #Save results to CSV
    output_path = config['output_path']
    df_results_sorted = df_results.sort_values(by='mean', ascending=False)
    if not os.path.exists(output_path):
            os.makedirs(output_path)

    df_results_sorted.to_csv(f"{output_path}/trends_{args.degree}_{args.frequency}_{args.sex}.csv", index=False)



if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Parser for audiometry data analyzer")
    parser.add_argument("--sex", 
                        nargs="?", 
                        default="M",
                        help="Sex of the subject")
    parser.add_argument("--frequency",
                        nargs="?",
                        default="HF",
                        help="Frequency range for audiometry data (e.g., HF for high frequencies, LF for low frequencies)")
    parser.add_argument("--degree",
                        nargs="?",
                        default="znaczny",
                        help="Degree of hearing loss (e.g., prawidlowy for normal hearing)")
    args = parser.parse_args()
    main(args)