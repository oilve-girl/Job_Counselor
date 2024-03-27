# training_pipeline.py

import os
import sys
import pandas as pd
from joblib import dump
from src.exception import CustomException
from src.logger import logging
from src.preprocessing import preprocess_skills_data, match_skills_with_jobs
from src.model import train_model
from src.resume_parser import extract_skills_from_resume

def main():
    try:
        # Specify file paths
        resume_dataset_path = "path/to/resume_dataset.json"
        job_postings_dataset_path = "path/to/job_postings_dataset.csv"

        # Load datasets
        resume_data = pd.read_json(resume_dataset_path)
        job_postings_data = pd.read_csv(job_postings_dataset_path)

        # Preprocess data
        processed_resume_data = preprocess_skills_data(resume_data)
        processed_job_postings_data = preprocess_skills_data(job_postings_data)

        # Extract skills from resume
        extracted_skills = []
        for resume_text in processed_resume_data['resume_text']:
            skills = extract_skills_from_resume(resume_text)
            extracted_skills.append(skills)

        # Match skills with jobs
        matching_urls = match_skills_with_jobs(extracted_skills, processed_job_postings_data)

        # Train model
        model = train_model(processed_resume_data, processed_job_postings_data)

        # Save trained model
        model_path = "path/to/trained_model.pkl"
        save_model(model, model_path)

        logging.info("Training pipeline completed successfully.")

    except Exception as e:
        logging.error(f"An error occurred in the training pipeline: {e}")
        raise CustomException(e, sys)

if __name__ == "__main__":
    main()


