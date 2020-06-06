import uuid
import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from paynting.models import Masterpiece, MadeWith, Sort, Search
from .tokens import account_activation_token


@pytest.mark.django_db
def test_user_create():
    User.objects.create_user('yan', 'ysmaliak@gmail.com', 'justmypassword')
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_home_view(client):
    url = reverse('home')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_view(client):
    response = client.get('/masterpiece/create/')
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize("username, status_code", [
    ("yan", 200),
    ("ellie", 200),
])
def test_user_detail(client, django_user_model, username, status_code):
    user = django_user_model.objects.create(
        username=username, password='password'
    )
    url = reverse('account_view', args=[username])
    print(url)
    response = client.get(url)
    assert response.status_code == status_code
    assert str(user) == username


@pytest.mark.django_db
def test_activation_sent_view(client):
    url = reverse('activation_sent')
    response = client.get(url)
    assert response.status_code == 200


def test_an_admin_view(admin_client):
    response = admin_client.get('/admin/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_with_client(client):
    response = client.get('/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_with_authenticated_client(client, django_user_model):
    username = "yan"
    password = "justmypassword"
    django_user_model.objects.create_user(username=username, password=password)
    client.login(username=username, password=password)
    response = client.get('/account/' + username)
    assert response.status_code == 200


@pytest.fixture
def test_password():
    return 'strong-test-pass'


@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs['password'] = test_password
        if 'username' not in kwargs:
            kwargs['username'] = str(uuid.uuid4())
        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def auto_login_user(db, client, create_user, test_password):
    def make_auto_login(user=None):
        if user is None:
            user = create_user()
        client.login(username=user.username, password=test_password)
        return client, user

    return make_auto_login


@pytest.mark.django_db
def test_auth_view(auto_login_user):
    client, user = auto_login_user()
    url = reverse('signup')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_activate_view(auto_login_user):
    client, user = auto_login_user()
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)
    url = reverse('activate', args=[uid, token])
    response = client.get(url)
    assert response.status_code == 302


def test_masterpiece_view(auto_login_user):
    client, user = auto_login_user()
    mp = Masterpiece(masterpiece_name="test_name",
                     image='static/media/2018-singer-porsche-911-dls.jpg',
                     uploaded_by=user)
    mp.save()
    url = reverse('masterpiece_detail', kwargs={'primary_key': mp.id})
    response = client.get(url)
    assert response.status_code == 200


def test_masterpiece_update_view(auto_login_user):
    client, user = auto_login_user()
    mp = Masterpiece(masterpiece_name="test_name",
                     image='static/media/2018-singer-porsche-911-dls.jpg',
                     uploaded_by=user)
    mp.save()
    url = reverse('masterpiece_update', kwargs={'pk': mp.id})
    response = client.get(url)
    assert response.status_code == 200


def test_masterpiece_delete_view(auto_login_user):
    client, user = auto_login_user()
    mw = MadeWith(hardware="iPad", software='Procreate')
    mw.save()
    mp = Masterpiece(masterpiece_name="test_name",
                     image='static/media/2018-singer-porsche-911-dls.jpg',
                     uploaded_by=user, made_with=mw)
    mp.save()
    url = reverse('masterpiece_delete', kwargs={'pk': mp.id})
    response = client.get(url)
    assert response.status_code == 200


def test_masterpiece_create_view(auto_login_user):
    client, user = auto_login_user()
    url = reverse('masterpiece_create')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_search(client):
    search = Search(search='by')
    search.save()
    url = reverse('search')
    response = client.get(url + '?q=' + search.search)
    assert response.status_code == 200


@pytest.mark.django_db
def test_sort(client):
    sort = Sort(sort_type='az')
    sort.save()
    url = reverse('sort')
    response = client.get(url + '?sort_type=' + sort.sort_type)
    assert response.status_code == 200


@pytest.mark.django_db
def test_str(auto_login_user):
    client, user = auto_login_user()
    mw = MadeWith(hardware="iPad", software='Procreate')
    mw.save()
    mp = Masterpiece(masterpiece_name="test_name",
                     image='static/media/2018-singer-porsche-911-dls.jpg',
                     made_with=mw)
    mp.save_user(user)
    mp.save()
    url = reverse('masterpiece_detail', args=[str(mp.id)])
    search = Search(search='test_search')
    search_verbose_name_plural = search._meta.verbose_name_plural
    assert mp.get_absolute_url() == url
    assert str(mp) == 'test_name'
    assert str(search) == 'test_search'
    assert search_verbose_name_plural == 'Searches'
