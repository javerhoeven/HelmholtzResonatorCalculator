import cadquery as cq
from calculation.simulation import Simulation

def export_cad(sim : Simulation, path : str):
    """This function is still in BETA state. It exports the resonator geometry and aperture to a CAD file.

    Args:
        sim (Simulation): Simulation object containing the resonator geometry and aperture.
        path (str): path to save the CAD file.

    """
    # TODO: add n_apertures with even distribution

    # create basic cad model of the resonator geometry
    form = sim.resonator.geometry.form
    if form == 'cuboid':
        x, y, z = sim.resonator.geometry.x, sim.resonator.geometry.y, sim.resonator.geometry.z
        model = cq.Workplane("XY").box(x, y, z)
    elif form == 'cylinder':
        radius, height = sim.resonator.geometry.radius, sim.resonator.geometry.height
        model = cq.Workplane("XY").cylinder(height, radius)
    else:
        raise ValueError(f"Unsupported geometry form: {form}")
    
    # aperture
    ap_form = sim.resonator.aperture.form
    n_ap = sim.resonator.aperture.amount
    if ap_form == 'tube':
        length, radius = sim.resonator.aperture.length, sim.resonator.aperture.radius
       
        # add a simple tube
        model = model.faces(">Z").workplane().circle(radius).extrude(-length)

        # add more apertures here with loop
        # TODO: fix
        # for i in range(aperture_count):
        #     angle = i * 360 / aperture_count
        #     x = aperture_distance * math.cos(math.radians(angle))
        #     y = aperture_distance * math.sin(math.radians(angle))
        #     model = model.pushPoints([(x, y)]).circle(radius).extrude(aperture_depth)
    elif ap_form == 'slit':
        length, width, height = (sim.resonator.aperture.length,
                                         sim.resonator.aperture.width, sim.resonator.aperture.height)
        # add a slit
        model = model.faces(">Z").workplane().rect(width, height).extrude(length)
    
    cq.exporters.export(model, path)