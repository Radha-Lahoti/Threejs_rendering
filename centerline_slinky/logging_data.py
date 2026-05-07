import numpy as np

def logDataForRendering(dofs, time_array, n_nodes, Nsteps, rod_file='rawDataRod.txt'):
    dof_with_time = np.hstack([time_array, dofs])
    print(np.shape(dof_with_time), np.shape(time_array), np.shape(dofs))
    
    # For dynamic case
    rod_data = np.zeros((n_nodes * Nsteps, 4))
    for i in range(Nsteps):
        for j in range(n_nodes):
            rod_data[i * n_nodes + j, 0] = dof_with_time[i, 0]
            rod_data[i * n_nodes + j, 1:] = dof_with_time[i, 1 + 3*j: 1 + 3*j + 3]

    np.savetxt(rod_file, rod_data, fmt='%.6e')

    return

def export_rod_shell_data(n_nodes,
                        rod_file='rawDataRod.txt',
                        rod_js='rodData.js',  
                        rod_radius=0.1, scaleFactor=100):
    """
    Export rod and shell data to .js files for visualization.

    Parameters
    ----------
    robot : object
        Object with attributes `rod_edges` and `face_nodes_shell`.
    rod_file : str
        Path to raw rod data (.txt).
    rod_js : str
        Output JS file path for rod data.
    rod_radius : float
        Radius of rods.
    scaleFactor : float
        Scale factor for coordinates.
    """

    # === Load rod data ===
    df = np.loadtxt(rod_file)

    # Write rod data
    with open(rod_js, 'w') as fileID:
        fileID.write(f'nNodes = {n_nodes};\n')
        fileID.write(f'rodRadius = {rod_radius};\n')
        fileID.write('nodesRod = [\n')

        for row in df:
            t, x, y, z = row
            x, y, z = x * scaleFactor, y * scaleFactor, z * scaleFactor
            fileID.write(f'{t}, 1, {x}, {y}, {z},\n')

        fileID.write(']\n;\n')
