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

'''Test neurom.io.utils'''
import os
from neurom.fst import _io as io
from neurom.io import utils
from nose import tools as nt


_path = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(_path, '../../../test_data')
SWC_PATH = os.path.join(DATA_PATH, 'swc')

FILES = [os.path.join(SWC_PATH, f)
         for f in ['Neuron.swc',
                   'Single_apical_no_soma.swc',
                   'Single_apical.swc',
                   'Single_basal.swc',
                   'Single_axon.swc',
                   'sequential_trunk_off_0_16pt.swc',
                   'sequential_trunk_off_1_16pt.swc',
                   'sequential_trunk_off_42_16pt.swc',
                   'Neuron_no_missing_ids_no_zero_segs.swc']]

NO_SOMA_FILE = os.path.join(SWC_PATH, 'Single_apical_no_soma.swc')

DISCONNECTED_POINTS_FILE = os.path.join(SWC_PATH, 'Neuron_disconnected_components.swc')

MISSING_PARENTS_FILE = os.path.join(SWC_PATH, 'Neuron_missing_parents.swc')

NON_CONSECUTIVE_ID_FILE = os.path.join(SWC_PATH,
                                       'non_sequential_trunk_off_1_16pt.swc')

INVALID_ID_SEQUENCE_FILE = os.path.join(SWC_PATH,
                                        'non_increasing_trunk_off_1_16pt.swc')

SOMA_IDS = [[1, 2, 3],
            [],
            [1, 2, 3],
            [1, 2, 3],
            [1, 2, 3],
            [1, 9],
            [2, 10],
            [43, 51],
            [1, 2, 3]]

INIT_IDS = [[4, 215, 426, 637],
            [],
            [4],
            [4],
            [4],
            [2, 10],
            [3, 11],
            [44, 52],
            [4]]


_path = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(_path, '../../../test_data')
SWC_PATH = os.path.join(DATA_PATH, 'swc')

RAW_DATA = [io.load_data(f) for f in FILES]
NO_SOMA_RAW_DATA = io.load_data(NO_SOMA_FILE)



def _get_name(filename):
    return os.path.splitext(os.path.basename(filename))[0]


def _mock_load_neuron(filename):
    class MockNeuron(object):
        def __init__(self, name):
            self.soma = 42
            self.neurites = list()
            self.name = name

    return MockNeuron(_get_name(filename))


def test_load_neurons():
    nrns = utils.load_neurons(FILES, neuron_loader=_mock_load_neuron)
    for i, nrn in enumerate(nrns):
        nt.assert_equal(nrn.name, _get_name(FILES[i]))


def test_get_morph_files():
    ref = set(['Neuron_h5v2.h5', 'Neuron_2_branch_h5v2.h5',
               'Neuron.swc', 'Neuron_h5v1.h5', 'Neuron_2_branch_h5v1.h5'])

    FILE_PATH = os.path.abspath(os.path.join(DATA_PATH, 'valid_set'))
    files = set(os.path.basename(f) for f in utils.get_morph_files(FILE_PATH))

    nt.assert_equal(ref, files)
