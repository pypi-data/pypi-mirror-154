import requests
import urllib.parse
from os import getenv
from actelink.logger import log
from actelink.models import Context

_stores     = dict()
_session    = None

def init(url: str = None, key: str = None):
    """Initialise le module actelink.variables

    :param str url: L'url de connexion au moteur de varibales.
    :param str key: La clé d'API avec laquelle s'authentifier auprès du moteur de variables.

    :raises ConnectionError: en cas d'échec de connexion au moteur de variables.
    """
    # use variable engine url & api-key from environment variables by default
    var_url = getenv("VARIABLE_ENGINE_URL", url)
    var_key = getenv("VARIABLE_ENGINE_API_KEY", key)
    log.info(f"call variables engine with url: {var_url}, key: {var_key}")
    global __CUSTOMER_KEY, __VARIABLES_ENDPOINT, __STORES_ENDPOINT, _stores, _session
    __CUSTOMER_KEY       = var_key
    __VARIABLES_ENDPOINT = urllib.parse.urljoin(var_url, "/api/v1/stores/{storeId}/variables/{label}")
    __STORES_ENDPOINT    = urllib.parse.urljoin(var_url, "/api/v1/stores")
    _session = requests.Session()
    _session.headers.update({"api-key": __CUSTOMER_KEY})
    # retrieve the list of stores for this customer
    try:
        response = _session.get(__STORES_ENDPOINT)
    except requests.exceptions.ConnectionError as error:
        log.error(f"CONNECTION FAILED!\n\n{error})")
        raise
    # check response is valid
    if response.status_code != 200:
        raise requests.exceptions.ConnectionError(f"Request failed, reason: {response.reason}")
    elif response.json() is None:
        log.warn("Warning: no stores found")
    else:
        for s in response.json():
            context = Context.from_string(s["name"])
            if context is not None:
                _stores[context] = {"id": s["id"], "name": s["name"]}
                log.debug(f"found store {s['name']} (id {s['id']})")
            else:
                log.error(f"invalid store name {s['name']} (id {s['id']})")

def get_stores() -> tuple:
    """Retourne les stores existants sous forme d'un tuple.
    
    :returns: Un tuple contenant l'ensemble des stores associés à votre clé d'API.
    :rtype: tuple
    """
    return tuple((store['name']) for store in _stores.values())

def __context_to_store(context: Context) -> dict:
    try:
        store = _stores[context]
    except KeyError:
        log.error(f"no store found for {context}")
        raise
    return store

def get_variable(context: Context, var_label: str, var_keys=None) -> float:
    """Retourne la valeur d'une variable dans un contexte donné.

    :param Context context: Le contexte dans lequel on demande cette variable.
    :param str var_label: Le nom de la variable à retourner.
    :param str var_keys: La ou les clés à spécifier pour cette variable (None par défaut).
    :type var_keys: str or list or None

    :returns: La valeur de la variable *var_label* pour la/les clé(s) donnée(s) si spécifiée(s).
    :rtype: float
    :raises NameError: si le contexte donné n'existe pas.
    :raises ConnectionError: si la variable/clé n'existe pas.

    Exemples d'utilisation :

    * Cas d'une variable d0

    >>> import actelink.variables as av
    >>> from actelink.models import Context, Calcul

    >>> context = Context(...)
    >>> intercept = av.get_variable(context, 'intercept')
    >>> print(intercept)
    0.893

    * Cas d'une variable d1
    
    >>> niveau = av.get_variable(context, 'niveau', 'medium')
    >>> print(niveau)
    0.24

    * Cas d'une variable d2
    
    >>> situation = av.get_variable(context, 'situation', 'homme,celibataire')
    >>> print(situation)
    0.893

    .. NOTE:: Dans le cas d'une variable de type d2, où deux clés doivent être spécifiées, celles ci peuvent être passées en paramètre sous la forme d'une string ou d'une liste :
    
    >>> situation = av.get_variable(context, 'situation', 'homme,celibataire')

    est équivalent à :

    >>> situation = av.get_variable(context, 'situation', ['homme', 'celibataire'])
    """
    store = __context_to_store(context)
    log.info(f"get_variable {var_label} on store {store['id']}, requested key: {var_keys}")
    url = __VARIABLES_ENDPOINT.replace("{storeId}", store['id']).replace("{label}", var_label)
    # var_keys can be passed as a string or array of strings
    var_keys = ",".join(k.strip() for k in var_keys) if isinstance(var_keys, list) else var_keys
    try:
        response = _session.get(url, params={"key": var_keys})
    except requests.exceptions.ConnectionError as error:
        log.error(f"GET {url} FAILED\n\n{error})")
        raise
    if response.status_code != 200:
        log.error(f"GET {url} failed, reason: {response.reason}")
        raise requests.exceptions.ConnectionError(f"GET {url} failed, reason: {response.reason}")
    #log.debug(f"GET {url} Compute-Time: {response.headers["Compute-Time"]}")
    return float(response.json())

def get_variables(context: Context) -> list:
    """Retourne la liste de toutes les variables d'un contexte (store) donné.

    :param Context context: Le contexte pour lequel on veut récupérer la liste de variables.

    :returns: La liste des variables du contexte donné.
    :rtype: list

    Exemples d'utilisation :

    >>> context = Context(...)
    >>> all_vars = av.get_variables(context)
    """
    store = __context_to_store(context)
    try:
        response = _session.get(__STORES_ENDPOINT)
    except requests.exceptions.ConnectionError as error:
        log.error(f"GET {__STORES_ENDPOINT} failed\n\n{error})")
        raise
    # check response is valid
    if response.status_code != 200:
        raise requests.exceptions.ConnectionError(f"GET {__STORES_ENDPOINT} failed, reason: {response.reason}")
    store = next(s for s in response.json() if s["id"] == store["id"])
    return store["variables"]
