from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module


def load_backend(path):
	i = path.rfind('.')
	module, attr = path[:i], path[i+1:]
	try:
		mod = import_module(module)
	except ImportError, e:
		raise ImproperlyConfigured('Error importing ticketeer backend %s: "%s"' % (path, e))
	except ValueError, e:
		raise ImproperlyConfigured('Error importing ticketeer backends. Is TICKETEER_BACKEND correctly defined?')
	try:
		cls = getattr(mod, attr)
	except AttributeError:
		raise ImproperlyConfigured('Module "%s" does not define a "%s" ticketeer backend' % (module, attr))

	return cls()
