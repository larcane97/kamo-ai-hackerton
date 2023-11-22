import os

from models.recommend_rest_loaction.recommend_rest_gpt import RecommendRestGpt


# os.environ["OPENAI_API_TYPE"] = "azure"
# os.environ["OPENAI_API_BASE"] = "https://kmt-oai-fr-37.openai.azure.com/"
# os.environ["OPENAI_API_KEY"] = "7b214487cbbb49058ad896b129b1cafc"
# os.environ["OPENAI_API_VERSION"] = "2023-07-01-preview"
os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_BASE"] = "https://kmt-oai-uk-37.openai.azure.com/"
os.environ["OPENAI_API_KEY"] = "dbbe0f299cd44d38ba566abf5202f52d"
os.environ["OPENAI_API_VERSION"] = "2023-07-01-preview"

if __name__ == "__main__":
    recommend_rest_gpt =RecommendRestGpt(azure_deployment="gpt-4")

    resp = recommend_rest_gpt.predict(36.5392100317962, 126.989006461325)
    print(resp)
