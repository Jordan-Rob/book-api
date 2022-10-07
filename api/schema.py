import graphene

from graphene_django import DjangoObjectType, DjangoListView
from .models import Book



class BookType(DjangoObjectType):
    class Meta:
        model = Book
        fields = "__all__"


class Query(graphene.ObjectType):
    all_books = graphene.List(BookType)
    book = graphene.Field(BookType, book_id=graphene.Int())

    def resolve_all_books(self, info, **kwargs):
        return Book.objects.all()

    def resolve_book(self, info, book_id):
        return Book.objects.get(pk=book_id)



class BookInput(graphene.InputObjectType):
    id = graphene.ID()
    title = graphene.String()
    author = graphene.String()
    year_published = graphene.String()
    review = graphene.Int()



class CreateBook(graphene.Mutation):
    class Arguments:
        book_data = BookInput(required=True)

    book = graphene.Field(BookType)

    @staticmethod
    def mutate(root, info, book_data=None):
        book_instance = Book(
            title = book_data.title,
            author = book_data.author,
            year_published = book_data.year_published,
            review = book_data.review
        )

        book_instance.save()
        return CreateBook(book=book_instance)