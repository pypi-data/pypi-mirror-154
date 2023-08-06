from collections.abc import MutableMapping
from typing import Optional


class InstallProgressHandler(object):
    def __init__(self, module_name, module_version):
        self.module_name = module_name
        self.module_version = module_version
        self.display_name = None
        self._make_display_name()
        self.cur_stage = None

    def _make_display_name(self):
        ver_str = self.module_version if self.module_version is not None else ""
        self.display_name = ":".join([self.module_name, ver_str])

    def stage_start(self, __stage__):
        pass

    def stage_progress(
        self, __cur_chunk__, __total_chunks__, __cur_size__, __total_size__
    ):
        pass

    def set_module_version(self, module_version):
        self.module_version = module_version
        self._make_display_name()

    def set_module_name(self, module_name):
        self.module_name = module_name
        self._make_display_name()

    def _stage_msg(self, stage):
        from .util import get_current_time_str

        if stage is None or stage == "":
            return ""
        elif stage == "start":
            return (
                f"[{get_current_time_str()}] Starting to install {self.display_name}..."
            )
        elif stage == "download_code":
            return f"[{get_current_time_str()}] Downloading code archive of {self.display_name}..."
        elif stage == "extract_code":
            return f"[{get_current_time_str()}] Extracting code archive of {self.display_name}..."
        elif stage == "verify_code":
            return f"[{get_current_time_str()}] Verifying code integrity of {self.display_name}..."
        elif stage == "download_data":
            return (
                f"[{get_current_time_str()}] Downloading data of {self.display_name}..."
            )
        elif stage == "extract_data":
            return (
                f"[{get_current_time_str()}] Extracting data of {self.display_name}..."
            )
        elif stage == "verify_data":
            return f"[{get_current_time_str()}] Verifying data integrity of {self.display_name}..."
        elif stage == "finish":
            return f"[{get_current_time_str()}] Finished installation of {self.display_name}"
        elif stage == "killed":
            return f"[{get_current_time_str()}] Aborted installation of {self.display_name}"
        elif stage == "Unqueued":
            return f"Unqueued {self.display_name} from installation"
        else:
            raise ValueError(stage)


class LocalInfoCache(MutableMapping):
    """
    LocalInfoCache will initially store the paths to modules. When a module info
    is requested, the module info will be created from the path, stored, and returned.
    LocalInfoCache exposes the same interface as a dictionary.
    """

    def __init__(self, *args, **kwargs):
        self.version = None
        self.store = dict()
        self.update(dict(*args, **kwargs))  # use the free update to set keys

    def __getitem__(self, key):
        if key not in self.store:
            raise KeyError(key)
        if not isinstance(self.store[key], LocalModuleInfo):
            self.store[key] = LocalModuleInfo(self.store[key])
        return self.store[key]

    def __setitem__(self, key, value):
        import os

        if not (isinstance(value, LocalModuleInfo) or os.path.isdir(value)):
            raise ValueError(value)
        self.store[key] = value

    def __delitem__(self, key):
        del self.store[key]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)


class LocalModuleInfo(object):
    def __init__(self, dir_path, __module_type__=None, name=None):
        import os

        self.directory = dir_path
        if name is None:
            self.name = os.path.basename(self.directory)
        else:
            self.name = name
        self.script_path = os.path.join(self.directory, self.name + ".py")
        self.script_exists = os.path.exists(self.script_path)
        self.conf_path = os.path.join(self.directory, self.name + ".yml")
        self.conf_exists = os.path.exists(self.conf_path)
        self.exists = self.conf_exists
        startofinstall_path = os.path.join(self.directory, "startofinstall")
        if os.path.exists(startofinstall_path):
            endofinstall_path = os.path.join(self.directory, "endofinstall")
            if os.path.exists(endofinstall_path):
                self.exists = True
            else:
                self.exists = False
        self.data_dir = os.path.join(dir_path, "data")
        self.data_dir_exists = os.path.isdir(self.data_dir)
        self.has_data = self.data_dir_exists and len(os.listdir(self.data_dir)) > 0
        self.test_dir = os.path.join(dir_path, "test")
        self.test_dir_exists = os.path.isdir(self.test_dir)
        self.tests = self.get_tests()
        self.has_test = len(self.tests) > 0
        self.readme_path = os.path.join(self.directory, self.name + ".md")
        self.readme_exists = os.path.exists(self.readme_path)
        if self.readme_exists:
            with open(self.readme_path, encoding="utf-8") as f:
                self.readme = f.read()
        else:
            self.readme = ""
        self.helphtml_path = os.path.join(self.directory, "help.html")
        self.helphtml_exists = os.path.exists(self.helphtml_path)
        self.conf = {}
        if self.conf_exists:
            self.conf = load_yml_conf(self.conf_path)
        self.type = self.conf.get("type")
        self.version = self.conf.get("version")
        self.description = self.conf.get("description")
        self.hidden = self.conf.get("hidden", False)
        dev_dict = self.conf.get("developer", {})
        if not (type(dev_dict) == dict):
            dev_dict = {}
        self.developer = get_developer_dict(**dev_dict)
        if "type" not in self.conf:
            self.conf["type"] = "unknown"
        self.type = self.conf["type"]
        self.level = self.conf.get("level")
        self.input_format = self.conf.get("input_format")
        self.secondary_module_names = list(self.conf.get("secondary_inputs", {}))
        if self.type == "annotator":
            if self.level == "variant":
                self.output_suffix = self.name + ".var"
            elif self.level == "gene":
                self.output_suffix = self.name + ".gen"
            else:
                self.output_suffix = self.name + "." + self.type
        self.title = self.conf.get("title", self.name)
        self.size = None
        self.tags = self.conf.get("tags", [])
        self.datasource = str(self.conf.get("datasource", ""))
        self.smartfilters = self.conf.get("smartfilters")
        self.groups = self.conf.get("groups", [])

    def is_valid_module(self):
        r = self.exists
        r = r and self.name is not None
        r = r and self.conf_path is not None
        r = r and self.version is not None
        r = r and self.type is not None
        return r

    def get_size(self):
        """
        Gets the total installed size of a module
        """
        from oakvar.util import get_directory_size

        if self.size is None:
            self.size = get_directory_size(self.directory)
        return self.size

    def get_tests(self):
        """
        Gets the module test input file(s) if the module has tests.  A test is a input file / key file pair.
        """
        import os

        tests = []
        if self.test_dir_exists:
            for i in os.listdir(self.test_dir):
                if (
                    "input" in i
                    and os.path.isfile(os.path.join(self.test_dir, i))
                    and os.path.isfile(
                        os.path.join(self.test_dir, i.replace("input", "key"))
                    )
                ):
                    tests.append(i)
        return tests

    def serialize(self):
        return self.__dict__


class ModuleInfoCache(object):
    def __init__(self):
        from oakvar.store_utils import PathBuilder
        from .sysadmin import get_system_conf
        from .sysadmin import get_modules_dir

        self._sys_conf = get_system_conf()
        self._modules_dir = get_modules_dir()
        self.local = LocalInfoCache()
        self._remote_url = None
        self.remote = None
        self._remote_fetched = False
        self.remote_readme = {}
        self.remote_config = {}
        self.update_local()
        self._store_path_builder = PathBuilder(self._sys_conf["store_url"], "url")
        self.download_counts = {}
        self._counts_fetched = False

    def get_local(self):
        return self.local

    def update_download_counts(self, force=False):
        import oyaml as yaml
        from oakvar.store_utils import get_file_to_string

        if force or not (self._counts_fetched):
            counts_url = self._store_path_builder.download_counts()
            counts_str = get_file_to_string(counts_url)
            if counts_str != "" and type(counts_str) != str:
                self.download_counts = yaml.safe_load(counts_str).get("modules", {})
                self._counts_fetched = True
            else:
                self._counts_fetched = False

    def update_local(self):
        import os
        from .constants import install_tempdir_name
        from .sysadmin import get_modules_dir

        self.local = LocalInfoCache()
        self._modules_dir = get_modules_dir()
        if self._modules_dir is None:
            from .exceptions import SystemMissingException

            raise SystemMissingException(msg="Modules directory is not set")
        if not (os.path.exists(self._modules_dir)):
            return None
        for mg in os.listdir(self._modules_dir):
            if mg == install_tempdir_name:
                continue
            mg_path = os.path.join(self._modules_dir, mg)
            basename = os.path.basename(mg_path)
            if (
                not (os.path.isdir(mg_path))
                or basename.startswith(".")
                or basename.startswith("_")
            ):
                continue
            for module_name in os.listdir(mg_path):
                if module_name == "hgvs":  # deprecate hgvs
                    continue
                module_dir = os.path.join(mg_path, module_name)
                if (
                    module_dir.startswith(".") == False
                    and os.path.isdir(module_dir)
                    and not module_name.startswith(".")
                    and not module_name.startswith("_")
                    and os.path.exists(os.path.join(module_dir, module_name + ".yml"))
                ):
                    self.local[module_name] = module_dir

    def load_remote_manifest(self):
        from .sysadmin import get_local_oc_manifest

        oc_manifest = get_local_oc_manifest()
        if not oc_manifest:
            get_mic().update_remote()
            oc_manifest = get_local_oc_manifest()
        self.remote = oc_manifest
        self._remote_fetched = True

    def update_remote(self):
        from .sysadmin import fetch_and_save_oc_manifest
        from .sysadmin import get_local_oc_manifest

        fetch_and_save_oc_manifest()
        oc_manifest = get_local_oc_manifest()
        if oc_manifest:
            self.remote = oc_manifest
            self._remote_fetched = True
        """
        self._remote_fetched = True
        if force or not (self._remote_fetched):
            if self._remote_url is None:
                self._remote_url = self._store_path_builder.manifest()
                manifest_str = get_file_to_string(self._remote_url)
                # Current version may not have a manifest if it's a dev version
                if not manifest_str:
                    self._remote_url = self._store_path_builder.manifest_nover(
                    )
                    manifest_str = get_file_to_string(self._remote_url)
            else:
                manifest_str = get_file_to_string(self._remote_url)
            self.remote = {}
            if manifest_str != "" and type(manifest_str) == str:
                self.remote = safe_load(manifest_str)
                self.remote.pop("hgvs", None)  # deprecate hgvs annotator
            else:
                from sys import stderr
                msg = f"WARNING: Could not list modules from {self._remote_url}. The store or the internet connection can be off-line."
                stderr.write(msg + "\n")
            self._remote_fetched = True
        """

    def get_remote_readme(self, module_name, version=None):
        from oakvar.store_utils import get_file_to_string

        # self.update_remote()
        # Resolve name and version
        if module_name not in self.remote:
            raise LookupError(module_name)
        if (
            version != None
            and self.remote
            and version not in self.remote[module_name]["versions"]
        ):
            raise LookupError(version)
        if version == None:
            if self.remote:
                version = self.remote[module_name]["latest_version"]
        # Try for cache hit
        try:
            readme = self.remote_readme[module_name][version]
            return readme
        except LookupError:
            readme_url = self._store_path_builder.module_readme(module_name, version)
            readme = get_file_to_string(readme_url)
            # add to cache
            if module_name not in self.remote_readme:
                self.remote_readme[module_name] = {}
            self.remote_readme[module_name][version] = readme
        return readme

    def get_remote_config(self, module_name, version=None):
        import oyaml as yaml
        from oakvar.store_utils import get_file_to_string

        # self.update_remote()
        if version == None:
            if self.remote:
                version = self.remote[module_name]["latest_version"]
        # Check cache
        try:
            config = self.remote_config[module_name][version]
            return config
        except LookupError:
            config_url = self._store_path_builder.module_conf(module_name, version)
            config = yaml.safe_load(get_file_to_string(config_url))
            # add to cache
            if module_name not in self.remote_config:
                self.remote_config[module_name] = {}
            self.remote_config[module_name][version] = config
        return config


class ReadyState(object):

    READY = 0
    MISSING_MD = 1
    UPDATE_NEEDED = 2
    NO_BASE_MODULES = 3

    messages = {
        0: "",
        1: "Modules directory not found",
        2: 'Update on system modules needed. Run "oc module install-base"',
        3: "Base modules do not exist.",
    }

    def __init__(self, code=READY):
        if code not in self.messages:
            raise ValueError(code)
        self.code = code

    @property
    def message(self):
        return self.messages[self.code]

    def __bool__(self):
        return self.code == self.READY

    def __iter__(self):
        yield "ready", bool(self)
        yield "code", self.code
        yield "message", self.message


class RemoteModuleInfo(object):
    def __init__(self, __name__, **kwargs):
        from typing import Optional

        self.data = kwargs
        self.data.setdefault("versions", [])
        self.data.setdefault("latest_version", "")
        self.data.setdefault("type", "")
        self.data.setdefault("title", "")
        self.data.setdefault("description", "")
        self.data.setdefault("size", "")
        self.data.setdefault("data_size", 0)
        self.data.setdefault("code_size", 0)
        self.data.setdefault("datasource", "")
        self.data.setdefault("hidden", False)
        self.data.setdefault("developer", {})
        self.data.setdefault("data_versions", {})
        self.data.setdefault("data_sources", {})
        self.data.setdefault("tags", [])
        self.data.setdefault("publish_time", None)
        self.name = self.data.get("name")
        self.versions = self.data.get("versions", [])
        self.latest_version = self.data.get("latest_version", "")
        self.type = self.data.get("type")
        self.title = self.data.get("title")
        self.description = self.data.get("description")
        self.size = self.data.get("size")
        self.data_size = self.data.get("data_size")
        self.code_size = self.data.get("code_size")
        self.datasource = self.data.get("datasource")
        self.data_versions = self.data.get("data_versions", {})
        self.hidden = self.data.get("hidden")
        self.tags = self.data.get("tags")
        self.publish_time = self.data.get("publish_time")
        dev_dict = self.data.get("developer", {})
        self.developer = get_developer_dict(**dev_dict)
        self.data_sources = {
            x: str(y) for x, y in self.data.get("data_sources").items()  # type: ignore
        }
        self.installed: Optional[str] = None
        self.local_version: Optional[str] = None
        self.local_datasource: Optional[str] = None

    def has_version(self, version):
        return version in self.versions


def change_password(username, cur_pw, new_pw):
    from requests import post
    from .sysadmin import get_system_conf

    sys_conf = get_system_conf()
    publish_url = sys_conf["publish_url"]
    change_pw_url = publish_url + "/change-password"
    r = post(change_pw_url, auth=(username, cur_pw), json={"newPassword": new_pw})
    if r.status_code == 500:
        from .exceptions import StoreServerError

        raise StoreServerError()
    elif r.status_code == 401:
        from .exceptions import StoreIncorrectLogin

        raise StoreIncorrectLogin()
    if r.text:
        return r.text


def check_login(username, password):
    from requests import get
    from .sysadmin import get_system_conf

    sys_conf = get_system_conf()
    publish_url = sys_conf["publish_url"]
    login_url = publish_url + "/login"
    r = get(login_url, auth=(username, password))
    if r.status_code == 200:
        return True
    elif r.status_code == 500:
        from .exceptions import StoreServerError

        raise StoreServerError()
    else:
        from .exceptions import StoreIncorrectLogin

        raise StoreIncorrectLogin()


def compare_version(v1, v2):
    from distutils.version import LooseVersion

    sv1 = LooseVersion(v1)
    sv2 = LooseVersion(v2)
    if sv1 == sv2:
        return 0
    elif sv1 > sv2:
        return 1
    else:
        return -1


def create_account(username, password):
    from requests import post
    from .sysadmin import get_system_conf

    sys_conf = get_system_conf()
    publish_url = sys_conf["publish_url"]
    create_account_url = publish_url + "/create-account"
    d = {
        "username": username,
        "password": password,
    }
    r = post(create_account_url, json=d)
    if r.status_code == 500:
        from .exceptions import StoreServerError

        raise StoreServerError()
    if r.text:
        return r.text


def get_annotator_dir(module_name):
    import os
    from .sysadmin import get_modules_dir

    module_dir = os.path.join(get_modules_dir(), "annotators", module_name)
    if os.path.exists(module_dir) == False:
        module_dir = None
    return module_dir


def get_annotator_script_path(module_name):
    import os
    from .sysadmin import get_modules_dir

    module_path = os.path.join(
        get_modules_dir(), "annotators", module_name, module_name + ".py"
    )
    if os.path.exists(module_path) == False:
        module_path = None
    return module_path


def get_main_conf():
    from .sysadmin import get_main_conf_path

    conf_path = get_main_conf_path()
    ret = load_yml_conf(conf_path)
    ret["conf_path"] = conf_path
    return ret


def get_current_package_version():
    from pkg_resources import get_distribution

    version = get_distribution("oakvar").version
    return version


def get_default_assembly():
    conf = get_main_conf()
    default_assembly = conf.get("default_assembly", None)
    return default_assembly


def get_developer_dict(**kwargs):
    kwargs.setdefault("name", "")
    kwargs.setdefault("email", "")
    kwargs.setdefault("organization", "")
    kwargs.setdefault("citation", "")
    kwargs.setdefault("website", "")
    return {
        "name": kwargs["name"],
        "email": kwargs["email"],
        "organization": kwargs["organization"],
        "citation": kwargs["citation"],
        "website": kwargs["website"],
    }


def get_download_counts():
    get_mic().update_download_counts()
    counts = get_mic().download_counts
    return counts


def get_install_deps(module_name, version=None, skip_installed=True):
    from distutils.version import LooseVersion
    from pkg_resources import Requirement

    # get_mic().update_remote()
    # If input module version not provided, set to highest
    if version is None:
        version = get_remote_latest_version(module_name)
    config = get_mic().get_remote_config(module_name, version=version)
    req_list = config.get("requires", [])
    deps = {}
    for req_string in req_list:
        req = Requirement.parse(req_string)
        rem_info = get_remote_module_info(req.unsafe_name)
        # Skip if module does not exist
        if rem_info is None and get_local_module_info(req.unsafe_name) is None:
            continue
        if skip_installed:
            # Skip if a matching version is installed
            local_info = get_local_module_info(req.unsafe_name)
            if local_info and local_info.version and local_info.version in req:
                continue
        # Select the highest matching version
        lvers = []
        if rem_info is not None and rem_info.versions is not None:
            lvers = [LooseVersion(v) for v in rem_info.versions]
        lvers.sort(reverse=True)
        highest_matching = None
        for lv in lvers:
            if lv.vstring in req:
                highest_matching = lv.vstring
                break
        # Dont include if no matching version exists
        if highest_matching is not None:
            deps[req.unsafe_name] = highest_matching
    req_pypi_list = config.get("requires_pypi", [])
    req_pypi_list.extend(config.get("pypi_dependency", []))
    deps_pypi = {}
    for req_pypi in req_pypi_list:
        deps_pypi[req_pypi] = True
    return deps, deps_pypi


def get_last_assembly():
    conf = get_main_conf()
    last_assembly = conf.get("last_assembly")
    return last_assembly


def get_latest_package_version():
    """
    Return latest oakvar version on pypi
    """
    all_vers = get_package_versions()
    if all_vers:
        return all_vers[-1]
    else:
        return None


def get_local_module_info(module_name):
    """
    Returns a LocalModuleInfo object for a module.
    """
    import os

    if module_name in get_mic().get_local():
        module_info = get_mic().get_local()[module_name]
    else:
        if os.path.exists(module_name):
            module_info = LocalModuleInfo(module_name)
        else:
            module_info = None
    return module_info


def get_local_module_infos(types=[], names=[]):
    all_infos = list(get_mic().get_local().values())
    return_infos = []
    for minfo in all_infos:
        if types and minfo.type not in types:
            continue
        elif names and minfo.name not in names:
            continue
        elif minfo.exists == False:
            continue
        else:
            return_infos.append(minfo)
    return return_infos


def get_local_module_infos_by_names(module_names):
    modules = {}
    for module_name in module_names:
        module = get_local_module_info(module_name)
        if module is not None:
            modules[module.name] = module
    return modules


def get_local_module_info_by_name(module_name):
    return get_local_module_info(module_name)


def get_local_reporter_module_infos_by_names(module_names):
    modules = {}
    for module_name in module_names:
        if not module_name.endswith("reporter"):
            module_name += "reporter"
        module = get_local_module_info(module_name)
        if module is not None:
            modules[module.name] = module
    return modules


def get_local_module_infos_of_type(t, update=False):
    modules = {}
    if update:
        get_mic().update_local()
    for module_name in get_mic().get_local():
        if get_mic().get_local()[module_name].type == t:
            modules[module_name] = get_mic().get_local()[module_name]
    return modules


def get_local_module_types():
    types = []
    for module in get_mic().get_local():
        if get_mic().get_local()[module].type not in types:
            types.append(get_mic().get_local()[module].type)
    return types


def get_mapper_script_path(module_name):
    import os
    from .sysadmin import get_modules_dir

    module_path = os.path.join(
        get_modules_dir(), "mappers", module_name, module_name + ".py"
    )
    if os.path.exists(module_path) == False:
        module_path = None
    return module_path


def get_module_dir(module_name, module_type=None) -> Optional[str]:
    from os import listdir
    from os.path import join
    from os.path import exists
    from os.path import isdir
    from .sysadmin import get_modules_dir

    if exists(module_name):
        return module_name
    modules_dir = get_modules_dir()
    if module_type:  # module name and type are given.
        p = join(modules_dir, module_type + "s", module_name)
        if exists(p):
            return p
    else:  # module folder should be searched.
        type_fns = listdir(modules_dir)
        for type_fn in type_fns:
            type_dir = join(modules_dir, type_fn)
            if isdir(type_dir) == False:
                continue
            module_fns = listdir(type_dir)
            for module_fn in module_fns:
                if module_fn == module_name:
                    return join(modules_dir, type_fn, module_fn)
    return None


def get_module_conf(module_name, module_type=None):
    conf_path = get_module_conf_path(module_name, module_type=module_type)
    if conf_path:
        return load_yml_conf(conf_path)
    else:
        return None


def get_module_conf_path(module_name, module_type=None):
    from os.path import join
    from os.path import basename

    module_dir = get_module_dir(module_name, module_type=module_type)
    if not module_dir:
        return None
    # module_name can be a folder path.
    yml_fn = basename(module_name) + ".yml"
    return join(module_dir, yml_fn)


def get_package_versions():
    """
    Return available oakvar versions from pypi, sorted asc
    """
    import json
    from requests import get
    from requests.exceptions import ConnectionError
    from distutils.version import LooseVersion

    try:
        r = get("https://pypi.org/pypi/oakvar/json", timeout=(3, None))
    except ConnectionError:
        from .exceptions import InternetConnectionError

        raise InternetConnectionError()
    if r.status_code == 200:
        d = json.loads(r.text)
        all_vers = list(d["releases"].keys())
        all_vers.sort(key=LooseVersion)
        return all_vers
    else:
        return None


def get_readme(module_name, version=None):
    """
    Get the readme. Use local if available.
    """
    import os

    exists_remote = module_exists_remote(module_name, version=version)
    exists_local = module_exists_local(module_name)
    if exists_remote:
        remote_readme = get_mic().get_remote_readme(module_name)
    else:
        remote_readme = ""
    if exists_local:
        local_info = get_local_module_info(module_name)
        if local_info and os.path.exists(local_info.readme_path):
            local_readme = open(local_info.readme_path).read()
        else:
            local_readme = ""
        if local_info and exists_remote == True:
            remote_version = get_remote_latest_version(module_name)
            local_version = local_info.version
            if compare_version(remote_version, local_version) > 0:
                return remote_readme
            else:
                return local_readme
        else:
            return local_readme
    else:
        local_readme = ""
        if exists_remote == True:
            return remote_readme
        else:
            return local_readme


def get_remote_data_version(module_name, version):
    """
    Get the data version to install for a module.
    Return the input version if module_name or version is not found.
    """
    # get_mic().update_remote()
    mic = get_mic()
    if not mic or not mic.remote:
        return None
    try:
        manifest_entry = mic.remote[module_name]
    except KeyError:
        return version
    try:
        return manifest_entry["data_versions"][version]
    except KeyError:
        return version


def get_remote_latest_version(module_name):
    """
    Returns latest remotely available version of a module.
    """
    # get_mic().update_remote()
    mic = get_mic()
    if mic and mic.remote:
        return mic.remote[module_name]["latest_version"]


def get_remote_oc_manifest():
    mic = get_mic()
    if not mic.remote:
        mic.load_remote_manifest()
    return mic.remote


def get_remote_module_config(module_name):
    conf = get_mic().get_remote_config(module_name)
    return conf


def get_remote_module_info(module_name):
    """
    Returns a RemoteModuleInfo object for a module.
    """
    # get_mic().update_remote()
    if module_exists_remote(module_name, version=None):
        mic = get_mic()
        if mic and mic.remote:
            mdict = mic.remote[module_name]
            module = RemoteModuleInfo(module_name, **mdict)
            module.name = module_name
            return module


def get_remote_module_infos_of_type(t):
    # get_mic().update_remote()
    mic = get_mic()
    if mic and mic.remote:
        modules = {}
        for module_name in mic.remote:
            if mic.remote[module_name]["type"] == t:
                modules[module_name] = mic.remote[module_name]
        return modules
    return None


def get_remote_module_readme(module_name, version=None):
    """
    Get the detailed description file about a module as a string.
    """
    return get_mic().get_remote_readme(module_name, version=version)


async def get_updatable_async(modules=[], strategy="consensus"):
    update_vers, resolution_applied, resolution_failed = get_updatable(
        modules=modules, strategy=strategy
    )
    return [update_vers, resolution_applied, resolution_failed]


def get_updatable(modules=[], strategy="consensus"):
    from distutils.version import LooseVersion
    from pkg_resources import Requirement
    from collections import defaultdict
    from types import SimpleNamespace

    if strategy not in ("consensus", "force", "skip"):
        raise ValueError('Unknown strategy "{}"'.format(strategy))
    if not modules:
        modules = list_local()
    reqs_by_dep = defaultdict(dict)
    all_versions = {}
    for mname in list_local():
        local_info = get_local_module_info(mname)
        remote_info = get_remote_module_info(mname)
        if remote_info:
            all_versions[mname] = sorted(remote_info.versions, key=LooseVersion)
        if local_info is not None:
            req_strings = local_info.conf.get("requires", [])
            reqs = [Requirement.parse(s) for s in req_strings]
            for req in reqs:
                dep = req.unsafe_name
                reqs_by_dep[dep][mname] = req
    update_vers = {}
    resolution_applied = {}
    resolution_failed = {}
    for mname in modules:
        if mname not in list_local():
            continue
        local_info = get_local_module_info(mname)
        remote_info = get_remote_module_info(mname)
        reqs = reqs_by_dep[mname]
        versions = all_versions.get(mname, [])
        if not versions:
            continue
        selected_version = versions[-1]
        if (
            selected_version
            and local_info
            and local_info.version
            and LooseVersion(selected_version) <= LooseVersion(local_info.version)
        ):
            continue
        if reqs:
            resolution_applied[mname] = reqs
            if strategy == "force":
                pass
            elif strategy == "skip":
                selected_version = None
            elif strategy == "consensus":
                passing_versions = []
                for version in versions:
                    version_passes = True
                    for _, requirement in reqs.items():
                        version_passes = version in requirement
                        if not version_passes:
                            break
                    if version_passes:
                        passing_versions.append(version)
                selected_version = passing_versions[-1] if passing_versions else None
        if (
            selected_version
            and remote_info
            and local_info
            and local_info.version
            and LooseVersion(selected_version) > LooseVersion(local_info.version)
        ):
            update_data_version = get_remote_data_version(mname, selected_version)
            installed_data_version = get_remote_data_version(mname, local_info.version)
            if (
                update_data_version is not None
                and update_data_version != installed_data_version
            ):
                update_size = remote_info.size
            else:
                update_size = remote_info.code_size
            update_vers[mname] = SimpleNamespace(
                version=selected_version, size=update_size
            )
        else:
            resolution_failed[mname] = reqs
    return update_vers, resolution_applied, resolution_failed


def get_widgets_for_annotator(annotator_name, skip_installed=False):
    """
    Get webviewer widgets that require an annotator. Optionally skip the
    widgets that are already installed.
    """
    linked_widgets = []
    l = list_remote()
    if not l:
        return None
    for widget_name in l:
        widget_info = get_remote_module_info(widget_name)
        if widget_info is not None and widget_info.type == "webviewerwidget":
            widget_config = get_mic().get_remote_config(widget_name)
            linked_annotator = widget_config.get("required_annotator")
            if linked_annotator == annotator_name:
                if skip_installed and module_exists_local(widget_name):
                    continue
                else:
                    linked_widgets.append(widget_info)
    return linked_widgets


def input_formats():
    import os
    from .sysadmin import get_modules_dir

    formats = set()
    d = os.path.join(get_modules_dir(), "converters")
    if os.path.exists(d):
        fns = os.listdir(d)
        for fn in fns:
            if fn.endswith("-converter"):
                formats.add(fn.split("-")[0])
    return formats


def install_module(
    module_name,
    version=None,
    force_data=False,
    skip_data=False,
    stage_handler=None,
    quiet=True,
    **kwargs,
):
    import zipfile
    import shutil
    import os
    import oyaml as yaml
    from .constants import install_tempdir_name
    from oakvar.store_utils import (
        PathBuilder,
        stream_to_file,
        get_file_to_string,
        verify_against_manifest,
    )
    from requests import HTTPError
    from .exceptions import KillInstallException

    # import signal
    import subprocess
    from .sysadmin import get_system_conf
    from .sysadmin import get_modules_dir
    from .util import quiet_print

    quiet_args = {"quiet": quiet}
    modules_dir = get_modules_dir()
    temp_dir = os.path.join(modules_dir, install_tempdir_name, module_name)
    shutil.rmtree(temp_dir, ignore_errors=True)
    os.makedirs(temp_dir)

    # Ctrl-c in this func must be caught to delete temp_dir
    # def raise_kbi(__a__, __b__):
    #    raise KeyboardInterrupt

    # original_sigint = signal.signal(signal.SIGINT, raise_kbi)
    try:
        if stage_handler is None:
            stage_handler = InstallProgressHandler(module_name, version)
        if version is None:
            version = get_remote_latest_version(module_name)
            stage_handler.set_module_version(version)
        if hasattr(stage_handler, "install_state") == True:
            install_state = stage_handler.install_state  # type: ignore
        else:
            install_state = None
        stage_handler.stage_start("start")
        # Checks and installs pip packages.
        config = get_mic().get_remote_config(module_name, version=version)
        pypi_deps = config.get("requires_pypi", [])
        pypi_deps.extend(config.get("pypi_dependency", []))
        idx = 0
        while idx < len(pypi_deps):
            dep = pypi_deps[idx]
            r = subprocess.run(
                ["pip", "show", dep],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            if r.returncode == 0:
                pypi_deps.remove(dep)
            else:
                idx += 1
        if len(pypi_deps) > 0:
            quiet_print(
                f"Following PyPI dependencies should be met before installing {module_name}.",
                args=quiet_args,
            )
            for dep in pypi_deps:
                quiet_print(f"- {dep}", args=quiet_args)
            quiet_print(f"Installing required PyPI packages...", args=quiet_args)
            idx = 0
            while idx < len(pypi_deps):
                dep = pypi_deps[idx]
                r = subprocess.run(["pip", "install", dep])
                if r.returncode == 0:
                    pypi_deps.remove(dep)
                else:
                    idx += 1
            if len(pypi_deps) > 0:
                quiet_print(
                    f"Following PyPI dependencies could not be installed.",
                    args=quiet_args,
                )
                for dep in pypi_deps:
                    quiet_print(f"- {dep}", args=quiet_args)
        if len(pypi_deps) > 0:
            if version is not None:
                quiet_print(
                    f"Skipping installation of {module_name}=={version} due to unmet requirement for PyPI packages",
                    args=quiet_args,
                )
            else:
                quiet_print(
                    f"Skipping installation of {module_name} due to unmet requirement for PyPI packages",
                    args=quiet_args,
                )
            return False
        sys_conf = get_system_conf()
        store_url = sys_conf["store_url"]
        store_path_builder = PathBuilder(store_url, "url")
        remote_data_version = get_remote_data_version(module_name, version)
        if module_name in list_local():
            local_info = get_local_module_info(module_name)
            if local_info and local_info.has_data:
                local_data_version = get_remote_data_version(
                    module_name, local_info.version
                )
            else:
                local_data_version = None
        else:
            local_data_version = None
        code_url = store_path_builder.module_code(module_name, version)
        zipfile_fname = module_name + ".zip"
        remote_info = get_remote_module_info(module_name)
        if remote_info is not None:
            module_type = remote_info.type
        else:
            # Private module. Fallback to remote config.
            remote_config = get_mic().get_remote_config(module_name, version)
            module_type = remote_config["type"]
        if module_type is None:
            from .exceptions import ModuleLoadingError

            raise ModuleLoadingError(module_name)
        if install_state:
            if (
                install_state["module_name"] == module_name
                and install_state["kill_signal"] == True
            ):
                raise KillInstallException
        zipfile_path = os.path.join(temp_dir, zipfile_fname)
        stage_handler.stage_start("download_code")
        r = stream_to_file(
            code_url,
            zipfile_path,
            stage_handler=stage_handler.stage_progress,
            install_state=install_state,
            **kwargs,
        )
        if r.status_code != 200:
            raise (HTTPError(r))
        if install_state:
            if (
                install_state["module_name"] == module_name
                and install_state["kill_signal"] == True
            ):
                raise KillInstallException
        stage_handler.stage_start("extract_code")
        zf = zipfile.ZipFile(zipfile_path)
        zf.extractall(temp_dir)
        zf.close()
        if install_state:
            if (
                install_state["module_name"] == module_name
                and install_state["kill_signal"] == True
            ):
                raise KillInstallException
        stage_handler.stage_start("verify_code")
        code_manifest_url = store_path_builder.module_code_manifest(
            module_name, version
        )
        code_manifest = yaml.safe_load(get_file_to_string(code_manifest_url))
        verify_against_manifest(temp_dir, code_manifest)
        os.remove(zipfile_path)
        if install_state:
            if (
                install_state["module_name"] == module_name
                and install_state["kill_signal"] == True
            ):
                raise KillInstallException
        data_installed = False
        if (
            not (skip_data)
            and (remote_data_version is not None)
            and (remote_data_version != local_data_version or force_data)
        ):
            data_installed = True
            data_url = store_path_builder.module_data(module_name, remote_data_version)
            data_fname = ".".join([module_name, "data", "zip"])
            data_path = os.path.join(temp_dir, data_fname)
            stage_handler.stage_start("download_data")
            r = stream_to_file(
                data_url,
                data_path,
                stage_handler=stage_handler.stage_progress,
                install_state=install_state,
                **kwargs,
            )
            if install_state:
                if (
                    install_state["module_name"] == module_name
                    and install_state["kill_signal"] == True
                ):
                    raise KillInstallException
            if r.status_code == 200:
                stage_handler.stage_start("extract_data")
                zf = zipfile.ZipFile(data_path)
                zf.extractall(temp_dir)
                zf.close()
                if install_state:
                    if (
                        install_state["module_name"] == module_name
                        and install_state["kill_signal"] == True
                    ):
                        raise KillInstallException
                stage_handler.stage_start("verify_data")
                data_manifest_url = store_path_builder.module_data_manifest(
                    module_name, remote_data_version
                )
                data_manifest = yaml.safe_load(get_file_to_string(data_manifest_url))
                verify_against_manifest(temp_dir, data_manifest)
                os.remove(data_path)
                if install_state:
                    if (
                        install_state["module_name"] == module_name
                        and install_state["kill_signal"] == True
                    ):
                        raise KillInstallException
            elif r.status_code == 404:
                # Probably a private module that does not have data
                pass
            else:
                raise (HTTPError(r))
        if install_state:
            if (
                install_state["module_name"] == module_name
                and install_state["kill_signal"] == True
            ):
                raise KillInstallException
        module_dir = os.path.join(modules_dir, module_type + "s", module_name)
        if os.path.isdir(module_dir):
            # Module being updated
            if data_installed:
                # Overwrite the whole module
                shutil.rmtree(module_dir)
                shutil.move(temp_dir, module_dir)
            else:
                # Remove all code items
                for item in os.listdir(module_dir):
                    item_path = os.path.join(module_dir, item)
                    if item != "data":
                        if os.path.isdir(item_path):
                            shutil.rmtree(item_path)
                        else:
                            os.remove(item_path)
                # Copy in new code items
                for item in os.listdir(temp_dir):
                    old_path = os.path.join(temp_dir, item)
                    new_path = os.path.join(module_dir, item)
                    if item != "data":
                        shutil.move(old_path, new_path)
                shutil.rmtree(temp_dir)
        else:
            # Move the module to the right place
            shutil.move(temp_dir, module_dir)
        wf = open(os.path.join(module_dir, "startofinstall"), "w")
        wf.close()
        wf = open(os.path.join(module_dir, "endofinstall"), "w")
        wf.close()
        get_mic().update_local()
        stage_handler.stage_start("finish")
    # except (Exception, KeyboardInterrupt, SystemExit) as e:
    except Exception as e:
        shutil.rmtree(temp_dir, ignore_errors=True)
        if type(e) == KillInstallException:
            if stage_handler:
                stage_handler.stage_start("killed")
        elif isinstance(e, KeyboardInterrupt):
            # signal.signal(signal.SIGINT, original_sigint)
            raise e
        elif isinstance(e, SystemExit):
            pass
        else:
            # signal.signal(signal.SIGINT, original_sigint)
            raise e
    # finally:
    #    signal.signal(signal.SIGINT, original_sigint)


def install_widgets_for_module(module_name):
    widget_name = "wg" + module_name
    install_module(widget_name)


def list_local():
    """
    Returns a list of locally installed modules.
    """
    from .sysadmin import get_modules_dir

    modules_dir = get_modules_dir()
    if get_mic()._modules_dir != modules_dir:
        get_mic()._modules_dir = modules_dir
        get_mic().update_local()
    return sorted(list(get_mic().get_local().keys()))


def list_remote():
    """
    Returns a list of remotely available modules.
    """
    # get_mic().update_remote()
    oc_manifest = get_remote_oc_manifest()
    if oc_manifest:
        return sorted(list(oc_manifest.keys()))


def load_yml_conf(yml_conf_path):
    """
    Load a .yml file into a dictionary. Return an empty dictionary if file is
    empty.
    """
    from oyaml import safe_load

    with open(yml_conf_path, encoding="utf-8") as f:
        conf = safe_load(f)
    if conf == None:
        conf = {}
    return conf


def fn_new_exampleinput(d):
    import shutil
    import os

    fn = "exampleinput"
    ifn = os.path.join(get_packagedir(), fn)
    ofn = os.path.join(d, fn)
    shutil.copyfile(ifn, ofn)
    return ofn


def module_exists_local(module_name):
    """
    Returns True if a module exists locally. False otherwise.
    """
    import os

    if module_name in get_mic().get_local():
        return True
    else:
        if os.path.exists(module_name):
            if os.path.exists(
                os.path.join(module_name, os.path.basename(module_name) + ".yml")
            ):
                return True
    return False


def module_exists_remote(module_name, version=None, private=False):
    """
    Returns true if a module (optionally versioned) exists in remote
    """
    from oakvar.store_utils import PathBuilder
    from requests import get
    from .sysadmin import get_system_conf

    # get_mic().update_remote()
    mic = get_mic()
    if not mic.remote:
        mic.load_remote_manifest()
    found = False
    if module_name in mic.remote:
        if version is None:
            found = True
        elif mic and mic.remote:
            found = version in mic.remote[module_name]["versions"]
    if private and not found:
        sys_conf = get_system_conf()
        path_builder = PathBuilder(sys_conf["store_url"], "url")
        if version is None:
            check_url = path_builder.module_dir(module_name)
        else:
            check_url = path_builder.module_version_dir(module_name, version)
        if check_url:
            r = get(check_url)
            found = r.status_code != 404 and r.status_code < 500
    return found


def new_annotator(annot_name):
    import shutil
    import os
    from .sysadmin import get_modules_dir

    annot_root = os.path.join(get_modules_dir(), "annotators", annot_name)
    template_root = os.path.join(get_packagedir(), "annotator_template")
    shutil.copytree(template_root, annot_root)
    for dir_path, _, fnames in os.walk(annot_root):
        for old_fname in fnames:
            old_fpath = os.path.join(dir_path, old_fname)
            new_fname = old_fname.replace("annotator_template", annot_name, 1)
            new_fpath = os.path.join(dir_path, new_fname)
            os.rename(old_fpath, new_fpath)
    get_mic().update_local()


def print_stage_handler(cur_stage, total_stages, __cur_size__, __total_size__):
    import sys

    rem_stages = total_stages - cur_stage
    perc = cur_stage / total_stages * 100
    out = "\r[{1}{2}] {0:.0f}% ".format(perc, "*" * cur_stage, " " * rem_stages)
    sys.stdout.write(out)
    if cur_stage == total_stages:
        print()


def publish_module(
    module_name, user, password, overwrite=False, include_data=True, quiet=True
):
    import os
    import json
    from oakvar.store_utils import (
        VersionExists,
        ModuleArchiveBuilder,
        stream_multipart_post,
    )
    from requests import get
    from .sysadmin import get_modules_dir
    from .sysadmin import get_system_conf
    from .util import quiet_print

    quiet_args = {"quiet": quiet}
    sys_conf = get_system_conf()
    publish_url = sys_conf["publish_url"]
    get_mic().update_local()
    local_info = get_local_module_info(module_name)
    if local_info == None:
        from .exceptions import ModuleNotExist

        raise ModuleNotExist(module_name)
    check_url = publish_url + "/%s/%s/check" % (module_name, local_info.version)
    r = get(check_url, auth=(user, password))
    if r.status_code != 200:
        if r.status_code == 401:
            from .exceptions import StoreIncorrectLogin

            raise StoreIncorrectLogin()
        elif r.status_code == 400:
            err = json.loads(r.text)
            if err["code"] == VersionExists.code:
                while True:
                    if overwrite:
                        break
                    resp = input("Version exists. Do you wish to overwrite (y/n)? ")
                    if resp == "y":
                        overwrite = True
                        break
                    if resp == "n":
                        from .exceptions import NormalExit

                        raise NormalExit()
                    else:
                        continue
            else:
                from .exceptions import ModuleVersionError

                raise ModuleVersionError(module_name, local_info.version)
        elif r.status_code == 500:
            from .exceptions import StoreServerError

            raise StoreServerError(500)
        else:
            from .exceptions import StoreServerError

            raise StoreServerError(r.status_code)
    zf_name = "%s.%s.zip" % (module_name, local_info.version)
    zf_path = os.path.join(get_modules_dir(), zf_name)
    quiet_print("Zipping module and generating checksums", args=quiet_args)
    zip_builder = ModuleArchiveBuilder(zf_path, base_path=local_info.directory)
    for item_name in os.listdir(local_info.directory):
        item_path = os.path.join(local_info.directory, item_name)
        if item_name.endswith("ofinstall"):
            continue
        elif item_name == "__pycache__":
            continue
        elif item_path == local_info.data_dir and not (include_data):
            continue
        else:
            zip_builder.add_item(item_path)
    manifest = zip_builder.get_manifest()
    zip_builder.close()
    if local_info.version is None:
        post_url = "/".join([publish_url, module_name])
    else:
        post_url = "/".join([publish_url, module_name, local_info.version])
    if overwrite:
        post_url += "?overwrite=1"
    with open(zf_path, "rb") as zf:
        fields = {
            "manifest": ("manifest.json", json.dumps(manifest), "application/json"),
            "archive": (zf_name, zf, "application/octet-stream"),
        }
        quiet_print("Uploading to store", args=quiet_args)
        r = stream_multipart_post(
            post_url, fields, stage_handler=print_stage_handler, auth=(user, password)
        )
    if r.status_code != 200:
        from .exceptions import StoreServerError

        raise StoreServerError(status_code=r.status_code, text=r.text)
    if r.text:
        quiet_print(r.text, args=quiet_args)
    os.remove(zf_path)


def ready_resolution_console():
    return system_ready()


def recursive_update(d1, d2):
    """
    Recursively merge two dictionaries and return a copy.
    d1 is merged into d2. Keys in d1 that are not present in d2 are preserved
    at all levels. The default Dict.update() only preserved keys at the top
    level.
    """
    import copy

    d3 = copy.deepcopy(d1)  # Copy perhaps not needed. Test.
    for k, v in d2.items():
        if k in d3:
            orig_v = d3[k]
            if isinstance(v, dict):
                if isinstance(orig_v, dict) == False:
                    d3[k] = v
                else:
                    t = recursive_update(d3.get(k, {}), v)
                    d3[k] = t
            else:
                d3[k] = d2[k]
        else:
            d3[k] = v
    return d3


def report_issue():
    import webbrowser

    webbrowser.open("http://github.com/rkimoakbioinformatics/oakvar/issues")


def search_local(*patterns):
    """
    Return local module names which match any of supplied patterns
    """
    from re import fullmatch
    from .sysadmin import get_modules_dir

    mic = get_mic()
    modules_dir = get_modules_dir()
    if mic._modules_dir != modules_dir:
        mic._modules_dir = modules_dir
        mic.update_local()
    matching_names = []
    l = list_local()
    for module_name in l:
        if any([fullmatch(pattern, module_name) for pattern in patterns]):
            matching_names.append(module_name)
    return matching_names


def search_remote(*patterns):
    """
    Return remote module names which match any of supplied patterns
    """
    from re import fullmatch

    matching_names = []
    l = list_remote()
    if not l:
        return None
    for module_name in l:
        if any([fullmatch(pattern, module_name) for pattern in patterns]):
            matching_names.append(module_name)
    return matching_names


def send_reset_email(username, args=None):
    from requests import post
    from .sysadmin import get_system_conf
    from .util import quiet_print

    if args:
        quiet = args.get("quiet", True)
    else:
        quiet = True
    quiet_args = {"quiet": quiet}
    sys_conf = get_system_conf()
    publish_url = sys_conf["publish_url"]
    reset_pw_url = publish_url + "/reset-password"
    r = post(reset_pw_url, params={"username": username})
    if r.status_code == 500:
        from .exceptions import StoreServerError

        raise StoreServerError(status_code=r.status_code)
    if r.text:
        quiet_print(r.text, args=quiet_args)


def send_verify_email(username, args=None):
    from requests import post
    from .sysadmin import get_system_conf
    from .util import quiet_print

    sys_conf = get_system_conf()
    publish_url = sys_conf["publish_url"]
    reset_pw_url = publish_url + "/verify-email"
    r = post(reset_pw_url, params={"username": username})
    if r.status_code == 500:
        from .exceptions import StoreServerError

        raise StoreServerError(status_code=r.status_code)
    if r.text:
        quiet_print(r.text, args=args)


def set_cravat_conf_prop(key, val):
    import oyaml as yaml
    from .sysadmin import get_main_conf_path

    conf = get_main_conf()
    conf[key] = val
    wf = open(get_main_conf_path(), "w")
    yaml.dump(conf, wf, default_flow_style=False)
    wf.close()


def set_jobs_dir(d):
    from .sysadmin import update_system_conf_file

    update_system_conf_file({"jobs_dir": d})


# return a list of module types (e.g. annotators) in the local install
def show_main_conf(args):
    import oyaml as yaml
    from .util import quiet_print

    conf = get_main_conf()
    if args["fmt"] == "yaml":
        conf = yaml.dump(conf, default_flow_style=False)
    if args["to"] == "stdout":
        quiet_print(conf, args=args)
    else:
        return conf


def oakvar_version():
    version = get_current_package_version()
    return version


def system_ready():
    import os
    from .sysadmin import get_modules_dir
    from .exceptions import NoModulesDir
    from .exceptions import NoSystemModule

    modules_dir = get_modules_dir()
    if not (os.path.exists(modules_dir)):
        raise NoModulesDir()
    elif not (os.path.exists(os.path.join(modules_dir, "converters", "vcf-converter"))):
        raise NoSystemModule()
    else:
        return ReadyState()


def uninstall_module(module_name):
    """
    Uninstalls a module.
    """
    import shutil

    uninstalled_modules = False
    if module_name in list_local():
        local_info = get_local_module_info(module_name)
        if local_info:
            shutil.rmtree(local_info.directory)
            uninstalled_modules = True
    if uninstalled_modules:
        get_mic().update_local()


def write_cravat_conf(cravat_conf):
    import oyaml as yaml
    from .sysadmin import get_main_conf_path

    confpath = get_main_conf_path()
    wf = open(confpath, "w")
    yaml.dump(cravat_conf, wf, default_flow_style=False)
    wf.close()


def update_mic():
    global mic
    global custom_system_conf
    mic = ModuleInfoCache()


def get_liftover_chain_paths():
    from os.path import join

    liftover_chains_dir = get_liftover_chains_dir()
    liftover_chain_paths = {
        "hg19": join(liftover_chains_dir, "hg19ToHg38.over.chain"),
        "hg18": join(liftover_chains_dir, "hg18ToHg38.over.chain"),
    }
    return liftover_chain_paths


def get_packagedir():
    from os.path import dirname, abspath

    return dirname(abspath(__file__))


def get_platform():
    from platform import platform

    pl = platform()
    if pl.startswith("Windows"):
        pl = "windows"
    elif pl.startswith("Darwin") or pl.startswith("macOS"):
        pl = "macos"
    elif pl.startswith("Linux"):
        pl = "linux"
    else:
        pl = "linux"
    return pl


def get_admindb_path():
    from os.path import join as pathjoin
    from .sysadmin import get_conf_dir

    return pathjoin(get_conf_dir(), "admin.sqlite")


def get_liftover_chains_dir():
    from os.path import join as pathjoin

    return pathjoin(get_packagedir(), "liftover")


def get_mic():
    global mic
    if mic is None:
        mic = ModuleInfoCache()
    return mic


def get_max_version_supported_for_migration():
    from distutils.version import LooseVersion

    return LooseVersion("1.7.0")


mic = None
custom_sys_conf = {}
