import requests
import geoip2.database
ip_address = '202.96.99.60' # 杭州西湖
# ip_address = '103.172.41.202' #香港湾仔

from geopy.geocoders import Nominatim
from ip2region.binding.python.iptest import searchWithContent
def state_finder(long, lat):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.reverse(lat + "," + long)
    address = location.raw['address']
    return address

def check_ip(ip_address):

 
    region_str = searchWithContent(ip_address)

    reader = geoip2.database.Reader('GeoLite2-City.mmdb')

    response = reader.city(ip_address)

    print("地区：{}({})".format(response.continent.names["es"],
                                        response.continent.names["zh-CN"]))

    print("国家：{}({}) ，简称:{}".format(response.country.name,
                                                            response.country.names["zh-CN"],
                                                            response.country.iso_code))
    try:
        print("洲／省：{}({})".format(response.subdivisions.most_specific.name,
                                            response.subdivisions.most_specific.names["zh-CN"]))
        print("城市：{}({})".format(response.city.name, 
                                            response.city.names["zh-CN"]))
        print("邮编:{}".format(response.postal.code))
    except Exception as e:
        pass

    print("经度：{}，纬度{}".format(response.location.longitude,
                                                response.location.latitude))

    print("时区：{}".format(response.location.time_zone))
    
    longitude = str(response.location.longitude)
    latitude = str(response.location.latitude)
    reader.close()


    if region_str.split('|')[-1] == '0':
        # addr = state_finder(longitude,latitude)
        res = requests.get(f'https://api.vore.top/api/IPdata?ip={ip_address}')
        res = res.json()
        addr = res['adcode']['n']

    else: 
        addr = region_str.split('|')[2]+'-'+region_str.split('|')[3]
        
    if response.country.names["zh-CN"]  in ["香港","澳门","中国"]:
        response.country.names["zh-CN"]  =  "中国"
    addr = response.country.names["zh-CN"] + '-'+ addr

    return addr,longitude,latitude

if __name__ == '__main__':
    print(check_ip(ip_address))