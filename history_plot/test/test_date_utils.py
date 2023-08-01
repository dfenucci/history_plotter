import pytest
import numpy as np
from ..date_utils import year_to_string
from ..date_utils import year_interval_to_string
from ..date_utils import start, end

def test_date_utils_constants():
  assert start == -np.inf 
  assert end == np.inf 

def test_year_to_string_fail():
  with pytest.raises(TypeError):
    assert year_to_string([100])
  with pytest.raises(TypeError):
    assert year_to_string('100')
  with pytest.raises(TypeError):
    assert year_to_string(None)

def test_year_to_string():
  assert year_to_string(300) == "300\u00A0d.C."
  assert year_to_string(-300) == "300\u00A0a.C."
  assert year_to_string(0) == "0"

def test_year_interval_to_string_fail():
  with pytest.raises(AssertionError) as e_info:
    year_interval_to_string(start, end)
  assert str(e_info.value) == 'Undefined interval, provide at least a semi-closed time interval' 
  with pytest.raises(AssertionError) as e_info:
    year_interval_to_string(end, 0)
  assert str(e_info.value) == 'Ill-formed interval, last cannot be less or equal to first' 

def test_year_interval_to_string():
  assert year_interval_to_string(start, -18) == "-\u00A018\u00A0a.C."
  assert year_interval_to_string(start, 0) == "-\u00A00"
  assert year_interval_to_string(start, 18) == "-\u00A018\u00A0d.C."
  assert year_interval_to_string(-100, -18) == "100-18\u00A0a.C."
  assert year_interval_to_string(-100, 0) == "100\u00A0a.C.\u00A0-\u00A00"
  assert year_interval_to_string(-100, 18) == "100\u00A0a.C.\u00A0-\u00A018\u00A0d.C."
  assert year_interval_to_string(-100, end) == "100\u00A0a.C.\u00A0-"
  assert year_interval_to_string(0, 18) == "0\u00A0-\u00A018\u00A0d.C."
  assert year_interval_to_string(0, end) == "0\u00A0-"
  assert year_interval_to_string(100, 180) == "100-180\u00A0d.C."
  assert year_interval_to_string(100, end) == "100\u00A0d.C.\u00A0-"
