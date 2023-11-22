import os

from models.recommend_location.recommend_location_gpt import RecommendLocationGpt

os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_BASE"] = "https://kmt-oai-fr-37.openai.azure.com/"
os.environ["OPENAI_API_KEY"] = "7b214487cbbb49058ad896b129b1cafc"
os.environ["OPENAI_API_VERSION"] = "2023-07-01-preview"

if __name__ == "__main__":
    recommend_location_gpt = RecommendLocationGpt(azure_deployment="gpt-4")

    resp = recommend_location_gpt.predict(
        driver_lat=37.508811,
        driver_lng=127.040978)

    print(resp)
