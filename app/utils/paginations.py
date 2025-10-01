from app.blogs.models import Blogs

class Pagination:

    def __init__(self, offset, limit):
        self.offset = offset
        self.limit = limit


    def page_level_pagination(self, queryset):
        
        new_offset = self.offset * self.limit
        new_limit = new_offset + self.limit

        total_records = queryset.count()
        paginated_response = queryset.offset(new_offset).limit(new_limit).all()
        print("paginated Response: ", paginated_response)

        res = { "offset": self.offset,
                "limit": self.limit,
                "pagination_type": "page_level",
                "total_records": total_records,
                "results": paginated_response
               }
        
        return res

    def queryset_level_pagination(self, queryset):

        total_records = queryset.count()
        paginated_response = queryset.offset(self.offset).limit(self.limit).all()
        
        res = { "offset": self.offset,
                "limit": self.limit,
                "pagination_type": "queryset_level",
                "total_records": total_records,
                "results": paginated_response   #
               }
        
        return res