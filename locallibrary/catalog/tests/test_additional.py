from django.test import TestCase
from django.urls import reverse
from catalog.models import BookInstance, Book, Author, Genre, Language
from populate_catalog import populate
from django.contrib.auth.models import User, Permission

user = "user1"
password = "biblioteca"
email = "user@user.es"

class AdditionalModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        populate()
        User.objects.create_user(user, email, password)
    
    def test_display_genre(self):
        book= Book.objects.filter(title='The Shining').first()
        genre_str = book.display_genre()
        expected_str = 'Horror, Thriller'
        self.assertEqual(genre_str, expected_str)
    
    def test_str(self):
        book_instance = BookInstance.objects.filter(
            book__title='The Shining').first()
        expected_str = f'{book_instance.id} ({book_instance.book.title})'
        self.assertEqual(str(book_instance), expected_str)

    def test_delete_book(self):
        u  = User.objects.get(username=user)
        u.is_staff = True
        permission = Permission.objects.get(codename='add_book')
        u.user_permissions.add(permission)
        permission = Permission.objects.get(codename='change_book')
        u.user_permissions.add(permission)
        permission = Permission.objects.get(codename='delete_book')
        u.user_permissions.add(permission)
        permission = Permission.objects.get(codename='can_mark_returned')
        u.user_permissions.add(permission)
        u.save()
        loginDict = {}
        loginDict["username"] = user
        loginDict["password"] = password
        response = self.client.post(reverse('login'), loginDict, follow=True)
        bookDict = {}
        bookDict['title'] = 'Julio'
        bookDict["summary"] = 'Verne'
        bookDict["isbn"] = '1234123412341'
        bookDict["author"] = Author.objects.first().pk
        bookDict['genre'] = Genre.objects.first().pk
        bookDict['language'] = Language.objects.first().pk
        response = self.client.post(reverse('book-create'),
                                    bookDict, follow=True)
        b=Book.objects.filter(title__contains='Julio').first()
        response = self.client.delete(reverse('book-delete',
                                              kwargs={'pk': b.pk}),
                                              bookDict, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_delete_author(self):
        u  = User.objects.get(username=user)
        u.is_staff = True
        permission = Permission.objects.get(codename='add_author')
        u.user_permissions.add(permission)
        permission = Permission.objects.get(codename='change_author')
        u.user_permissions.add(permission)
        permission = Permission.objects.get(codename='delete_author')
        u.user_permissions.add(permission)
        permission = Permission.objects.get(codename='can_mark_returned')
        u.user_permissions.add(permission)
        u.save()
        loginDict = {}
        loginDict["username"] = user
        loginDict["password"] = password
        response = self.client.post(reverse('login'), loginDict, follow=True)
        authorDict = {}
        authorDict["first_name"] = 'Julio'
        authorDict["last_name"] = 'Verne'
        authorDict["birth_date"] = '1928-02-08'
        authorDict["die_date"] = '1905-03-24'
        response = self.client.post(reverse('author-create'), authorDict,
                                    follow=True)
        a=Author.objects.filter(first_name__contains='Julio').first()
        response = self.client.delete(reverse('author-delete',
                                              kwargs={'pk': a.pk}),
                                              follow=True)
        self.assertEqual(response.status_code, 200)