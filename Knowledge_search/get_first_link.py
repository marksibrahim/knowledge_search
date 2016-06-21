class Article():
    """
    article class used for parsing the first link 

    for a list of articles: https://en.wikipedia.org/wiki/Special:AllPages
    entire dump is https://dumps.wikimedia.org/enwiki/20141008/


    parsing logic:
        1. article body via xml tag
        2. clean tags: <ref>, <div>
        3. clean Media wiki templates {{ }}
        5. disregard parenthesis, not embedeed in links
        6. find first link 
            * eliminating outermost false links:
                *Image, wiktionary etc.
        first level of hierachy is check whether {{}}
            proceed to ()
            then test link
            link
    """
    # template, parenthesis, and html tag markers
    w_marker = ["{{", "}}"]
    par_marker = ["(", ")"]
    rtag_marker = ["<ref", "</re"]
    dtag_marker = ["<div", "</di"]

    def __init__(self, article_xml):
        """
        article is initialized with xml text contained inside 
        <page> tags
        """
        self.article_xml = article_xml
        self.links = self.grab_links()
        self.first_link = self.parse_first_link()

    def inside_char(self, char, marker, tracker, i):
        """
        checks whether inside char such as parentheses or wiki_template
            handles nested tags and parenthesis
        """
        if char == marker[0]:
            tracker.append(i)
        elif char == marker[1]:
            try:
                tracker.pop()
            except IndexError:
                pass
        return tracker

    def grab_links(self):
        """
        returns a list of the outer-most links not in parenthesis
        a tempalte, or a tag
        """
        links = []
        link_char = []
        w_temp = [] #in template?
        par = [] #in parentheses?
        rtag = [] #in <ref> tag?
        dtag = [] #in <div> tag?

        skip_char = []

        for i, c in enumerate(self.article_xml):
            if i in skip_char: continue #eliminates double counting
            char = self.article_xml[i:i+2]
            tag = self.article_xml[i:i+4]
            
            #wiki template
            w_temp = self.inside_char(char, Article.w_marker, w_temp, i)
            if char in Article.w_marker: skip_char.append(i+1)
            if w_temp:
                continue #doesn't process if inside wiki template
            
            #parentheses
            par = self.inside_char(c, Article.par_marker, par, i)
            if par:
                continue
            
            #<ref> or <div>
            rtag = self.inside_char(tag, Article.rtag_marker, rtag, i)
            dtag = self.inside_char(tag, Article.dtag_marker, dtag, i)
            if rtag or dtag:
                continue
            
            #clear to add outer-most link
            if char == '[[':
                link_char.append(i)
            elif char == ']]' and len(link_char) == 1:
                links.append( self.article_xml[link_char[0]:i+2])
                link_char.pop()
            elif char == ']]' and len(link_char) > 1:
                link_char.pop()
        return links
    
    def check_link(self, link):
        """
        filters links to images, files, or other Wikimedia projects
        returns false if it's an invalid link (including links with a colon)
        """
        false_links = ["wikipedia:", "w:", "wikitionary:", "wikt:", "wikinews:",
                        "n:", "wikibooks:", "b:", "wikiquote:", "q:", "wikisource:",
                        "s:", "wikispecies:", "species:", "wikiversity", "v:", 
                        "wikivoyage:", "voy:", "wikimedia:", "foundation:", "wmf:", 
                        "commonds:", "c:", "chapter:", "metawikipedia:", "meta:", 
                        "m:", "incubator:", "outreach:", "mw:", "mediazilla:", 
                        "bugzilla:", "testwiki:", "wikitech:", "wikidata:", "d:",
                        "phabricator:", "phab:", "talk:", "user talk:", "file:", 
                        "user:", "template:", "category:", "file talk:", 
                        "category talk:", "image:", "media:", "special:", 
                        "help:", "portal:", "portal talk:", "\#"]
        is_bad = any(false_link in link.lower() for false_link in false_links)
        if is_bad or link[0] == ":":
            return False
        else:
            return True

    def clean_link(self, link):
        """
        strips brackets, returns link destination (not display name)
        """
        link = link.strip("[]")
        if "|" in link:            
            link = link.split("|",1)[0]
        link = link.strip() #remove trailing white space
        return link 

    def parse_first_link(self):
        """
        returns the first link not in parenthesis or side bar
        linking to another Wikipedia article
        """
        for link in self.links:
            if self.check_link(link):
                return self.clean_link(link)
        return None

    

