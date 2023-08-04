# !/usr/bin/env python
"""Define the unit tests for the :mod:`colour.io.luts.__init__` module."""

from __future__ import annotations

import numpy as np
import os
import shutil
import tempfile
import unittest

from colour.io import LUTSequence, read_LUT, write_LUT

__author__ = "Colour Developers"
__copyright__ = "Copyright 2013 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "ROOT_LUTS",
    "TestReadLUT",
    "TestWriteLUT",
]

ROOT_LUTS: str = os.path.join(os.path.dirname(__file__), "resources")


class TestReadLUT(unittest.TestCase):
    """
    Define :func:`colour.io.luts.__init__.read_LUT` definition unit tests
    methods.
    """

    def test_read_LUT(self):
        """Test :func:`colour.io.luts.__init__.read_LUT` definition."""

        LUT_1 = read_LUT(
            os.path.join(ROOT_LUTS, "sony_spi1d", "eotf_sRGB_1D.spi1d")
        )

        np.testing.assert_array_almost_equal(
            LUT_1.table,
            np.array(
                [
                    -7.73990000e-03,
                    5.16000000e-04,
                    1.22181000e-02,
                    3.96819000e-02,
                    8.71438000e-02,
                    1.57439400e-01,
                    2.52950100e-01,
                    3.75757900e-01,
                    5.27729400e-01,
                    7.10566500e-01,
                    9.25840600e-01,
                    1.17501630e00,
                    1.45946870e00,
                    1.78049680e00,
                    2.13933380e00,
                    2.53715520e00,
                ]
            ),
        )
        self.assertEqual(LUT_1.name, "eotf sRGB 1D")
        self.assertEqual(LUT_1.dimensions, 1)
        np.testing.assert_array_equal(LUT_1.domain, np.array([-0.1, 1.5]))
        self.assertEqual(LUT_1.size, 16)
        self.assertListEqual(
            LUT_1.comments,
            ['Generated by "Colour 0.3.11".', '"colour.models.eotf_sRGB".'],
        )

        LUT_2 = read_LUT(
            os.path.join(ROOT_LUTS, "resolve_cube", "LogC_Video.cube")
        )
        np.testing.assert_array_almost_equal(
            LUT_2[0].table,
            np.array(
                [
                    [0.00000000, 0.00000000, 0.00000000],
                    [0.02708500, 0.02708500, 0.02708500],
                    [0.06304900, 0.06304900, 0.06304900],
                    [0.11314900, 0.11314900, 0.11314900],
                    [0.18304900, 0.18304900, 0.18304900],
                    [0.28981100, 0.28981100, 0.28981100],
                    [0.41735300, 0.41735300, 0.41735300],
                    [0.54523100, 0.54523100, 0.54523100],
                    [0.67020500, 0.67020500, 0.67020500],
                    [0.78963000, 0.78963000, 0.78963000],
                    [0.88646800, 0.88646800, 0.88646800],
                    [0.94549100, 0.94549100, 0.94549100],
                    [0.97644900, 0.97644900, 0.97644900],
                    [0.98924800, 0.98924800, 0.98924800],
                    [0.99379700, 0.99379700, 0.99379700],
                    [1.00000000, 1.00000000, 1.00000000],
                ]
            ),
        )
        self.assertEqual(LUT_2[1].size, 4)

    def test_raise_exception_read_LUT(self):
        """
        Test :func:`colour.io.luts.__init__.read_LUT` definition raised
        exception.
        """

        self.assertRaises(
            ValueError,
            read_LUT,
            os.path.join(ROOT_LUTS, "sony_spi1d", "Exception_Raising.spi1d"),
        )


class TestWriteLUT(unittest.TestCase):
    """
    Define :func:`colour.io.luts.__init__.write_LUT` definition unit tests
    methods.
    """

    def setUp(self):
        """Initialise the common tests attributes."""

        self._temporary_directory = tempfile.mkdtemp()

    def tearDown(self):
        """After tests actions."""

        shutil.rmtree(self._temporary_directory)

    def test_write_LUT(self):
        """Test :func:`colour.io.luts.__init__.write_LUT` definition."""

        LUT_1_r = read_LUT(
            os.path.join(ROOT_LUTS, "sony_spi1d", "eotf_sRGB_1D.spi1d")
        )

        write_LUT(
            LUT_1_r,
            os.path.join(self._temporary_directory, "eotf_sRGB_1D.spi1d"),
        )

        LUT_1_t = read_LUT(
            os.path.join(self._temporary_directory, "eotf_sRGB_1D.spi1d")
        )

        self.assertEqual(LUT_1_r, LUT_1_t)

        write_LUT(
            LUTSequence(LUT_1_r),
            os.path.join(self._temporary_directory, "eotf_sRGB_1D.spi1d"),
        )

        self.assertEqual(LUT_1_r, LUT_1_t)

        LUT_2_r = read_LUT(
            os.path.join(
                ROOT_LUTS,
                "resolve_cube",
                "Three_Dimensional_Table_With_Shaper.cube",
            )
        )

        write_LUT(
            LUT_2_r,
            os.path.join(
                self._temporary_directory,
                "Three_Dimensional_Table_With_Shaper.cube",
            ),
        )

        LUT_2_t = read_LUT(
            os.path.join(
                self._temporary_directory,
                "Three_Dimensional_Table_With_Shaper.cube",
            )
        )

        self.assertEqual(LUT_2_r, LUT_2_t)


if __name__ == "__main__":
    unittest.main()
