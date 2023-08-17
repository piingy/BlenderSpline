import bpy

# Number of vertices per control point
vertex_group = 100

# Get the active object (selected mesh)
active_obj = bpy.context.active_object

# Make sure the active object is a mesh
if active_obj and active_obj.type == 'MESH':
    mesh = active_obj.data
    uv_layer = mesh.uv_layers.active.data

    # Get the number of vertices in the mesh
    num_vertices = len(mesh.vertices)

    # Calculate the vertex index for the start and end points
    start_vertex_index = int((num_vertices - 1) * 0.25)
    end_vertex_index = int((num_vertices - 1) * 0.75)

    # Calculate a vertex index step based on the mesh's vertex count
    vertex_step = (end_vertex_index - start_vertex_index) // (vertex_group - 1)

    # Create a new curve object
    curve_data = bpy.data.curves.new(name="Generated Curve", type='CURVE')
    curve_data.dimensions = '3D'

    # Create a spline for the curve
    spline = curve_data.splines.new(type='NURBS')

    # Create a list to hold the control points
    control_points = []

    # Calculate the start point using UV coordinates
    uv_start = uv_layer[start_vertex_index].uv
    start_vertex = active_obj.matrix_world @ mesh.vertices[start_vertex_index].co
    control_points.append((start_vertex.x + (uv_start.x - 0.5) * active_obj.scale.x,
                           start_vertex.y + (uv_start.y - 0.5) * active_obj.scale.y,
                           start_vertex.z))

    # Iterate through vertices to create control points
    for i, vert in enumerate(mesh.vertices[start_vertex_index:end_vertex_index + 1]):
        if i % vertex_group == 0:
            control_points.append(vert.co)

    # Calculate the end point using UV coordinates
    uv_end = uv_layer[end_vertex_index].uv
    end_vertex = active_obj.matrix_world @ mesh.vertices[end_vertex_index].co
    control_points.append((end_vertex.x + (uv_end.x - 0.5) * active_obj.scale.x,
                           end_vertex.y + (uv_end.y - 0.5) * active_obj.scale.y,
                           end_vertex.z))

    # Set the control points of the spline
    spline.points.add(len(control_points))
    for i, co in enumerate(control_points):
        spline.points[i].co = (co[0], co[1], co[2], 1)


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
