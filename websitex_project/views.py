from django.http import HttpResponse

def home(request):
    html = """
        <!DOCTYPE html>
        <html>
        <head>
            <script src="https://unpkg.com/htmx.org@1.9.10"></script>
        </head>
        <body>
            <button hx-get="/test/" hx-swap="outerHTML">
            Click Me
            </button>
        </body>
        </html>
    """
    return HttpResponse(html)

def test(request):
    html = "<p>Hello World my friend</p>"
    return HttpResponse(html)
