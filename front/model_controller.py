import os

from models.event_push.event_push_gpt import EventPushGpt
from models.recommend_cafe_location.recommend_cafe_gpt import RecommendCafeGpt

from models.recommend_rest_loaction.recommend_rest_gpt import RecommendRestGpt
from models.recommend_call_location.recommend_call_location_gpt import RecommendCallLocationGpt

# os.environ["OPENAI_API_TYPE"] = "azure"
# os.environ["OPENAI_API_BASE"] = "https://kmt-oai-uk-37.openai.azure.com/"
# os.environ["OPENAI_API_KEY"] = "dbbe0f299cd44d38ba566abf5202f52d"
# os.environ["OPENAI_API_VERSION"] = "2023-07-01-preview"
import dotenv
dotenv.load_dotenv()

recommend_rest_gpt = None
recommend_call_gpt = None
recommend_cafe_gpt = None
event_push_gpt = None


def get_recommend_rest_location(lat, lon, driver_type, current_time=None):
    global recommend_rest_gpt
    if recommend_rest_gpt is None:
        recommend_rest_gpt = RecommendRestGpt(azure_deployment="gpt-4")

    result = recommend_rest_gpt.predict(
        driver_lat=lat, driver_lon=lon, driver_type=driver_type, current_time=current_time)
    return result


def get_recommend_call_location(lat, lon, current_time=None):
    global recommend_call_gpt
    if recommend_call_gpt is None:
        recommend_call_gpt = RecommendCallLocationGpt(azure_deployment="gpt-4")

    result = recommend_call_gpt.predict(lat, lon, current_time=current_time)
    return result


def get_recommend_cafe_loaction(lat, lon):
    global recommend_cafe_gpt
    if recommend_cafe_gpt is None:
        recommend_cafe_gpt = RecommendCafeGpt(azure_deployment="gpt-4")

    result = recommend_cafe_gpt.predict(lat, lon)
    return result


def get_event_push(event_type, current_time=None):
    global event_push_gpt
    if event_push_gpt is None:
        event_push_gpt = EventPushGpt(azure_deployment="gpt-4")

    result = event_push_gpt.predict(event_type=event_type, driver_id=1, current_time=current_time)
    return result
