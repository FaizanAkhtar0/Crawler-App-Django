from Core.Scrapper_libs.scrapper import Scrapper

# Test Case
#
# Use whatever web you want to test

# full_link = 'https://craftcms.stackexchange.com/questions/20745/custom-routes-with-url-parameters-and-pagination'
full_link = 'https://webscraper.io/test-sites/e-commerce/scroll'
pagination_syntax = 'questions/20745'
pages = [20745, 20755] # can also use specific selective pages like [20745, 20750, 20755]


scrapper = Scrapper("", pagination_syntax, 2, page_numbers=pages, deprecate_later_syntax=True)
"""
    :param: deprecate_later_syntax: When set 'Ture' removes the route following the pagination_syntax 
            for next generated urls.
"""

# l = []
#
# for link in scrapper.get_sub_links():
#     if str(link['href']).startswith("http" or "https"):
#         l.append(link['href'])
# else:
#     print(l)

# links = scrapper.get_sub_links_at_page_depth(full_link)
#
# if links:
#     for link in links:
#         print(link)
# else:
#     print("Link Dead!")


# for link in scrapper.construct_next_URIS():
#     print(link)
#
# #
# # # for custom separators i.e:('page?=1', 'page/id=1')
# # scrapper.set_separator("?=")
# # scrapper.set_separator("/id=")
# #
#
# for content in scrapper.get_content():
#     print(content)
#
