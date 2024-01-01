import speech recognition as sr
import os
import webbrowser
import openai
from config import apikey
import datetime
import random
import numpy as np
import requests

chatStr = ""
def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"Harry: {query}\n Jarvis: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt= chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    say(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]


def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    text += response["choices"][0]["text"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    # creates a new text file as a response to the asked question to AI (response is devloped by openAI)
    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip() }.txt", "w") as f:
        f.write(text)
        
def search_python_docs(topic):
    base_url = 'https://docs.python.org/3/search.html'
    params = {'q': topic, 'check_keywords': 'yes', 'area': 'default'}

    try:
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            # Extract the relevant information from the response
            # For instance, you might parse the HTML or extract data using regex
            # Here, we're just printing the URL
            print("Here is the Python documentation for", topic)
            print(response.url)
        else:
            print("Failed to fetch documentation.")
    except requests.RequestException as e:
        print("Error fetching documentation:", e)
        
def stack_overflow_search(query):
    base_url = "https://api.stackexchange.com/2.3/search"
    params = {
        "order": "desc",
        "sort": "relevance",
        "site": "stackoverflow",
        "intitle": query,
    }

    try:
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data.get("items"):
                print("Top results from Stack Overflow for:", query)
                for item in data["items"]:
                    print("Title:", item["title"])
                    print("Link:", item["link"])
                    print("-" * 30)
            else:
                print("No results found on Stack Overflow.")
        else:
            print("Failed to fetch results from Stack Overflow.")
    except requests.RequestException as e:
        print("Error fetching Stack Overflow results:", e)

def say(text):
    os.system(f'say "{text}"')

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # r.pause_threshold =  0.6
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some Error Occurred. Sorry from Jarvis"

if __name__ == '__main__':
    print('Welcome to Jarvis A.I')
    say("Jarvis A.I")
    while True:
        print("Listening...")
        query = takeCommand()
        
        #Top 50 websites used by programmers
        sites = [
            ["GitHub", "https://github.com"],
            ["Stack Overflow", "https://stackoverflow.com"],
            ["Medium", "https://medium.com"],
            ["Dev.to", "https://dev.to"],
            ["CodePen", "https://codepen.io"],
            ["MDN Web Docs", "https://developer.mozilla.org"],
            ["Hacker News", "https://news.ycombinator.com"],
            ["Product Hunt", "https://www.producthunt.com"],
            ["GitLab", "https://gitlab.com"],
            ["TechCrunch", "https://techcrunch.com"],
            ["Ars Technica", "https://arstechnica.com"],
            ["The Verge", "https://www.theverge.com"],
            ["TechRadar", "https://www.techradar.com"],
            ["InfoWorld", "https://www.infoworld.com"],
            ["FreeCodeCamp", "https://www.freecodecamp.org"],
            ["Codecademy", "https://www.codecademy.com"],
            ["CSS-Tricks", "https://css-tricks.com"],
            ["Mozilla Developer Network (MDN)", "https://developer.mozilla.org"],
            ["DZone", "https://dzone.com"],
            ["Hackernoon", "https://hackernoon.com"],
            ["SitePoint", "https://www.sitepoint.com"],
            ["Programming Reddit", "https://www.reddit.com/r/programming"],
            ["The Practical Dev", "https://dev.to"],
            ["Coding Horror", "https://blog.codinghorror.com"],
            ["Smashing Magazine", "https://www.smashingmagazine.com"],
            ["CodeProject", "https://www.codeproject.com"],
            ["InfoQ", "https://www.infoq.com"],
            ["ProgrammableWeb", "https://www.programmableweb.com"],
            ["A List Apart", "https://alistapart.com"],
            ["Ray Wenderlich", "https://www.raywenderlich.com"],
            ["Tuts+", "https://tutsplus.com"],
            ["Bitbucket", "https://bitbucket.org"],
            ["Kaggle", "https://www.kaggle.com"],
            ["Coursera", "https://www.coursera.org"],
            ["EdX", "https://www.edx.org"],
            ["Pluralsight", "https://www.pluralsight.com"],
            ["LeetCode", "https://leetcode.com"],
            ["HackerRank", "https://www.hackerrank.com"],
            ["GeeksforGeeks", "https://www.geeksforgeeks.org"],
            ["CodeSignal", "https://codesignal.com"],
            ["Coderbyte", "https://coderbyte.com"],
            ["Topcoder", "https://www.topcoder.com"],
            ["Rosetta Code", "https://rosettacode.org"],
            ["Exercism", "https://exercism.io"],
            ["Stack Exchange", "https://stackexchange.com"],
            ["Codeforces", "https://codeforces.com"],
            ["Atlassian", "https://www.atlassian.com"],
            ["Reddit r/learnprogramming", "https://www.reddit.com/r/learnprogramming"],
            ["Reddit r/coding", "https://www.reddit.com/r/coding"],
            ["Reddit r/webdev", "https://www.reddit.com/r/webdev"],
        ]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])

        #To ask for the time 
        if "the time" in query:
            musicPath = "/Users/harry/Downloads/downfall-21371.mp3"
            hour = datetime.datetime.now().strftime("%H")
            min = datetime.datetime.now().strftime("%M")
            say(f"Sir time is {hour} bajke {min} minutes")

        #Open PyCharm
        elif "open Pycharm".lower() in query.lower():
            os.system(f"open /Applications/PyCharm.app")
        
        #Open VS Code 
        elif "open Pycharm".lower() in query.lower():
            os.system(f"open /Applications/VSCode.app")
        
        #Search for any python documentation
        elif "search python documentation for" in query.lower():
            topic = query.split("for", 1)[-1].strip()
            search_python_docs(topic)
        
        #Stack Overflow Search
        elif "search Stack Overflow for" in query.lower():
            search_query = query.split("for", 1)[-1].strip()
            stack_overflow_search(search_query)

        elif "Using artificial intelligence".lower() in query.lower():
            ai(prompt=query)

        elif "Jarvis Quit".lower() in query.lower():
            exit()

        elif "reset chat".lower() in query.lower():
            chatStr = ""

        else:
            print("Chatting...")
            chat(query)