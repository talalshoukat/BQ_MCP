from pydantic import BaseModel, SecretStr
from hydra import compose, initialize
from omegaconf import OmegaConf
from typing import List, Dict
import os
from enum import Enum


class SubAgentsEnum(str, Enum):
    gitlab_agent: str = "gitlab_agent"
    gosi_laws_agent: str = "gosi_laws_agent"
    hr_policies_agent: str = "hr_policies_agent"
    faqs_agent: str = "faqs_agent"
    fraud_agent: str = "fraud_agent"


class LLMConfig(BaseModel):
    base_url: str
    model_name: str
    api_key: SecretStr


class Config(BaseModel):
    verify_ssl: bool
    llm: LLMConfig
    subagents: Dict[SubAgentsEnum, dict]


class ConfigFactory:
    config: Config = None

    @staticmethod
    def parse_yaml_with_hydra(
            config_path: str = "../configs",
            config_name: str = "config",
            overrides: List[str] = [],
    ) -> Config:
        if ConfigFactory.config is not None:
            return ConfigFactory.config

        # global initialization
        initialize(version_base=None, config_path=config_path, job_name="gosi_brain_agent")
        cfg = compose(config_name=config_name, overrides=overrides)

        dct = OmegaConf.to_object(cfg)
        conf = Config(**dct)

        os.environ["LITELLM_PROXY_API_KEY"] = conf.llm.api_key.get_secret_value()
        os.environ["LITELLM_PROXY_API_BASE"] = conf.llm.base_url

        ConfigFactory.config = conf
        return conf
