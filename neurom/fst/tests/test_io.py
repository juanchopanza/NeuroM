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

'''Test neurom.fst._io module loaders'''

from nose import tools as nt
import os
from neurom.fst import _io
from neurom.fst import _neuritefunc as _nf
from neurom.fst import get
from neurom.exceptions import SomaError, RawDataError
from neurom.core.tree import ipreorder


_path = os.path.dirname(os.path.abspath(__file__))
DATA_ROOT = os.path.join(_path, '../../../test_data')
DATA_PATH = os.path.join(_path, '../../../test_data/valid_set')
FILENAMES = [os.path.join(DATA_PATH, f)
             for f in ['Neuron.swc', 'Neuron_h5v1.h5', 'Neuron_h5v2.h5']]

NRN_NAMES = ('Neuron', 'Neuron_h5v1', 'Neuron_h5v2')


SWC_PATH = os.path.join(DATA_ROOT, 'swc')
NO_SOMA_FILE = os.path.join(SWC_PATH, 'Single_apical_no_soma.swc')

DISCONNECTED_POINTS_FILE = os.path.join(SWC_PATH, 'Neuron_disconnected_components.swc')

MISSING_PARENTS_FILE = os.path.join(SWC_PATH, 'Neuron_missing_parents.swc')

NON_CONSECUTIVE_ID_FILE = os.path.join(SWC_PATH,
                                       'non_sequential_trunk_off_1_16pt.swc')

INVALID_ID_SEQUENCE_FILE = os.path.join(SWC_PATH,
                                        'non_increasing_trunk_off_1_16pt.swc')

def test_load_neuron():

    nrn = _io.load_neuron(FILENAMES[0])
    nt.assert_true(isinstance(NRN, _io.Neuron))
    nt.assert_equal(NRN.name, 'Neuron')


def test_neuron_name():

    for fn, nn in zip(FILENAMES, NRN_NAMES):
        nrn = _io.load_neuron(fn)
        nt.eq_(nrn.name, nn)


NRN = _io.load_neuron(FILENAMES[0])


def test_neuron_section_ids():

    # check section IDs
    for i, sec in enumerate(NRN.sections):
        nt.eq_(i, sec.id)

def test_neuron_sections():
    all_nodes = set(NRN.sections)
    neurite_nodes = set(_nf.iter_sections(NRN.neurites))

    # check no duplicates
    nt.assert_true(len(all_nodes) == len(NRN.sections))

    # check all neurite tree nodes are
    # in sections attribute
    nt.assert_true(len(set(NRN.sections) - neurite_nodes) > 0)


def test_neuron_sections_are_connected():
    # check traversal by counting number of sections un trees
    for nrt in NRN.neurites:
        root_node = nrt.root_node
        nt.assert_equal(sum(1 for _ in ipreorder(root_node)),
                        sum(1 for _ in ipreorder(NRN.sections[root_node.id])))


def test_load_neuron_soma_only():

    nrn = _io.load_neuron(os.path.join(DATA_ROOT, 'swc', 'Soma_origin.swc'))
    nt.eq_(len(nrn.neurites), 0)
    nt.assert_equal(nrn.name, 'Soma_origin')


@nt.raises(SomaError)
def test_load_neuron_no_soma_raises_SomaError():
    _io.load_neuron(NO_SOMA_FILE)


# TODO: decide if we want to check for this in fst.
@nt.nottest
@nt.raises(RawDataError)
def test_load_neuron_disconnected_points_raises():
    _io.load_neuron(DISCONNECTED_POINTS_FILE)


@nt.raises(RawDataError)
def test_load_neuron_missing_parents_raises():
    _io.load_neuron(MISSING_PARENTS_FILE)


# TODO: decide if we want to check for this in fst.
@nt.nottest
@nt.raises(RawDataError)
def test_load_neuron_invalid_id_sequence_raises():
    _io.load_neuron(INVALID_ID_SEQUENCE_FILE);


def test_load_neurons_directory():

    pop = _io.load_neurons(DATA_PATH)
    nt.assert_equal(len(pop.neurons), 5)
    nt.assert_equal(len(pop), 5)
    nt.assert_equal(pop.name, 'valid_set')
    for nrn in pop:
        nt.assert_true(isinstance(nrn, _io.Neuron))


def test_load_neurons_directory_name():
    pop = _io.load_neurons(DATA_PATH, name='test123')
    nt.assert_equal(len(pop.neurons), 5)
    nt.assert_equal(len(pop), 5)
    nt.assert_equal(pop.name, 'test123')
    for nrn in pop:
        nt.assert_true(isinstance(nrn, _io.Neuron))


def test_load_neurons_filenames():

    pop = _io.load_neurons(FILENAMES, name='test123')
    nt.assert_equal(len(pop.neurons), 3)
    nt.assert_equal(pop.name, 'test123')
    for nrn, name in zip(pop.neurons, NRN_NAMES):
        nt.assert_true(isinstance(nrn, _io.Neuron))
        nt.assert_equal(nrn.name, name)

SWC_PATH = os.path.join(DATA_ROOT, 'swc', 'ordering')
SWC_ORD_REF = _io.load_neuron(os.path.join(SWC_PATH, 'sample.swc'))


def test_load_neuron_mixed_tree_swc():
    nrn_mix =  _io.load_neuron(os.path.join(SWC_PATH, 'sample_mixed_tree_sections.swc'))
    nt.assert_items_equal(get('number_of_sections_per_neurite', nrn_mix), [5, 3])

    nt.assert_items_equal(get('number_of_sections_per_neurite', nrn_mix),
                          get('number_of_sections_per_neurite', SWC_ORD_REF))

    nt.assert_items_equal(get('number_of_segments', nrn_mix),
                          get('number_of_segments', SWC_ORD_REF))

    nt.assert_items_equal(get('total_length', nrn_mix),
                          get('total_length', SWC_ORD_REF))


def test_load_neuron_section_order_break_swc():
    nrn_mix =  _io.load_neuron(os.path.join(SWC_PATH, 'sample_disordered.swc'))

    nt.assert_items_equal(get('number_of_sections_per_neurite', nrn_mix), [5, 3])

    nt.assert_items_equal(get('number_of_sections_per_neurite', nrn_mix),
                          get('number_of_sections_per_neurite', SWC_ORD_REF))

    nt.assert_items_equal(get('number_of_segments', nrn_mix),
                          get('number_of_segments', SWC_ORD_REF))

    nt.assert_items_equal(get('total_length', nrn_mix),
                          get('total_length', SWC_ORD_REF))


H5_PATH = os.path.join(DATA_ROOT, 'h5', 'v1', 'ordering')
H5_ORD_REF = _io.load_neuron(os.path.join(H5_PATH, 'sample.h5'))


def test_load_neuron_mixed_tree_h5():
    nrn_mix =  _io.load_neuron(os.path.join(H5_PATH, 'sample_mixed_tree_sections.h5'))
    nt.assert_items_equal(get('number_of_sections_per_neurite', nrn_mix), [5, 3])
    nt.assert_items_equal(get('number_of_sections_per_neurite', nrn_mix),
                          get('number_of_sections_per_neurite', H5_ORD_REF))
