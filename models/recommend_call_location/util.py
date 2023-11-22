import requests


def get_address_by_lat_lng(lat_lng_list):
    headers = {"Content-type": "application/json"}

    if len(lat_lng_list) < 2:
        return []

    query_params = []
    for i in range(0, len(lat_lng_list), 2):
        query_param = f"locations={','.join(map(str, lat_lng_list[i:i + 2]))}"
        query_params.append(query_param)

    facility_url = f"http://navi-facility-api.dev.onkakao.net/region/v1/hcodes?{'&'.join(query_params)}"

    resp = requests.get(facility_url, headers)

    if resp.status_code != 200:
        print(resp.content)
        return None

    return resp.json()


def get_call_demand(lat, lng, current_threshold=2, after_30m_threshold=2, max_num=3):
    header = {"Content-Type": "application/json"}
    body = {
        "center_lat": lat,
        "center_lng": lng,
        "radius": 16,
        "resolution": 7
    }

    model_url = "https://airnd-wheel-gateway-dev.onkm.co.kr/call-demand-forecasting/predict"

    response = requests.post(model_url, json=body, headers=header)

    if response.status_code != 200:
        return None

    data = response.json()["predictions"]["data"]

    current_recommend_call = []
    call_after_30m_recommend_call = []
    for d in data:
        if d["call_now"] >= current_threshold:
            current_recommend_call.extend([d["hex_center"]["lat"], d["hex_center"]["lng"]])
        if d["call_after_30m"] > after_30m_threshold:
            call_after_30m_recommend_call.extend([d["hex_center"]["lat"], d["hex_center"]["lng"]])

    return current_recommend_call[:min(len(current_recommend_call), max_num * 2)], call_after_30m_recommend_call[:min(
        len(call_after_30m_recommend_call), max_num * 2)]


def parsing_address(address: dict):
    addresses = [addr for addr in [address.get('name1', ''), address.get('name2', ''), address.get('name3', '')] if
                 addr != '']
    lat_lng = f"({address['y']}, {address['x']})"
    return " ".join(addresses) + lat_lng
