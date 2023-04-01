"""Views, one for each Insta485 page."""
from swish_academy.views.index import show_index
from swish_academy.views.accounts import show_login
from swish_academy.views.users import show_users
from swish_academy.views.posts import show_posts
from swish_academy.views.login import do_accounts
from swish_academy.views.helpers import execute_get_likes
