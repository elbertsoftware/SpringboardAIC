# implemented for list of str objects only
import math


def is_empty(str_list: list) -> bool:
	if str_list is None:
		return True

	if len(str_list) < 1:
		return True

	for s in str_list:
		if s is not None and len(str(s).strip()) > 0:
			return False

	return True


def remove_empty(str_list: list) -> list:
	if str_list is None:
		return []

	return [s for s in str_list if s is not None and len(str(s).strip()) > 0]


def min_len(str_list: list) -> int:
	str_list = remove_empty(str_list)

	length = len(str_list[0])
	for s in str_list[1:]:
		slen = len(str(s))
		if slen < length:
			length = slen

	return length


def is_in(name: str, str_list: list) -> bool:
	if str_list is None:
		return False

	if name is None or len(name) < 1:
		return False

	for s in str_list:
		if name.startswith(str(s)):
			return True

	return False


def to_int(str_value: str, default: int = 0) -> int:
	try:
		return math.floor(float(str_value))
	except TypeError:
		return default


def to_float(str_value: str, default: float = 0.0) -> float:
	try:
		return float(str_value)
	except (TypeError, ValueError):
		return default
