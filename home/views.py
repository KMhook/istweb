from annoying.decorators import render_to
from notification.models import Notification

@render_to('home/index.html')
def index(request):
    notifications = Notification.objects.order_by('-updated_at')[:10]
    return { 'notifications': notifications }
