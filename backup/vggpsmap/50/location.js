var marker;
var data = [];
var map

function initMap() {
    var MyLatLng = new google.maps.LatLng(35.388023, 139.428457);
    var Options = {
        zoom: 17,      //地図の縮尺値
        center: MyLatLng,    //地図の中心座標
        mapTypeId: 'roadmap'   //地図の種類
    };
    map = new google.maps.Map(document.getElementById('map'), Options);
    getrequest();
}


var getrequest = function () {
    var getresult = "";
    var geturl = "https://icar-svr.sfc.wide.ad.jp/vggps/all_50";
    // APIたたく
    const request = new XMLHttpRequest();
    request.open('GET', geturl);
    request.onreadystatechange = function () {
        if (request.readyState != 4) {
            // リクエスト中!なんも書くな!!
        } else if (request.status != 200) {
            // 失敗
        } else {
            // 取得成功
            getresult = request.responseText;
            var lastdata = sessionStorage.getItem('jsondata');
            sessionStorage.clear();
            sessionStorage.setItem('jsondata', getresult);
            markerfunc(getresult);
        }
    };
    request.send(null); // GETrequestここまで
    // setTimeout(getrequest, 1000);
}


const markerfunc = function (getresult) {
    if (marker !== undefined) {
        marker.setMap(null);
    }
    getresult = sessionStorage.getItem('jsondata');
    getresult = JSON.parse(getresult);
    console.log(getresult);

    for (let index = 0; index < getresult.length; index++) {
        create_marker(getresult[index].lat, getresult[index].lon, getresult[index].SNR, getresult[index].RSRP);
    }
}


function create_marker(lat, lng, SNR, RSRP) {
    console.log(lat)
    if (SNR > 10) {
        incolor = "#5D639E"
    } else if (SNR > 5) {
        incolor = "#0086AB"
    } else if (SNR > 0) {
        incolor = "#23AC0E"
    } else if (SNR > -5) {
        incolor = "#EDAD0B"
    } else {
        incolor = "#C7243A"
    }

    //外側の色
    if (RSRP > -70) {
        outcolor = "#5D639E"
    } else if (RSRP > -80) {
        outcolor = "#0086AB"
    } else if (RSRP > -90) {
        outcolor = "#23AC0E"
    } else {
        outcolor = "#C7243A"
    }
    var marker = new google.maps.Marker({
        map: map,
        position: new google.maps.LatLng(lat, lng),
        animation: google.maps.Animation.DROP,
        icon: {
            fillColor: incolor,                //塗り潰し色
            fillOpacity: 0.8,                    //塗り潰し透過率
            path: google.maps.SymbolPath.CIRCLE, //円を指定
            scale: 9,                           //円のサイズ
            strokeColor: outcolor,              //枠の色
            strokeWeight: 5.0                    //枠の透過率
        }
    });
}
