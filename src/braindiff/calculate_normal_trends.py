import argparse
from braindiff.objects.preprocess_data import DataPreprocessor
from braindiff.common import tools


def main(args):
    config = tools.load_config()
    path = config['mrihearingdata']
    file = path + f"mri_audiometry_{args.degree}_{args.frequency}.csv"

    processor = DataPreprocessor(file)
    processor.delete_features_from_wm() 
    processor.filter_data()
    
    normal_data = processor.data



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
                        default="prawidlowy",
                        help="Degree of hearing loss (e.g., prawidlowy for normal hearing)")
    args = parser.parse_args()
    main(args)