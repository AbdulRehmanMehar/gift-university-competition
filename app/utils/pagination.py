from math import ceil
from sqlalchemy.orm.collections import InstrumentedList


class Pagination:

    def __init__(self, model, items_per_page, current_page_number, filter=None):
        if type(model) is InstrumentedList:
            self.list = model
            self.total_pages = int(ceil(len(self.list) / items_per_page))
        else:
            self.model = model
            self.total_pages = int(ceil(model.query.count() / items_per_page))

        self.items_per_page = items_per_page
        self.current_page_number = current_page_number
        self.filter = filter

    @property
    def pages(self):
        return self.total_pages

    def get_items_per_page(self):
        return self.items_per_page

    def get_current_page_number(self):
        return self.current_page_number

    def get_results(self):

        try:
            st_idx = (self.current_page_number - 1) * self.items_per_page
            end_idx = self.current_page_number * self.items_per_page
            return self.list[st_idx: end_idx]
        except AttributeError:
            if self.current_page_number == 1:
                return self.model.query\
                        .filter(self.filter)\
                        .limit(self.items_per_page)\
                        .all()

            elif self.current_page_number <= self.total_pages:

                return self.model.query\
                        .filter(self.filter)\
                        .limit(self.items_per_page)\
                        .offset((self.current_page_number - 1) * self.items_per_page)\
                        .all()

            return None

