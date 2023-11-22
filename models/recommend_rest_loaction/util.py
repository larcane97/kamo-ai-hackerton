import requests
import json
from haversine import haversine

def get_hcode_coord(hcode):
    hcode_url = f"http://navi-facility-api.dev.onkakao.net/internal/region/v1/hcode_by_code/?code={hcode}&locale=ko&service=hackathon"
    response = requests.get(hcode_url).json()
    x = response['x']
    y = response['y']
    return [x,y]


def get_detail_coord(name, hcode_x, hcode_y, radius):
    headers={
        "Content-type" : "application/json",
        "Authorization" : "KakaoAK ad47acc7167c0a53565e938d1f2586e6"
    }
    query ,x,y,radius = name, hcode_x,hcode_y,radius
    kakao_url = f"https://dapi.kakao.com/v2/local/search/keyword.json?query={query}&x={x}&y={y}&radius={radius}"
    try:
        response = requests.get(kakao_url, headers=headers).json()['documents'][0]
        return [response['y'], response['x']]
    except:
        return ['0','0']

# coord = get_hcode_coord(1171071000)
# detail_coord = get_detail_coord("서울책보고", coord[0], coord[1], 1000)
# print(detail_coord)


def get_detail_coord_with_hcode(row):
    name, hcode = row['poi_name'], row['hcode']
    coord = get_hcode_coord(hcode)
    return (get_detail_coord(name, coord[0], coord[1], 1000))


def get_distance(coord1, coord2):
    try:
        return haversine((float(coord1[0]), float(coord1[1]) ), coord2, "m")
    except:
        return 10000

