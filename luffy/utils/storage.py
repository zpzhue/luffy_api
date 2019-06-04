import os

from django.core.files import locks
from django.core.files.storage import Storage
from django.utils._os import safe_join

from luffy import settings
from luffy.settings import MEDIA_ROOT


class CustomStorage(Storage):
    def url(self, name):
        # return settings.HOST + '/static/' + name
        return f'http://{settings.HOST}/static/{name}'

    def _open(self, name, mode='rb'):
        '打开文件时使用'
        return open(file=name, mode=mode)

    def _save(self, name, content):
        full_path = self.path(name)

        # Create any intermediate directories that do not exist.
        directory = os.path.dirname(full_path)
        if not os.path.exists(directory):
            try:
                old_umask = os.umask(0)
                try:
                    os.makedirs(directory)
                finally:
                    os.umask(old_umask)
            except FileExistsError:
                pass
        if not os.path.isdir(directory):
            raise IOError("%s exists and is not a directory." % directory)
        flags = (os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                 getattr(os, 'O_BINARY', 0))
        fd = os.open(full_path, flags, 0o666)
        _file = None
        try:
            locks.lock(fd, locks.LOCK_EX)
            for chunk in content.chunks():
                if _file is None:
                    mode = 'wb' if isinstance(chunk, bytes) else 'wt'
                    _file = os.fdopen(fd, mode)
                _file.write(chunk)
        finally:
            locks.unlock(fd)
            if _file is not None:
                _file.close()
            else:
                os.close(fd)
        return name.replace('\\', '/')

    def exists(self, name):
        'Django 判断文件名是否可用'
        pass

    def path(self, name):
        return safe_join(MEDIA_ROOT, name)