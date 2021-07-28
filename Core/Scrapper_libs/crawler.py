import threading
import uuid

import requests
from bs4 import BeautifulSoup

from Core.Scrapper_libs.scrapper import Scrapper
from Core.models import MasterURL, SubURL, Content, Image, Document
from Crawler.settings import MEDIA_SAVE_PATH


class Crawler:

    def __init__(self, web_link=None, page_depth=None):
        self.stop_crawler = False
        self.queue = []
        self.queue_thread = None
        self.link_thread = None
        self.previous_set = False
        self.documents_extensions = ['.pdf', '.doc', '.docx', '.odt', '.ppt', '.pptx', '.txt', '.html', '.htm']
        self.image_extensions = ['.tif', '.tiff', '.bmp', '.jpg', '.jpeg', '.gif', '.png', '.svg']
        if page_depth and web_link:
            self.scrapper = Scrapper(Web_URI=web_link, page_depth=web_link)
        else:
            self.scrapper = Scrapper()

    def start_queue_thread(self):
        if self.queue_thread.isAlive():
            return False
        else:
            self.queue_thread.start()
            return True

    def start_queue(self):
        print("|====> Crawler Started...")
        self.stop_crawler = False
        self.queue = [i for i in SubURL.objects.filter(completed=False)]
        self.get_content(self.queue)

    def stop_queue(self):
        self.stop_crawler = True
        print("|===> Stopping the crawler service...")
        while self.queue_thread.is_alive():
            continue
        else:
            pass

    def save_sub_links(self, links, master, master_link):
        if links:
            links = [master_link, *links]
            for _link in links:
                content = self.create_content(_link)
                if content:
                    pass
                else:
                    content = Content()

                content.save()

                sub_url = SubURL(master_url=master, sub_url=_link, content=content, completed=False)
                sub_url.save()
            else:
                print("|=> Links Added to the Queue")
                self.start_queue_thread()
                print("|=> <---- Queue Automatically Started ---->")
        else:
            print("|-> No Links to save...")

    def start_link_acquisition_thread(self):
        if self.link_thread.isAlive():
            return False
        else:
            self.link_thread.start()
            return True

    def get_all_links(self, link=None, page_depth=None):
        if link and page_depth:
            master = MasterURL(master_url=link, page_depth=page_depth)
            master.save()
            links = self.scrapper.get_sub_links_at_page_depth(link, page_depth)
            self.save_sub_links(links, master, link)
            self.previous_set = False
        else:
            print("|=> Insufficient parameters received-----------------------------------|")

    def verify_image(self, name):
        for ext in self.image_extensions:
            if name.endswith(ext):
                return True
        else:
            return False

    def save_images(self, url, content):
        img_links = self.scrapper.get_images(page_url=url)
        if img_links:
            for img in img_links:
                if img.has_attr('src'):
                    img_url = str(img['src'])
                    if img_url.startswith('http' or 'https'):
                        response = requests.get(img_url)
                        file_name = img_url.split('/')[-1]
                        if self.verify_image(file_name):
                            if response:
                                img_name = file_name.split('.')[0]
                                img_ext = file_name.split('.')[-1]
                                img_name = f"{img_name}-{uuid.uuid4()}.{img_ext}"
                                file = open(MEDIA_SAVE_PATH + "\\images\\" + img_name, "wb")
                                file.write(response.content)
                                file.close()

                                image = Image(content=content, image_name=img_name)
                                image.save()
                            else:
                                continue
                    elif img_url.startswith('/'):
                        response = requests.get(url + img_url)
                        file_name = img_url.split('/')[-1]
                        if self.verify_image(file_name):
                            if response:
                                img_name = file_name.split('.')[0]
                                img_ext = file_name.split('.')[-1]
                                img_name = f"{img_name}-{uuid.uuid4()}.{img_ext}"
                                file = open(MEDIA_SAVE_PATH + "\\images\\" + img_name, "wb")
                                file.write(response.content)
                                file.close()

                                image = Image(content=content, image_name=img_name)
                                image.save()
                            else:
                                continue
                    else:
                        continue
                else:
                    continue
        else:
            print(f"|=> No Valid Image found @{url}...")

    def create_content(self, url):
        text = self.scrapper.get_text(page_url=url)
        if text:
            return Content(text=text)
        else:
            return None

    def filter_doc_links(self, links):
        doc_links = []
        for _link in links:
            for ext in self.documents_extensions:
                if str(_link['href']).endswith(ext):
                    doc_links.append(str(_link['href']))
                else:
                    continue
            else:
                pass
        else:
            return doc_links

    def save_documents(self, url, content):
        links = self.scrapper.get_documents(page_url=url)
        if links:
            doc_links = self.filter_doc_links(links)
            if doc_links:
                for _link in doc_links:
                    if _link.startswith('http' or 'https'):
                        response = self.scrapper.get_document_content(_link)
                        if response:
                            file_name = _link.split('/')[-1]
                            file_name = file_name.split('.')[0]
                            img_ext = file_name.split('.')[-1]
                            file_name = f"{file_name}-{uuid.uuid4()}.{img_ext}"
                            file = open(MEDIA_SAVE_PATH + "\\documents\\" + file_name, "wb")
                            file.write(response)
                            file.close()

                            doc = Document(content=content, file=file_name)
                            doc.save()
                        else:
                            continue
                    elif _link.startswith('/'):
                        response = self.scrapper.get_document_content(url + _link)
                        if response:
                            file_name = _link.split('/')[-1]
                            file_name = file_name.split('.')[0]
                            img_ext = file_name.split('.')[-1]
                            file_name = f"{file_name}-{uuid.uuid4()}.{img_ext}"
                            file = open(MEDIA_SAVE_PATH + "\\documents\\" + file_name, "wb")
                            file.write(response)
                            file.close()

                            doc = Document(content=content, file=file_name)
                            doc.save()
                        else:
                            continue
                    else:
                        continue
        else:
            print(f"|=> No Valid Document found @{url}...")

    def get_content(self, filtered_queue):
        for sub_link_obj in filtered_queue:
            if self.stop_crawler:
                break
            self.save_images(sub_link_obj.sub_url, sub_link_obj.content)
            print(f'|=> Saved images for @{sub_link_obj.sub_url}')
            self.save_documents(sub_link_obj.sub_url, sub_link_obj.content)
            print(f'|=> Saved documents for @{sub_link_obj.sub_url}')
            sub_link_obj.completed = True
            sub_link_obj.save()
            print("|=> Saving Scrapped data at server...")
            self.check_queue()
            print("|=> Entry Removed from Queue...")
        else:
            print("|=> Data Saved Successfully!")

        print(f"|=> Crawler Stopping Status: {self.stop_crawler}")

    def load(self):
        return [i for i in SubURL.objects.filter(completed=False)]

    def check_queue(self):
        self.queue = [i for i in SubURL.objects.filter(completed=False)]

    def set_thread(self):
        self.queue_thread = threading.Thread(target=self.start_queue)

    def set_link_thread(self, link, page_depth):
        if not self.previous_set:
            self.previous_set = True
            self.link_thread = threading.Thread(target=self.get_all_links, args=(link, page_depth))
        else:
            pass

