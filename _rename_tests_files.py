import os

ROOT = "tests"

for dirpath, _, filenames in os.walk(ROOT):
    for filename in filenames:
        if not filename.startswith("test_") and filename.endswith(".py"):
            old = os.path.join(dirpath, filename)
            new = os.path.join(dirpath, f"test_{filename}")
            os.rename(old, new)
            print(f"Renamed: {old} -> {new}")
