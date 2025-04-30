import random
import threading
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont, ImageOps
import time
import sys
import os
import textwrap
import socket

home = os.path.expanduser("~")
sys.path.append(os.path.join(home, 'e-Paper', 'RaspberryPi_JetsonNano', 'python', 'lib'))
from waveshare_epd import epd2in13_V4

def check_wifi():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

def display_scp(epd, title, object_class, description, scp_image):
    if object_class.lower() == "keter":
        scp_logo = Image.open(os.path.join(home, 'scp_logo.bmp'))
        scp_logo = scp_logo.resize((50, 50)).convert('L')
        scp_logo = ImageOps.invert(scp_logo).convert('1')
        alert_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 20)

        for _ in range(3):
            frame = Image.new('1', (epd.height, epd.width), 0)
            frame_draw = ImageDraw.Draw(frame)
            frame_draw.bitmap(((epd.height - scp_logo.width) // 2, 10), scp_logo, fill=1)
            text = "ALERT. KETER ANOMALY."
            bbox = frame_draw.textbbox((0, 0), text, font=alert_font)
            text_x = (epd.height - (bbox[2] - bbox[0])) // 2
            text_y = (epd.width - (bbox[3] - bbox[1])) // 2
            frame_draw.text((text_x, text_y), text, font=alert_font, fill=1)
            epd.displayPartial(epd.getbuffer(frame))
            time.sleep(0.5)
            frame = Image.new('1', (epd.height, epd.width), 255)
            epd.displayPartial(epd.getbuffer(frame))
            time.sleep(0.5)

    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)
    small_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 10)
    heading_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 16)

    scp_logo = Image.open(os.path.join(home, 'scp_logo.bmp'))
    scp_logo = scp_logo.resize((30, 30))
    scp_logo = ImageOps.invert(scp_logo.convert('L')).convert('1')

    if scp_image:
        try:
            img_response = requests.get(scp_image, timeout=10)
            if img_response.status_code == 200:
                with open('/tmp/scp_temp.jpg', 'wb') as f:
                    f.write(img_response.content)
                temp_img = Image.open('/tmp/scp_temp.jpg').convert('L')
                temp_img = ImageOps.invert(temp_img).resize((40, 40))
            else:
                temp_img = None
        except Exception as e:
            print(f"Image download failed: {e}")
            temp_img = None
    else:
        temp_img = None

    wrapped_text = textwrap.fill(description, width=30)
    text_lines = wrapped_text.split('\n')

    overlay_height = max(len(text_lines) * 12 + 50 + epd.width, epd.width + 100)
    scroll_canvas = Image.new('1', (epd.height, overlay_height), 255)
    draw = ImageDraw.Draw(scroll_canvas)

    y = 50
    for line in text_lines:
        if line.strip().lower().startswith(("addendum", "note")):
            draw.text((5, y), line, font=heading_font, fill=0)
        else:
            draw.text((5, y), line, font=font, fill=0)
        y += 12

    scroll_speed = 0.5

    if overlay_height <= epd.width + 40:
        frame = Image.new('1', (epd.height, epd.width), 255)
        frame_draw = ImageDraw.Draw(frame)

        object_class_font = heading_font if heading_font.getlength(object_class) <= 60 else small_font
        frame_draw.text((5, 0), f"{object_class}", font=object_class_font, fill=0)
        frame_draw.text((70, 0), f"{title}", font=heading_font, fill=0)
        frame_draw.bitmap((epd.height - 35, 0), scp_logo, fill=0)
        frame_draw.line((0, 30, epd.height, 30), fill=0, width=1)

        if check_wifi():
            frame_draw.text((epd.height - 45, epd.width - 15), "WiFi: OK", font=small_font, fill=0)
        else:
            frame_draw.text((epd.height - 45, epd.width - 15), "WiFi: ERR", font=small_font, fill=0)

        if temp_img:
            frame.paste(temp_img, (epd.height - 45, epd.width - 45))

        scroll_part = scroll_canvas.crop((0, 0, epd.height, epd.width))
        frame.paste(scroll_part, (0, 50))

        epd.displayPartial(epd.getbuffer(frame))
        time.sleep(2)
    else:
        start_y = 0
        refresh_counter = 0
        while True:
            frame = Image.new('1', (epd.height, epd.width), 255)
            frame_draw = ImageDraw.Draw(frame)

            object_class_font = heading_font if heading_font.getlength(object_class) <= 60 else small_font
            frame_draw.text((5, 0), f"{object_class}", font=object_class_font, fill=0)
            frame_draw.text((70, 0), f"{title}", font=heading_font, fill=0)
            frame_draw.bitmap((epd.height - 35, 0), scp_logo, fill=0)
            frame_draw.line((0, 30, epd.height, 30), fill=0, width=1)

            if check_wifi():
                frame_draw.text((epd.height - 45, epd.width - 15), "WiFi: OK", font=small_font, fill=0)
            else:
                frame_draw.text((epd.height - 45, epd.width - 15), "WiFi: ERR", font=small_font, fill=0)

            scroll_part = scroll_canvas.crop((0, start_y, epd.height, start_y + epd.width))
            frame.paste(scroll_part, (0, 50))

            epd.displayPartial(epd.getbuffer(frame))

            time.sleep(scroll_speed)

            start_y += 5
            if start_y >= overlay_height - (epd.width - 50):
                break  # Exit scrolling after full scroll to load next SCP

def get_random_scp():
    scp_image = None
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        }
        for _ in range(5):
            scp_number = random.randint(2, 999)
            scp_url = f"http://scp-wiki.wikidot.com/scp-{scp_number:03d}"

            response = requests.get(scp_url, timeout=20, headers=headers)
            if response.status_code != 200:
                continue

            soup = BeautifulSoup(response.text, 'html.parser')

            title_element = soup.find('div', {'id': 'page-title'})
            if not title_element:
                continue

            title = title_element.text.strip()

            paragraphs = soup.find('div', {'id': 'page-content'}).find_all('p')
            if not paragraphs:
                continue

            description_paragraphs = []
            for para in paragraphs:
                text = para.text.strip()
                if len(text) > 50:
                    description_paragraphs.append(text)

            if not description_paragraphs:
                continue

            description = "\n\n".join(description_paragraphs)

            if description == "No description found.":
                continue

            object_class = "Unknown"
            for para in paragraphs:
                if "Object Class:" in para.text:
                    object_class = para.text.split("Object Class:")[1].split("\n")[0].strip()
                    break

            if object_class == "Unknown":
                continue

                        # Try to find the first image
            img_tag = soup.find('div', {'id': 'page-content'}).find('img')
            if img_tag and 'src' in img_tag.attrs:
                scp_image = img_tag['src']

            return title, object_class, description, scp_image

        return None
    except Exception as e:
        print(f"Exception occurred: {e}")
        return None

def loading_screen(epd, stop_event):
    epd.Clear(0x00)
    # Removed epd.init_partial(), not needed for this screen

    scp_logo = Image.open('/home/veritium/scp_logo.bmp')
    scp_logo = scp_logo.resize((50, 50)).convert('L')
    scp_logo = ImageOps.invert(scp_logo).convert('1')

    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 16)
    small_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 10)

    angle = 0
    while not stop_event.is_set():
        frame = Image.new('1', (epd.height, epd.width), 0)
        frame_draw = ImageDraw.Draw(frame)

        rotated_logo = scp_logo.rotate(angle, expand=True)
        angle = (angle + 30) % 360
        x = (epd.height - rotated_logo.width) // 2
        y = (epd.width - rotated_logo.height) // 2
        frame.paste(rotated_logo, (x, y))
        text = "Loading Database..."
        bbox = frame_draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = (epd.height - text_width) // 2
        text_y = epd.width - 30
        frame_draw.text((text_x, text_y), text, font=font, fill=1)

        if check_wifi():
            frame_draw.text((5, 5), "WiFi: OK", font=small_font, fill=1)
        else:
            frame_draw.text((5, 5), "WiFi: ERR", font=small_font, fill=1)

        epd.displayPartial(epd.getbuffer(frame))
        time.sleep(1.0)

epd = epd2in13_V4.EPD()
epd.init()
epd.Clear(0xFF)

# Main loop
while True:

    scp = None
    stop_event = threading.Event()
    loader_thread = threading.Thread(target=loading_screen, args=(epd, stop_event))
    loader_thread.start()
    loading_start = time.time()

    while scp is None:
        scp = get_random_scp()

    elapsed = time.time() - loading_start
    if elapsed < 5:
        time.sleep(5 - elapsed)

    stop_event.set()
    loader_thread.join()

    epd.Clear(0xFF)
    time.sleep(0.5)

    title, object_class, description, scp_image = scp

    epd.Clear(0xFF)
    time.sleep(0.5)

   
    display_scp(epd, title, object_class, description, scp_image)
