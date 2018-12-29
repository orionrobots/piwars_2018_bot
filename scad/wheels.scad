include <tapered_cuboid.scad>

module initio_bot_wheel() {
    r=55/2;
    angle=360/40;
    difference() {
        cylinder(h=30, r=r);
        for(i=[1: 1: 40]) {
            rotate([0,0, angle * i])
            translate([r, 0, 15]) 
                rotate([0, 270, 0])
                translate([-16, -2, -5])
                tapered_cuboid(36,4, 10, taper=2);
        }
    }
}

module initio_gearbox() {
    
}

initio_bot_wheel();