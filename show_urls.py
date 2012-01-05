import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import urls

def show_urls(urllist, depth=0):
    for entry in urllist:
        if hasattr(entry, 'name'):
            print "  " * depth, entry.name, entry.regex.pattern
        else:
            print "  " * depth, entry.regex.pattern
        if hasattr(entry, 'url_patterns'):
            show_urls(entry.url_patterns, depth + 1)


def main():
    show_urls(urls.urlpatterns)


if __name__ == '__main__':
    main()