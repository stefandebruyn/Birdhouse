import requests
import xml.etree.ElementTree as ET

zwsid = 'X1-ZWz18ayeq7khl7_32ywy'
state = '';
city = '';
childType = '';
county = '';

url1 = 'http://www.zillow.com/webservice/GetRegionChildren.htm?zws-id=' + zwsid;
url2 = 'state=' + state + '&city=' + city + '&childtype=' + childType + '&county=' + county;


getZillowInfo = requests.get(url1+url2);
zillowXML = ET.parse(getZillowInfo.text)

