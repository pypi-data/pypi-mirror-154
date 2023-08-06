"""MIDAS upgrade module for Smart Nord data simulator."""
import logging

from midas.util.runtime_config import RuntimeConfig

from .sbdata import SimbenchDataModule

LOG = logging.getLogger(__name__)


class DLPDataModule(SimbenchDataModule):
    def __init__(self):
        super().__init__("dlpdata", LOG)
        self.default_grid = "midasmv"
        self.default_sim_name = "DefaultLoadProfiles"
        self.default_import_str = "midas.core:DLPSimulator"
        self.models = {
            "H0": ["p_mw", "q_mvar"],
            "G0": ["p_mw", "q_mvar"],
            "G1": ["p_mw", "q_mvar"],
            "G2": ["p_mw", "q_mvar"],
            "G3": ["p_mw", "q_mvar"],
            "G4": ["p_mw", "q_mvar"],
            "G5": ["p_mw", "q_mvar"],
            "G6": ["p_mw", "q_mvar"],
            "L0": ["p_mw", "q_mvar"],
            "L1": ["p_mw", "q_mvar"],
            "L2": ["p_mw", "q_mvar"],
        }

    def check_sim_params(self, module_params, **kwargs):
        """Check the params for a certain simulator instance."""
        self.sim_params.setdefault("sim_name", module_params["sim_name"])
        self.sim_params.setdefault("cmd", module_params["cmd"])
        self.sim_params.setdefault("import_str", module_params["import_str"])
        self.sim_params.setdefault("step_size", module_params["step_size"])
        self.sim_params.setdefault("start_date", module_params["start_date"])
        self.sim_params.setdefault("data_path", module_params["data_path"])
        self.sim_params.setdefault("cos_phi", module_params["cos_phi"])
        self.sim_params.setdefault("interpolate", module_params["interpolate"])
        self.sim_params.setdefault(
            "randomize_data", module_params["randomize_data"]
        )
        self.sim_params.setdefault(
            "randomize_cos_phi", module_params["randomize_cos_phi"]
        )
        self.sim_params.setdefault(
            "noise_factor", module_params["noise_factor"]
        )
        self.sim_params.setdefault("mapping", dict())
        self.sim_params.setdefault("seed_max", self.scenario["seed_max"])
        self.sim_params.setdefault(
            "seed", self.scenario["rng"].randint(self.scenario["seed_max"])
        )
        self.sim_params.setdefault(
            "filename",
            RuntimeConfig().data["default_load_profiles"][0]["name"],
        )

    def create_default_mapping(self):
        default_mapping = dict()
        # if self.sim_name == self.default_grid:
        #     if model == "land":
        #         default_mapping = {
        #             1: [[0, 1.0], [2, 1.0], [3, 3.0], [6, 2.0], [7, 1.0]],
        #             3: [[0, 1.0], [2, 1.0], [3, 1.0], [6, 1.0], [7, 1.0]],
        #             4: [[0, 3.0], [3, 2.0], [7, 1.0]],
        #             5: [[3, 2.0], [7, 1.0]],
        #             6: [[0, 1.0], [3, 2.0]],
        #             7: [[0, 3.0], [2, 1.0], [3, 2.0], [7, 1.0]],
        #             8: [[0, 2.0], [3, 1.0], [6, 1.0]],
        #             9: [[2, 1.0], [3, 2.0], [6, 2.0], [7, 1.0]],
        #             10: [[0, 2.0], [2, 1.0], [3, 2.0], [6, 2.0], [7, 1.0]],
        #             11: [[0, 2.0], [2, 1.0], [3, 2.0], [6, 2.0], [7, 1.0]],
        #         }

        return default_mapping

    def start_models(self):
        """Start models of a certain simulator."""
        map_key = "mapping"

        if not self.sim_params[map_key]:
            self.sim_params[map_key] = self.create_default_mapping()

        mapping = self.scenario.setdefault(
            f"{self.name}_{self.sim_name}_mapping", dict()
        )
        for bus, entities in self.sim_params[map_key].items():
            mapping.setdefault(bus, list())
            for eidx, (model, scale) in enumerate(entities):
                mod_key = self.gen_mod_key(model, bus, eidx)
                scaling = scale * float(self.sim_params.get("scaling", 1.0))

                params = {"p_mwh_per_a": scaling}
                self.start_model(mod_key, f"DefaultLoad{model}", params)

                info = self.scenario[self.sim_key].get_data_info()[
                    self.scenario[mod_key].eid
                ]
                mapping[bus].append((model, info["p_mwh_per_a"]))

    def connect(self):
        grid_key = f"powergrid_{self.sim_name}"
        attrs = ["p_mw", "q_mvar"]
        for bus, entities in self.sim_params["mapping"].items():
            for eidx, (model, _) in enumerate(entities):
                entity_key = self.gen_mod_key(model, bus, eidx)
                grid_entity_key = self.get_grid_entity(grid_key, "load", bus)
                self.connect_entities2(entity_key, grid_entity_key, attrs)

    def connect_to_db(self):
        """Connect the models to db."""

        map_key = "mapping"
        attrs = ["p_mw", "q_mvar"]
        for bus, entities in self.sim_params[map_key].items():
            for eidx, (model, _) in enumerate(entities):
                mod_key = self.gen_mod_key(model, bus, eidx)
                self.connect_entities2(mod_key, "database", attrs)
