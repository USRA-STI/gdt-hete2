#  CONTAINS TECHNICAL DATA/COMPUTER SOFTWARE DELIVERED TO THE U.S. GOVERNMENT
#  WITH UNLIMITED RIGHTS
#
#  Grant No.: 80NSSC21K0651
#  Grantee Name: Universities Space Research Association
#  Grantee Address: 425 3rd Street SW, Suite 950, Washington DC 20024
#
#  Copyright (c) 2024 by Universities Space Research Association (USRA). All rights reserved.
#
#  Developed by:
#       William Cleveland
#       Universities Space Research Association
#       Science and Technology Institute
#       https://sti.usra.edu
#
#  This work is a derivative of the Gamma-ray Data Tools (GDT), including the Core and Fermi packages, originally
#  developed by the following:
#
#       William Cleveland and Adam Goldstein
#       Universities Space Research Association
#       Science and Technology Institute
#       https://sti.usra.edu
#
#       Daniel Kocevski
#       National Aeronautics and Space Administration (NASA)
#       Marshall Space Flight Center
#       Astrophysics Branch (ST-12)
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance
#   with the License. You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
#  an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations under the License.

import unittest
from gdt.core import data_path
from gdt.core.data_primitives import TimeBins, TimeEnergyBins, Gti

from gdt.missions.hete2.fregate.detectors import FregateDetectors
from gdt.missions.hete2.fregate.lightcurve import FregateLightCurve, FregatePhaii


class TestFregateLightCurve(unittest.TestCase):
    lc_file: FregateLightCurve

    @classmethod
    def setUpClass(cls):
        path = data_path / 'hete2-fregate' / 'GAMMA_sum_20020531.lc'
        cls.lc_file = FregateLightCurve.open(path)

    @classmethod
    def tearDownClass(cls):
        cls.lc_file.close()

    def test_metadata(self):
        self.assertEqual(self.lc_file.num_dets, 4)
        self.assertEqual(self.lc_file.detectors, [FregateDetectors.A, FregateDetectors.B,
                                                  FregateDetectors.C, FregateDetectors.D])
        self.assertEqual(self.lc_file.time_zero, 706916972.2000004)

    def test_time_bins(self):
        time_bin = self.lc_file.time_bins('A', 0)
        self.assertEqual(type(time_bin), TimeBins)
        self.assertAlmostEqual(time_bin.range[0], -403.381, places=3)
        self.assertAlmostEqual(time_bin.range[1], 83885.53, places=2)
        self.assertEqual(len(time_bin.counts), 73620)

    def test_time_energy_bins(self):
        te_bins = self.lc_file.time_energy_bins('A', 0)
        self.assertEqual(type(te_bins), TimeEnergyBins)
        self.assertAlmostEqual(te_bins.tstart[0], -403.381, places=3)
        self.assertAlmostEqual(te_bins.tstop[-1], 83885.53, places=2)
        self.assertEqual(len(te_bins.counts), 73620)
        self.assertEqual(te_bins.energy_range[0], 8.0)
        self.assertEqual(te_bins.energy_range[1], 40.0)

    def test_phaii(self):
        pha = self.lc_file.phaii('B', 2)
        self.assertEqual(type(pha), FregatePhaii)
        self.assertEqual(pha.ebounds.num_intervals, 1)
        self.assertEqual(pha.ebounds.range[0], 32.0)
        self.assertEqual(pha.ebounds.range[1], 400.0)
        self.assertAlmostEqual(pha.time_range[0], -403.381, places=3)
        self.assertAlmostEqual(pha.time_range[1], 83885.53, places=2)
        self.assertAlmostEqual(pha.trigtime, 706916972.2000, places=4)
        self.assertEqual(type(pha.gti), Gti)
        self.assertEqual(pha.gti.num_intervals, 22)
        self.assertAlmostEqual(pha.gti.range[0], -395.517, places=3)
        self.assertAlmostEqual(pha.gti.range[1], 83884.219, places=3)

    def test_gti(self):
        gti = self.lc_file.gti
        self.assertEqual(type(gti), Gti)
        self.assertEqual(gti.num_intervals, 22)
        self.assertAlmostEqual(gti.range[0], -395.517, places=3)
        self.assertAlmostEqual(gti.range[1], 83884.219, places=3)


if __name__ == '__main__':
    unittest.main()
