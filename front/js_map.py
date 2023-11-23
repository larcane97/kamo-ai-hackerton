import streamlit.components.v1 as components

kakaoJsKey = "290e69ffccf6e3f29446798bb518010d"
def getMap():
    return components.html(
        """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8"/>
            <title>Kakao 지도 시작하기</title>
        </head>
        <body>
            <div id="map" style="width:500px;height:400px;"></div>
            <script type="text/javascript" src="//dapi.kakao.com/v2/maps/sdk.js?appkey=290e69ffccf6e3f29446798bb518010d"></script>
            <script>
                var container = document.getElementById('map');
                var options = {
                    center: new kakao.maps.LatLng(33.450701, 126.570667),
                    level: 3
                };

                var map = new kakao.maps.Map(container, options);
            </script>
        </body>
        </html>
        """
        , height=600
    )

def getMapWithMarkerList(picker , place):

    positions = ""
    for i in range(len(place)):
        poi_name, coord_list = place[i]
        positions+=f"""{{title :'{poi_name}', latlng: new kakao.maps.LatLng({coord_list[0]}, {coord_list[1]}) }},"""
    positions = positions[:-1]

    return components.html(
        f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>여러개 마커 표시하기</title>
                
            </head>
            <body>
            <div id="map" style="width:100%;height:350px;"></div>
            
            <script type="text/javascript" src="//dapi.kakao.com/v2/maps/sdk.js?appkey={kakaoJsKey}"></script>
            <script>
            var mapContainer = document.getElementById('map'), // 지도를 표시할 div  
                mapOption = {{ 
                    center: new kakao.maps.LatLng({picker[0]}, {picker[1]}), // 지도의 중심좌표
                    level: 3 // 지도의 확대 레벨
                }};
            
            var map = new kakao.maps.Map(mapContainer, mapOption); // 지도를 생성합니다
             
            // 마커를 표시할 위치와 title 객체 배열입니다 
            var positions = [{positions}]

            // 마커 이미지의 이미지 주소입니다
            var imageSrc = "https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/markerStar.png"; 
            
            
            //픽커??
            var marker = new kakao.maps.Marker({{
                    map: map, // 마커를 표시할 지도
                    position: new kakao.maps.LatLng({picker[0]}, {picker[1]}), // 마커를 표시할 위치
                }});
            
            //마커 생성
            for (var i = 0; i < positions.length; i ++) {{
                
                // 마커 이미지의 이미지 크기 입니다
                var imageSize = new kakao.maps.Size(24, 35); 
                
                // 마커 이미지를 생성합니다    
                var markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize); 
                // 마커를 생성합니다
                var marker = new kakao.maps.Marker({{
                    map: map, // 마커를 표시할 지도
                    position: positions[i].latlng, // 마커를 표시할 위치
                    title : positions[i].title, // 마커의 타이틀, 마커에 마우스를 올리면 타이틀이 표시됩니다
                    image : markerImage // 마커 이미지 
                }});
                
                // 마커에 표시할 인포윈도우를 생성합니다.
                var infowindow = new kakao.maps.InfoWindow({{
                    content: positions[i].title // 인포윈도우에 표시할 내용
                }});
                
                kakao.maps.event.addListener(marker, 'mouseover', makeOverListener(map, marker, infowindow));
                kakao.maps.event.addListener(marker, 'mouseout', makeOutListener(infowindow));
            }}
            // 인포윈도우를 표시하는 클로저를 만드는 함수입니다 
            function makeOverListener(map, marker, infowindow) {{
                return function() {{
                    infowindow.open(map, marker);
                }};
            }}
            
            // 인포윈도우를 닫는 클로저를 만드는 함수입니다 
            function makeOutListener(infowindow) {{
                return function() {{
                    infowindow.close();
                }};
            }}
            </script>
            </body>
            </html>
        """
        , height=600
    )


def getMapWithPicker(picker):

    return components.html(
        f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>마커 생성하기</title>

        </head>
        <body>
        <div id="map" style="width:100%;height:350px;"></div>
        <script type="text/javascript" src="//dapi.kakao.com/v2/maps/sdk.js?appkey={kakaoJsKey}"></script>
        <script>
        var mapContainer = document.getElementById('map'), // 지도를 표시할 div 
            mapOption = {{ 
                center: new kakao.maps.LatLng({picker[0]}, {picker[1]}), // 지도의 중심좌표
                level: 3 // 지도의 확대 레벨
            }};
        var map = new kakao.maps.Map(mapContainer, mapOption); // 지도를 생성합니다

        // 마커가 표시될 위치입니다 
        var markerPosition  = new kakao.maps.LatLng({picker[0]}, {picker[1]}); 
        // 마커를 생성합니다
        var marker = new kakao.maps.Marker({{
            position: markerPosition
        }});

        // 마커가 지도 위에 표시되도록 설정합니다
        marker.setMap(map);

        // 아래 코드는 지도 위의 마커를 제거하는 코드입니다
        // marker.setMap(null);    
        </script>
        </body>
        </html>
        """
        , height=600
    )