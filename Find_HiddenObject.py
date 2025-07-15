import bpy

target_name = "Insert Here the name of your missign object"  # Replace with the name you're searching for

def get_excluded_objects(view_layer):
    excluded_objects = []

    def recurse_layer(layer_collection):
        if layer_collection.exclude:
            for obj in layer_collection.collection.objects:
                excluded_objects.append(obj.name)
        for child in layer_collection.children:
            recurse_layer(child)

    recurse_layer(view_layer.layer_collection)
    return excluded_objects

# Usage
excluded = get_excluded_objects(bpy.context.view_layer)

def select_excluded_object(layer_collection):
    if layer_collection.exclude:
        for obj in layer_collection.collection.objects:
            if obj.name == target_name:
                # Re-include the collection so the object becomes selectable
                layer_collection.exclude = False
                bpy.context.view_layer.update()
                obj.select_set(True)
                bpy.context.view_layer.objects.active = obj
                print(f"Selected object: {obj.name}")
                return True
    for child in layer_collection.children:
        if select_excluded_object(child):
            return True
    return False

found = select_excluded_object(bpy.context.view_layer.layer_collection)
if not found:
    print(f"Object '{target_name}' not found in excluded collections.")
