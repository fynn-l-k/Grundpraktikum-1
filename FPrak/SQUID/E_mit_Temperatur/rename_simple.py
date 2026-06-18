import os
import glob

# Get directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

print("="*60)
print("Renaming E_Temp_*.csv files (80-97 → 63-80)")
print("="*60)

# Create mapping (Umkehrung: 63↔97, 64↔96, ..., 80↔80)
mapping = {}
for i in range(63, 98):
    old_name = f'E_Temp_{i}.csv'
    new_num = 160 - i  # 63→97, 64→96, ..., 97→63
    new_name = f'E_Temp_{new_num}.csv'
    if os.path.exists(old_name):
        mapping[old_name] = new_name
        print(f"{old_name} → {new_name}")

# Confirm
print("\n" + "="*60)
response = input("Proceed with renaming? (yes/no): ")

if response.lower() == 'yes':
    # Rename with temp names first
    for old_name in mapping.keys():
        temp_name = old_name.replace('.csv', '_tmp.csv')
        os.rename(old_name, temp_name)
    
    # Rename to final names
    for old_name, new_name in mapping.items():
        temp_name = old_name.replace('.csv', '_tmp.csv')
        os.rename(temp_name, new_name)
        print(f"✓ {old_name} → {new_name}")
    
    print("\n✓ Done!")
else:
    print("Cancelled.")
