"""
* This script takes an input string and accesses the wikipedia
  page of that string (if there is one) and while the current url
  is not https://en.wikipedia.org/wiki/Philosophy, the first
  hyperlink url in the article is followed

* r/dailyprogrammer Challenge #340 [Hard] Path to Philosophy
* https://www.reddit.com/r/dailyprogrammer/comments/6j7k3x/
  20170624_challenge_320_hard_path_to_philosophy/

"""
import urllib.request
from bs4 import BeautifulSoup

def get_wiki_page(title):
    
    url = "https://en.wikipedia.org/wiki/" + title
    with urllib.request.urlopen(url) as response:
        html = response.read()

    soup = BeautifulSoup(html, "html.parser")
    #next_hyperlink = soup.find_all("a", class_ = "mw-redirect")
    #print(soup.prettify())
    #print(next_hyperlink)

    base_html = html
    html = soup.prettify()
    summary_bounds = [html.find("<p>")] # from first paragraph tag
    summary_bounds.append(html.find('div class="toc"')) # to table of contents
    summary = html[summary_bounds[0]:summary_bounds[1]]

    next_page = get_next_title(summary)

    return next_page

def get_next_title(summary):
    """Gets the page title of the first hyperlink in the input"""
    search_in = summary[summary.find('title="'):]
    title = search_in[len('title="') : search_in.find('">')]

    return title

def main():
    #title = "Molecule"
    title = "Modern Greek"
    titles = [title]
    
    for i in range(10):
        try:
            titles.append(get_wiki_page(titles[i]))
        except:
            print(titles[i])
            print("\nError with url -- check title validity\n")
            break
        print(titles[i])

    print(titles)

def TODO():
    """
    * Exclude text in summary in parentheses -> cycle between checking
      normal text and removing parentheses
    """
    pass

main()
