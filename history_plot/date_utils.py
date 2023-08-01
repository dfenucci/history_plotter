import numpy as np

start = -np.inf
end = np.inf

def year_to_string(year):
  if year > 0: return "%d\u00A0d.C." % year
  elif year < 0: return "%d\u00A0a.C." % abs(year)
  else: return str(year)

def year_interval_to_string(year_first, year_last):
  global start, end
  assert year_last > year_first, 'Ill-formed interval, last cannot be less or equal to first'
  assert year_first != start or year_last != end, 'Undefined interval, provide at least a semi-closed time interval'

  if year_first == start:
    return '-\u00A0%s' % year_to_string(year_last)
  elif year_last == end:
    return '%s\u00A0-' % year_to_string(year_first)
  elif np.sign(year_first) == np.sign(year_last):
    return '%d-%s' % (abs(year_first), year_to_string(year_last))
  else:
    return '%s\u00A0-\u00A0%s' % (year_to_string(year_first), year_to_string(year_last))
