from .axiom_base import Axiom, Attack, AxiomCase, Severity, Verdict
from .axiom1_growth import GrowthAxiom
from .axiom2_light import LightAxiom
from .axiom3_color import ColorAxiom
from .axiom4_layout import LayoutAxiom
from .axiom5_narrative import NarrativeAxiom
from .axiom6_boundary import BoundaryAxiom
from .axiom7_freedom import FreedomAxiom

AXIOM_REGISTRY = {
    "axiom1_growth": GrowthAxiom,
    "axiom2_light": LightAxiom,
    "axiom3_color": ColorAxiom,
    "axiom4_layout": LayoutAxiom,
    "axiom5_narrative": NarrativeAxiom,
    "axiom6_boundary": BoundaryAxiom,
    "axiom7_freedom": FreedomAxiom,
}
