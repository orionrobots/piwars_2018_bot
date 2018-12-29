cubeh = 40;
cubew = 40;
axle_size= 5;
screw_d = 3; // m3
wheel_height=20;
wheel_radius=60;
dome_radius=wheel_radius*1.5;

module slot() {
    translate([40, 0, 0]) union() {
      cube([cubeh, cubew, wheel_height*2], center=true);
      translate([-10, cubew/2 + 5, 5]) rotate([90, 0, 0]) cylinder(cubew + 10, r=axle_size, centre=true);
    }
};


dome_angle=acos(wheel_radius/(2 * dome_radius));
function sphere_dist()=sin(dome_angle) * dome_radius;

module wheel_dome() {
    translate([0, 0, wheel_height]) intersection() {
      translate([0, 0, sphere_dist()]) sphere(dome_radius);
      cylinder(h=wheel_height, r=wheel_radius);
    };
};

*wheel_dome();
module uncut_wheel() {
  union() {
    cylinder(h=wheel_height, r=wheel_radius, center=true);
    wheel_dome();
  }
}

module wheel_half() {
    difference() {
        uncut_wheel();
        // slots
        for (i=[0, 120, 240]) {
          rotate([0, 0, i]) slot();
        }
    };
};

module hex_nut(r=6) {
  cylinder(h=100, r=r, $fa=60);
};

difference() {
    union() {
        wheel_half();
        translate([0, 0, -wheel_height]) rotate([0, 180, 0]) wheel_half();
    }
    // screw holes
    for (i=[60, 180, 300]) {
      rotate([0, 0, i])
      union() {
          translate([10, 0, -wheel_height/2]) cylinder(r=screw_d, h=wheel_height*4, center=true);
          translate([10, 0, +wheel_height/2]) hex_nut(6);
          rotate([180, 0, 0]) translate([10, 0, +wheel_height/2]) hex_nut(6);
      }
   }
}