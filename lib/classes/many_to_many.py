# lib/many_to_many.py

class Article:
    all = []

    def __init__(self, author, magazine, title):
        """Initialize an Article with author, magazine, and title"""
        if not isinstance(author, Author):
            raise Exception("Author must be an instance of Author")
        if not isinstance(magazine, Magazine):
            raise Exception("Magazine must be an instance of Magazine")
        if not isinstance(title, str):
            raise Exception("Title must be a string")
        if not (5 <= len(title) <= 50):
            raise Exception("Title must be between 5 and 50 characters")
        self._author = author
        self._magazine = magazine
        self._title = title
        Article.all.append(self)

    @property
    def title(self):
        """Get the article title"""
        return self._title

    @title.setter
    def title(self, value):
        """Prevent title from being changed by ignoring the assignment"""
        pass  # Silently ignore attempts to change the title

    @property
    def author(self):
        """Get the article author"""
        return self._author

    @author.setter
    def author(self, value):
        """Set the article author with validation"""
        if not isinstance(value, Author):
            raise Exception("Author must be an instance of Author")
        self._author = value

    @property
    def magazine(self):
        """Get the article magazine"""
        return self._magazine

    @magazine.setter
    def magazine(self, value):
        """Set the article magazine with validation"""
        if not isinstance(value, Magazine):
            raise Exception("Magazine must be an instance of Magazine")
        self._magazine = value


class Author:
    def __init__(self, name):
        """Initialize an Author with a name"""
        if not isinstance(name, str):
            raise Exception("Name must be a string")
        if len(name) == 0:
            raise Exception("Name must be longer than 0 characters")
        self._name = name

    @property
    def name(self):
        """Get the author name"""
        return self._name

    @name.setter
    def name(self, value):
        """Prevent name from being changed by ignoring the assignment"""
        pass  # Silently ignore attempts to change the name

    def articles(self):
        """Return a list of all articles by this author"""
        return [article for article in Article.all if article.author == self]

    def magazines(self):
        """Return a unique list of magazines this author has contributed to"""
        return list(set(article.magazine for article in self.articles()))

    def add_article(self, magazine, title):
        """Create and return a new article for this author and given magazine"""
        return Article(self, magazine, title)

    def topic_areas(self):
        """Return a unique list of magazine categories or None if no articles"""
        articles = self.articles()
        if not articles:
            return None
        return list(set(article.magazine.category for article in articles))


class Magazine:
    all = []

    def __init__(self, name, category):
        """Initialize a Magazine with name and category"""
        if not isinstance(name, str):
            raise Exception("Name must be a string")
        if not (2 <= len(name) <= 16):
            raise Exception("Name must be between 2 and 16 characters")
        if not isinstance(category, str):
            raise Exception("Category must be a string")
        if len(category) == 0:
            raise Exception("Category must be longer than 0 characters")
        self._name = name
        self._category = category
        Magazine.all.append(self)

    @property
    def name(self):
        """Get the magazine name"""
        return self._name

    @name.setter
    def name(self, value):
        """Set the magazine name with validation, ignoring invalid assignments"""
        if isinstance(value, str) and 2 <= len(value) <= 16:
            self._name = value
        # Silently ignore invalid assignments (non-string or incorrect length)

    @property
    def category(self):
        """Get the magazine category"""
        return self._category

    @category.setter
    def category(self, value):
        """Set the magazine category with validation, ignoring invalid assignments"""
        if isinstance(value, str) and len(value) > 0:
            self._category = value
        # Silently ignore invalid assignments (non-string or empty string)

    def articles(self):
        """Return a list of all articles published by this magazine"""
        return [article for article in Article.all if article.magazine == self]

    def contributors(self):
        """Return a unique list of authors who have contributed to this magazine"""
        return list(set(article.author for article in self.articles()))

    def article_titles(self):
        """Return a list of article titles or None if no articles"""
        articles = self.articles()
        if not articles:
            return None
        return [article.title for article in articles]

    def contributing_authors(self):
        """Return a list of authors with more than 2 articles or None if none"""
        author_counts = {}
        for article in self.articles():
            author = article.author
            author_counts[author] = author_counts.get(author, 0) + 1
        result = [author for author, count in author_counts.items() if count > 2]
        return result if result else None

    @classmethod
    def top_publisher(cls):
        """Return the magazine with the most articles or None if no articles"""
        if not Article.all:
            return None
        magazine_counts = {}
        for article in Article.all:
            magazine = article.magazine
            magazine_counts[magazine] = magazine_counts.get(magazine, 0) + 1
        return max(magazine_counts, key=magazine_counts.get)