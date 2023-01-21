import glob
import os

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm

from config import cfg
from utils.utils_data import load_pickle, load_txt, load_yaml, save_pickle
from utils.utils_general import get_basename_no_ext


class Model:
    def __init__(self):
        # Load the semantic search model; will be downloaded if it doesn't exist yet
        self.model = SentenceTransformer(cfg.model_name)
        # Load the summaries and embeddings
        self.database = self.get_database()
        self.summaries = np.array([entry["summary"] for entry in self.database])
        self.embeddings = np.array([entry["embedding"] for entry in self.database])

    def embed_sentences(self, sentences):
        return self.model.encode(sentences)

    def predict(self, query):
        # Embed the query
        embeddings = self.embed_sentences(query)
        # Compare query embedding with all embeddings in the database
        cos_sim_array = cosine_similarity(embeddings, self.embeddings)
        # Get the ID of the most similar embedding from the database
        entry_ids = np.argmax(cos_sim_array, axis=1)
        # Return the summary that matches that ID
        return_summaries = [self.summaries[id] for id in entry_ids]
        return return_summaries

    def save(self):
        save_pickle(cfg.model_savepath, self)

    @staticmethod
    def transform(input_df):
        return list(input_df)

    def get_database(self):
        if not os.path.isfile(cfg.database_path):
            self.save_embeddings()
        return load_pickle(cfg.database_path)

    def save_embeddings(self):
        summary_path = os.path.join(cfg.cwd, "thuisarts-summaries")
        if not os.path.isdir(summary_path):
            # If there are no summaries (e.g. when we run for the first time),
            #   we need to scrape them from the thuisarts.nl website
            self.scrape()
        # Get all the saved summaries (both txt and yaml)
        summaries_path_list = glob.glob(os.path.join(summary_path, "*.txt"))
        entry_dict = load_yaml("thuisarts.yaml")
        # Run through each summary and get the embedding from the model
        for summary_id in tqdm(range(len(summaries_path_list))):
            summary_path = summaries_path_list[summary_id]
            id = int(get_basename_no_ext(summary_path))
            # Concatenate each line in the summary into a single string
            summary_txt = "".join(load_txt(summary_path))
            for entry_id, entry in enumerate(entry_dict):
                if entry["ID"] == id:
                    entry_dict[entry_id]["summary"] = summary_txt
                    # Get the embedding from the model
                    entry_dict[entry_id]["embedding"] = self.embed_sentences(
                        summary_txt
                    )
                    break
        # Save as pickle file
        save_pickle(cfg.database_path, entry_dict)

    @staticmethod
    def scrape():
        print("No summaries found. Scraping the website ...")
        from thuisarts_db.get_thuisarts_topics import Scraper

        # Run the scraper
        scraper = Scraper()
        scraper.dump_summaries()
