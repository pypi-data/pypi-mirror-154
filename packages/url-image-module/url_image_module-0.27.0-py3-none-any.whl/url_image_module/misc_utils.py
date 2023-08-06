from .constants import (
    __version__,
    ABBREVIATION_DICT
)
# Get Version of the URL Image Module
def get_version() -> str:
  """Gets version of the url_image_module package.
  
  Returns:
   __version__: version of the url_image_module package.
  """
  return __version__

# String manipulation
def prettify_underscore_string(underscore_string: str) -> str:
  """Makes a string containing words separated by underscore and returns a prettifed version.

  Args:
    underscore_string: Input string containing words separated by underscores, such as 'batch_size'.
  
  Returns:
    prettified_string: A prettified version of the underscore_string which is white space separated between words and 
      each word is capitilized. Words present in ABBREVIATION_DICT, will be converted to the value that correspondings
        to the orgiinal word as a key
  """
  words = underscore_string.split('_')
  prettified_words = [ABBREVIATION_DICT[word] if word in ABBREVIATION_DICT else word.capitalize() for word in words]
  prettified_string = ' '.join(prettified_words)
  return prettified_string