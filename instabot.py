print "hello"
import requests;
def getDetails():
    url = "https://api.instagram.com/v1/users/search?q=niravnikhil&access_token=5793537413.13b9c2a.0e37b8ae91714cdfab5ae87559175055";
    obj = requests.get(url);
    print obj.json();
getDetails();

