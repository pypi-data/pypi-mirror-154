import ast
import copy
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple, TypeVar

import jinja2
from func_adl import ObjectStream
from func_adl.ast.meta_data import lookup_query_metadata


@dataclass
class CalibrationEventConfig:
    # Name of the jet collection to calibrate and use by default
    jet_collection: str

    # Name of the truth jets to be used for the jet calibration
    jet_calib_truth_collection: str

    ########### Electrons
    # Name of the electron collection to calibrate and use by default
    electron_collection: str

    # The working point (e.g. xxx)
    electron_working_point: str

    # The isolation (e.g. xxxx)
    electron_isolation: str

    ########### Photons
    # Name of the photon collection to calibrate and use by default.
    photon_collection: str

    # The working point (e.g. xxx)
    photon_working_point: str

    # The isolation (e.g. xxxx)
    photon_isolation: str

    ########### Muons
    # Name of the muon collection to calibration and use by default.
    muon_collection: str

    # The working point (e.g. xxx)
    muon_working_point: str

    # The isolation (e.g. xxxx)
    muon_isolation: str

    ########### Taus
    # Name of the tau collection to calibrate and use by default.
    tau_collection: str

    # The working point (e.g. xxxx)
    tau_working_point: str

    ###### Other Config Options
    perform_overlap_removal: bool


T = TypeVar('T')


class calib_tools:
    '''Helper functions to work with a query's calibration configuration.'''

    _default_calibration: Optional[CalibrationEventConfig] = None

    _default_sys_error: Optional[str] = 'NOSYS'

    @classmethod
    def reset_config(cls):
        '''Reset calibration config to the default.

        * This is configured for working with R21 DAOD_PHYS samples.

        '''
        cls._default_calibration = CalibrationEventConfig(
        jet_collection="AntiKt4EMPFlowJets",
        jet_calib_truth_collection="AntiKt4TruthDressedWZJets",
        electron_collection="Electrons",
        electron_working_point="MediumLHElectron",
        electron_isolation="NonIso",
        photon_collection="Photons",
        photon_working_point="Tight",
        photon_isolation="FixedCutTight",
        muon_collection="Muons",
        muon_working_point="Medium",
        muon_isolation="NonIso",
        tau_collection="TauJets",
        tau_working_point="Tight",
        perform_overlap_removal=True,
    )

    @classmethod
    def _setup(cls):
        if cls._default_calibration is None:
            cls.reset_config()

    @classmethod
    def set_default_config(cls, config: CalibrationEventConfig):
        'Store a copy of a new default config for use in all future queries.'
        cls._default_calibration = copy.copy(config)

    @classmethod
    def default_config(cls) -> CalibrationEventConfig:
        'Return a copy of the current default calibration configuration.'
        cls._setup()
        assert cls._default_calibration is not None
        return copy.copy(cls._default_calibration)

    @classmethod
    def query_update(cls, query: ObjectStream[T], calib_config: Optional[CalibrationEventConfig] = None, **kwargs) -> ObjectStream[T]:
        '''Add metadata to a query to indicate a change in the calibration configuration for the query.

        Args:
            query (ObjectStream[T]): The query to update.

            calib_config (Optional[CalibrationEventConfig]): The new calibration configuration to use. If specified
                will override all calibration configuration options in the query.

            jet_collection, ...: Use any property name from the `CalibrationEventConfig` class to override that particular
                options for this query. You may specify as many of them as you like.

        Returns:
            ObjectStream[T]: The updated query.

        Notes:

            * This function can be chained - resolution works by looking at the most recent `query_update` in the query.
            * This function works by storing a complete `CalibrationEventConfig` object, updated as requested, in the query. So
                even if you just update `jet_collection`, changing the `default_config` after calling this will have no effect.
        '''

        # Get a base calibration config we can modify (e.g. a copy)
        config = calib_config
        if config is None:
            config = calib_tools.query_get(query)

        # Now, modify by any arguments we were given
        for k, v in kwargs.items():
            if hasattr(config, k):
                setattr(config, k, v)
            else:
                raise ValueError(f'Unknown calibration config option: {k} in `query_update`')

        # Place it in the query stream for later use
        return query.QMetaData({
            'calibration': config
        })


    @classmethod
    def query_get(cls, query:ObjectStream[T]) -> CalibrationEventConfig:
        '''Return a copy of the calibration if the query were issued at this point.

        Args:
            query (ObjectStream[T]): The query to inspect.

        Returns:
            CalibrationEventConfig: The calibration configuration for the query.
        '''
        r = lookup_query_metadata(query, 'calibration')
        if r is None:
            return calib_tools.default_config()
        else:
            return copy.copy(r)

    @classmethod
    def default_sys_error(cls) -> str:
        '''Return the default systematic error'''
        if cls._default_sys_error is None:
            return 'NOSYS'
        return cls._default_sys_error

    @classmethod
    def set_default_sys_error(cls, value: str):
        '''Set the default systematic error'''
        cls._default_sys_error = value

    @classmethod
    def reset_sys_error(cls):
        '''Reset to 'NOSYS' the default systematic error'''
        cls._default_sys_error = 'NOSYS'

    @classmethod
    def query_sys_error(cls, query: ObjectStream[T], sys_error: str) -> ObjectStream[T]:
        '''Add metadata to a query to indicate a change in the systematic error for the events.

        Args:
            query (ObjectStream[T]): The query to update.

            sys_error (str): The systematic error to fetch. Only a single one is possible at any time. The sys error names
                are the same as used by the common CP algorithms.

        Returns:
            ObjectStream[T]: The updated query.

        Notes:

            * This function can be chained - resolution works by looking at the most recent `query_sys_error` in the query.
        '''
        return query.QMetaData({
            'calibration_sys_error': sys_error
        })


_g_jinja2_env: Optional[jinja2.Environment] = None


def template_configure() -> jinja2.Environment:
    '''Configure the jinja2 template
    '''
    global _g_jinja2_env
    if _g_jinja2_env is None:
        template_path = Path(__file__).parent / "templates"
        loader = jinja2.FileSystemLoader(str(template_path))
        _g_jinja2_env = jinja2.Environment(loader=loader)
    return _g_jinja2_env


_g_metadata_names_no_overlap = {
    'jet_collection': ["sys_error_tool", "pileup_tool", "corrections_jet", "add_calibration_to_job"],
    'electron_collection': ["sys_error_tool", "pileup_tool", "corrections_electron", "add_calibration_to_job"],
    'muon_collection': ["sys_error_tool", "pileup_tool", "corrections_muon", "add_calibration_to_job"],
    'photon_collection': ["sys_error_tool", "pileup_tool", "corrections_photon", "add_calibration_to_job"],
    'tau_collection': ["sys_error_tool", "pileup_tool", "corrections_tau", "add_calibration_to_job"],
    'met_collection': ["sys_error_tool", "pileup_tool", "corrections_jet", "corrections_muon", "corrections_electron", "corrections_met", "add_calibration_to_job"],
}

_g_metadata_names_overlap = {
    'jet_collection': ["sys_error_tool", "pileup_tool", "corrections_jet", "corrections_muon", "corrections_electron", "corrections_photon", "corrections_tau", "corrections_overlap", "add_calibration_to_job"],
    'electron_collection': ["sys_error_tool", "pileup_tool", "corrections_jet", "corrections_muon", "corrections_electron", "corrections_photon", "corrections_tau", "corrections_overlap", "add_calibration_to_job"],
    'muon_collection': ["sys_error_tool", "pileup_tool", "corrections_jet", "corrections_muon", "corrections_electron", "corrections_photon", "corrections_tau", "corrections_overlap", "add_calibration_to_job"],
    'photon_collection': ["sys_error_tool", "pileup_tool", "corrections_jet", "corrections_muon", "corrections_electron", "corrections_photon", "corrections_tau", "corrections_overlap", "add_calibration_to_job"],
    'tau_collection': ["sys_error_tool", "pileup_tool", "corrections_jet", "corrections_muon", "corrections_electron", "corrections_photon", "corrections_tau", "corrections_overlap", "add_calibration_to_job"],
    'met_collection': ["sys_error_tool", "pileup_tool", "corrections_jet", "corrections_muon", "corrections_electron", "corrections_met", "add_calibration_to_job"],
}

def fixup_collection_call(s: ObjectStream[T], a: ast.Call, collection_attr_name: str) -> Tuple[ObjectStream[T], ast.Call]:
    'Apply all the fixes to the collection call'

    # Find the two arguments
    uncalibrated_bank_name = None
    calibrated_bank_name = None

    if len(a.args) >= 1:
        calibrated_bank_name = ast.literal_eval(a.args[0])

    if len(a.args) >= 2:
        uncalibrated_bank_name = ast.literal_eval(a.args[1])

    for arg in a.keywords:
        if arg.arg == 'calibrated_collection':
            calibrated_bank_name = ast.literal_eval(arg.value)
        if arg.arg == 'uncalibrated_collection':
            uncalibrated_bank_name = ast.literal_eval(arg.value)

    if uncalibrated_bank_name is not None and calibrated_bank_name is not None:
        raise ValueError(f"Illegal to specify both `calibrated_collection` and `uncalibrated_collection` when accessing `collection_attr_name`.")

    new_s = s
    if calibrated_bank_name is not None:
        new_s = calib_tools.query_update(new_s, **{collection_attr_name: calibrated_bank_name})

    # See if there is a systematic error we need to fetch
    sys_error = lookup_query_metadata(new_s, 'calibration_sys_error')
    if sys_error is None:
        sys_error = calib_tools.default_sys_error()

    # Uncalibrated collection is pretty easy - nothing to do here!
    if uncalibrated_bank_name is not None:
        output_collection_name = uncalibrated_bank_name
    else:

        # Get the most up to date configuration for this run.
        calibration_info = calib_tools.query_get(new_s)

        # Next, load up all the meta-data for this collection.
        j_env = template_configure()
        dependent_md_name = None
        output_collection_name = None
        md_to_transmit = _g_metadata_names_overlap[collection_attr_name] if calibration_info.perform_overlap_removal else _g_metadata_names_no_overlap[collection_attr_name]
        for md_name in md_to_transmit:
            md_template = j_env.get_template(f"{md_name}.py")
            text = md_template.render(calib=calibration_info, sys_error=sys_error)
            md_text = {
                "metadata_type": "add_job_script",
                "name": md_name,
                "script": text.splitlines()
            }
            if dependent_md_name is not None:
                md_text["depends_on"] = [dependent_md_name]

            new_s = new_s.MetaData(md_text)

            dependent_md_name = md_name

            # Have we found the output collection name?
            found = re.search(f"# Output {collection_attr_name} = (.+)(\\s|$)", text)
            if found is not None:
                output_collection_name = found.group(1)

    if output_collection_name is None:
        raise RuntimeError(f"Could not find output collection name in templates for collection '{collection_attr_name} - xAOD job options templates are malformed.")

    # Finally, rewrite the call to fetch the collection with the actual collection name we want
    # to fetch.
    new_call = copy.copy(a)
    new_call.args = [ast.parse(f"'{output_collection_name}'").body[0].value]  # type: ignore

    return new_s, new_call
