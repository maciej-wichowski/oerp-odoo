from . import common


class TestPackageConfiguratorBox(common.TestProductPackageConfiguratorCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.package_box_type_1 = cls.PackageBoxType.create({'name': 'MY-BOX-TYPE-1'})
        cls.package_configurator_box_1 = cls.PackageConfiguratorBox.create(
            {
                'box_type_id': cls.package_box_type_1.id,
                # thickness: 1.5mm
                'carton_id': cls.package_carton_1.id,
                'wrappingpaper_inside_id': cls.package_wrappingpaper_1.id,
                'wrappingpaper_outside_id': cls.package_wrappingpaper_2.id,
                'base_length': 0,
                'base_width': 0,
                'base_height': 0,
                'lid_height': 0,
                # unit_cost == 2.0
                'lamination_outside_id': cls.package_lamination_1.id,
                'lamination_inside_id': cls.package_lamination_1.id,
            }
        )

    def test_01_configure_box(self):
        # WHEN
        cfg = self.package_configurator_box_1
        cfg.write(
            {
                'base_length': 165,
                'base_width': 42,
                'base_height': 14.5,
                'lid_height': 16,
                'lid_extra': 2.0,
                'outside_wrapping_extra': 20.0,
            }
        )
        # THEN
        # Layouts
        self.assertEqual(cfg.base_layout_length, 224)
        self.assertEqual(cfg.base_layout_width, 101)
        self.assertEqual(cfg.base_inside_wrapping_length, 224)
        self.assertEqual(cfg.base_inside_wrapping_width, 101)
        self.assertEqual(cfg.base_outside_wrapping_length, 264)
        self.assertEqual(cfg.base_outside_wrapping_width, 141)
        self.assertEqual(cfg.lid_layout_length, 232)
        self.assertEqual(cfg.lid_layout_width, 109)
        self.assertEqual(cfg.lid_inside_wrapping_length, 232)
        self.assertEqual(cfg.lid_inside_wrapping_width, 109)
        self.assertEqual(cfg.lid_outside_wrapping_length, 272)
        self.assertEqual(cfg.lid_outside_wrapping_width, 149)
        # Lamination
        # (224*101+232*109) * 1.2 / 1000000
        self.assertEqual(cfg.lamination_inside_area, 0.0574944)
        # 2 * 0.0574944
        self.assertEqual(cfg.lamination_inside_price, 0.1149888)
        # (264*141+272*149) * 1.2 / 1000000
        self.assertEqual(cfg.lamination_outside_area, 0.0933024)
        # 2 * 0.0933024
        self.assertEqual(cfg.lamination_outside_price, 0.1866048)
        # Quantities
        # carton layout is 1000x700 (mm)
        # outside wrappingpaper layout is 800x400 (mm)
        # inside wrappingpaper layout is 700x400 (mm)
        self.assertEqual(cfg.base_layout_fit_qty, 27)
        self.assertEqual(cfg.base_inside_fit_qty, 9)
        self.assertEqual(cfg.base_outside_fit_qty, 6)
        self.assertEqual(cfg.lid_layout_fit_qty, 27)
        self.assertEqual(cfg.lid_inside_fit_qty, 9)
        self.assertEqual(cfg.lid_outside_fit_qty, 5)

    def test_02_configure_box_with_circulation(self):
        # GIVEN
        cfg = self.package_configurator_box_1
        cfg.write(
            {
                'base_length': 165,
                'base_width': 42,
                'base_height': 14.5,
                'lid_height': 16,
                'lid_extra': 2.0,
                'outside_wrapping_extra': 20.0,
            }
        )
        # WHEN
        circulation_1, circulation_2 = self.PackageConfiguratorBoxCirculation.create(
            [
                {'quantity': 100, 'configurator_id': cfg.id},
                {'quantity': 200, 'configurator_id': cfg.id},
            ]
        )
        # THEN
        # Layouts
        self.assertEqual(cfg.base_layout_length, 224)
        self.assertEqual(cfg.base_layout_width, 101)
        self.assertEqual(cfg.base_inside_wrapping_length, 224)
        self.assertEqual(cfg.base_inside_wrapping_width, 101)
        self.assertEqual(cfg.base_outside_wrapping_length, 264)
        self.assertEqual(cfg.base_outside_wrapping_width, 141)
        self.assertEqual(cfg.lid_layout_length, 232)
        self.assertEqual(cfg.lid_layout_width, 109)
        self.assertEqual(cfg.lid_inside_wrapping_length, 232)
        self.assertEqual(cfg.lid_inside_wrapping_width, 109)
        self.assertEqual(cfg.lid_outside_wrapping_length, 272)
        self.assertEqual(cfg.lid_outside_wrapping_width, 149)
        # Lamination
        # (224*101+232*109) * 1.2 / 1000000
        self.assertEqual(cfg.lamination_inside_area, 0.0574944)
        # 2 * 0.0574944
        self.assertEqual(cfg.lamination_inside_price, 0.1149888)
        # (264*141+272*149) * 1.2 / 1000000
        self.assertEqual(cfg.lamination_outside_area, 0.0933024)
        # 2 * 0.0933024
        self.assertEqual(cfg.lamination_outside_price, 0.1866048)
        # Quantities
        # carton layout is 1000x700 (mm)
        # outside wrappingpaper layout is 800x400 (mm)
        # inside wrappingpaper layout is 700x400 (mm)
        self.assertEqual(cfg.base_layout_fit_qty, 27)
        self.assertEqual(cfg.base_inside_fit_qty, 9)
        self.assertEqual(cfg.base_outside_fit_qty, 6)
        self.assertEqual(cfg.lid_layout_fit_qty, 27)
        self.assertEqual(cfg.lid_inside_fit_qty, 9)
        self.assertEqual(cfg.lid_outside_fit_qty, 5)
        # Circulations
        # With 100 box circulation
        # 4 from base and 4 from lid
        self.assertEqual(circulation_1.total_carton_quantity, 8)
        # 12 from base, 12 from lid
        self.assertEqual(circulation_1.total_inside_wrappingpaper_quantity, 24)
        # 17 from base, 20 from lid.
        self.assertEqual(circulation_1.total_outside_wrappingpaper_quantity, 37)
        # 8*0.05 + 24*0.04 + 37*0.06
        self.assertEqual(circulation_1.total_cost, 3.5799999999999996)
        # 3.5799999999999996 / 100
        self.assertEqual(circulation_1.unit_cost, 0.0358)
        # With 200 box circulation
        # 4 from base and 4 from lid
        self.assertEqual(circulation_2.total_carton_quantity, 16)
        # 12 from base, 12 from lid
        self.assertEqual(circulation_2.total_inside_wrappingpaper_quantity, 46)
        # 17 from base, 20 from lid.
        self.assertEqual(circulation_2.total_outside_wrappingpaper_quantity, 74)
        # 16*0.05 + 46*0.04 + 74*0.06
        self.assertEqual(circulation_2.total_cost, 7.08)
        # 6.52 / 200
        self.assertEqual(circulation_2.unit_cost, 0.0354)

    def test_03_configure_box_missing_base_height(self):
        # WHEN
        cfg = self.package_configurator_box_1
        cfg.write(
            {
                'base_length': 165,
                'base_width': 42,
                'base_height': 0,
                'lid_height': 16,
                'lid_extra': 2.0,
                'outside_wrapping_extra': 20.0,
            }
        )
        # THEN
        self.assertEqual(cfg.base_layout_length, 0)
        self.assertEqual(cfg.base_layout_width, 0)
        self.assertEqual(cfg.base_inside_wrapping_length, 0)
        self.assertEqual(cfg.base_inside_wrapping_width, 0)
        self.assertEqual(cfg.base_outside_wrapping_length, 0)
        self.assertEqual(cfg.base_outside_wrapping_width, 0)
        self.assertEqual(cfg.lid_layout_length, 0)
        self.assertEqual(cfg.lid_layout_width, 0)
        self.assertEqual(cfg.lid_inside_wrapping_length, 0)
        self.assertEqual(cfg.lid_inside_wrapping_width, 0)
        self.assertEqual(cfg.lid_outside_wrapping_length, 0)
        self.assertEqual(cfg.lid_outside_wrapping_width, 0)
        self.assertEqual(cfg.lamination_inside_area, 0)
        self.assertEqual(cfg.lamination_inside_price, 0)
        self.assertEqual(cfg.lamination_outside_area, 0)
        self.assertEqual(cfg.lamination_outside_price, 0)
