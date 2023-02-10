from flask import Flask, render_template, request
from text_generation import ApiTextGeneration


class BookPrompt:
    book_prompt = None


book = BookPrompt()
api_text_generation = ApiTextGeneration()
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    story = [
        '\n\nOnce upon a time, there were three dogs named Max, Daisy, and Toby They were all very different, but they were the best of friends',
        ' \n\nMax was a big, strong Labrador Retriever He was always the leader of the pack, and he was always ready for a new adventure Daisy was a small, sweet Chihuahua She was always the one to keep everyone in line, and she was always ready to cuddle Toby was a medium-sized Beagle He was always the one to make everyone laugh, and he was always ready to play',
        ' \n\nThe three dogs had been living on the streets for a while, but they were always looking for a new home One day, they were walking down the street when they came across a big, beautiful house They looked in the windows and saw a family inside They were so excited! \n\nThe dogs knocked on the door, and the family welcomed them']

    if request.method == "POST":
        book.book_prompt = request.form.get("book-prompt")  # getting input from form with name = book-prompt
        api_text_generation.enter_prompt(book.book_prompt)
        api_text_generation.generate_image_urls(api_text_generation.story)

    generate_book = False
    try:
        if len(book.book_prompt) > 1:
            generate_book = True
    except TypeError:
        print("A prompt hasn't been entered yet")
    return render_template("HomePage.html", generate_book=generate_book)


class PageNumber:
    page = 0


page_number = PageNumber()


@app.route("/page", methods=["GET", "POST"])
def page():
    book.book_prompt = None
    image = "http://cliparts.co/cliparts/rcj/GgB/rcjGgBKdi.png"
    story = ['\n\nOnce upon a time, there were three dogs named Max, Daisy, and Toby They were all very different, but they were the best of friends', ' \n\nMax was a big, strong Labrador Retriever He was always the leader of the pack, and he was always ready for a new adventure Daisy was a small, sweet Chihuahua She was always the one to keep everyone in line, and she was always ready to cuddle Toby was a medium-sized Beagle He was always the one to make everyone laugh, and he was always ready to play', ' \n\nThe three dogs had been living on the streets for a while, but they were always looking for a new home One day, they were walking down the street when they came across a big, beautiful house They looked in the windows and saw a family inside They were so excited! \n\nThe dogs knocked on the door, and the family welcomed them']
    if request.method == "POST":
        if request.form.to_dict()["switch-page"] == ">":
            print(page_number.page)
            print(request.form.to_dict()["switch-page"])
            if page_number.page < len(story)-1:
                page_number.page += 1
        else:
            print(page_number.page)
            print(request.form.to_dict()["switch-page"])
            if page_number.page != 0:
                page_number.page -= 1
    story_text = api_text_generation.story[page_number.page]
    image_url = api_text_generation.image_urls[page_number.page]
    return render_template("PageDesign.html",
                           story_text=story_text,
                           image_url=image_url)


if __name__ == "__main__":
    app.run(debug=True)
