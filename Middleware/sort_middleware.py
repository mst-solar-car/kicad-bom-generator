import Middleware


@Middleware.Register("sort")
def sort_middleware(components):
  """ Sorts the components by their reference """
  return sorted(components, key=lambda c: c['reference'])