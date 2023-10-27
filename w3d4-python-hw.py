# Exercise 1
# Describe in your own words the following concepts and 
# give an analogy tying to a real-world concept.

# Difference between a Class and an Object
# A class is like a blueprint for creating objects. It contains attributes and methods that objects in a class will have. An object is an instance of a class. In our exercise(s) earlier this week we had a Car class, that was the blueprint for a car and the object was a particular car.

# Encapsulation
# Encapsulation is like packaging or wrapping a gift.The wrapping aka encapsulation hides the internal details.

# Inheritance
# Inheritance allows a child class to inherit attributes and methods from a parent class. Similar to the way trits and characteristics are passed down from parents to their children.

# Polymorphism
# Allows for a function or object to take on multiple forms. The idea that comes to mind is how water takes on different forms depending on context. If it's below 0 degrees, it takes the form of ice. For hygiene, it is used to cleanse/wash. In consumption, it is used to hydrate, etc..

# Abstraction
# Abstraction hides the details to the user. The user doesn't see any of the backend stuff. They only see fields that they interact with. It's like having a mobile phone, you don't know how it connects to a mobile network or the process to send a message or make a call, you just know that when you hit "send" that the call or message will be sent.



# Exercise 2 (Optional):
# Discuss what other classes, methods, or fields (attributes) we could make to improve our streaming service using these principles.

# Start making a few of them and see where it leads. Make sure you either write out your thoughts in the below cell or comment where you added code to the above Classes.


from datetime import timedelta, date
from sys import displayhook
from IPython.display import Image
import requests
from time import sleep

generic_image = 'codeflix.png'

class Video():
    
    generic_image = 'codeflix.png'
    def __init__(self):
        self.title = None
        self.length = timedelta()
        self.link = generic_image
        
    def play(self):
        print(f"Now playing {self.title} \nSummary: \n {self.summary}") # added \nSummary: \n {self.summary} to display summary for each episode
        displayhook(Image(url = self.link))
        
    def __len__(self):
        return self.length
        
    def __repr__(self):
        return f"{self.title} is {self.length.seconds} seconds long"

class Episode(Video):
    def __init__(self, data):
        Video.__init__(self)
        self.number = data['number']
        self.season = data['season']
        self.date_aired = data['airdate']
        self.summary = data['summary']
        self.rating = data['rating']['average']
        self.title = data['name']
        self.length = timedelta(minutes = data['runtime'])
        if data['image']:
            self.link = data['image']['medium']

class Series():
    def __init__(self):
        self.id = None
        self.network = None
        self.seasons = None
        self.summary = None
        self.title = None
        self.genres = []
        self.episodes = []
        
    def get_info(self, query = ''):
        data = None 
        while not data:
            if not query:
                query = input("What is the name of the series? ")
                
            r = requests.get(f"https://api.tvmaze.com/singlesearch/shows?q={query}")
            if r.status_code == 200:
                data = r.json()
            else:
                print(f"Series Error: {r.status_code}")
                

        self.id = data['id']
        self.title = data['name']
        self.genres = data['genres']
        self.summary = data['summary'] # added this line to address why summary wasn't displaying
        if data['network']:
            self.network = data['network']['name']
        else:
            self.network = data['webChannel']['name']
            
            

        r = requests.get(f"https://api.tvmaze.com/shows/{self.id}/episodes")
        if r.status_code == 200:
            episodes = r.json() 
            self.seasons = episodes[-1]['season']
            self.episodes = [Episode(ep) for ep in episodes] 
            print(f"{self.title} has {len(self.episodes)} episodes")
        else:
            print(f"Print Episode Error: status_code {r.status_code}")
            
    def watch(self):
        for i in range(len(self.episodes)):
            if i > 0 and i % 3 == 0:
                watching = input("Are you still watching? Also, get a job y/n ")
                if watching.lower().strip() not in ("yes", "y", "yeah", "ye", "affirmative", "si", "indeed"):
                    break
            self.episodes[i].play()
            sleep(self.episodes[i].length.seconds/1000)

    def __len__(self):
        return len(self.episodes)

    def __repr__(self):
        return f"Title: {self.title}"

my_show = Series()

my_show.get_info("Scrubs")

my_show.watch()

class User:
    __id_counter = 1 
    def __init__(self, username, password):
        self.username = username
        self.id = User.__id_counter
        self.password = password[::-2]
        User.__id_counter += 1
        self.watch_list = []
        
    def __str__(self):
        formatted_user = f"""
        {self.id} - {self.username.title()}
        pw: {self.password}
        """
        
        return formatted_user
    
    def __repr__(self):
        return f"<User {self.id} | {self.username}>"
    
    def check_password(self, password_guess):
        return self.password == password_guess[::-2]
    
class Theater():
    def __init__(self):
        self.users = set()
        self.current_user = None
        
   
    def add_user(self):
        username = input("Please enter a username: ")
        
        if username in {u.username for u in self.users}:
            print('User with that name already exists. Please try again!')
        else:
            password = input("Please enter your password: ")
            user = User(username, password)
            self.users.add(user)
            print(f"{user} has been created!!!")
            
        self.login_user()
        
#       Login user
    def login_user(self):
        username = input("What is your username? ")
        password = input("What is your password? ")
        
        for user in self.users:
            if user.username == username and user.check_password(password):
                self.current_user = user
                print(f"{user} has logged in!")
                break
        else:
            print("Username and/or password is incorrect!")
            
#        Logout user
    def logout(self):
        self.current_user = None
        print("You have successfully been logged out!")
        
#       Update user
    def update_user(self):
        if self.current_user:
            print(self.current_user)
            new_user = input("Please enter the updated username or enter skip to keep your current username")
            if new_user.lower() != "skip":
                self.current_user.username = new_user
            new_pw = input("Please enter the updated password or enter skip to keep current password")
            if new_pw != "skip":
                self.current_user.password = new_pw
            print(f"{self.current_user.username}'s info has been updated!")
        else:
            print("Please login to update your information")
            self.login_user()
            
# --------------------------------------------------------------------------------------------------
# watchlist section

# add to watch list
    def add_to_watchlist(self, query=""):
        if self.current_user:
            show = Series()
            show.get_info(query)
            self.current_user.watch_list.append(show)
            
            print(f"{show.title} has been added to the watchlist!")
            
        else:
            print("please sign in to add to your watchlist")
            self.login_user()
            
    # view watchlist
    def view_watch_list(self):
        if self.current_user:
            for series in self.current_user.watch_list:
                print(f"\n\n{series} | Episodes: {(len(series))}")
                print(f"\nSummary: \n {series.summary}")
                displayhook(Image(series.episodes[0].link))
        else:
            print("please sign in to add to your watchlist")
            self.login_user()
            
#    remove from watchlist
    def delete(self):
        if self.current_user:
            print("Your current watchlist: ")
            self.view_watch_list()
            
            response = input("What would you like to remove from your watchlist? ")
            
            for series in self.current_user.watch_list:
                if series.title.title() == response.title():
                    self.current_user.watch_list.remove(series)
                    print(f"{response.title()} has been removed from your watchlist!")
                    break
            else:
                print("That title is not in your watchlist! You GOON!") # 404 error
                
            self.view_watch_list()
            
        else:
            print("please sign in to add to your watchlist")
            self.login_user()
            
    def choose_from_watch_list(self):
        if self.current_user:
            self.view_watch_list()
            
            watch = input("What would you like to watch? ")
            for series in self.current_user.watch_list:
                if series.title.lower() == watch.lower().strip():
                    series.watch()
                    break
            else:
                response = input(f"{watch} is not in your watchlist... would you like to add it? y/n ")
                if response in ("yes", "y"):
                    self.add_to_watchlist(watch)
                    
                    print(".........")
                    sleep(2)
                    print("...............")
                    self.current_user.watch_list[-1].watch()
        else:
            print("please sign in to add to your watchlist")
            self.log_user()
            
            
            
            

    def run(self):
        """
        Method allowing users to choose a series and play episodes
        """
        displayhook(Image(url=generic_image))
        
        if self.users:
            self.login_user()
        else:
            self.add_user()
            
            print("""
            What would you like to do?
            Add - add a new user
            Login - login to your profile
            Update - update user information
            Logout - Logout of your profile
            Search - search for shows
            Watch - pick something from your watchlist
            View - view your watchlist
            Delete - delete from watchlist
            Quit - close the application
            
            """)
            
        while True:
            response = input("What would you like to do? (add, update, login, search, watch, view, delete, quit?) ").lower()
            
            if response == "search":
                self.add_to_watchlist()
            elif response == "watch":
                self.choose_from_watch_list()
            elif response == "add":
                self.add_user()
            elif response == "logout":
                self.logout()
                new_response = input("What would you like to do next? login, add, quit ").lower()
                if new_response == "add":
                    self.add_user()
                elif new_response == "login":
                    self.login_user()
                elif new_response == "quit":
                    print("thanks for watching!")
                    break
                    
                else:
                    print("Please enter a valid response and try again!")
                    
            elif response == "login":
                self.login_user()
                
            elif response == "update":
                self.update_user()
                
            elif response == "view":
                self.view_watch_list()
                
            elif response == "delete":
                self.delete()
                
            elif response == "quit":
                print(f"Thanks for watching {self.current_user.username}! Now go outside and touch some grass!")
                break
            else:
                print("Please enter a valid input and try again!")

codeflix = Theater()

codeflix.run()