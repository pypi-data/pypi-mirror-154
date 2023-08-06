from typing import Optional, List

from phiterm.conf.phi_conf import PhiWsData
from phiterm.utils.cli_console import (
    print_info,
    print_heading,
    print_info,
)
from phiterm.utils.log import logger
from phiterm.workspace.ws_enums import WorkspaceEnv


def run_command(
    command: str,
    ws_data: PhiWsData,
    target_env: WorkspaceEnv,
    target_app: Optional[str] = None,
) -> None:
    """Run a command in databox."""

    if ws_data is None or ws_data.ws_config is None:
        logger.error("WorkspaceConfig invalid")
        return
    ws_config = ws_data.ws_config
    # Set the local environment variables before processing configs
    ws_config.set_local_env()

    # Final run status
    run_status: bool = False
    if target_env == WorkspaceEnv.dev:
        from phidata.infra.docker.config import DockerConfig
        from phiterm.docker.docker_operator import run_command_docker
        from phidata.utils.prep_infra_config import prep_infra_config

        docker_configs: Optional[List[DockerConfig]] = ws_config.docker
        filtered_docker_config: Optional[DockerConfig] = None
        if docker_configs is not None and isinstance(docker_configs, list):
            if len(docker_configs) == 1:
                filtered_docker_config = docker_configs[0]
            else:
                for dc in docker_configs:
                    if dc.env == target_env.value:
                        filtered_docker_config = dc
                        break
        if filtered_docker_config is None:
            logger.error(f"No DockerConfig found for env: {target_env.value}")
            return

        ######################################################################
        # NOTE: VERY IMPORTANT TO GET RIGHT
        # Update DockerConfig data using WorkspaceConfig
        # 1. Pass down the paths from the WorkspaceConfig
        #       These paths are used everywhere from Infra to Apps
        # 2. Pass down docker_env which is used to set the env variables
        #       when running the docker command
        ######################################################################

        docker_config_to_use: Optional[DockerConfig] = None
        _config = prep_infra_config(
            infra_config=filtered_docker_config,
            ws_config=ws_config,
        )
        if isinstance(_config, DockerConfig):
            docker_config_to_use = _config

        if docker_config_to_use is None:
            logger.error(f"No DockerConfig found for env: {target_env.value}")
            return

        run_status = run_command_docker(
            command=command,
            docker_config=docker_config_to_use,
            target_app=target_app,
        )
    elif target_env == WorkspaceEnv.prd:
        from phidata.infra.k8s.config import K8sConfig
        from phiterm.k8s.k8s_operator import run_command_k8s
        from phidata.utils.prep_infra_config import prep_infra_config

        k8s_configs: Optional[List[K8sConfig]] = ws_config.k8s
        filtered_k8s_config: Optional[K8sConfig] = None
        if k8s_configs is not None and isinstance(k8s_configs, list):
            if len(k8s_configs) == 1:
                filtered_k8s_config = k8s_configs[0]
            else:
                for kc in k8s_configs:
                    if kc.env == target_env.value:
                        filtered_k8s_config = kc
                        break
        if filtered_k8s_config is None:
            logger.error(f"No K8sConfig found for env: {target_env.value}")
            return

        ######################################################################
        # NOTE: VERY IMPORTANT TO GET RIGHT
        # Update K8sConfig data using WorkspaceConfig
        # 1. Pass down the paths from the WorkspaceConfig
        #       These paths are used everywhere from Infra to Apps
        # 2. Pass down k8s_env which is used to set the env variables
        #       when running the k8s command
        ######################################################################

        k8s_config_to_use: Optional[K8sConfig] = None
        _config = prep_infra_config(
            infra_config=filtered_k8s_config,
            ws_config=ws_config,
        )
        if isinstance(_config, K8sConfig):
            k8s_config_to_use = _config

        if k8s_config_to_use is None:
            logger.error(f"No K8sConfig found for env: {target_env.value}")
            return

        command_array = command.split()
        run_status = run_command_k8s(
            command=command_array,
            k8s_config=k8s_config_to_use,
            target_app=target_app,
        )
    else:
        logger.error(f"WorkflowEnv: {target_env} not supported")

    if run_status:
        print_heading("Command run success")
    else:
        logger.error("Command run failure")
