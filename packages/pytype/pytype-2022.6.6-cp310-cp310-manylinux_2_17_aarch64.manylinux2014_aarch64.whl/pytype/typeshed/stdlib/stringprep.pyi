b1_set: set[int]
b3_exceptions: dict[int, str]
c22_specials: set[int]
c6_set: set[int]
c7_set: set[int]
c8_set: set[int]
c9_set: set[int]

def in_table_a1(code: str) -> bool: ...
def in_table_b1(code: str) -> bool: ...
def map_table_b3(code: str) -> str: ...
def map_table_b2(a: str) -> str: ...
def in_table_c11(code: str) -> bool: ...
def in_table_c12(code: str) -> bool: ...
def in_table_c11_c12(code: str) -> bool: ...
def in_table_c21(code: str) -> bool: ...
def in_table_c22(code: str) -> bool: ...
def in_table_c21_c22(code: str) -> bool: ...
def in_table_c3(code: str) -> bool: ...
def in_table_c4(code: str) -> bool: ...
def in_table_c5(code: str) -> bool: ...
def in_table_c6(code: str) -> bool: ...
def in_table_c7(code: str) -> bool: ...
def in_table_c8(code: str) -> bool: ...
def in_table_c9(code: str) -> bool: ...
def in_table_d1(code: str) -> bool: ...
def in_table_d2(code: str) -> bool: ...
