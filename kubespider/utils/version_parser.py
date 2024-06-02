from typing import List, Tuple


def check_version_at_lest(current_version: str, target_version: str) -> bool:
    if current_version == target_version:
        return True
    current_vers, current_n = parse_version(current_version)
    target_vers, target_n= parse_version(target_version)
    index = 0
    while index < current_n and index < target_n:
        if current_vers[index] < target_vers[index]:
            return False
        elif current_vers[index] > target_vers[index]:
            return True
        index += 1
    return current_n >= target_n


def parse_version(version_name: str) -> Tuple[List[int], int]:
    vers = [int(x) for x in version_name.split('.')]
    return vers, len(vers)

if __name__ == "__main__":
    assert check_version_at_lest("3.11.2", "3.12.2") == False, "False"
    assert check_version_at_lest("3.12", "3.12.2") == False, "False"
    assert check_version_at_lest("3.12.2", "3.12.1") == True, "True"
    assert check_version_at_lest("3.12.2", "3.12") == True, "True"
    assert check_version_at_lest("03.12.2", "3.12") == True, "True"
