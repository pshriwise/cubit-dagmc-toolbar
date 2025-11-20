#!python

for (group_name, group_id) in cubit.group_names_ids():
    # ignore group "picked". It is always present by default and isn't
    # relevant for DAGMC metadata
    if group_name == 'picked':
        continue
    tokens = group_name.split('_')
    properties = [f'{p}:{v}' for p, v in zip(tokens[::2], tokens[1::2])]
    new_name = '/'.join(properties)
    print(f'Renaming group {group_id} to {new_name}')
    cubit.set_entity_name("Group", group_id, new_name)
    cubit.silent_cmd(f'group {group_id} rename "{new_name}"')
