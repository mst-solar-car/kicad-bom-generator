import Parser
import Middleware
import Formatter
import Logger

@Parser.Pipeline
@Middleware.Pipeline
@Formatter.Pipeline
def PerformPipeline(result):
  """ End of the pipeline """
  Logger.Debug("Pipeline returned:", result)
  return result


def startPipeline(val):
  """ Starts the pipeline """
  Logger.Debug("Starting pipeline with:", val)
  return PerformPipeline(val)


def RunOnValue(val):
  """ Runs the pipeline on a specific value """
  return startPipeline(val)


def RunOnReturnValue(fn):
  """ Starts the pipeline once an initial function is called """
  def pipelineWrapper(*args, **kwargs):
    result = fn(*args, **kwargs)
    return startPipeline(result)

  return pipelineWrapper


