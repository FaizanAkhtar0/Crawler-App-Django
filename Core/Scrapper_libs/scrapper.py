import random
import requests
from itertools import cycle

from bs4 import BeautifulSoup
from fake_useragent import UserAgent, FakeUserAgentError


class Scrapper:
    __proxy_url = 'https://www.sslproxies.org/'
    __index_separators = ['=', '-', '/', '?', '?=']

    def __init__(self, Web_URI=None, pagination_route_syntax=None, page_depth=None, page_numbers=None, deprecate_later_syntax=False):
        self._WEB_URI = Web_URI
        self._PAGE_NO = page_numbers
        self._page_depth = page_depth
        self._ROUTE_SYNTAX = pagination_route_syntax
        self._DEPRECATION = deprecate_later_syntax

    def set_separator(self, separator):
        if separator != None and separator != '':
            if separator not in self.__index_separators:
                self.__index_separators.append(separator)

    def __get_page_index_in_str(self):
        fixed_link_ending_index = self._WEB_URI.index(self._ROUTE_SYNTAX)
        route_length = 0
        for item in Scrapper.__index_separators:
            separated_route = self._ROUTE_SYNTAX.split(item)
            if separated_route.__len__() == 1:
                continue
            else:
                route_length = separated_route[0].__len__() + 1
                self._PRESENT_PAGE_NO = separated_route[1]
                break

        if route_length != 0:
            return fixed_link_ending_index + route_length
        else:
            return None

    def construct_next_URIS(self):
        start_index = self.__get_page_index_in_str()
        ending_index = (self._WEB_URI.index(self._PRESENT_PAGE_NO) + self._PRESENT_PAGE_NO.__len__())

        if self._DEPRECATION and self._PAGE_NO != None:
            if self._PAGE_NO.__len__() > 2:
                return [('' + self._WEB_URI[:start_index] + str(number)) for number in
                        self._PAGE_NO]
            else:
                return [('' + self._WEB_URI[:start_index] + str(number)) for number in
                        range(self._PAGE_NO[0], self._PAGE_NO[1] + 1, 1)]
        elif self._PAGE_NO != None:
            if self._PAGE_NO.__len__() > 2:
                return [('' + self._WEB_URI[:start_index] + str(number) + self._WEB_URI[ending_index:]) for number in
                        self._PAGE_NO]
            else:
                return [('' + self._WEB_URI[:start_index] + str(number) + self._WEB_URI[ending_index:]) for number in
                        range(self._PAGE_NO[0], self._PAGE_NO[1] + 1, 1)]
        else:
            return [self._WEB_URI]

    def __proxies_pool(self):
        with requests.Session() as res:
            proxies_page = res.get(self.__proxy_url)

        soup = BeautifulSoup(proxies_page.content, 'html.parser')
        proxies_table = soup.find(id='proxylisttable')

        proxies = []
        for row in proxies_table.tbody.find_all('tr'):
            proxies.append('{}:{}'.format(row.find_all('td')[0].string, row.find_all('td')[1].string))
        return proxies

    def __random_header(self):
        accepts = {"Firefox": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                   "Safari, Chrome": "application/xml,application/xhtml+xml,text/html;q=0.9, text/plain;q=0.8,image/png,*/*;q=0.5"}
        try:
            # Getting a user agent using the fake_useragent package
            ua = UserAgent()
            if random.random() > 0.5:
                self.__random_user_agent = ua.chrome
            else:
                self.__random_user_agent = ua.firefox
        except FakeUserAgentError  as error:
            user_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
                "Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1"]
            self.__random_user_agent = random.choice(user_agents)
        finally:
            valid_accept = accepts['Firefox'] if self.__random_user_agent.find('Firefox') > 0 else accepts['Safari, Chrome']
            headers = {"User-Agent": self.__random_user_agent, "Accept": valid_accept}
        return headers

    def __create_pools(self):
        proxies = self.__proxies_pool()
        headers = [self.__random_header() for index in range(len(proxies))]

        proxies_pool = cycle(proxies)
        headers_pool = cycle(headers)
        return proxies_pool, headers_pool

    def __get_pages_response(self, page_uris):
        proxie_pool, header_pool = self.__create_pools()
        for uri in page_uris:
            current_proxy = next(proxie_pool)
            current_header = next(header_pool)

            for uri in page_uris:
                with requests.session() as req:
                    try:
                        return req.get(uri,
                                       proxies={"http": current_proxy, "https": current_proxy},
                                       headers=current_header, timeout=5)
                    except:
                        print(
                            f"Proxy Server: {current_proxy} - timed out at 5secs.\n|-> with Headers: {current_header}\n|=> Trying({i + 1}) new proxy for {page_url}...")
                        continue

    def __get_page_response(self, page_url):
        proxie_pool, header_pool = self.__create_pools()

        for i in range(30): # Tries for 30 times if no successes return None
            current_proxy = next(proxie_pool)
            current_header = next(header_pool)

            with requests.session() as req:
                try:
                    return req.get(page_url,
                                  proxies={"http": current_proxy, "https": current_proxy},
                                  headers=current_header, timeout=5)
                except:
                    print(f"Proxy Server: {current_proxy} - timed out at 5secs.\n|-> with Headers: {current_header}\n|=> Trying({i+1}) new proxy for {page_url}...")
                    continue
        else:
            print(f"|=> Dead Link @{page_url}... Unable to Scrape data..")
            return None

    def get_content(self):
        for response in self.__get_pages_response(self.construct_next_URIS()):
            yield response.content.decode("utf-8")

    def get_sub_links(self, page_url=None):
        if page_url:
            response = self.__get_page_response(page_url)
            if response:
                print('|-----------------Proxy Fetch Success-----------------|')
                return BeautifulSoup(response.content, "html.parser").find_all('a', href=True)
            else:
                return None
        else:
            if self._WEB_URI:
                response = self.__get_page_response(self._WEB_URI)
                if response:
                    print('|-----------------Proxy Fetch Success-----------------|')
                    return BeautifulSoup(response.content, "html.parser").find_all('a', href=True)
                else:
                    return None
            else:
                return None

    def extract_proper_links(self, link_soup):
        l = []
        if link_soup:
            for link in link_soup:
                if str(link['href']).startswith("http" or "https"):
                    l.append(str(link['href']))
            else:
                return l
        else:
            return None

    def get_sub_links_at_page_depth(self, page_url=None, page_depth=None):

        if page_depth:
            self._page_depth = page_depth

        if page_url:
            links = self.extract_proper_links(self.get_sub_links(page_url))

            if links:
                sub_links = [*links]
                for i in range(self._page_depth):
                    temp_links = []
                    for link in links:
                        extracted_sub_links = self.extract_proper_links(self.get_sub_links(link))
                        if extracted_sub_links:
                            temp_links = [_link for _link in temp_links if _link not in sub_links]
                            extracted_sub_links = [_link for _link in extracted_sub_links if _link not in sub_links]
                            extracted_sub_links = [_link for _link in extracted_sub_links if _link not in temp_links]
                            temp_links += extracted_sub_links
                        else:
                            print(f"|=> No valid link found! @{link}...")
                            continue
                    else:
                        sub_links += temp_links
                        links = temp_links
                else:
                    sub_links = list(dict.fromkeys(sub_links))
                    return sub_links
            else:
                return None
        else:
            links = self.extract_proper_links(self.get_sub_links(self._WEB_URI))

            if links:
                sub_links = [*links]
                for i in range(self._page_depth):
                    temp_links = []
                    for link in links:
                        temp_links += self.extract_proper_links(self.get_sub_links(link))
                    else:
                        sub_links += temp_links
                        links = temp_links
                else:
                    return sub_links
            else:
                return None

    def get_images(self, page_url=None):
        if page_url:
            response = self.__get_page_response(page_url)
            if response:
                print(f'|-----------------Proxy Success for ALL Image Links Fetch @{page_url} -----------------|')
                return BeautifulSoup(response.content, "html.parser").find_all('img')
            else:
                return None

    def get_text(self, page_url=None):
        if page_url:
            response = self.__get_page_response(page_url)
            if response:
                print(f'|-----------------Proxy Success for Text Fetch @{page_url} -----------------|')
                return BeautifulSoup(response.content, "html.parser").text
            else:
                return None
        else:
            return None

    def get_documents(self, page_url=None):
        if page_url:
            response = self.__get_page_response(page_url)
            if response:
                print(f'|-----------------Proxy Success for All Document Links Fetch @{page_url} -----------------|')
                return BeautifulSoup(response.content, "html.parser").find_all('a', href=True)
            else:
                return None
        else:
            return None

    def get_document_content(self, page_url=None):
        if page_url:
            response = self.__get_page_response(page_url)
            if response:
                print(f'|-----------------Proxy Success for Document Content Fetch @{page_url} -----------------|')
                return response.content
            else:
                return None
        else:
            return None


