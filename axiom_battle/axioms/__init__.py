from .axiom_base import Axiom, Attack, AxiomCase, Severity, Verdict
from .axiom1_growth import GrowthAxiom
from .axiom2_light import LightAxiom
from .axiom3_color import ColorAxiom
from .axiom4_layout import LayoutAxiom
from .axiom5_narrative import NarrativeAxiom
from .axiom6_boundary import BoundaryAxiom
from .axiom7_freedom import FreedomAxiom
from .axiom8_causal import CausalAxiom

# v2 精化版
from .axiom_v2_growth import GrowthAxiomV2
from .axiom_v2_light import LightAxiomV2
from .axiom_v2_color import ColorAxiomV2
from .axiom_v2_narrative import NarrativeAxiomV2
from .axiom_v2_boundary import BoundaryAxiomV2
from .axiom_v2_freedom import FreedomAxiomV2
from .axiom_v2_layout import LayoutAxiomV2
from .axiom8_causal_v2 import CausalAxiomV2
from .axiom8_causal_v3 import CausalAxiomV3
from .axiom_v3_growth import GrowthAxiomV3
from .axiom_v3_layout import LayoutAxiomV3

AXIOM_REGISTRY = {
    "axiom1_growth": GrowthAxiom,
    "axiom2_light": LightAxiom,
    "axiom3_color": ColorAxiom,
    "axiom4_layout": LayoutAxiom,
    "axiom5_narrative": NarrativeAxiom,
    "axiom6_boundary": BoundaryAxiom,
    "axiom7_freedom": FreedomAxiom,
    "axiom8_causal": CausalAxiom,
}

AXIOM_REGISTRY_V2 = {
    "axiom1_growth_v2": GrowthAxiomV2,
    "axiom2_light_v2": LightAxiomV2,
    "axiom3_color_v2": ColorAxiomV2,
    "axiom4_layout_v2": LayoutAxiomV2,
    "axiom5_narrative_v2": NarrativeAxiomV2,
    "axiom6_boundary_v2": BoundaryAxiomV2,
    "axiom7_freedom_v2": FreedomAxiomV2,
    "axiom8_causal_v2": CausalAxiomV2,
}

AXIOM_REGISTRY_V3 = {
    "axiom1_growth_v3": GrowthAxiomV3,
    "axiom8_causal_v3": CausalAxiomV3,
    "axiom4_layout_v3": LayoutAxiomV3,
}

__all__ = [
    "Axiom", "Attack", "AxiomCase", "Severity", "Verdict",
    "GrowthAxiom", "LightAxiom", "ColorAxiom",
    "LayoutAxiom", "NarrativeAxiom", "BoundaryAxiom", "FreedomAxiom",
    "CausalAxiom",
    "GrowthAxiomV2", "LightAxiomV2", "ColorAxiomV2",
    "LayoutAxiomV2",
    "NarrativeAxiomV2", "BoundaryAxiomV2", "FreedomAxiomV2",
    "CausalAxiomV2",
    "GrowthAxiomV3", "CausalAxiomV3", "LayoutAxiomV3",
    "AXIOM_REGISTRY", "AXIOM_REGISTRY_V2", "AXIOM_REGISTRY_V3",
]
