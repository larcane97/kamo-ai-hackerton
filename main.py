import os

from models.event_push.event_push_gpt import EventPushGpt
from models.recommend_call_location.recommend_call_location_gpt import RecommendCallLocationGpt

os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_BASE"] = "https://kmt-oai-fr-37.openai.azure.com/"
os.environ["OPENAI_API_KEY"] = "7b214487cbbb49058ad896b129b1cafc"
os.environ["OPENAI_API_VERSION"] = "2023-07-01-preview"

if __name__ == "__main__":
    # recommend_location_gpt = RecommendCallLocationGpt(azure_deployment="gpt-4")

    event_push_gpt = EventPushGpt(azure_deployment="gpt-4")

    resp = event_push_gpt.predict(
        event_type="우천 알람",
        driver_id=1,
        current_time="2023-11-21T18:00"
    )
    # resp = recommend_location_gpt.predict(
    #     driver_lat=37.508811,
    #     driver_lng=127.040978,
    #     current_time="2023-11-21T18:00"
    # )

    print(resp)
