import os
import openai
from dotenv import load_dotenv
from nltk.corpus import wordnet

load_dotenv()
API_KEY = os.getenv("API_KEY")


class ApiTextGeneration:
    openai.api_key = API_KEY

    def __init__(self):
        self.story = None
        self.image_urls = None
        # self.image_url = "https://oaidalleapiprodscus.blob.core.windows.net/private/org-yRcXMvcPi7VsHrtkbNk9Oifz/user-ZpMTT4g5ZYkDyu6NwLAkLyAf/img-OO9KWaOBKIMEYOHCaDuOyB3e.png?st=2023-01-22T22%3A25%3A01Z&se=2023-01-23T00%3A25%3A01Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2023-01-22T18%3A35%3A49Z&ske=2023-01-23T18%3A35%3A49Z&sks=b&skv=2021-08-06&sig=9e2dWLjvfhOmiL/qyEXJT5BqYeWAvrKBL8/mPUa9WD8%3D"

    def enter_prompt(self, user_input):
        """Takes a string input that is sent to openai then takes the response and stores it in the variable
        self.story."""

        prompt = user_input
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.4,
            max_tokens=250
        )

        text = response["choices"][0]["text"]
        sentences = text.split(".")

        # Creates a list of paragraphs with three sentences in each
        story = []
        count = 0
        paragraph = ""
        for sentence in sentences:
            count += 1
            if count % 3 != 0:
                paragraph += sentence + "."
            else:
                paragraph += sentence
            if count % 3 == 0:
                story.append(paragraph)
                paragraph = ""
            elif count == len(sentences):
                story.append(paragraph)

        self.story = story

    def __generate_image_prompt(self, text):
        image_prompt_lst = ["A drawing of", "insert noun", "insert noun"]
        word_list = text.split(" ")
        lexnames = []
        for word in word_list:
            syns = wordnet.synsets(word)
            lexnames.append([word, syns[0].lexname()] if syns else [word, None])
        for lexname in lexnames:
            if lexname[1] == "noun.quantity":
                image_prompt_lst[1] = lexname[0]
            elif lexname[1] == "noun.animal":
                image_prompt_lst[2] = lexname[0]
        image_prompt = " ".join(image_prompt_lst)
        return image_prompt

    def __image_generation(self, image_prompt):
        """Generates an image url from a given prompt"""
        response = openai.Image.create(
            prompt=image_prompt,
            n=1,
            size="1024x1024"
        )
        image_url = response['data'][0]['url']
        return image_url

    def generate_image_urls(self, story_text: list):
        """Generates image urls from a list of prompts and saves the urls as a list in self.image_urls"""
        image_urls = []
        for text in story_text:
            # image_prompt = self.__generate_image_prompt(text)

            image_urls.append(self.__image_generation("A digital image of " + text))

        self.image_urls = image_urls

