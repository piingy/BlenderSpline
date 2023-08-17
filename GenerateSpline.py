import bpy

# Number of vertices per control point
vertex_interval = 68

# Get the active object (selected mesh)
active_obj = bpy.context.active_object

# Make sure the active object is a mesh
if active_obj and active_obj.type == 'MESH':
    mesh = active_obj.data

    # Calculate a vertex index step based on the mesh's vertex count
    vertex_step = len(mesh.vertices) // (vertex_interval - 1)

    # Create a new curve object
    curve_data = bpy.data.curves.new(name="Generated Curve", type='CURVE')
    curve_data.dimensions = '3D'

    # Create a spline for the curve
    spline = curve_data.splines.new(type='NURBS')

    # Create a list to hold the control points
    control_points = []

    # Iterate through vertices to create control points
    for i in range(0, len(mesh.vertices), vertex_step):
        vertex = mesh.vertices[i]
        if vertex.groups:
            group_index = vertex.groups[0].group
            group = active_obj.vertex_groups[group_index]
            weights = [v.weight for v in group.weight_groups]
            control_points.append(vertex.co + (vertex.normal * weights[0]))

    # Set the control points of the spline
    spline.points.add(len(control_points))
    for i, co in enumerate(control_points):
        spline.points[i].co = (co.x, co.y, co.z, 1)

    # Apply the same transformations as the selected mesh
    curve_obj = bpy.data.objects.new("Generated Curve", curve_data)
    curve_obj.location = active_obj.location
    curve_obj.rotation_euler = active_obj.rotation_euler
    curve_obj.scale = active_obj.scale

    # Link the curve object to the collection and scene
    bpy.context.collection.objects.link(curve_obj)
    bpy.context.view_layer.objects.active = curve_obj
    curve_obj.select_set(True)

    # Update the scene
    bpy.context.view_layer.update()

else:
    print("Please select a valid mesh object.")
