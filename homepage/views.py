"""View-функции приложения homepage."""

from django.http import HttpResponse

BOOTSTRAP_CSS = (
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/"
    "bootstrap.min.css"
)


def page(title: str, content: str) -> str:
    """Собрать HTML-страницу с общим каркасом."""
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="{BOOTSTRAP_CSS}">
  <title>{title}</title>
</head>
<body>
  <header>
    <nav class="navbar navbar-light" style="background-color: lightskyblue">
      <div class="container">
        <a class="navbar-brand" href="/">ChangeLog</a>
        <ul class="nav nav-pills">
          <li class="nav-item"><a class="nav-link" href="/">Главная</a></li>
          <li class="nav-item">
            <a class="nav-link" href="/projects/">Проекты</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/changes/">Изменения</a>
          </li>
        </ul>
      </div>
    </nav>
  </header>
  <main class="container py-5">{content}</main>
  <footer class="border-top text-center py-3">
    <p>© ChangeLog Tracker</p>
  </footer>
</body>
</html>"""


def index(request):
    """Главная страница."""
    content = """
    <h1 class="display-4">ChangeLog Tracker</h1>
    <p class="lead">Система ведения журнала изменений.</p>
    <a href="/projects/" class="btn btn-primary me-2">Проекты</a>
    <a href="/changes/" class="btn btn-secondary">Изменения</a>
    """
    return HttpResponse(page("ChangeLog Tracker", content))


def page_not_found(request, exception):
    """Обработчик ошибки 404."""
    content = """
    <h1 class="text-danger">404 — страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную.</p>
    <a href="/" class="btn btn-primary">На главную</a>
    """
    return HttpResponse(
        page("404 — страница не найдена", content),
        status=404,
    )
