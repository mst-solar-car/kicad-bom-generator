__all__ = ['GetFormatter']

import Arguments
import Middleware


args = Arguments.Parse()





def GetFormatter():
  """ Returns a function that can be used to format a list of components """
  formatter = args.formatter
  formatFn = None

  pass



@Middleware.Wrapper
def formatWrapper(formatFn):
  """ Wraps the Format Function for use in Middleware """
  def applyFormater(components):
    output = formatFn(components)

    return output

  return applyFormater



