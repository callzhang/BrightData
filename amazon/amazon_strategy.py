# Import the core filtering functionality
from import_util import *

print("✅ Successfully imported all modules!")
print(f"Available fields: {FilterFields.get_field_count()}")

# Test if DELIVERY field is available
try:
    print(f"DELIVERY field: {DELIVERY}")
    print(f"DELIVERY field type: {type(DELIVERY)}")
    print("✅ DELIVERY field is available!")
except NameError as e:
    print(f"❌ DELIVERY field not available: {e}")
    print("Need to reload modules to get the updated field list")