import requests
from PIL import Image
from io import BytesIO
import pytesseract
from bs4 import BeautifulSoup


# URL of the page with the captcha
url = "http://captcha.challs.olicyber.it/"

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
}

def process_page(session, page_content):
    # Parse the page to find the image URL using BeautifulSoup
    soup = BeautifulSoup(page_content, "html.parser")
    img_tag = soup.find("img")  # Find the first image tag

    if not img_tag or not img_tag.get("src"):
        raise ValueError("Captcha image not found on the page.")

    captcha_image_url = img_tag["src"]
    if not captcha_image_url.startswith("http"):
        captcha_image_url = requests.compat.urljoin(url, captcha_image_url)

    image_response = session.get(captcha_image_url)

    captcha_image = Image.open(BytesIO(image_response.content))
    solution = solve_captcha(captcha_image)

    # Submit the solution in the same session
    data = {
        "risposta": solution,
    }
    post_response = session.post(url + '/next', headers=headers, data=data)

    return solution, post_response

def solve_captcha(image):
    # Use pytesseract to extract text from the image
    text = pytesseract.image_to_string(image, config="--psm 6 digits")
    return text.strip()

if __name__ == "__main__":
        with requests.Session() as session:
            response = session.get(url)

            for _ in range(100):  # Loop for solving 100 captchas
                solution, response = process_page(session, response.text)
                print(f"Extracted Captcha: {solution}")
                print(f"progress: {_}/100")
            
            print(response.text)
