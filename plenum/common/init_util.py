from plenum.common.has_file_storage import HasFileStorage
from plenum.common.raet import initLocalKeep


def cleanup_environment(name, base_dir):
    dataLocation = HasFileStorage.getDataLocation(name, base_dir)
    HasFileStorage.wipeDataLocation(dataLocation)


def initialize_node_environment(name, base_dir, sigseed=None, override=False):
    # Question: Does this comment belong here? I dont think so.
    """
    transport-agnostic method; in the future when the transport protocol is
    abstracted a bit more, this function and the one below will be the same
    and likely a method of an interface
    """
    _, vk = initLocalKeep(name=name, baseDir=base_dir, sigseed=sigseed,
                          override=override)
    cleanup_environment(name, base_dir)
    return vk