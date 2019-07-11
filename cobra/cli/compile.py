from cobra import *


def _compile(more=False):
    configuration = Configuration()
    read_yaml = file_reader("./cobra.yaml")
    load_yaml = yaml_loader(read_yaml, more=more)
    if 'compile' in load_yaml:
        compile_yaml = load_yaml['compile']
        configurations_yaml = configuration\
            .compile(compile_yaml)
        for configuration_yaml in configurations_yaml:
            import_remappings = configuration_yaml['import_remappings']
            file_path_sol = join(configuration_yaml['solidity_path'], configuration_yaml['solidity'])
            if configuration_yaml['allow_paths'] is None:
                cobra_compiled = to_compile(file_path_sol, None,
                                            import_remappings, more=more)

                if not isdir(configuration_yaml['artifact_path']):
                    makedirs(configuration_yaml['artifact_path'])
                solidity_name = str(configuration_yaml['solidity'])
                artifact_path_json = join(configuration_yaml['artifact_path'],
                                          solidity_name[:-4] + ".json")

                if is_compiled(artifact_path_json, cobra_compiled):
                    console_log("%s already compiled in %s" %
                                (solidity_name, artifact_path_json), "warning", "Compile")
                    continue
                file_writer(artifact_path_json, str(cobra_compiled))
                console_log("%s done in %s" %
                            (solidity_name, artifact_path_json), "success", "Compile")
            else:
                cobra_compiled = to_compile(file_path_sol,
                                            configuration_yaml['allow_paths'], import_remappings, more)
                if not isdir(configuration_yaml['artifact_path']):
                    makedirs(configuration_yaml['artifact_path'])
                solidity_name = str(configuration_yaml['solidity'])
                artifact_path_json = join(configuration_yaml['artifact_path'],
                                          solidity_name[:-4] + ".json")

                if is_compiled(artifact_path_json, cobra_compiled):
                    console_log("%s already compiled in %s" %
                                (solidity_name, artifact_path_json), "warning", "Compile")
                    continue
                file_writer(artifact_path_json, str(cobra_compiled))
                console_log("%s done in %s" %
                            (solidity_name, artifact_path_json), "success", "Compile")
    else:
        console_log("compile in cobra.yaml", "error", "NotFound")
        sys.exit()
