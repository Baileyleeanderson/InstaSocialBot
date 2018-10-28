from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random

def print_same_line(text):
    sys.stdout.write('\r')
    sys.stdout.flush()
    sys.stdout.write(text)
    sys.stdout.flush()

class InstagramBot:

    def __init__(self, username, password, follow_userID, hashtag, location, location_hashtag, searchtype):
        self.username = username
        self.password = password
        self.hashtag = hashtag
        self.location = location
        self.location_hashtag = location_hashtag
        self.follow_userID = follow_userID
        self.searchtype = searchtype

        # use these lines for headless operations
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        self.driver = webdriver.Chrome(chrome_options = options)
        
        #use below line instead to show its operations
        # self.driver = webdriver.Chrome()

    def closeBrowser(self):
        self.driver.close()

    def login(self):
        driver = self.driver
        driver.get("https://www.instagram.com/")
        time.sleep(3)
        login_page = driver.find_element_by_xpath("/html/body/span/section/main/article/div[2]/div[2]/p/a")
        login_page.click()
        time.sleep(2)
        user_name_elem = driver.find_element_by_xpath("//input[@name='username']")
        user_name_elem.clear()
        user_name_elem.send_keys(self.username)
        password_elem = driver.find_element_by_xpath("//input[@name='password']")
        password_elem.clear()
        password_elem.send_keys(self.password)
        login_button = driver.find_element_by_xpath("/html/body/span/section/main/div/article/div/div[1]/div/form/div[3]/button")
        time.sleep(2)
        login_button.click()
        time.sleep(2)

        if self.searchtype == "hashtag":
            self.like_photo()
        elif self.searchtype == "username":
            self.follow_users()
        elif self.searchtype == "location":
            self.like_geo_location()
#_______________________________________________________________________________
    def like_photo(self):
        driver = self.driver
        pics_liked = 0
        accounts_followed = 0
        total_pics_liked = 0
        driver.get("https://www.instagram.com/explore/tags/" + self.hashtag + "/")
        time.sleep(2)

        # gathering photos
        pic_hrefs = []
        for i in range(1, 2): #page scroll range to gather photos
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                # get tags
                hrefs_in_view = driver.find_elements_by_tag_name('a')
                # finding relevant hrefs
                hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view if
                                 self.hashtag in elem.get_attribute('href')]
                # building list of unique photos
                [pic_hrefs.append(href) for href in hrefs_in_view if href not in pic_hrefs]
                print("Check: pic href length " + str(len(pic_hrefs)))
            except Exception:
                continue

        # Liking photos
        unique_photos = len(pic_hrefs)
        print ("length of pic list" + str(len(pic_hrefs)))
        for pic_href in pic_hrefs:
            driver.get(pic_href)
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                time.sleep(random.randint(2,3))
                like_bttn = driver.find_elements_by_xpath('/html/body/span/section/main/div/div/article/div[2]/section[1]/span[1]/button')
                aria_label = like_bttn[0].find_element_by_css_selector('span').get_attribute("aria-label")
                
                if (pics_liked == 15):
                    follow_button = driver.find_elements_by_tag_name("button")
                    follow_button_text = follow_button[0].text
                    print('followtext ' + follow_button_text)
                    if (follow_button_text == "Follow"):
                        follow_button[0].click()
                        accounts_followed += 1
                        print ("Followed " + str(accounts_followed) + " accounts")
                        pics_liked = 0
                        time.sleep(2)

                if aria_label == "Like":
                    time.sleep(random.randint(121, 130)) # time parameters for wait to like
                    pics_liked += 1 
                    total_pics_liked += 1
                    print ("Liked " + str(total_pics_liked) + " pics")
                    like_button = lambda: driver.find_element_by_xpath('/html/body/span/section/main/div/div/article/div[2]/section[1]/span[1]/button').click()
                    like_button().click()
                    for second in reversed(range(0, random.randint(18, 28))):
                        print_same_line("#" + self.hashtag + ': unique photos left: ' + str(unique_photos)
                                        + " | Sleeping " + str(second))
                        time.sleep(1)         
                
            except Exception as e:
                time.sleep(2)
            unique_photos -= 1
#_______________________________________________________________________________
    def follow_users(self):
        unfollowed_userList = []
        all_user_list_length = 0
        user_num = 1
        not_followed_list_num = 0
        driver = self.driver
        driver.get("https://www.instagram.com/" + self.follow_userID + "/")
        time.sleep(2)
        
        # bot clicks all users who follow account
        followers_button = driver.find_element_by_xpath("/html/body/span/section/main/div/header/section/ul/li[2]/a/span")
        followers_button.click()
        time.sleep(2)

        # bot scrolls down the followers pop up to display more of them
        followers_elem_popup = driver.find_element_by_xpath("/html/body/div[3]/div/div/div[2]")

        for i in range (0, 50):
            followers_elem_popup.send_keys(Keys.END)
            time.sleep(1)
        
        # creates a list of users to follow
        all_follow_buttons = driver.find_elements_by_tag_name("button")
        for buttn in all_follow_buttons:
            all_user_list_length += 1

        for follow_button in all_follow_buttons:
            # there are five extra buttons that is why its - 4
            if (user_num < all_user_list_length - 4):
                follow_user_button = driver.find_element_by_xpath("/html/body/div[3]/div/div/div[2]/ul/div/li[" + str(user_num) + "]/div/div[2]/button")

                if (follow_user_button.text == "Follow"):
                    new_account_to_follow = follow_user_button        
                    unfollowed_userList.append(user_num) 
            user_num += 1

        print ("list" + str(len(unfollowed_userList)))

        for bttn in unfollowed_userList:
            list_index_value = unfollowed_userList[not_followed_list_num]
            follow_user_button = driver.find_element_by_xpath("/html/body/div[3]/div/div/div[2]/ul/div/li[" + str(list_index_value) + "]/div/div[2]/button")
            follow_user_button.click()
            timeDelay = random.randrange(180, 450)
            time.sleep(timeDelay)
            not_followed_list_num += 1    
#_______________________________________________________________________________
    def like_geo_location(self):
        driver = self.driver
        driver.get("https://www.instagram.com/explore/locations/" + self.location + "/")
        liked_photos = 0
        accounts_followed = 0
        time.sleep(2)

        pic_hrefs = []
        for i in range(1,100):
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                hrefs_in_view = driver.find_elements_by_tag_name('a')
                hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view if self.location in elem.get_attribute('href')]
                [pic_hrefs.append(href) for href in hrefs_in_view if href not in pic_hrefs]
            except Exception:
                continue

        # Liking photos
        unique_photos = len(pic_hrefs)
        print ("length of pic list" + str(len(pic_hrefs)))

        for pic_href in pic_hrefs:
            driver.get(pic_href)
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            #find the user post
            try:
                user_post = driver.find_element_by_xpath("/html/body/span/section/main/div/div/article/div[2]/div[1]/ul/li[1]/div/div/div/span")

                #find all <a> tags and push href text into list
                elems = user_post.find_elements_by_tag_name('a')
                all_elems = []
                #these are the hashtags they wrote
                for e in elems:
                    all_elems.append(e.text)
                    
                for href in all_elems:
                    if self.location_hashtag not in href:
                        continue
                    else:
                        #like photo if not liked
                        time.sleep(random.randint(3, 8)) #amount of time to like a photo
                        follow_buttn = driver.find_element_by_xpath("/html/body/span/section/main/div/div/article/header/div[2]/div[1]/div[2]/button")
                        button_text = follow_buttn.text
    
                        if (button_text == "Follow"):
                            follow_buttn.click()
                            accounts_followed += 1
                            print("Followed " + str(accounts_followed) + " accounts")

                        time.sleep(2)   
                        like_bttn = driver.find_elements_by_xpath("/html/body/span/section/main/div/div/article/div[2]/section[1]/span[1]/button")
                        aria_label = like_bttn[0].find_element_by_css_selector('span').get_attribute("aria-label")
                        print("aria_label " + aria_label)

                        if (aria_label == "Like"):
                            like_bttn[0].click()
                            liked_photos += 1
                            print ("Liked " + str(liked_photos) + "Photos")
                        time.sleep(2)
                        unique_photos -= 1
            except Exception:
                continue 
                       



    