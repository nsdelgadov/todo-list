from django.conf import settings
from django.http import HttpResponse


def health(request):
    return HttpResponse("Django OK")


def index(request):
    index_path = settings.BASE_DIR / "frontend" / "dist" / "index.html"
    if not index_path.exists():
        return HttpResponse(
            "React build not found. Run 'pixi run frontend-build' first.",
            status=503,
        )
    return HttpResponse(index_path.read_text(encoding="utf-8"))
