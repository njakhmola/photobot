import urllib
import requests
from keys import ACCESS_TOKEN
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
insta_user_name='jakhmolanidhi22'
BASE_URL = 'https://api.instagram.com/v1/'
# get self info
def self_info():
  request_url = (BASE_URL + 'users/self/?access_token=%s') % (ACCESS_TOKEN)
  print 'Requesting info for:'+  (request_url)
  my_info = requests.get(request_url).json()
  print 'my info is/n',my_info
self_info();


def getDetails():
    url = "https://api.instagram.com/v1/users/search?q=niravnikhil&access_token=5793537413.13b9c2a.0e37b8ae91714cdfab5ae87559175055";
    obj = requests.get(url);
    print obj.json();
getDetails();

def get_user_id(insta_user_name):
  request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_user_name, ACCESS_TOKEN)
  print 'GET request url : %s' % (request_url)
  user_info = requests.get(request_url).json()
  print 'user info is/n',user_info
  if user_info['meta']['code'] == 200:
    if len(user_info['data']):
      return user_info['data'][0]['id']
      print 'Username: %s' % (user_info['data']['username'])
      print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
      print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
      print 'No. of posts: %s' % (user_info['data']['counts']['media'])
    else:
      return None
  else:
    print 'Something went wrong..please try later!'
    exit()

get_user_id(insta_user_name);

def get_own_post():
  request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (ACCESS_TOKEN)
  print 'GET request url: %s' % (request_url)
  own_media=requests.get(request_url).json()
  if (own_media['meta']['code']) == 200:
    if len(own_media['data']):
     return own_media['data'][0]['id']
    else:
     print 'no post to show'
  else:
    print 'something is wrong'
    return None

get_own_post();



def get_user_post(insta_user_name):
  user_id=get_user_id(insta_user_name)
  if user_id == None:
    print 'User does not exist'
    exit
  request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id , ACCESS_TOKEN)
  print 'GET request url: %s' % (request_url)
  user_media=requests.get(request_url).json()
  # print 'user media/n',user_media
  if user_media['meta']['code'] == 200:
    if len(user_media['data']):
      image_name = user_media['data'][0]['id'] + '.jpeg'
      image_url = user_media['data'][0]['images']['standard_resolution']['url']
      urllib.urlretrieve(image_url, image_name)
      print 'Your image has been downloaded!'
    else:
      print 'Post does not exist!'
  else:
    print 'Something went wrong..please try later!'

get_user_post(insta_user_name)



def get_id_post(insta_user_name):
  user_id=get_user_id(insta_user_name)
  if user_id == None:
    print 'User does not exist'
    exit
  request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id , ACCESS_TOKEN)
  print 'GET request url: %s' % (request_url)
  user_media=requests.get(request_url).json()
  if user_media['meta']['code'] == 200:
    if len(user_media['data']):
      return user_media['data'][0]['id']
    else:
      print 'Post does not exist!'
  else:
    print 'Something went wrong..please try later!'

get_id_post(insta_user_name);



def like_user_post(insta_username):
  media_id = get_id_post(insta_username)
  request_url = (BASE_URL + 'media/%s/likes') % (media_id)
  payload = {"access_token": ACCESS_TOKEN}
  print 'POST request url : %s' % (request_url)
  like_media = requests.post(request_url, payload).json()
  if like_media['meta']['code'] == 200:
    print 'Like was successful!'
  else:
    print 'Your like was unsuccessful. Try again!'
like_user_post(insta_user_name)


def comment_user_post(insta_username):
  media_id=get_id_post(insta_user_name)
  text_comment=raw_input('enter your text:')
  request_url = (BASE_URL + 'media/%s/comments') % (media_id)
  payload = {"access_token": ACCESS_TOKEN , "text":text_comment}
  print 'POST request url : %s' % (request_url)
  comment_media = requests.post(request_url, payload).json()
  if comment_media['meta']['code'] == 200:
    print 'comment was successful!'
  else:
    print 'Your comment was unsuccessful. Try again!'
comment_user_post(insta_user_name)


# def delete_comments(insta_username):
#   media_id=get_id_post(insta_user_name)

def delete_negative_comment(insta_user_name):
    media_id = get_id_post(insta_user_name)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            #Here's a naive implementation of how to delete the negative comments :)
            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print 'Negative comment : %s' % (comment_text)
                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (media_id, comment_id, ACCESS_TOKEN)
                    print 'DELETE request url : %s' % (delete_url)
                    delete_info = requests.delete(delete_url).json()

                    if delete_info['meta']['code'] == 200:
                        print 'Comment successfully deleted!\n'
                    else:
                        print 'Unable to delete comment!'
                else:
                    print 'Positive comment : %s\n' % (comment_text)
        else:
            print 'There are no existing comments on the post!'
    else:
        print 'Status code other than 200 received!'


def start_bot():
    while True:
        print '\n'
        print 'Hey! Welcome to instaBot!'
        print 'Here are your menu options:'
        print "a.Get your own details\n"
        print "b.Get details of a user by username\n"
        print "c.Get your own recent post\n"
        print "d.Get the recent post of a user by username\n"
        print "e.Get a list of people who have liked the recent post of a user\n"
        print "f.Like the recent post of a user\n"
        print "g.Get a list of comments on the recent post of a user\n"
        print "h.Make a comment on the recent post of a user\n"
        print "i.Delete negative comments from the recent post of a user\n"
        print "j.Exit"

        choice = raw_input("Enter you choice: ")
        if choice == "a":
            self_info()
        elif choice == "b":
            insta_username = raw_input("Enter the username of the user: ")
            getDetails(insta_user_name)
        elif choice == "c":
            get_own_post()
        elif choice == "d":
            insta_user_name = raw_input("Enter the username of the user: ")
            get_user_post(insta_username)
        elif choice=="e":
           insta_username = raw_input("Enter the username of the user: ")
           like_user_post(insta_username)
        elif choice=="f":
           insta_username = raw_input("Enter the username of the user: ")
           comment_user_post(insta_username)
        elif choice=="g":
           insta_username = raw_input("Enter the username of the user: ")
           delete_negative_comment(insta_username)
        elif choice == "h":
            exit()
        else:
            print "wrong choice"

start_bot()