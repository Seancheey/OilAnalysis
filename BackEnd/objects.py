class OilPrice:
    __slots__ = ("type_id", "price", "time")

    def __init__(self, type_id, price, time):
        self.type_id = type_id
        self.price = price
        self.time = time


class OilNews:
    __slots__ = ("news_id", "title", "publish_date", "author", "content", "reference")

    def __init__(self, news_id, title, publish_date, author, content, reference):
        self.news_id = news_id
        self.title = title
        self.publish_date = publish_date
        self.author = author
        self.content = content
        self.reference = reference
