import os
# import sys
# sys.path.append('/Users/frankie.gg/Documents/GitHub/kamo-ai-hackerton/models')

from models.recommend_rest_loaction.recommend_rest_gpt import RecommendRestGpt

os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_BASE"] = "https://kmt-oai-uk-37.openai.azure.com/"
os.environ["OPENAI_API_KEY"] = "dbbe0f299cd44d38ba566abf5202f52d"
os.environ["OPENAI_API_VERSION"] = "2023-07-01-preview"

def get_recommend_rest_location(lat, lon):
    recommend_rest_gpt = RecommendRestGpt(azure_deployment="gpt-4")
    result = recommend_rest_gpt.predict(lat, lon)
    return result
