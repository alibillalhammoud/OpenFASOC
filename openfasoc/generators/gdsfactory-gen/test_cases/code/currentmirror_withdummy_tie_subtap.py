from glayout.pdk.mappedpdk import MappedPDK
from gdsfactory import Component
from glayout.pdk.util.comp_utils import move
from glayout.pdk.util.port_utils import remove_ports_with_prefix
from glayout.primitives.fet import nmos
from glayout.primitives.fet import pmos
from glayout.primitives.guardring import tapring
from glayout.primitives.mimcap import mimcap
from glayout.primitives.mimcap import mimcap_array
from glayout.primitives.via_gen import via_stack
from glayout.primitives.via_gen import via_array
from glayout.placement.two_transistor_interdigitized import two_nfet_interdigitized
from glayout.placement.two_transistor_interdigitized import two_pfet_interdigitized
from glayout.components.diff_pair import diff_pair
from glayout.routing.smart_route import smart_route
from glayout.routing.L_route import L_route
from glayout.routing.c_route import c_route
from glayout.routing.straight_route import straight_route
from glayout.pdk.util.comp_utils import prec_ref_center
from glayout.pdk.util.comp_utils import evaluate_bbox

def currentmirror_cell(
	pdk: MappedPDK,
	numcols: int, 
):
	currentmirror = Component()
	maxmetalsep = pdk.util_max_metal_seperation()
	double_maxmetalsep = 2*pdk.util_max_metal_seperation()
	triple_maxmetalsep = 3*pdk.util_max_metal_seperation()
	quadruple_maxmetalsep = 4*pdk.util_max_metal_seperation()
	# placing cmirror_nfet centered at the origin
	cmirror_nfet = two_nfet_interdigitized(pdk,**{'numcols': numcols})
	cmirror_nfet_ref = prec_ref_center(cmirror_nfet)
	currentmirror.add(cmirror_nfet_ref)
	currentmirror.add_ports(cmirror_nfet_ref.get_ports_list(),prefix="cmirror_nfet_")
	currentmirror << c_route(pdk,currentmirror.ports["cmirror_nfet_A_source_E"],currentmirror.ports["cmirror_nfet_B_source_E"],**{})
	currentmirror << c_route(pdk,currentmirror.ports["cmirror_nfet_A_gate_E"],currentmirror.ports["cmirror_nfet_B_gate_E"],**{})
	currentmirror << c_route(pdk,currentmirror.ports["cmirror_nfet_A_gate_W"],currentmirror.ports["cmirror_nfet_A_drain_W"],**{})
	return currentmirror
