# 목표
1. 인증(로그인, 로그아웃) 구현


# django
```python

# 상위 폴더로 올라와서 하셔야 합니다.

mkdir accounts
cd accounts
python -m venv venv
.\venv\Scripts\activate
pip install django
django-admin startproject tutorialdjango .
python manage.py migrate
python manage.py startapp blog

################################
# tutorialdjango > settings.py

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "blog",
    'main',
]

################################
# urls 기획
1. 다음 url이 실제 작동하도록 해주세요.
1.1 ''                          : 메인페이지
1.1 'blog/'                     : 블로그 글 목록
1.2 'blog/<int:pk>/'            : 블로그 상세 글 읽기
1.3 'accounts/signup/'          : 회원가입
1.4 'accounts/login/'           : 로그인
1.5 'accounts/logout/'          : 로그아웃
1.6 'accounts/profile/'         : 프로필

###################################
앱이름: main               views 함수이름        html 파일이름  비고
'main/sign_up/'            accounts_sign_up     sign_up.html
'main/login/'              account_login        login.html
'main/logout'              account_logout       logout.html
'main/profile'             account_profile      profile.html

###################################
앱이름: blog                views 함수이름        html 파일이름  비고
'blog/'                     blog_list            blog_list.html	
'blog/<int:pk>/'            blog_details         blog_details.html


###################################
# 아래처럼 GitHub Readme에 정리가 되어있어야 합니다.
# 예제입니다. 지금 이렇게 구현하겠다는 것은 아닙니다.
|app:accounts|HTTP Method|설명|로그인 권한 필요|작성자 권한 필요|
|:-|:-|:-|:-:|:-:|
|signup/|POST|회원가입|||
|login/|POST|로그인|||
|logout/|POST|로그아웃| ✅ ||
|\<int:pk\>/|GET|프로필 조회| ✅ ||
|\<int:pk\>/|PUT|프로필 수정| ✅ | ✅ |
|\<int:pk\>/|DELETE|회원 탈퇴| ✅ | ✅ |
|status/|GET|로그인 상태 확인|||
|token/refresh/|POST|만료 토큰 재발급|||
<br>  

################################
# tutorialdjango > urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls")),
    path("blog/", include("blog.urls")),
    path("accounts/", include("accounts.urls")),
]
################################
# main > urls.py

from django.urls import path
from .views import index

urlpatterns = [
    path("", index, name="index"),
]

################################
# main > views.py

from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the main index.")

################################
# blog > urls.py

from django.urls import path
from .views import blog_list, blog_details

urlpatterns = [
    path("", blog_list, name="blog_list"),
    path("<int:pk>/", blog_details, name="blog_details"),
]

################################
# blog > views.py

from django.shortcuts import render
from .models import Post


def blog_list(request):
    blogs = Post.objects.all()
    context = {"blogs": blogs}
    return render(request, "blog/blog_list.html", context)


def blog_details(request, pk):
    blog = Post.objects.get(pk=pk)
    context = {"blog": blog}
    return render(request, "blog/blog_detail.html", context)

################################
#blog > models.py
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=100)
    contents = models.TextField()

    def __str__(self):
        return self.title
################################
python manage.py makemigrations
python manage.py migrate
################################


################################
# accounts > urls.py

from django.urls import path
from .views import signup, login, logout, profile

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("profile/", profile, name="profile"),
]

################################
# accounts > views.py
from django.shortcuts import render


def signup(request):
    pass


def login(request):
    pass


def logout(request):
    pass


def profile(request):
    pass

################################
# urls/views/models 코딩 후
# 이미지객체 있을 경우 pip install pillow 필요

python manage.py makemigrations
python manage.py migrate

################################

# 비교
# 어떤 것이 우위에 있지 않습니다!

FBV: 추상화 정도는 약합니다. 어떤 원리로 이 페이지가 나오는지 상세히 알 수 있습니다. 커스터마이징은 편하게 할 수 있습니다.

CBV: 추상화 정도가 강합니다. 어떤 원리로 이 페이지가 나오는지 알지 못하게 합니다.(마법처럼 보이게 합니다.) 커스터마이징이 불편한 것은 아니지만, 모든 코드가 다 보이는 것이 아니니 명쾌하지 않습니다.
################################

# 로그인/로그아웃 기능 def이렇게 함수로 코딩하지 말것
# 이제부터는 class로 구현!!!!!!!!
# accounts> views.py
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.shortcuts import render


signup = CreateView.as_view(
    form_class=UserCreationForm,
    template_name="accounts/form.html",
    success_url=settings.LOGIN_URL,
)


login = LoginView.as_view(
    template_name="accounts/form.html",
    # success_url=settings.LOGIN_REDIRECT_URL,
    # next_page=settings.LOGIN_REDIRECT_URL,
)


logout = LogoutView.as_view(
    next_page=settings.LOGOUT_URL,
)


@login_required
def profile(request):
    return render(request, "accounts/profile.html")


################################
# tutorialdjango > settings.py 맨 아래에 로그인 URL 넣기

LOGIN_URL = '/accounts/hellologin/'
LOGOUT_URL = '/accounts/hellologout/'


################################
# tutorialdjango > settings.py templates 작성

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
###############################
#폴더 생성
blog > templates > blog > blog_list.html
blog > templates > blog > blog_details.html
blog > tempaltes > account > profile.html
blog > tempaltes > account > form.html
################################
# blog_list.html
<ul>
    {% for blog in blogs %}
    <li><a href="/blog/{{blog.id}}">{{blog.title}}</a></li>
    {% endfor %}
</ul>
################################
# blog_details.html
<p>{{blog.title}}</p>
<p>{{blog.contents}}</p>
################################
# profile.html
<h1>개인 프로필 페이지</h1>
<p>{{ user }}</p>
################################
# form.html
<form action="" method="post" enctype="multipart/form-data">
    {% csrf_token %}
    <table>
        {{ form.as_table }}
    </table>
    <input type="submit">
</form>
################################
################################


python manage.py createsuperuser

leehojun
leehojun@gmail.com
이호준1234!

################################
python manage.py runserver

# 실습하기 전 admin페이지와 http://127.0.0.1:8000/ 페이지 2개를 띄어주세요.
# blog는 들어갈 필요 없습니다. 생성되는 것을 구현하지 않았으니까요. user클릭해서 user만 확인해주세요.

http://127.0.0.1:8000/accounts/login/
http://127.0.0.1:8000/accounts/profile/
http://127.0.0.1:8000/accounts/logout/
http://127.0.0.1:8000/accounts/signup/ -> http://127.0.0.1:8000/accounts/hellologin/ 으로 이동되는 것 확인

################################
signup 했을때,
settings.py > language code 변환

LANGUAGE_CODE = "ko-kr"
################################

################################

# hash알고리즘
md5(이거는 깨졌습니다. 사용하시면 안됩니다.)
sha256
sha512

원본
leehojun

sha256(64개의 문자열)
859E57E3
E4197F11
C95F97DF
171B77F7
E03FA280
6D86A5DE
1C65CCC5
04C42831

원본
leehojun2

sha256(64개의 문자열, 지난 텍스트와 연관성이 없습니다.)
94D748F3C756496422CE4F0FBC29F2D483F4E75BA9CE6FE48BDB071C5FE369C0


원본
아주 큰 소설, 이미지, 영상

sha256(그래도 64개의 문자열을 줍니다.)
94D748F3C756496422CE4F0FBC29F2D483F4E75BA9CE6FE48BDB071C5FE369C0


원본 -> sha256 값은 되지만
sha256 -> 원본으로는 불가합니다.

그렇기 때문에 DB에 password를 sha256을 저장하면 해커가 해킹해도 user의 패스워드를 알지 못합니다!

---

md5(32자) => 레인보우어택으로 깨졌습니다.

1q2w3e4r! => 1E9E9F6FEF3369CDC763284D80AE5FEB
admin => 21232F297A57A5A743894A0E4A801FC3

해커가 해킹을 했는데 21232F297A57A5A743894A0E4A801FC3 를 발견했습니다! 이 패스워드는 무엇일까요? 족보를 저장해두었는데 저기에서 찾는 것입니다! 이걸 레인보우 어택이라 합니다.

---
salt(암호화 소금)

admin + 'hojun' => md5
1q2w3e4r! + 'hojun' => md5


adminhojun => B73105D4A2A8B8AE6F7A19C268437A46

이제는 '소금' 값을 알지 못하면 B73105D4A2A8B8AE6F7A19C268437A46 이 무엇인지 알지 못합니다.

---
소금을 연속으로 돌리는 방법
B73105D4A2A8B8AE6F7A19C268437A46 + 'hojun'

=> 5E7F66BFBDA59C8B3D6C3F03638A2E56

많이 할 수록 보안성은 올라가겠네요? => 성능이 떨어집니다.

---
이 소금이 django에 어디있냐?
settings.py
SECRET_KEY = "django-insecure-j=tox_7-#^hr%5e#jrv!*d6al@@dlaskv*i=3*yev0qra59kxc"

이제 SECRET_KEY이 값이 얼마나 중요한지 아시겠죠?
이 값은 개발자도 보지 못해야 합니다. => 대표, 이사급 인원만 이 key값을 보게 세팅해야 합니다.

# 해커가 들어왔을 때 사용자의 password가 DB 단에서 노출이 되어야 합니다.
# 해커가 들어왔을 때 SECRET_KEY값을 구할 수 있어야 합니다.
# 이 2개가 다 충족이 되어도 패스워드가 10자 이상이고 특수문자, 숫자 들어있으면 sha256값을 얻는데 아주 큰 시간이 소요됩니다.
################################
# profile.html 수정해서 로그아웃되게 수정 

<h1>개인 프로필 페이지</h1>
<p>{{ user }}</p>

<!-- 로그아웃 버튼 -->
<form action="{% url 'logout' %}" method="post">
  {% csrf_token %}
  <input type="submit" value="로그아웃">
</form>
################################
# accounts > urls.py
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.shortcuts import render
from django.http import HttpResponse


signup = CreateView.as_view(
    form_class=UserCreationForm,
    template_name="accounts/form.html",
    success_url=settings.LOGIN_URL,
)


login = LoginView.as_view(
    template_name="accounts/form.html",
    # success_url=settings.LOGIN_REDIRECT_URL,
    # next_page=settings.LOGIN_REDIRECT_URL,
)


logout = LogoutView.as_view(
    next_page=settings.LOGOUT_URL,
)


@login_required
def profile(request):
    return render(request, "accounts/profile.html")


def logincheck(request):
    if request.user.is_authenticated:
        return HttpResponse("로그인 됨!")
    return HttpResponse("로그인 안됨!!")
################################
# accounts > logincheck.html

<p>django.contrib.auth.models.User</p>
<p>{{user}}</p>
<p>{{user.username}}</p>
<p>{{user.email}}</p>
<p>{{user.first_name}}</p>
<p>{{user.last_name}}</p>
<p>{{user.is_staff}}</p>
<p>{{user.is_active}}</p>
<p>{{user.is_superuser}}</p>
<p>{{user.last_login}}</p>
<p>{{user.date_joined}}</p>
################################
# 함수 기반 뷰로 로그인 구현하기
# accounts > urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('logincheck/', views.logincheck, name='logincheck'),
    path('loginfbv/', views.loginfbv, name='loginfbv'),
]
################################
# accounts > views.py 업데이트 
def loginfbv(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse("login 성공")
        else:
            return HttpResponse("login 실패")
    return render(request, 'accounts/loginfbv.html')
################################
# accounts/loginfbv.html

<form method="post">
    {% csrf_token %}
    <label for="username_id">아이디</label>
    <input id = 'username_id' type="text" name="username">
    <label  for="password_id">비밀번호</label>
    <input id = 'password_id' type="password" name="password">
    <button type="submit">로그인</button>
</form>
################################
# login/out 테스트 후 tutorialsdjango>settings.py에서 로그인아웃 url 수정
LOGIN_URL = "/accounts/login/"
LOGOUT_URL = "/accounts/profile/"
################################

