# Copyright (c) 2015, Ecole Polytechnique Federale de Lausanne, Blue Brain Project
# All rights reserved.
#
# This file is part of NeuroM <https://github.com/BlueBrain/NeuroM>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     1. Redistributions of source code must retain the above copyright
#        notice, this list of conditions and the following disclaimer.
#     2. Redistributions in binary form must reproduce the above copyright
#        notice, this list of conditions and the following disclaimer in the
#        documentation and/or other materials provided with the distribution.
#     3. Neither the name of the copyright holder nor the names of
#        its contributors may be used to endorse or promote products
#        derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

'''Test neurom.fst.get features'''

import os
import numpy as np
from nose import tools as nt
from neurom.core.types import NeuriteType
from neurom.core.population import Population
from neurom import fst


_PWD = os.path.dirname(os.path.abspath(__file__))
NRN_FILES = [os.path.join(_PWD, '../../../test_data/h5/v1', f)
             for f in ('Neuron.h5', 'Neuron_2_branch.h5', 'bio_neuron-001.h5')]

NRNS = fst.load_neurons(NRN_FILES)
NRN = NRNS[0]
POP = Population(NRNS)

NEURITES = (NeuriteType.axon,
            NeuriteType.apical_dendrite,
            NeuriteType.basal_dendrite,
            NeuriteType.all)


def test_number_of_sections_pop():

    feat = 'number_of_sections'

    nt.assert_items_equal(fst.get(feat, POP), [84, 42, 202])

    nt.assert_items_equal(fst.get(feat, POP, neurite_type=NeuriteType.all),
                          [84, 42, 202])

    nt.assert_items_equal(fst.get(feat, POP, neurite_type=NeuriteType.axon),
                          [21, 21, 179])

    nt.assert_items_equal(fst.get(feat, POP, neurite_type=NeuriteType.apical_dendrite),
                          [21, 0, 0])

    nt.assert_items_equal(fst.get(feat, POP, neurite_type=NeuriteType.basal_dendrite),
                          [42, 21, 23])


def test_number_of_sections_nrn():

    feat = 'number_of_sections'

    nt.assert_items_equal(fst.get(feat, NRN), [84])

    nt.assert_items_equal(fst.get(feat, NRN, neurite_type=NeuriteType.all),
                          [84])

    nt.assert_items_equal(fst.get(feat, NRN, neurite_type=NeuriteType.axon),
                          [21])

    nt.assert_items_equal(fst.get(feat, NRN, neurite_type=NeuriteType.apical_dendrite),
                          [21])

    nt.assert_items_equal(fst.get(feat, NRN, neurite_type=NeuriteType.basal_dendrite),
                          [42])


def test_number_of_segments_pop():

    feat = 'number_of_segments'

    nt.assert_items_equal(fst.get(feat, POP), [840, 419, 5179])

    nt.assert_items_equal(fst.get(feat, POP, neurite_type=NeuriteType.all),
                          [840, 419, 5179])

    nt.assert_items_equal(fst.get(feat, POP, neurite_type=NeuriteType.axon),
                          [210, 209, 4508])

    nt.assert_items_equal(fst.get(feat, POP, neurite_type=NeuriteType.apical_dendrite),
                          [210, 0, 0])

    nt.assert_items_equal(fst.get(feat, POP, neurite_type=NeuriteType.basal_dendrite),
                          [420, 210, 671])


def test_number_of_segments_nrn():

    feat = 'number_of_segments'

    nt.assert_items_equal(fst.get(feat, NRN), [840])

    nt.assert_items_equal(fst.get(feat, NRN, neurite_type=NeuriteType.all),
                          [840])

    nt.assert_items_equal(fst.get(feat, NRN, neurite_type=NeuriteType.axon),
                          [210])

    nt.assert_items_equal(fst.get(feat, NRN, neurite_type=NeuriteType.apical_dendrite),
                          [210])

    nt.assert_items_equal(fst.get(feat, NRN, neurite_type=NeuriteType.basal_dendrite),
                          [420])


def test_number_of_neurites_pop():

    feat = 'number_of_neurites'

    nt.assert_items_equal(fst.get(feat, POP), [4, 2, 4])

    nt.assert_items_equal(fst.get(feat, POP, neurite_type=NeuriteType.all),
                          [4, 2, 4])

    nt.assert_items_equal(fst.get(feat, POP, neurite_type=NeuriteType.axon),
                          [1, 1, 1])

    nt.assert_items_equal(fst.get(feat, POP, neurite_type=NeuriteType.apical_dendrite),
                          [1, 0, 0])

    nt.assert_items_equal(fst.get(feat, POP, neurite_type=NeuriteType.basal_dendrite),
                          [2, 1, 3])


def test_number_of_neurites_nrn():

    feat = 'number_of_neurites'

    nt.assert_items_equal(fst.get(feat, NRN), [4])

    nt.assert_items_equal(fst.get(feat, NRN, neurite_type=NeuriteType.all),
                          [4])

    nt.assert_items_equal(fst.get(feat, NRN, neurite_type=NeuriteType.axon),
                          [1])

    nt.assert_items_equal(fst.get(feat, NRN, neurite_type=NeuriteType.apical_dendrite),
                          [1])

    nt.assert_items_equal(fst.get(feat, NRN, neurite_type=NeuriteType.basal_dendrite),
                          [2])


def test_total_length_pop():

    feat = 'total_length'

    nt.ok_(np.allclose(fst.get(feat, POP),
                       [840.47744821, 418.83424432, 13250.82577394]))

    nt.ok_(np.allclose(fst.get(feat, POP, neurite_type=NeuriteType.all),
                       [840.47744821, 418.83424432, 13250.82577394]))

    nt.ok_(np.allclose(fst.get(feat, POP, neurite_type=NeuriteType.axon),
                       [207.81090481, 207.81088342, 11767.15611522]))

    nt.ok_(np.allclose(fst.get(feat, POP, neurite_type=NeuriteType.apical_dendrite),
                       [214.34043344, 0, 0]))

    nt.ok_(np.allclose(fst.get(feat, POP, neurite_type=NeuriteType.basal_dendrite),
                       [418.32610997, 211.0233609, 1483.66965872]))


def test_total_length_nrn():

    feat = 'total_length'

    nt.ok_(np.allclose(fst.get(feat, NRN),
                       [840.47744821]))

    nt.ok_(np.allclose(fst.get(feat, NRN, neurite_type=NeuriteType.all),
                       [840.47744821]))

    nt.ok_(np.allclose(fst.get(feat, NRN, neurite_type=NeuriteType.axon),
                       [207.81090481]))

    nt.ok_(np.allclose(fst.get(feat, NRN, neurite_type=NeuriteType.apical_dendrite),
                       [214.34043344]))

    nt.ok_(np.allclose(fst.get(feat, NRN, neurite_type=NeuriteType.basal_dendrite),
                       [418.32610997]))
