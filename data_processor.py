import pandas as pd
import os
import sys
import ast  # Import for literal_eval

def process_and_save_data(data_list, endpoint_name, output_folder="output"):
    """
    Processes a list of API records, normalizes them into a DataFrame,
    and saves to a CSV file.
    """
    if not data_list:
        print(f"No data to process for {endpoint_name}.", file=sys.stderr)
        return

    print(f"\nProcessing {len(data_list)} records for '{endpoint_name}'...")

    # Define common meta fields for PCO API responses
    common_meta = ["id", "type", ["links", "self"]]

    if endpoint_name == 'check_ins':
        meta_fields = common_meta + [
            ['attributes', 'checked_out_at'],
            ['attributes', 'confirmed_at'],
            ['attributes', 'created_at'],
            ['attributes', 'emergency_contact_name'],
            ['attributes', 'emergency_contact_phone_number'],
            ['attributes', 'first_name'],
            ['attributes', 'kind'],
            ['attributes', 'last_name'],
            ['attributes', 'medical_notes'],
            ['attributes', 'number'],
            ['attributes', 'one_time_guest'],
            ['attributes', 'security_code'],
            ['attributes', 'updated_at'],
            # Relationships - for direct data like IDs/types
            ['relationships', 'event_period', 'data', 'id'],
            ['relationships', 'event_period', 'data', 'type'],
            ['relationships', 'person', 'data', 'id'],
            ['relationships', 'person', 'data', 'type'],
            ['relationships', 'station', 'data', 'id'],
            ['relationships', 'station', 'data', 'type'],
            ['relationships', 'event', 'data', 'id'],
            ['relationships', 'event', 'data', 'type'],
            ['relationships', 'attendance', 'data', 'id'],
            ['relationships', 'attendance', 'data', 'type'],
            ['relationships', 'tag_instance', 'data', 'id'],
            ['relationships', 'tag_instance', 'data', 'type'],
            ['relationships', 'parent', 'data', 'id'],
            ['relationships', 'parent', 'data', 'type'],
            # For 'locations', we want the entire 'data' list to become a column first
            ['relationships', 'locations', 'data'],
        ]
        column_renames = {
            'links_self': 'self_link',
            'relationships_event_period_data_id': 'event_period_id',
            'relationships_event_period_data_type': 'event_period_type',
            'relationships_person_data_id': 'person_id',
            'relationships_person_data_type': 'person_type',
            'relationships_station_data_id': 'station_id',
            'relationships_station_data_type': 'station_type',
            'relationships_event_data_id': 'event_id',
            'relationships_event_data_type': 'event_type',
            'relationships_attendance_data_id': 'attendance_id',
            'relationships_attendance_data_type': 'attendance_type',
            'relationships_tag_instance_data_id': 'tag_instance_id',
            'relationships_tag_instance_data_type': 'tag_instance_type',
            'relationships_parent_data_id': 'parent_id',
            'relationships_parent_data_type': 'parent_type',
            # Removed direct renames for locations_data_0_id/type
        }
    elif endpoint_name == 'people_v2':
        meta_fields = common_meta + [
            ['attributes', 'created_at'],
            ['attributes', 'updated_at'],
            ['attributes', 'first_name'],
            ['attributes', 'last_name'],
            ['attributes', 'full_name'],
            ['attributes', 'sex'],
            ['attributes', 'birthdate'],
            ['attributes', 'email_address'],
            ['attributes', 'phone_number'],
            ['attributes', 'remote_id'],
            ['attributes', 'avatar_url'],
            ['attributes', 'child'],
            ['attributes', 'passed_background_check'],
            ['attributes', 'medical_notes'],
            ['attributes', 'inactivated_at'],
            ['attributes', 'contact_data'],
            ['attributes', 'birthdate_specificity'],
            # Relationships
            ['relationships', 'avatar', 'data', 'id'],
            ['relationships', 'avatar', 'data', 'type'],
            # Add other relationships for People API if needed (e.g., campus, organization)
        ]
        column_renames = {
            'links_self': 'self_link',
            'relationships_avatar_data_id': 'avatar_id',
            'relationships_avatar_data_type': 'avatar_type',
        }
    elif endpoint_name == 'tabs':
        meta_fields = common_meta + [
            ['attributes', 'name'],
            ['attributes', 'slug'],
            ['attributes', 'created_at'],
            ['attributes', 'updated_at'],
        ]
        column_renames = {
            'links_self': 'self_link',
        }
    elif endpoint_name == 'field_definitions':
        meta_fields = common_meta + [
            ['attributes', 'name'],
            ['attributes', 'data_type'],
            ['attributes', 'sequence'],
            ['attributes', 'created_at'],
            ['attributes', 'updated_at'],
            ['attributes', 'data_options'] # May be a list/dict, might need further flattening
        ]
        column_renames = {
            'links_self': 'self_link',
        }
    elif endpoint_name == 'field_data':
        meta_fields = common_meta + [
            ['attributes', 'value'],
            ['attributes', 'created_at'],
            ['attributes', 'updated_at'],
            # Relationships
            ['relationships', 'person', 'data', 'id'],
            ['relationships', 'person', 'data', 'type'],
            ['relationships', 'field_definition', 'data', 'id'],
            ['relationships', 'field_definition', 'data', 'type'],
        ]
        column_renames = {
            'links_self': 'self_link',
            'relationships_person_data_id': 'person_id',
            'relationships_person_data_type': 'person_type',
            'relationships_field_definition_data_id': 'field_definition_id',
            'relationships_field_definition_data_type': 'field_definition_type',
        }
    else:
        # Default for other endpoints or if specific attributes/relationships are unknown
        meta_fields = common_meta + ['attributes']
        column_renames = {'links_self': 'self_link'}


    # Normalize the data
    df_expanded = pd.json_normalize(
        data_list,
        meta=meta_fields,
        errors='ignore',
        sep='_'
    )

    # --- Post-normalization processing for specific columns ---
    if endpoint_name == 'check_ins' and 'relationships_locations_data' in df_expanded.columns:
        def extract_location_info(data_value):
            """
            Extracts location type and ID from the relationships_locations_data column.
            Handles cases where data_value might be NaN, empty list, or incorrectly formatted.
            """
            # 1. Handle lists directly to bypass pd.isna() entirely
            if isinstance(data_value, list):
                data_list_parsed = data_value
            
            # 2. Handle string representations of lists
            elif isinstance(data_value, str):
                try:
                    data_list_parsed = ast.literal_eval(data_value)
                except (ValueError, SyntaxError):
                    return None, None
            
            # 3. If it's neither a list nor a string, it's missing/invalid (e.g., NaN, None)
            else:
                return None, None 

            # 4. Safely extract data if the parsed list is not empty
            if data_list_parsed and isinstance(data_list_parsed, list):
                first_location = data_list_parsed[0]
                # Ensure the first item is a dictionary before using .get()
                if isinstance(first_location, dict):
                    return first_location.get('type'), first_location.get('id')
            
            return None, None

        # Apply the function to create new 'location_type' and 'location_id' columns
        df_expanded[['location_type', 'location_id']] = df_expanded['relationships_locations_data'].apply(
            lambda x: pd.Series(extract_location_info(x))
        )
        # Drop the original relationships_locations_data column
        df_expanded.drop(columns=['relationships_locations_data'], inplace=True)


    # Apply renaming for common prefixes and specific relationship renames
    final_renames = {}
    for col in df_expanded.columns:
        if col.startswith('attributes_'):
            final_renames[col] = col[len('attributes_'):]
        elif col in column_renames:
            final_renames[col] = column_renames[col]
        # Fallback for relationships not explicitly listed in column_renames
        # This part handles generic relationships like 'person_id', 'event_period_id'
        elif col.startswith('relationships_') and '_data_id' in col:
            new_name = col.replace('relationships_', '').replace('_data_id', '_id')
            final_renames[col] = new_name
        elif col.startswith('relationships_') and '_data_type' in col:
            new_name = col.replace('relationships_', '').replace('_data_type', '_type')
            final_renames[col] = new_name

    df_expanded.rename(columns=final_renames, inplace=True)

    # --- COLUMN REORDERING LOGIC ---
    fixed_start_cols = ['id', 'type']
    link_cols = []
    other_cols = []

    for col in df_expanded.columns:
        if col in fixed_start_cols:
            continue

        if 'link' in col.lower() or col.endswith('_url'):
            link_cols.append(col)
        else:
            other_cols.append(col)

    other_cols.sort()
    link_cols.sort()

    # Place location_type and location_id near other relationship IDs if they exist
    if 'location_id' in df_expanded.columns and 'location_type' in df_expanded.columns:
        # Remove them from other_cols to reinsert them specifically
        if 'location_id' in other_cols: other_cols.remove('location_id')
        if 'location_type' in other_cols: other_cols.remove('location_type')
        
        # Find a suitable insertion point, e.g., after person_type or other relationship types
        # For simplicity, let's just add them after 'id' and 'type' or at a consistent place
        # You can customize this further based on desired order.
        # Here, adding them after other relationship IDs alphabetically
        rel_cols = [col for col in other_cols if '_id' in col or '_type' in col]
        non_rel_cols = [col for col in other_cols if col not in rel_cols]
        
        rel_cols.append('location_id')
        rel_cols.append('location_type')
        rel_cols.sort() # Sort relationship columns for consistency

        new_cols_order = fixed_start_cols + rel_cols + non_rel_cols + link_cols
    else:
        new_cols_order = fixed_start_cols + other_cols + link_cols


    # Ensure all columns actually exist in the DataFrame after filtering and sorting
    new_cols_order = [col for col in new_cols_order if col in df_expanded.columns]

    df_expanded = df_expanded[new_cols_order]

    # Replace newline characters with a comma in all string columns to prevent CSV formatting issues
    df_expanded = df_expanded.replace(to_replace=[r'\r\n', r'\n', r'\r'], value=', ', regex=True)

    # --- Output Folder Logic ---
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output folder: '{output_folder}'")

    csv_filename = os.path.join(output_folder, f"{endpoint_name}.csv")
    df_expanded.to_csv(csv_filename, encoding='utf-8', index=False)
    print(f"Data for '{endpoint_name}' saved to '{csv_filename}' successfully.")
    print(f"\nFirst 5 rows of '{endpoint_name}' DataFrame:")
    print(df_expanded.head())
    print("-" * 50)