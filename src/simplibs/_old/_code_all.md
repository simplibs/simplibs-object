>>> src/simplibs/object/_metadata/constants/BASE_CLASS_NAMES.py
BASE_CLASS_NAMES = ("SimpleBase", "SimpleConstant", "SimpleObject")

>>> src/simplibs/object/_metadata/constants/INDENT.py
INDENT = "    "

>>> src/simplibs/object/_metadata/init_processors/attributes/default/process_default_for_constant.py
def process_default_for_constant(
    default_type: type,
    owner_class: SimpleClassType,
):

    # 1. Natažení defaultu
    row_default = getattr(owner_class, "_default", UNSET)

    # 2. Kontrola validity
    if (row_default is UNSET or
        not isinstance(row_default, default_type)):
        validate_default_is_defined(row_default, owner_class)
        validate_default_matches_annotation(row_default, default_type, owner_class)

    # 3. Navrácení defaultu
    return row_default

>>> src/simplibs/object/_metadata/init_processors/attributes/inners/process_inners.py
def process_inners(
    used_names: set,
    name_snake: str,
    owner_class: SimpleClassType,
) -> tuple:

    # 1. Získání atributu
    raw_inners = getattr(owner_class, "_inners", UNSET)

    # 2. Ověření zda je nově dafinován
    need_validations = "_inners" in owner_class.__dict__ and raw_inners is not UNSET

    # 3. Základní validace
    if need_validations:

        # 3.1 Validace formátu
        if (not raw_inners or
            not isinstance(raw_inners, tuple)):
            validate_inners_is_defined(raw_inners, owner_class)
            validate_inners_is_tuple(raw_inners, owner_class)
            validate_inners_is_not_empty(raw_inners, owner_class)

    # 4. Prepare data containers
    new_used_names = used_names.copy()

    # 5. Main iteration through inners
    for inner in raw_inners:
        inner: SimpleClassType  # Přetypování pro PyCharm

        # 5.1 Base validations: type, subclass, and not base class
        if need_validations:
            from .....SimpleConstant import SimpleConstant
            from .....SimpleObject import SimpleObject
            if (not isinstance(inner, type) or
                not issubclass(inner, SimpleConstant) or
                inner is SimpleConstant or
                inner is SimpleObject):
                validate_inner_is_class(inner, raw_inners, owner_class)
                validate_inner_is_simple_subclass(inner, owner_class)
                validate_inner_is_not_simple_class(inner, owner_class)

        # 5.2 Check for name collisions with parent and siblings
        used_name_collisions = new_used_names & inner.meta.used_names
        if used_name_collisions:
            collision_name = next(iter(used_name_collisions))
            validate_if_collision_with_owner_class(collision_name, name_snake, inner, owner_class)
            if need_validations:
                validate_collision_within_inners(collision_name, name_snake, raw_inners, inner, owner_class)

        # 5.3 Register inner's names into the global namespace
        new_used_names.update(inner.meta.used_names)

    # 6. Return computed values
    return (
        raw_inners,
        new_used_names,
    )


>>> src/simplibs/object/_metadata/init_processors/attributes/type/process_type.py
def process_type(
    owner_class: SimpleClassType,
) -> tuple[type | UnionType, str]:

    # 1. Získání atributu
    raw_type = getattr(owner_class, "_type", UNSET)

    # 2. Základní validace
    if not raw_type:
        validate_type_is_defined(raw_type, owner_class)
        validate_type_is_not_none(raw_type, owner_class)
        validate_type_is_not_empty(raw_type, owner_class)

    # 3. Zpracování atomického typu
    if isinstance(raw_type, type):
        return  raw_type, raw_type.__name__

    # 4. Zpracování UnionType
    if isinstance(raw_type, UnionType):

        # 4.1 Kontrola zda neobsahuje None
        if NoneType in raw_type.__args__:
            raise_union_type_contain_none(owner_class)

        # 4.2 Navrácení UnionType
        return raw_type, str(raw_type)

    # 5. Zpracování tuple (transformace na UnionType)
    if isinstance(raw_type, tuple):

        # 5.1 Kontrola vnitřních prvků
        valid_types = []
        for inner_type in raw_type:

            # 5.1.1 Kontrola typu
            if isinstance(inner_type, tuple) or inner_type is None:
                validate_type_tuple_is_not_nested(inner_type, raw_type, owner_class)
                validate_type_from_tuple_is_not_none(inner_type, raw_type, owner_class)

            # 5.1.2 Přidání typu
            valid_types.append(inner_type)

        # 5.2 Navrácení UnionType (int | str | float)
        final_type = reduce(or_, valid_types)
        return final_type, str(final_type)

    # 6. Vyvolání výjimky pro neplatně zadaný typ
    raise_validate_type_is_not_valid(raw_type, owner_class)

>>> src/simplibs/object/_metadata/init_processors/methods/verifiers/annotations_and_defaults/verify_annotations_and_defaults.py
def verify_annotations_and_defaults(
    bound_method: ClassMethodProtocol,
    expected_params: tuple[str, ...],
    expected_args_params_count: int,
    bound_method_annotations: dict[str, Any],
    expected_args_defaults: tuple | None,
    expected_kwargs_defaults: dict[str, Any],
):

    # 1. Příprava dat pro výjimku
    base_info_for_exception = exception_info_for_classmethod(
        bound_method=bound_method,
        expected_params=expected_params,
        expected_args_params_count=expected_args_params_count
    )

    # 2. Validace anotací (jsu-li zadané)
    if bound_method.__func__.__annotations__:
        validate_annotations(bound_method_annotations, bound_method, base_info_for_exception)

    # 3. Validace defaultních args hodnot
    if bound_method.__func__.__defaults__:
        validate_args_defaults(expected_args_defaults, expected_params, bound_method, base_info_for_exception)

    # 4. Validace defaultních kwargs hodnot
    if bound_method.__func__.__kwdefaults__:
        validate_kwargs_defaults(expected_kwargs_defaults, bound_method, base_info_for_exception)

>>> src/simplibs/object/_metadata/init_processors/methods/verifiers/calculation/decompose_method/verify_decompose_outcome.py
def verify_decompose_outcome(
    calculate_default: tuple[Any, ...],
    owner_class: SimpleClassType,
    bound_method: ClassMethodProtocol,
):

    # 1. Získání inners
    # noinspection PyProtectedMember
    inners = owner_class._inners

    # 2. Kontrola délky (počet inners musí odpovídat počtu vrácených hodnot)
    if len(calculate_default) != len(inners):
        raise_decompose_unvalide_outcome_length(calculate_default, inners, bound_method)

    # 3. Kontrola typů jednotlivých prvků
    for i, inner in enumerate(inners):
        inner: SimpleClassType  # Přetypování pro PyCharm

        # 3.1 Získání hodnot
        value = calculate_default[i]
        expected_type = inner.meta.value_type

        # 3.2 Kontrola typu a vypočítané hodnoty
        if not isinstance(value, expected_type) and value != inner.meta.default:
            validate_decompose_unvalide_item_type(value, expected_type, inner, inners, bound_method)
            validate_decompose_unvalide_item_value(value, inner, inners, bound_method)

>>> src/simplibs/object/_metadata/init_processors/methods/verifiers/calculation/verify_calculation.py
def verify_calculation(
    bound_method: ClassMethodProtocol,
    test_value: Any,
    expected_return_type: type,
    owner_class: SimpleClassType,
):
    # 1. Definice výstupní proměné
    calculate_result = None

    # 2. Zkušební výpočet
    try:
        calculate_result = bound_method(*test_value)
    except Exception as e:
        raise_method_raised_exceptions(e, bound_method)

    # 3. Kontrola zda vypočítaná hodnota odpovídá očekávanému typu
    if not isinstance(calculate_result, expected_return_type):
        raise_method_return_unvalide_outcome_type(calculate_result, expected_return_type, bound_method)

    # 4. Kontrola vnitřních položek pro _decompose
    if bound_method.__func__.__name__ == "_decompose":
        verify_decompose_outcome(calculate_result, owner_class, bound_method)

    # 5. Navrácen vypočítené hodnoty
    return calculate_result

>>> src/simplibs/object/_metadata/init_processors/methods/verifiers/classmethod/verify_classmethod.py
def verify_classmethod(
    method_name: str,
    owner_class: SimpleClassType,
    expected_params: tuple[str, ...],
    expected_args_params_count: int,
) -> tuple[bool, ClassMethodProtocol]:  # tuple[bool(má se validovat), návratový objekt]

    # 1. Příprava dat
    row_method = owner_class.__dict__.get(method_name, None)
    bound_method = getattr(owner_class, method_name)

    # 2. Kontrola zda je definovaná jako classmethod
    if isinstance(bound_method, classmethod):
        bound_method: ClassMethodProtocol  # Přetypování pro PyCharm

        # 2.1 Vyřízení pro nově definované metody
        if row_method:
            return True, bound_method

        # 2.2 Vyřízení pro _validate (pokud se dědí nikdy se nevaliduje)
        if method_name == "_validate":
            return False, bound_method

        # 2.3 Kontrola zda se jedná o přímého potomka SimpleObject třídy
        from ......SimpleObject import SimpleObject
        is_direct_descendant = SimpleObject in owner_class.__bases__

        # 2.4 Vyřízení pro _logic a _decompose (když se nejedná o přímého potomka)
        if not is_direct_descendant:
            need_validations = bool(owner_class.__dict__.keys() & {"_inners", "_type", "_logic"})
            output_bound_method = clone_classmethod(bound_method) if need_validations else bound_method
            return need_validations, output_bound_method

        # 2.5 Vyřízení _decompose, pokud není definovaná (_logic propadává na výjimku)
        if method_name == "_decompose":
                return False, UNSET

    # 3. Vytvoření infa pro výjimky
    base_info_for_exception = exception_info_for_classmethod(
        bound_method=bound_method,
        expected_params=expected_params,
        expected_args_params_count=expected_args_params_count
    )

    # 4. Provedení validací
    validate_method_is_defined(method_name, owner_class, base_info_for_exception)
    validate_method_is_callable(row_method, base_info_for_exception)
    validate_method_is_classmethod(row_method, base_info_for_exception)
    return False, UNSET  # Nikdy by neměl nastat

>>> src/simplibs/object/_metadata/init_processors/methods/verifiers/params/verify_params.py
def verify_params(
    expected_params: tuple[str, ...],
    expected_args_params_count: int,
    bound_method: ClassMethodProtocol,
) -> None:

    # 1. Příprava dat
    # noinspection PyUnresolvedReferences
    code = bound_method.__func__.__code__
    total_params_count = code.co_argcount + code.co_kwonlyargcount
    method_params = code.co_varnames[:total_params_count]
    has_varargs = bool(code.co_flags & 0x04)
    has_varkwargs = bool(code.co_flags & 0x08)

    # 2. Podmínka pro Happy Path
    if (not has_varargs and
        not has_varkwargs and
        code.co_argcount == expected_args_params_count and
        method_params == expected_params):
        return

    # 3. Příprava dat pro výjimku
    base_info_for_exception = exception_info_for_classmethod(
        bound_method=bound_method,
        expected_params=expected_params,
        expected_args_params_count=expected_args_params_count
    )

    # 4. Vyvolání výjimky
    validate_method_param_match_expected(method_params, expected_params, base_info_for_exception)
    validate_method_has_exact_args_count(expected_args_params_count, code.co_argcount, base_info_for_exception)
    validate_method_not_use_param_placeholders(has_varargs, has_varkwargs, base_info_for_exception)

>>> src/simplibs/object/_metadata/init_processors/methods/process_classmethod.py
def process_classmethod(
    method_name: str,
    expected_params: tuple[str, ...],
    expected_args_params_count: int,
    expected_args_defaults: tuple | None,
    expected_kwargs_defaults: dict[str, Any],
    expected_param_types: dict[str, type],
    expected_return_type: type | UnionType,
    owner_class: SimpleClassType,
    test_value:tuple = (),
    return_calculated_value: bool = False,
) -> ClassMethodProtocol | tuple[ClassMethodProtocol, Any]:

    # 1. Základní ověření uživatelem definované metody
    need_validations, bound_method = verify_classmethod(
        method_name=method_name,
        owner_class=owner_class,
        expected_params=expected_params,
        expected_args_params_count=expected_args_params_count,
    )

    # 2. Pokud je metoda nově definovaná
    if need_validations:

        # 2.1 Validace parametrů metody
        verify_params(
            expected_params=expected_params,
            expected_args_params_count=expected_args_params_count,
            bound_method=bound_method,
        )

        # 2.2 Příprava anotací anotací
        bound_method_annotations = {
            **expected_param_types,
            "return": expected_return_type
        }

        # 2.3 Validace defaultních hodnot a anotací (jsu-li zadané)
        if (bound_method.__func__.__annotations__ or
            bound_method.__func__.__defaults__ or
            bound_method.__func__.__kwdefaults__):
            verify_annotations_and_defaults(
                bound_method=bound_method,
                expected_params=expected_params,
                expected_args_params_count=expected_args_params_count,
                bound_method_annotations=bound_method_annotations,
                expected_args_defaults=expected_args_defaults,
                expected_kwargs_defaults=expected_kwargs_defaults
            )

        # 2.4 Zapsání zpracovaných dat
        bound_method.__func__.__defaults__ = expected_args_defaults
        bound_method.__func__.__kwdefaults__ = expected_kwargs_defaults
        bound_method.__func__.__annotations__ = bound_method_annotations

    # 3. Ověření logiky - Zkušební výpočet pro ověření logiky
    calculated_value = verify_calculation(
        bound_method=bound_method,
        test_value=test_value,
        expected_return_type=expected_return_type,
        owner_class=owner_class
    )

    # 4. Navrácení vypočtených hodnot
    if return_calculated_value:
        return bound_method, calculated_value,
    return bound_method

>>> src/simplibs/object/_metadata/init_processors/names/class_name_splitter.py
def class_name_splitter(class_name: str) -> tuple[str, ...]:

    # 1. Validace jména třídy
    # Provádíme pouze nezbytné kontroly, které Python parser u __name__ negarantuje.
    if not class_name.isidentifier() or not class_name.isascii() or "_" in class_name:
        validate_class_name_is_identifier(class_name)
        validate_class_name_is_ascii(class_name)
        validate_class_name_has_no_underscores(class_name)

    # 2. Inicializace úložiště pro slova a akumulátoru znaků
    words = []
    char_stack = []

    # 3. Pomocná funkce pro vyprázdnění zásobníku a uložení slova
    def flush_stack() -> None:
        """
        Vytáhne aktuální slovo z char_stack, normalizuje ho a přidá do seznamu.
        Zásobník následně vyčistí.
        """
        if char_stack:
            word = "".join(char_stack)
            # Akronymy (všechna velká) zůstávají, ostatní se převedou na malá.
            normalized_word = word if word.isupper() else word.lower()
            words.append(normalized_word)
            char_stack.clear()

    # 4. Iterace přes jednotlivé znaky názvu třídy
    for char in class_name:

        # 4.1 Číslice: Začínají vždy nové slovo (User123 -> user, 123)
        if char.isdigit():

            # 4.1.1 Přechod z písmene na číslici → ukončit aktuální slovo
            if char_stack and not char_stack[-1].isdigit():
                flush_stack()

            # 4.1.2 Přidání číslice do zásobníku
            char_stack.append(char)

        # 4.2 Velká písmena: Potenciální start slova nebo akronymu (PascalCase)
        elif char.isupper():

            # 4.2.1 Přechod z malého písmena nebo číslice na velké → ukončit slovo
            if char_stack and (char_stack[-1].islower() or char_stack[-1].isdigit()):
                flush_stack()

            # 4.2.2 Přidání velkého písmene do zásobníku
            char_stack.append(char)

        # 4.3 Malá písmena: Pokračování slova nebo detekce konce akronymu
        else:
            # 4.3.1 Detekce akronymu: Pokud je v zásobníku více znaků a poslední je velký,
            # pak toto velké písmeno patří k novému slovu (např. 'HTTPServer' -> 'HTTP', 'Server')
            if len(char_stack) > 1 and char_stack[-1].isupper():
                last_uppercase = char_stack.pop()   # Vyjmout start nové slova
                flush_stack()                       # Uzavřít akronym
                char_stack.append(last_uppercase)   # Začít nové slovo

            # 4.3.2 Přidání malého písmene do zásobníku
            char_stack.append(char)

    # 5. Zpracování posledního slova zbývajícího v akumulátoru
    flush_stack()

    # 6. Vrácení n-tice sémantických slov
    return tuple(words)

>>> src/simplibs/object/_metadata/init_processors/names/create_names.py
def create_names(owner_class: SimpleClassType) -> tuple[str, ...]:

    class_name = owner_class.__name__

    # 1. Dekompozice názvu na jednotlivá slova (provádí i validaci názvu třídy)
    # Pipeline začíná rozkladem na sémantické jednotky (tuple slov).
    name_tuple = class_name_splitter(class_name)

    # 2. Vytvoření čitelné podoby (spojení mezerou)
    # Určeno pro popisy, logování a hlášení výjimek.
    name_readable = " ".join(name_tuple)

    # 3. Vytvoření podoby pro titulky/začátky vět
    # Zachovává akronymy (HTTP -> HTTP server, nikoliv Http server).
    name_title = name_readable[0].upper() + name_readable[1:]

    # 4. Vytvoření snake_case verze pro parametry (např. v __init__)
    # Standardní Python konvence pro proměnné a argumenty.
    name_snake = "_".join(name_tuple).lower()

    # 5. Vytvoření privátní verze pro vnitřní sloty a atributy
    # Technické jméno pro vnitřní integritu objektu.
    name_private = "_" + name_snake

    # 6. Navrácení tuple s vytvořenými názvy
    return (
        name_readable,
        name_title,
        name_snake,
        name_private
    )

>>> src/simplibs/object/_metadata/init_processors/others/calculate_blueprint_path.py
def calculate_blueprint_path(
    cls: SimpleClassType
) -> str:

    # 1. Vnitřní impor na základní třídu
    from ...SimpleBase import SimpleBase

    # 2. Kontrola předků
    # Vezmeme všechny předky z MRO, kteří jsou potomky SimpleBase,
    # ale nejsou to ty samé systémové kořeny (SimpleObject, SimpleConstant, SimpleBase)
    parents = [
        mro_class.__name__ for mro_class in cls.__mro__
        if issubclass(mro_class, SimpleBase) and
           mro_class.__name__ not in BASE_CLASS_NAMES and
           mro_class != cls
    ]

    # 3. Vytvoření a navrácení řetězce
    return (
        cls.__name__
        if not parents else
        f"{cls.__name__}({', '.join(parents)})"
    )

>>> src/simplibs/object/_metadata/instance_builders/atom_class/base_class/InstanceBase.py
class InstanceBase:

    # 1. Definice třídního atribut zajištujícího že se nebudou počítat metadata
    # a ty tak budou přejmutá z deklarační třídy.
    _is_instance_class: bool = True

    # 2. Nastavení slotu a slabé reference pro podporu hashování
    __slots__ = ("__weakref__",)

    # 3. Definice pomocné metody pro mixiny skrze kterou mají přístup do initu třídy
    def init_mixins(self) -> None:
        """Výchozí prázdná kotva pro reaktivní inicializaci mixinů."""
        pass

    # 3. Definice pomocné metody pro mixiny skrze kterou mají přístup před uložením hodnoty
    def _before_update(self, new_value):
        """Hook pro mixiny — výchozí implementace nedělá nic."""
        pass

    #--- Definice protperty zpřístupňující meta ---#
    # (pro přímí přístup bez procházení MRO)
    @property
    def meta(self: SimpleDefinitionClass) -> SimpleMetaType:
        return self.__class__.__metadata__

    #--- Definice __repr__ (reprezentačního řetězce objektu) ---#
    # (univerzální definice společná všem potomkům)
    def __repr__(self) -> str:
        class_name  = self.meta.class_name
        blueprint   = f"blueprint='{self.meta.blueprint_path}'"
        state       = f"value={self._value!r}" if hasattr(self, "_value") else ""
        hex_id      = f"id={hex(id(self))}"

        return f"<{class_name} {blueprint} {state} {hex_id}>"

    #--- Definice __str__ (řetězec reprezentující jméno třídy) ---#
    # (univerzální definice společná všem potomkům)
    def __str__(self) -> str:
        return self.meta.class_name

>>> src/simplibs/object/_metadata/instance_builders/atom_class/helpers/create_atom_init.py
def create_atom_init(
    meta: SimpleMetaType,
    base_class_name: str
) -> Callable:

    # 1. Definice logiky initu
    def __init__(self):

        # Vytvoření hodnoty z defaultu
        self._value = meta.default

        # Nastavení atributu pro vlastníka na None (definuje až konstanta skrze své inners)
        self._owner = None

        # Zpuštění pomocné metody pro mixiny (umožňující mixinům připsat logiku do initu)
        self.init_mixins()

    # 2. Dynamické přilepení metadat
    __init__.__name__ = "__init__"
    __init__.__qualname__ = f"{base_class_name}.__init__"
    __init__.__annotations__ = {"return": None}

    # 3. Navrácení metody
    return __init__

>>> src/simplibs/object/_metadata/instance_builders/atom_class/helpers/create_atom_value_property.py
def create_atom_value_property(
    meta: SimpleMetaType,
) -> property:

    # 1. Definice Getteru
    def getter(self) -> Any:
        return self._value

    # 2. Definice anotace getteru
    getter.__annotations__ = {"return": meta.value_type}

    # 3. Definice Setteru
    def setter(self, value: Any) -> None:

        # 3.1 Hook pro volání před uložením hodnoty
        self._before_update(value)

        # 3.1 Zápis hodnoty a aktivace přepočtu ownera
        self._root_value_setter(value, recalculate_up=True)

    # 4. Definice anotace setteru
    setter.__annotations__ = {"value": meta.value_type, "return": None}

    # 5. Definice docstringu
    doc_string = (
        f"Hodnota typu `{meta.value_type.__name__}`.\n"
        f"\n"
        f"Getter vrací hodnotu kterou třída reprezentuje.\n"
        f"Setter provádí normalizaci hodoty, uložení a spouští aktualizační kaskádu směrem nahoru."
    )

    # 6. Sestavení a navrácení hotové property
    return property(
        fget=getter,
        fset=setter,
        doc=doc_string
    )

>>> src/simplibs/object/_metadata/instance_builders/atom_class/helpers/create_root_value_setter.py
def create_root_value_setter(
    meta: SimpleMetaType,
    base_class_name: str
) -> Callable:

    def _root_value_setter(
        self,
        value: Any,
        recalculate_up: bool = True
    ) -> None:
        """Interní metoda pro zápis hodnoty s možností řízení reaktivního bublání."""

        # 1. Normalizace a validace nové hodnoty
        new_value = self.normalize(value, process_none=True)

        # 2. Kontrola, zda hodnota není shodná s aktuální
        if self._value == new_value:
            return

        # 3. Zápis hodnoty
        self._value = new_value

        # 4. Spuštění přepočtu pro vnější prvky
        if self._owner and recalculate_up:
            # noinspection PyProtectedMember
            self._owner._recalculate_self()

    # Nastavení správných jmen pro debugování a introspekci
    _root_value_setter.__name__ = "_root_value_setter"
    _root_value_setter.__qualname__ = f"{base_class_name}._root_value_setter"
    _root_value_setter.__annotations__ = {"value": Any, "recalculate_up": bool, "return": None}

    _root_value_setter.__doc__ = (
        f"Zabezpečuje zápis hodnoty do instance {meta.class_name}.\n"
        f"\n"
        f"Provede normalizaci, porovná hodnotu vůči stávající a v případě změny\n"
        f"může aktivovat reaktivní přepočet vlastníka (bublání nahoru).\n"
    )

    return _root_value_setter

>>> src/simplibs/object/_metadata/instance_builders/atom_class/make_atom_class.py
def make_atom_class(
    meta: SimpleMetaType
) -> type:

    # 1. Defnice jména třídy
    base_class_name = f"{meta.class_name}AtomBase"

    # 2. Definice předků třídy
    class_parents = (InstanceBase, meta.owner_class,)

    # 3. Definice slovníku třídy
    class_dict = {
        "__doc__": f"Atomický instanční objekt pro {meta.class_name}",
        "__slots__": ("_value", "_owner"),
        "__init__": create_atom_init(meta, base_class_name),
        "_root_value_setter": create_root_value_setter(meta, base_class_name),
        "value": create_atom_value_property(meta),
        "owner": property(lambda self: self._owner, doc="Reference na nadřazenou kompozici.")
    }

    # 4. Vytvoření třídy
    atom_class = type(
        base_class_name,
        class_parents,
        class_dict
    )

    # 5. Odstranění deklarativních atributů
    for name in ("_type", "_default", "_validate", "bool_or_raise_validate_error"):
        if hasattr(atom_class, name):
            delattr(atom_class, name)

    # 6. Navrácení třídy
    return atom_class

>>> src/simplibs/object/_metadata/instance_builders/composite_class/helpers/create_composite_init.py
def create_composite_init(
    meta: SimpleMetaType,
    base_class_name: str
) -> Callable:

    def __init__(self):
        # 1. Zavoláme init předka (AtomBase)
        # Ten nastaví základní self._value a self._owner = None
        meta.atom_class.__init__(self)

        # 2. Projdeme všechny přímé inners definované v metadatech
        for inner in meta.inners:
            inner_meta = inner.meta

            # Zjistíme živou instanční třídu pro tento pod-prvek
            # (buď atom_class nebo composite_class z jeho metadat)
            inner_instance_cls = inner_meta.atom_class if inner_meta.is_constant else inner_meta.composite_class

            # Zrodíme čistou instanci tohoto vnitřního prvku (zcela bez parametrů)
            inner_instance = inner_instance_cls()

            # Provážeme ji: nastavíme ji jako vlastníka tuto naši kompozici
            inner_instance._owner = self

            # Uložíme ji do příslušného privátního slotu (např. self._motor)
            setattr(self, inner_meta.name_private, inner_instance)

        # 3. Odstartujeme inicializační kaskádu pro případné mixiny kompozice
        self.init_mixins()

    # Nastavení správných jmen pro debugování a introspekci
    __init__.__name__ = "__init__"
    __init__.__qualname__ = f"{base_class_name}.__init__"
    __init__.__annotations__ = {"return": None}

    return __init__

>>> src/simplibs/object/_metadata/instance_builders/composite_class/helpers/create_composite_value_property.py
def create_composite_value_property(
    meta: SimpleMetaType
) -> property:

    # 1. Definice Getteru
    def getter(self) -> Any:
        return self._value

    # 2. Definice anotace getteru
    getter.__annotations__ = {"return": meta.value_type}

    # 3. Definice Setteru
    def setter(self, value: Any) -> None:

        # 3.1 Ověření, zda tato kompozice podporuje dekompozici
        if not meta.is_decomposeable:
            raise TypeError(
                f"Kompozice '{meta.class_name}' nepodporuje přímé přiřazení hodnoty, "
                f"protože nemá definovanou uživatelskou metodu decompose_value()."
            )

        # 3.2 Zápis hodnoty a aktivace přepočtu ownera
        self._root_value_setter(value, recalculate_up=True)

        # 3.3 Rozložení hodnoty a zápis do vnitřních prvků
        self._recalculate_inners()

    # 4. Definice anotace setteru
    setter.__annotations__ = {"value": meta.value_type, "return": None}

    # 5. Definice docstringu
    doc_string = (
        f"Kompozitní hodnota typu `{meta.value_type.__name__ if hasattr(meta.value_type, '__name__') else str(meta.value_type)}`.\n"
        f"\n"
        f"Getter vrací aktuální vypočítanou hodnotu kompozice.\n"
        f"Setter rozloží (dekomponuje) vstupní hodnotu a distribuuje ji do vnitřních prvků."
    )

    # 6. Sestavení a navrácení hotové property
    return property(
        fget=getter,
        fset=setter,
        doc=doc_string
    )

>>> src/simplibs/object/_metadata/instance_builders/composite_class/helpers/create_properties_for_inners.py
def create_properties_for_inners(
    meta: SimpleMetaType,
) -> dict:

    # 1. Definice prázdného slovníku
    property_dict = {}

    # 2. Zpracování innerů
    for inner in meta.inners:
        properties = create_properties_for_inner(inner.meta)
        property_dict.update(properties)

    # 3. Navrácení slovníku s property
    return property_dict

>>> src/simplibs/object/_metadata/instance_builders/composite_class/helpers/create_recalculate_inners.py
def create_recalculate_inners(
    meta: SimpleMetaType,
    base_class_name: str
)-> Callable:

    def _recalculate_inners(self) -> None:

        # 1. Rozložení hodnoty na hodnoty inners
        decomposed_values = self.decompose_value(self._value)

        # 2 Distribuce hodnot do inners
        for inner, inner_value in zip(meta.inners, decomposed_values):

            # 2.1 Načtení instance inneru
            inner_instance = getattr(self, inner.meta.name_private)

            # 2.2 Zápis nové hodnoty s potlačenou propagací nahoru
            # noinspection PyProtectedMember
            inner_instance._root_value_setter(inner_value, recalculate_up=False)

            # 2.3 Pokud je prvek kompozice - aktivace přepočtu jejích vnitřních prvků
            if not inner.meta.is_constant:
                # noinspection PyProtectedMember
                inner_instance._recalculate_inners()


    # Nastavení správných jmen pro debugování a introspekci
    _recalculate_inners.__name__ = "_recalculate_inners"
    _recalculate_inners.__qualname__ = f"{base_class_name}._recalculate_inners"
    _recalculate_inners.__annotations__ = {"return": None}

    _recalculate_inners.__doc__ = (
        f"Rozloží hodnotu kompozice {meta.class_name} a předá jejich hodnoty do vlastních inners.\n"
        f"\n"
        f"Tato metoda provádí reaktivní aktualizaci stavu pro vnitřní prvky. "
        f"Spustí se automaticky, jakmile dojde ke změně hlavní hodnoty.\n"
    )

    return _recalculate_inners

>>> src/simplibs/object/_metadata/instance_builders/composite_class/helpers/create_recalculate_self.py
def create_recalculate_self(
    meta: SimpleMetaType,
    base_class_name: str
) -> Callable:

    def _recalculate_self(self) -> None:

        # 1. Získání slovníku s hodnotami inners
        current_values = {
            inner.meta.name_snake: getattr(self, inner.meta.name_private).value
            for inner in meta.inners
        }

        # 2. Výpočet hodnoty
        new_value = self.calculate_value(**current_values)

        # 3. Zápis a propagace pouze při reálné změně hodnoty
        if self._value == new_value:
            return

        # Uložení nové vypočítané hodnoty
        self._value = new_value

        # 4. Pokud tuto kompozici vlastní jiná nadřazená kompozice, předáme update výše
        if self._owner:
            # noinspection PyProtectedMember
            self._owner._recalculate_self()

    # Nastavení správných jmen pro debugování a introspekci
    _recalculate_self.__name__ = "_recalculate_self"
    _recalculate_self.__qualname__ = f"{base_class_name}._recalculate_self"
    _recalculate_self.__annotations__ = {"return": None}

    _recalculate_self.__doc__ = (
        f"Přepočítá hodnotu kompozice {meta.class_name} a předá požadavek na přepočet směrem nahoru v hierarchii.\n"
        f"\n"
        f"Tato metoda provádí reaktivní aktualizaci stavu. "
        f"Spustí se automaticky, jakmile dojde ke změně hodnoty některého z vnitřních prvků (atomů či sub-kompozic).\n"
    )

    return _recalculate_self

>>> src/simplibs/object/_metadata/instance_builders/composite_class/make_composite_class.py
def make_composite_class(
    meta: SimpleMetaType
) -> type:

    # 1. Defnice jména třídy
    base_class_name = f"{meta.class_name}CompositeBase"

    # 2. Definice předků třídy
    class_parents = (meta.atom_class,)

    # 3. Definice slovníku třídy
    class_dict = {
        "__doc__": f"Kompozitní instanční objekt pro {meta.class_name}",
        "__slots__": tuple(inner.meta.name_private for inner in meta.inners),
        "__init__": create_composite_init(meta, base_class_name),
        "_recalculate_self": create_recalculate_self(meta, base_class_name),
        "_recalculate_inners": create_recalculate_inners(meta, base_class_name),
        "value": create_composite_value_property(meta),
    } | create_properties_for_inners(meta)

    # 4. Vytvoření třídy
    composite_class = type(
        base_class_name,
        class_parents,
        class_dict
    )

    # 5. Odstranění deklarativních atributů
    for name in ("inners", "_logic", "_decompose"):
        if hasattr(composite_class, name):
            delattr(composite_class, name)

    # 6. Navrácení třídy
    return composite_class

>>> src/simplibs/object/_metadata/instance_builders/instance/create_instance.py
def create_instance(
    cls: SimpleClassType,
    mixins: tuple,
    as_atom: bool
) -> Any:

    # 1. Validace třídy a bool parametru
    if (cls.__name__ in BASE_CLASS_NAMES or
        not isinstance(as_atom, bool)):
        validate_class_is_not_base_class(cls)
        validate_param_is_bool(as_atom)

    # 2. Získání základní třídy a určení režimu (Atom / Composite)
    is_atom = cls.meta.is_constant or as_atom
    base_class = cls.meta.atom_class if is_atom else cls.meta.composite_class

    # 3. Kontrola mixinů
    for mixin in mixins:
        from ....mixins.base_class import SimpleMixin
        # Ověření, že jde o třídu a že je to potomek SimpleMixin
        if (not isinstance(mixin, type) or
            not issubclass(mixin, SimpleMixin) or
            (is_atom and getattr(mixin, "_composite_only", False))):
            validate_mixin_is_class(cls, mixin)
            validate_mixin_is_simple_base_subclass(cls, mixin)
            validate_mixin_is_compatible(cls, mixin, is_atom)


    # 4. Příprava dat pro sestavení třídy
    class_parents = (*mixins, base_class)
    class_name = f"{cls.meta.class_name}Instance"
    class_dict = {"__slots__": ()}

    # 5. Sestavení instanční třídy (Chráněno před konflikty slotů)
    try:
        _instance_cls = type(class_name, class_parents, class_dict)
    except TypeError as error:
        # Python sám vyhodí TypeError, pokud dojde ke kolizi slotů mezi mixiny navzájem
        raise_mixin_slots_conflict_error(cls, mixins, error)

    # 6. Přepis jména třídy
    # noinspection PyUnboundLocalVariable
    _instance_cls.__qualname__ = class_name

    # 6.5 Doplnění třídní logiky
    for mixin in mixins:
        if hasattr(mixin, "__extend_instance_class__"):
            _instance_cls = mixin.__extend_instance_class__(_instance_cls)

    # 7. Vytvoření živé instance a její inicializace
    # noinspection PyTypeChecker
    instance = object.__new__(_instance_cls)
    # noinspection PyArgumentList
    instance.__init__()

    return instance

>>> src/simplibs/object/_metadata/SimpleBaseMetadata.py
class SimpleBaseMetadata:
    """
    Základní orchestrátor metadat systému Simple.
    Zajišťuje extrakci jmen a správu jmenného prostoru objektu.
    """

    #--- Definice __slots__ pro lepší výkon ---#
    # (každý potomek musí slots definovat jinak příjde o tuto výhodu)
    __slots__ = (
        # 1. Reference na třídu vlastníka
        "owner_class",

        # 2. Názvová identita (vypočtená z názvu třídy)
        "class_name",       # Např. "MojeData"
        "name_readable",    # Např. "moje data"
        "name_title",       # Např. "Moje data"
        "name_snake",       # Např. "moje_data"
        "name_private",     # Např. "_moje_data"

        # 3. Správa jmenného prostoru
        "used_names",       # Set použitých jmen pro detekci kolizí

        # 4. Pomocný předvýpočet pro __repr__
        "blueprint_path"
    )

    #--- Definice __init__ pro linicializaci hodnot ze slotů ---#
    # (přidává metodu skrze kterou se budou iniicalizovat potomci)
    def __init__(self, owner_class: SimpleClassType):
        """
        Inicializuje základní metadata.
        Pokud je bypass=True, vytvoří pouze prázdnou schránku pro systémové báze.
        """
        # 1. Přiřazení třídy
        self.owner_class = owner_class

        # 2. Výpočet jmenné identity
        self.class_name = owner_class.__name__
        (self.name_readable,
         self.name_title,
         self.name_snake,
         self.name_private) = create_names(owner_class)

        # 3. Registrace jména do setu použitých jmen (základ pro budoucí validace inners)
        self.used_names: Set[str] = {self.name_snake}

        # 4. Příprava parametru pro vytváření repr
        self.blueprint_path = calculate_blueprint_path(owner_class)

        # 5. Spuštění metod pro integraci logiky potomků
        self._process_user_data()

    #--- Definice metody pro inicializaci potomků ---#
    # (potomci nemají vlastní init a používají tuto metodu)
    def _process_user_data(self) -> None:
        """
        Hook pro procesy specifické pro daný typ metadata.

        Výchozí implementace: žádný obsah.
        Určeno pro přepsání v podtřídách.
        """
        pass

    #--- Metoda pro zápis atributů metadatové třídy ---#
    # (zamezuje přepisu již zadaných dat)
    def __setattr__(self, attr_name: str, new_value: Any) -> None:
        """Povolí zápis pouze pokud je pole UNSET nebo patří do cache."""

        # 1. Získání aktuální hodnoty
        current_value = getattr(self, attr_name, UNSET)

        # 2. Kontrola zda přepisujeme jen nedefinovaný prvek
        if current_value is not UNSET:
            raise_metadata_is_immutable(attr_name, current_value, new_value, self.owner_class)

        # 3. Provedení zápisu
        super().__setattr__(attr_name, new_value)

>>> src/simplibs/object/_metadata/SimpleConstantMetadata.py
class SimpleConstantMetadata(SimpleBaseMetadata):
    """
    Specializovaný orchestrátor pro konstanty (Atomy).
    Zajišťuje, že každý list systému má jasně definovaný typ,
    validní výchozí hodnotu a funkční validační rozhraní.
    """

    #--- Definice __slots__ pro lepší výkon ---#
    # (každý potomek musí slots definovat jinak příjde o tuto výhodu)
    __slots__ = (

        # 1. Data předaná uživatelem
        "value_type",       # Normalizovaný typ (_type)
        "default",          # Výchozí hodnota (_default)
        "validate",         # Reference na metodu _validate

        # 2. Veřejné rozhraní
        "value_type_name",  # Jméno typu (str)
        "is_constant",      # Bool parametr definující zda jde o konstantu

        # 3. Cache pro instanční třídu
        "_atom_class",
    )

    #--- Definice logiky pro inicializaci dat ---#
    # (metoda je spuštěna v initu základní třídy)
    def _process_user_interface(self):

        # 1. Deklarace že třída je konstanta
        self.is_constant = True

        # 2. Zpracování _type
        (self.value_type,
         self.value_type_name) = process_type(
            owner_class=self.owner_class
        )

        # 3. Zpracování _default
        self.default = process_default_for_constant(
            default_type=self.value_type,
            owner_class=self.owner_class
        )

        # 4. Zpracování _validate
        self.validate = process_classmethod(
            method_name="_validate",
            expected_params=("cls", "value", "return_bool"),
            expected_args_params_count=2,
            expected_args_defaults=(),
            expected_kwargs_defaults={"return_bool": False},
            expected_param_types={"value": Any, "return_bool": bool},
            expected_return_type=bool | None,
            test_value=(self.default,),
            owner_class=self.owner_class,
        )

        # 5. Příprava cache
        self._atom_class = UNSET

    #--- Definice property pro výpočet a cache ---#
    # (vrací atomický základ pro třídu na instance)
    @property
    def atom_class(self):
        """Lazy brána k core instanci parametru."""
        if self._atom_class is UNSET:
            self._atom_class = make_atom_class(self.owner_class.__metadata__)
        return self._atom_class

>>> src/simplibs/object/_metadata/SimpleMeta.py
class SimpleMeta(type):
    """
    Metatřída systému Simple. Zajišťuje automatickou orchestraci metadat
    při definici třídy a chrání integritu jejího rozhraní.
    """

    #--- Metoda pro vytvoření třídy ---#
    # (u defiičních tříd vytváří metadata)
    def __new__(
        mcls: Self,
        name: str,
        bases: Tuple[type, ...],
        namespace: Dict[str, Any]
    ) -> SimpleClassType:
        """
        Analyzuje vznikající třídu a rozhoduje o jejím zařazení (Kořen/Konstanta/Kompozice).
        """
        # 1. Vytvoření objektu třídy
        cls = super().__new__(mcls, name, bases, namespace)

        # 2. Přeskočení vytváření metadata pro základní a instanční třídy
        if hasattr(cls, "_is_instance_class") or name in BASE_CLASS_NAMES:
            return cls

        # 3. Výpočet metadat (pro deklarativní třídy)
        cls.__metadata__ = (
            SimpleObjectMetadata(owner_class=cls)
            if hasattr(cls, "_inners")
            else SimpleConstantMetadata(owner_class=cls)
        )

        # 4. Navrácení třídy
        return cls


    #--- Metoda pro zápis atributů hlavní třídy ---#
    # (zamezuje přepisu již zadaných dat)
    def __setattr__(
        cls,
        attr_name: str,
        new_value: Any
    ) -> None:
        """Definuje zamezení přepisu již zapsaných hodnot."""

        # 1. Kontrola zda nedochází k přepisu atributu
        if getattr(cls, attr_name, UNSET) is not UNSET:
            raise_attribut_allready_set(cls, attr_name, new_value)

        # 2. Zápis hodnoty
        super().__setattr__(attr_name, new_value)


    #--- Metoda pro vytváření instancí ---#
    # (dopočítá instanční třídu a vrátí instanci)
    def __call__(cls: SimpleClassType, mixins: tuple = (), as_atom: bool = False):
        """
        Metoda pro vytváření instancí, dopočítá instanční třídu a vrátí instanci.
        """
        return create_instance(cls, mixins, as_atom)


    # --- Definice __repr__ pro definiční třídy ---#
    def __repr__(cls) -> str:
        """
        Technická reprezentace samotné definiční třídy (šablony).
        Ukazuje typ blueprintu a informaci, zda jde o Konstantu nebo Kompozici.
        """
        return (
            f"<class {cls.__name__} (System Base)>"
            if cls.meta is UNSET else
            f"<{cls.meta.class_name}Blueprint blueprint='{cls.meta.blueprint_path}' "
            f"type={'Constant' if cls.meta.is_constant else 'Object'}>")


    # --- Definice __str__ pro definiční třídy ---#
    def __str__(cls) -> str:
        """
        Uživatelská reprezentace třídy.
        Vrací čisté byznysové jméno třídy.
        """
        return cls.__name__


    #--- Property usnadňující přístup k metadatům ---#
    @property
    def meta(cls) -> SimpleMetaType:
        """Veřejné rozhraní pro přístup k metadatům třídy."""
        # noinspection PyUnresolvedReferences
        return cls.__metadata__


>>> src/simplibs/object/_metadata/SimpleObjectMetadata.py
class SimpleObjectMetadata(SimpleConstantMetadata):
    """
    Orchestrátor pro kompozitní objekty (Nodes).
    Zajišťuje propojení vnitřních prvků (inners), definici výpočetní
    logiky a správu transformačních signatur.
    """

    #--- Definice __slots__ pro lepší výkon ---#
    # (každý potomek musí slots definovat jinak příjde o tuto výhodu)
    __slots__ = (

        # 1. Data předaná uživatelem
        "inners",               # Seznam/Mapa vnitřních prvků
        "logic",                # Metoda _logic pro výpočet jádra
        "decompose",            # Metoda _decompose pro rozklad

        # 2. Mapy pro inners prvky
        "inners_params_name",  # tuple[str, ...] -> Pro bleskové mapování *args na jména
        "inners_map",  # dict[str, SimpleClassType] -> Pro všechno ostatní!

        # 3. Veřejné rozhraní
        "is_decomposeable",     # Bool parametr definující zda je možné měnit hodnotu instance rozkladem

        # 4. Cache pro instanční třídu
        "_composite_class",
    )

    #--- Definice logiky pro inicializaci dat ---#
    # (metoda je spuštěna v initu základní třídy)
    def _process_user_interface(self):

        # 1. Deklarace že třída není konstanta
        self.is_constant = False

        # 2. Zpracování _default (na kompozici nesmí být definován)
        if hasattr(self.owner_class.__dict__, "_default"):
            raise_default_is_defined_in_composition(self.owner_class)

        # 3. Zpracování _type
        (self.value_type,
         self.value_type_name) = process_type(
            owner_class=self.owner_class
        )

        # 4. Zpracování _inners
        (self.inners,
         self.used_names) = process_inners(
            used_names=self.used_names,
            name_snake=self.name_snake,
            owner_class=self.owner_class
        )

        # 5. Vytvoření maperů a dat pro zpracvování metohod
        self.inners_map = {inner.meta.name_snake: inner for inner in self.inners}
        self.inners_params_name = tuple(inner.meta.name_snake for inner in self.inners)

        # 6. Příprava dat pro zpracování logik
        inners_default = tuple(inner.meta.default for inner in self.inners)
        inners_annotations = {
            inner.meta.name_snake: inner.meta.value_type
            for inner in self.inners
        }

        # 7. Zpracování _logic
        (self.logic,
         self.default) = process_classmethod(
            method_name="_logic",
            expected_params=("cls", *self.inners_params_name),
            expected_args_params_count=1+len(self.inners_params_name),
            expected_args_defaults=inners_default,
            expected_kwargs_defaults={},
            expected_param_types=inners_annotations,
            expected_return_type=self.value_type,
            owner_class=self.owner_class,
            return_calculated_value=True
        )

        # 8. Zpracování _decompose
        self.decompose = process_classmethod(
            method_name="_decompose",
            expected_params=("cls", "value"),
            expected_args_params_count=2,
            expected_args_defaults=(self.default,),
            expected_kwargs_defaults={},
            expected_param_types={"value": self.value_type},
            expected_return_type=reduce(or_, inners_annotations.values()),
            owner_class=self.owner_class,
        )

        # 9. Definice rozložitelnosti
        self.is_decomposeable = (
            self.decompose is not UNSET and
            all(inner.meta.is_constant or inner.meta.is_decomposeable
                for inner in self.inners)
        )

        # 10. Zpracování _validate
        self.validate = process_classmethod(
            method_name="_validate",
            expected_params=("cls", "value", "return_bool"),
            expected_args_params_count=2,
            expected_args_defaults=None,
            expected_kwargs_defaults={"return_bool": False},
            expected_param_types={"value": Any, "return_bool": bool},
            expected_return_type=bool | None,
            test_value=(self.default,),
            owner_class=self.owner_class,
        )

        # 11. Příprava cache
        self._atom_class = UNSET
        self._composite_class = UNSET


    #--- Definice property pro výpočet a cache ---#
    # (vrací atomický základ pro třídu na instance)
    @property
    def composite_class(self):
        """Lazy brána k atomické instanci parametru."""
        if self._composite_class is EMPTY:
            self._composite_class = make_composite_class(self.owner_class.__metadata__)
        return self._composite_class

>>> src/simplibs/object/_types/protocols/ClassMethodProtocol.py
@runtime_checkable
class FunctionProtocol(Protocol):
    __annotations__: dict[str, Any]
    __defaults__: tuple[Any, ...] | None
    __kwdefaults__: dict[str, Any] | None
    __code__: Any
    __globals__: dict[str, Any]
    __closure__: tuple[Any]


@runtime_checkable
class ClassMethodProtocol(Protocol):
    __func__: FunctionProtocol
    __self__: type
    __call__: Callable[..., Any]

>>> src/simplibs/object/_types/protocols/LogicSignature.py
# Typové proměnné pro magii s přenosem signatury
P = ParamSpec("P")
R = TypeVar("R")

class LogicSignature(Protocol[P, R]):
    """Protokol říkající: Jsem třída, která má metodu _logic s parametry P a návratem R."""
    @classmethod
    def _logic(cls, *args: P.args, **kwargs: P.kwargs) -> R: ...

    meta: SimpleMetaType
    _log_outcome: Callable

>>> src/simplibs/object/_types/type_chackings/SimpleClassType.py
# 1. Definice pro typovou kontrolu
if TYPE_CHECKING:

    # 1.1 Vnitřní import tříd
    from ...SimpleBase import SimpleBase
    from ...SimpleConstant import SimpleConstant
    from ...SimpleObject import SimpleObject

    # 1.2 Typ reprezentující konkrétní instance (např. moje_auto)
    SimpleDefinitionClass = SimpleBase | SimpleConstant | SimpleObject

    # 1.3 Typ reprezentující samotné základní třídy, které mají metadata UNSET (např. SimpleBase, SimpleConstant, SimpleObject)
    SimpleDefinitionClassType = Type[SimpleBase] | Type[SimpleConstant] | Type[SimpleObject]

    # 1.4 Typ reprezentující Ddefiniční třídy, které už mají metadata (např. Auto, Motorka)
    class SimpleClassType(SimpleDefinitionClassType):
        meta: SimpleMetaType

    # 1.5 Typ reprezentující vytvořenou instanci
    class SimpleInstanceType(SimpleClassType):
        _value: Any

# 2. Definice pro běh
else:
    SimpleDefinitionClass = Any
    SimpleDefinitionClassType = type
    SimpleClassType = type

>>> src/simplibs/object/_types/type_chackings/SimpleMetaType.py
# 1. Definice pro typovou kontrolu
if TYPE_CHECKING:

    # 1.1 Vnitřní import třídy pro metadtata
    from ..._metadata import SimpleMeta, SimpleBaseMetadata, SimpleConstantMetadata, SimpleObjectMetadata

    # 1.2 Typ reprezentující metadata
    SimpleMetaType = SimpleMeta | SimpleBaseMetadata | SimpleConstantMetadata | SimpleObjectMetadata

# 2. Definice pro běh
else:
    SimpleMetaType = Any

>>> src/simplibs/object/_utils/constant_class/bool_or_raise_validate_error.py
def bool_or_raise_validate_error(
    cls: Any,
    value: Any,
    problem: str,
    *,
    return_bool: bool = False,
) -> bool:
    """Interní implementace sdílené validační logiky."""

    # 1. Kontrola zda se má vrátit bool
    if return_bool:
        return False

    # 2. Vyvolání předpřipravené výjimky
    raise SimpleException(
        error_name="VALIDATION ERROR",
        value_label="input_value",
        value=value,
        expected=f"Valid configuration for {cls.__name__}",
        problem=problem,
        how_to_fix=(
            f"Ensure the data provided to '{cls.__name__}' meets the validation criteria.",
            f"The expected base type or format is '{cls.meta.value_type_name}'."
        ),
        context=f"Triggered within custom validation of {cls.__name__}.",
        exception=ValueError,
    )

>>> src/simplibs/object/_utils/constant_class/normalize.py
def normalize(
    cls,
    value: Any,
    *,
    process_none: bool = False
) -> Any:

    # 1. Ošetření None
    if value is None:

        # 1.1 Vyřízení pokud je None očekáváné
        if process_none:
            return cls.meta.default

        # 1.2 Vyovální výjimky
        raise_missing_value_error(cls)

    # 2. Ošetření situace kdy je hodnota schodná s defaultní
    # noinspection PyBroadException
    try:

        # 2.1 Pokud hodnota odpovídá defaultu - vrací se odkaz na default
        if value == cls.meta.default:
            return cls.meta.default

    # 2.2 Pokud hodnota není porovnatelná - pokračuje se na validaci
    except Exception:
        pass

    # 3. Validace
    cls.validate(value)

    # 4. Případné logování (je-li nastaveno)
    cls._log_outcome(value)

    # 5. Navrácení zvalidvoané hodnoty
    return value


>>> src/simplibs/object/_utils/constant_class/validate.py
def validate(
    cls,
    value: Any,
    *,
    return_bool: bool = False
) -> bool | None | NoReturn:

    # 1. Validace typu a validační metodou
    try:
        result = (
            cls.validate_type(value, return_bool=return_bool) and
            cls.meta.validate(value, return_bool=return_bool)
        )

    # 2. Zpracování výjimek
    except Exception as e:

        # 2.1 Vyřízení pro bool odpověd
        if return_bool:
            return False

        # 2.2 Zpracování definované výjimky
        if isinstance(e, SimpleError):
            raise

        # 2.3 Zpracování ostatních výjimmek
        raise_unexpected_validation_error(cls, value, e)

    # 3. Kontrola výsledku (případné vyvolání výjimky)
    if result is False and return_bool is False:
        raise_validation_error(cls, value)

    # 4. Navrácen bool odpovědi
    return result

>>> src/simplibs/object/_utils/constant_class/validate_type.py
def validate_type(
    cls,
    value: Any,
    *,
    return_bool: bool = False
) -> bool | NoReturn:

    # 1. Validace Happy path
    if isinstance(value, cls.meta.value_type):
        return True

    # 2. Vrácení bool negace
    if return_bool:
        return False

    # 3. Vyvolání výjimky
    raise_type_error(cls, value, cls.meta.value_type)

>>> src/simplibs/object/_utils/serializations/from_dict.py
def from_dict(cls, data):
    kwargs = {}
    for name, value in data.items():
        inner = cls.meta.inners_map[name]
        if inner.meta.is_constant:
            kwargs[name] = inner.meta.value_type(value)
        else:
            kwargs[name] = from_dict(inner, value)
    return cls(**kwargs)

>>> src/simplibs/object/_utils/serializations/to_dict.py
def to_dict(obj):
    if obj.is_atom:
        return obj.value

    result = {}
    for inner in obj.meta.inners:
        inner_obj = getattr(obj, inner.name_snake)
        result[inner.name_snake] = to_dict(inner_obj)
    return result

>>> src/simplibs/object/_utils/testing/randomize.py
TYPE_GENERATORS = {}

def register_generator(type_, func):
    """Umožní uživateli zaregistrovat vlastní generátor pro typ."""
    TYPE_GENERATORS[type_] = func

def fill_random(obj, *, retries=5):
    """
    Naplní Simple objekt náhodnými daty.
    Rekurzivně projde celý strom (inners).
    Respektuje validaci — při chybě zkusí znovu.
    """

    # 1) Pokud má inners → rekurze
    if obj.meta.inners:
        for inner in obj.meta.inners:
            fill_random(getattr(obj, inner.name_private), retries=retries)
        return obj

    # 2) Atomická hodnota → generujeme
    value_type = obj.meta.value_type

    for _ in range(retries):
        value = generate_random_value(value_type)
        try:
            obj.value = value
            return obj
        except Exception:
            continue

    raise ValueError(
        f"Cannot generate valid random value for {obj} "
        f"after {retries} attempts."
    )

def generate_random_value(type_):
    """
    Vygeneruje náhodnou hodnotu podle typu.
    Respektuje registr TYPE_GENERATORS.
    """

    # 1) Uživatelský generátor
    if type_ in TYPE_GENERATORS:
        return TYPE_GENERATORS[type_]()

    # 2) Built-in generátory
    if type_ is int:
        return random.randint(0, 1000)

    if type_ is float:
        return round(random.uniform(0, 1000), 2)

    if type_ is str:
        length = random.randint(5, 15)
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    if type_ is bool:
        return random.choice([True, False])

    if type_ is datetime:
        start = datetime(2020, 1, 1)
        end = datetime(2025, 12, 31)
        delta = end - start
        return start + timedelta(days=random.randint(0, delta.days))

    if type_ is date:
        start = date(2020, 1, 1)
        end = date(2025, 12, 31)
        delta = end - start
        return start + timedelta(days=random.randint(0, delta.days))

    if type_ is Path:
        name = ''.join(random.choices(string.ascii_lowercase, k=10))
        return Path(f"/tmp/{name}.txt")

    # List[T]
    if hasattr(type_, "__origin__") and type_.__origin__ is list:
        item_type = type_.__args__[0] if type_.__args__ else int
        return [generate_random_value(item_type) for _ in range(random.randint(3, 10))]

    # Dict[K, V]
    if hasattr(type_, "__origin__") and type_.__origin__ is dict:
        key_type = type_.__args__[0] if type_.__args__ else str
        val_type = type_.__args__[1] if len(type_.__args__) > 1 else int
        return {
            generate_random_value(key_type): generate_random_value(val_type)
            for _ in range(random.randint(2, 5))
        }

    # Enum
    if isinstance(type_, type) and issubclass(type_, Enum):
        return random.choice(list(type_))

    # Fallback
    return None

>>> src/simplibs/object/_validations/process_calculate_value_params.py
def process_calculate_value_params(
    cls,
    *args,
    **kwargs
) -> dict[str, Any]:

    # 1. Načtení mapy innerů
    inners_map = cls.meta.inners_class_map

    # 2. Rychlý „guard clause“ na počet pozičních parametrů
    if len(args) > len(inners_map):
        raise ValueError(f"Třída {cls.__name__} očekává maximálně {len(inners_map)} pozičních parametrů, ale bylo zadáno {len(args)}.")

    # 3. Příprava dat
    clean_kwargs = {}
    args_iter = iter(args)

    # 4. Cyklus procházející mapu innerů
    for param_name, inner_cls in inners_map.items():

        # 4.1 Zpracování args
        try:
            value = next(args_iter)
            if param_name in kwargs:
                raise ValueError(f"Parametr '{param_name}' byl zadán jako poziční i pojmenovaný argument zároveň.")

        # 4.2 Zpracování kwargs
        except StopIteration:
            value = kwargs.pop(param_name, None)

        # 4.3 Natažení nezadaných parametrů
        if value is None:
            value = inner_cls.meta.default

        # 4.4 Validace předaných hodnot
        else:
            inner_cls.validate(value)

        # 4.5 Přidání zvalidované hodnoty do slovníku
        clean_kwargs[param_name] = value

    # 5. Kontrola zda v kwarks něco nezbylo
    if kwargs:
        unknown_params = ", ".join(f"'{k}'" for k in kwargs)
        raise ValueError(f"Třída {cls.__name__} neobsahuje parametry: {unknown_params}.")

    # 6. Navrácení slovníku
    return clean_kwargs

>>> src/simplibs/object/exceptions/SimpleError.py
class SimpleError(SimpleException):
    """Základní výjimka pro celou knihovnu SimpleObject."""
    _skip_locations = ("simplibs/object",)

>>> src/simplibs/object/exceptions/SimpleLogicError.py
class SimpleLogicError(SimpleError):
    """Výjimka pro chyby vzniklé při manipulaci s daty (validace, tvorba, update)."""

>>> src/simplibs/object/exceptions/SimpleMetadataError.py
class SimpleMetadataError(SimpleError):
    """Výjimka pro chyby v definici metadat a struktuře SimpleObject tříd."""

>>> src/simplibs/object/exceptions/SimpleMixinError.py
class SimpleMixinError(SimpleError):
    """Výjimka pro nevalidní definici mixinů"""

>>> src/simplibs/object/mixins/base_class/validations/constants/FORBIDDEN_NAMES.py
FORBIDDEN_NAMES = {
    "_value",
    "_owner",
    "value",
    "owner",
    "meta",
    "__init__",
    "_recalculate_self",
    "_recalculate_inners",
    "_root_value_setter",
}

>>> src/simplibs/object/mixins/base_class/validations/verify_mixin_definition.py
def verify_mixin_definition(cls):

    # 1. Validace přístomnosti slotu
    if "__slots__" not in cls.__dict__:
        raise_mixin_slots_is_not_defined(cls)

    # 2. Vytvoření proměné
    slots = cls.__dict__["__slots__"]

    # 3. Validace typu slotu
    if not isinstance(slots, (tuple, str)):
        raise_mixin_slots_unsuport_type(cls)

    # 4. Validace zda všechny prvky jsou str
    if not all(isinstance(s, str) for s in slots):
        raise_mixin_slots_contain_unvalid_type(cls)

    # 5. Validace zda některý z prvků není zakázaný
    slots_set = set(slots) if isinstance(slots, tuple) else {slots}
    if FORBIDDEN_NAMES & slots_set:
        raise_mixin_slots_contains_forbidden_slot_names(cls)

    # 6. Validace zda nejsou na třídě definované třídní atributy s nepovolenými jmény
    if FORBIDDEN_NAMES & cls.__dict__.keys():
        raise_mixin_dict_contains_forbidden_attributes(cls)

    # 7. Validace zda _composite_only je v případě definice uživatelem zapsán jako bool
    if ("_composite_only" in cls.__dict__ and
        not isinstance(cls.__dict__["_composite_only"], bool)):
        raise_mixin_composite_only_flag_is_not_bool(cls)

    # 8. Validace přítomnosti super() v metodě init_mixins
    if "init_mixins" in cls.__dict__:
        func = cls.__dict__["init_mixins"]

        # 8.1 Získání všech jmen (funkcí/atributů) volaných uvnitř metody
        called_names = func.__code__.co_names

        # 8.2 Pro správné řetězení musíme najít jak 'super', tak název metody 'init_mixins'
        if "super" not in called_names or "init_mixins" not in called_names:
            raise_mixin_init_mixins_missing_super_call(cls)

>>> src/simplibs/object/mixins/base_class/SimpleMixin.py
class SimpleMixin:

    # 1. Definice sltu
    __slots__ = ()

    # 2. Flag zda je možné mixin použít i pro konstantu
    _composite_only: bool = False

    # 3. Definice pomocné metody pro mixiny skrze kterou mají přístup do initu třídy
    def init_mixins(self) -> None:
        """Výchozí prázdná kotva pro reaktivní inicializaci mixinů."""
        # noinspection PyUnresolvedReferences
        super().init_mixins()

    # 4. Definice metody pro kontrolu zapsaných dat
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        verify_mixin_definition(cls)

>>> src/simplibs/object/mixins/core/data/Serialization.py
class Serialization(SimpleMixin):
    """
    Pohodlné metody pro převod instance na dict/JSON a zpět,
    postavené nad externími serializačními funkcemi.
    """

    __slots__ = ()

    def to_dict(self):
        """Serializuje instanci do dict."""
        return to_dict(self)

    @classmethod
    def from_dict(cls, data):
        """Vytvoří instanci ze serializovaného dictu."""
        return from_dict(cls, data)

    def to_json(self, **kwargs):
        """Serializuje instanci do JSON."""
        return json.dumps(self.to_dict(), ensure_ascii=False, **kwargs)

    @classmethod
    def from_json(cls, json_str):
        """Vytvoří instanci z JSON."""
        return cls.from_dict(json.loads(json_str))

>>> src/simplibs/object/mixins/core/property/InnersProperty.py
class InnersProperty(SimpleMixin):

    __slots__ = ()
    _composite_only = True

    # ---------------------------------------------------------
    # 1) Hook volaný z create_instance → doplní _default_state
    # ---------------------------------------------------------
    @staticmethod
    def __extend_instance_class__(instance_cls):

        # 1. Načtení meta
        meta = instance_cls.meta

        # 2. Vytvoření potřebných properties
        nested_props = collect_all_nested_properties(meta)

        # 3. Připojení atributů k třídě
        for name, prop in nested_props.items():
            setattr(instance_cls, name, prop)

        # 4. Navrácení pozměněné třídy
        return instance_cls

>>> src/simplibs/object/mixins/core/property/MetaShortcuts.py
class MetaShortcuts(SimpleMixin):
    """
    Ergonomické zkratky pro často používané položky z metadata objektu.
    Nepřidává žádnou logiku – pouze zpřístupňuje vybrané informace
    přímo na instanci.
    """

    __slots__ = ()

    # -------------------------
    # Identita objektu
    # -------------------------
    @property
    def name_snake(self: SimpleInstanceType) -> str:
        """Snake_case jméno třídy objektu."""
        return self.meta.name_snake

    # -------------------------
    # Typová informace
    # -------------------------
    @property
    def value_type(self: SimpleInstanceType) -> type:
        """Pythoní typ hodnoty, kterou objekt uchovává."""
        return self.meta.value_type

    @property
    def default(self: SimpleInstanceType):
        """Výchozí hodnota objektu definovaná v metadatech."""
        return self.meta.default

    # -------------------------
    # Struktura objektu
    # -------------------------
    @property
    def is_atom(self: SimpleInstanceType) -> bool:
        """True, pokud objekt představuje atom (nemá inners)."""
        return self.meta.is_constant

    @property
    def is_composite(self: SimpleInstanceType) -> bool:
        """True, pokud objekt představuje kompozici (má inners)."""
        return not self.meta.is_constant

    @property
    def is_decomposeable(self: SimpleInstanceType) -> bool:
        """True, pokud lze hodnotu objektu měnit rozkladem."""
        return self.meta.is_decomposeable if not self.meta.is_constant else False

>>> src/simplibs/object/mixins/core/state/_default_state_helpers/_process_copy.py
def _process_copy(
    source_instance: SimpleInstanceType,
    target_instance: SimpleInstanceType,
    meta: SimpleMetaType,
    recurse: bool = False
) -> None:

    # 1. Načtení instancí
    private_name = meta.name_private
    source_instance_attr = getattr(source_instance, private_name)
    target_instance_attr = getattr(target_instance, private_name)

    # 2. Změna hodnot
    # noinspection PyProtectedMember
    target_instance_attr._value = source_instance_attr._value

    # 3. Rekurzivní volání mateřské funkce
    if recurse:
        from .copy_instance_values import copy_instance_values
        copy_instance_values(source_instance_attr, target_instance_attr)

>>> src/simplibs/object/mixins/core/state/_default_state_helpers/build_recursive_maps.py
def build_recursive_maps(
    meta: SimpleMetaType
) -> tuple[dict[str, SimpleMetaType], ...]:

    # 1. Vytvoření prázdných slovníků
    constants = {}
    composites = {}

    # 2. Funkce pro rekurzivní zběr
    def walk(m):

        # 2.1 Průchod zkrze inners
        for inner in m.inners:

            # 2.1.1 Vyřízení konstanty
            if inner.meta.is_constant:
                constants[inner.meta.name_snake] = inner.meta

            # 2.1.2 Vyžízení kompozice (rekurzivní volání)
            else:
                composites[inner.meta.name_snake] = inner.meta
                walk(inner.meta)

    # 3. Zpuštění rekurze
    walk(meta)

    # 4. Návrat slovníků
    return constants, composites

>>> src/simplibs/object/mixins/core/state/_default_state_helpers/copy_instance_values.py
def copy_instance_values(
    source: SimpleInstanceType,
    target: SimpleInstanceType
) -> None:
    """
    Zkopíruje hodnoty všech atomů a kompozic z jiné instance.
    Rekurzivní, deterministické, bez validací.
    """

    # 1. Kopírování atomů
    for const_meta in target._constants_map.values():
        _process_copy(source, target, const_meta)

    # 2. Kopírování kompozic (rekurzivně)
    for comp_meta in target._composites_map.values():
        _process_copy(source, target, comp_meta, recurse=True)

    # 3. Kopírování hlavní hodnoty kompozice
    target._value = source._value

>>> src/simplibs/object/mixins/core/state/_history_helpers/builders/_collect_nested_inner_data.py
def _collect_nested_inner_data(instance, path, snapshot):
    """Rekurzivní funkce pro pžidání vnitřních prvků"""

    # 1. Procházení inners
    for inner in instance.meta.inners:

        # 2. Načtení proměných
        inner_meta = inner.meta
        name_private = inner_meta.name_private

        # 3. Vytvoření instance a cesty
        inner_instance = getattr(instance, name_private)
        new_path = path + (name_private,)

        # 4. Přidání záznamu
        snapshot.append((new_path, inner_instance._value))

        # 5. Vyřízení kompozic
        if not inner_meta.is_constant:
            _collect_nested_inner_data(inner_instance, new_path, snapshot)

>>> src/simplibs/object/mixins/core/state/_history_helpers/builders/build_snapshot.py
def build_snapshot(instance):
    """
    Vytvoří snapshot všech hodnot (_value) včetně všech inners.
    Vrací tuple:
        (name_snake,path_tuple, value)
    """

    # 1. Definice prázdné cesty
    path = ()

    # 2. Definice seznamu
    snapshot = [(path, instance._value),]

    # 3. Rekurzivní přidání vnitřních prvků
    if not instance.meta.is_constant:
        _collect_nested_inner_data(instance, path, snapshot)

    # 4. Navrácení tuple
    return tuple(snapshot)

>>> src/simplibs/object/mixins/core/state/_history_helpers/builders/restore_snapshot.py
def restore_snapshot(instance, snapshot):
    """
    Obnoví stav instance podle snapshotu.
    Snapshot má formát:
        name_snake: (path_tuple, value)
    """

    # 1. Procházení snapshotu
    for path, value in snapshot:

        # 2. Začínáme na root instanci
        target = instance

        # 3. Projdeme všechny prvky (když není žádný, použije se instance)
        for attr in path:
            target = getattr(target, attr)

        # 4. Zápis hodnoty
        object.__setattr__(target, "_value", value)

>>> src/simplibs/object/mixins/core/state/_history_helpers/comparators/compare_snapshots.py
def compare_snapshots(snap1, snap2, leaves_only=False):

    # Zachycení nevalidních snapshotů
    try:

        # 1. Vtyvoření proměných
        diffs = []
        last_path = None

        # 2. Cyklus skrtze oba snapshoty
        for (path, snap1_val), (_, snap2_val) in zip(snap1, snap2):

            # 2.1 Pokud hodnoty jsou stejné → pokračujeme dále
            if snap1_val == snap2_val:
                continue

            # 2.2 Pokud leaves_only=False → rovnou přidáme
            if not leaves_only:
                diffs.append((path, snap1_val, snap2_val))
                continue

            # 2.3 Pokud leaves_only=True
            # Kontrola zda ancestor existuje a je ze stejné větve
            if (last_path is not None and
                path[:len(last_path)] == last_path):

                # 2.3.1 Pokud ano ahradíme ancestor aktuálním leafem
                diffs[-1] = (path, snap1_val, snap2_val)
                last_path = path

            else:
                # 2.3.2 Pokud ne, pak zapíšeme a přidáme mezi ancestory
                diffs.append((path, snap1_val, snap2_val))
                last_path = path

        # 3. Navrácení tuple se změnami
        return tuple(diffs)

    # Zpracování případných výjimek
    except (ValueError, TypeError) as e:
        """
        ValueError zachytí rozbalování tuplů špatné délky (not enough values to unpack),
        TypeError zachytí případ kdy snapshot není iterovatelný vůbec.
        """
        raise ValueError(
            f"Snapshots are incompatible and cannot be compared: {e}"
        ) from e

>>> src/simplibs/object/mixins/core/state/_history_helpers/comparators/resolve_snapshot.py
def resolve_snapshot(key: int | datetime | tuple, history: list) -> tuple:
    """
    Převede klíč na snapshot.
    Přijímá: index (int), timestamp (datetime), nebo přímo snapshot (tuple).
    """

    # 1. Přímý snapshot → vrátíme rovnou
    if isinstance(key, tuple):
        return key

    # 2. Index
    if isinstance(key, int):
        if not (0 <= key < len(history)):
            raise IndexError(f"Snapshot index {key} out of range (history length: {len(history)})")
        _, snapshot = history[key]
        return snapshot

    # 3. Timestamp
    if isinstance(key, datetime):
        for ts, snapshot in history:
            if ts == key:
                return snapshot
        raise KeyError(f"No snapshot found for timestamp {key!r}")

    # 4. Neznámý typ
    raise TypeError(f"Expected int, datetime or tuple, got {type(key).__name__!r}")

>>> src/simplibs/object/mixins/core/state/_history_helpers/dicts/dict_to_snapshot.py
def dict_to_snapshot(snapshot_dict):
    """
    Převede dict (vytvořený pomocí snapshot_to_dict) zpět na snapshot.
    Snapshot má formát: tuple of (path_tuple, value)
    """

    # 1. Definice seznamu
    snapshot = []

    # 2. Rekurzivní pomocná funkce
    def _collect(processed_dict, path):

        # 2.1 Kořenová nebo vnitřní hodnota
        if "value" in processed_dict:
            snapshot.append((path, processed_dict["value"]))

        # 2.2 Procházení ostatních klíčů
        for key, val in processed_dict.items():

            # 2.3 Přeskočení klíče value (ten jsme zpracovali výše)
            if key == "value":
                continue

            # 2.4 Rekonstrukce původního názvu s prefixem
            private_key = "_" + key
            new_path = path + (private_key,)

            # 2.5 Vyřízení zanořené kompozice → rekurze
            if isinstance(val, dict):
                _collect(val, new_path)

            # 2.6 Vyřízení skalární hodnota → přímý zápis
            else:
                snapshot.append((new_path, val))

    # 3. Spuštění rekurze od kořene
    _collect(snapshot_dict, ())

    # 4. Navrácení tuple
    return tuple(snapshot)

>>> src/simplibs/object/mixins/core/state/_history_helpers/dicts/snapshot_to_dict.py
def snapshot_to_dict(snapshot):

    # 1. Definice proměnných
    result = {}
    last_created_key = None

    # 2. Cyklus na položky snapshotu
    for path, value in snapshot:

        # 2.1 Vyřízení kořenové hodnoty
        if not path:
            result["value"] = value
            continue

        # 2.2 Odstranění prefixů
        clean_path = tuple(key[1:] for key in path)

        # 2.3 Vyřízení pro jeden prvek
        if len(clean_path) == 1:
            key = clean_path[0]
            result[key] = value
            last_created_key = key
            continue

        # 2.4 Kontrola zda nevytváříme vnitřní slovník
        is_same_key = clean_path[-2] == last_created_key

        # 2.5 Vyřízení pro nově založený vnitřní slovník
        if is_same_key:

            # 2.5.1 Definice proměnných
            previouse_key = clean_path[-2]
            new_key = clean_path[-1]

            # 2.5.2 Načtení poslední hodnoty
            current = result
            for key in clean_path[:-2]:
                current = current[key]
            last_value = current[previouse_key]

            # 2.5.3 Přepis hodnoty na dict
            current[previouse_key] = {
                "value": last_value,
                new_key: value
            }
            last_created_key = new_key
            continue

        # 2.6 Vyřízení popožky odkazující na hodnotu
        else:

            # 2.6.1 Definice proměnných
            new_key = clean_path[-1]

            # 2.6.2 Načtení poslední položky
            current = result
            for key in clean_path[:-1]:
                current = current.setdefault(key, {})

            # Zápis nové položky s hodnotou
            current[new_key] = value
            last_created_key = new_key

    # 3. Navrácení slovníku
    return result

>>> src/simplibs/object/mixins/core/state/_inners_property_helpers/properties/helpers/create_inner_atom_property.py
def create_inner_atom_property(
    inner_meta: SimpleMetaType,
    path: tuple[str, ...]
) -> property:
    """
    Vytváří plnohodnotnou property (getter/setter) pro přístup k vnitřnímu slotu.
    Uzamkne název atributu do closure pro maximální čitelnost a rychlost.
    """

    # 1. Definice pomocné funkce pro rychlý přístup k privátnímu slotu instance
    get_inner_instance = attrgetter(*path)

    # 2. Definice Getteru
    def getter(self) -> Any:
        return get_inner_instance(self).value

    # 3. Definice anotace getteru
    getter.__annotations__ = {"return": inner_meta.value_type}

    # 4. Definice Setteru
    def setter(self, value: Any) -> None:

        # 4.1 Získání instance
        inner_instance = get_inner_instance(self)

        # 4.2 Zápis hodnoty a aktivace přepočtu ownera
        # noinspection PyProtectedMember
        inner_instance._root_value_setter(value, recalculate_up=True)

    # 5. Definice anotace setteru
    setter.__annotations__ = {"value": inner_meta.value_type, "return": None}

    # 6. Definice docstringu
    doc_string = (
        f"Hodnota typu `{inner_meta.value_type.__name__}`.\n"
        f"\n"
        f"Getter vrací normalizovanou hodnotu uloženou ve vnitřním slotu `{inner_meta.name_snake}`.\n"
        f"Setter provádí normalizaci hodoty, uložení a spouští aktualizační kaskádu směrem nahoru."
    )

    # 7. Sestavení a navrácení hotové property
    return property(
        fget=getter,
        fset=setter,
        doc=doc_string
    )

>>> src/simplibs/object/mixins/core/state/_inners_property_helpers/properties/helpers/create_inner_composite_property.py
def create_inner_composite_property(
    inner_meta: SimpleMetaType,
    path: tuple[str, ...]
) -> property:
    """
    Vytváří plnohodnotnou property (getter/setter) pro přístup ke kompozitní hodnotě.
    Getter vrací hodnotu kompozice (self.<private>.value).
    Setter je povolen pouze pokud kompozice definuje decompose_value.
    """

    # 1. Definice pomocné funkce pro rychlý přístup k privátnímu slotu instance
    get_inner_instance = attrgetter(*path)

    # 2. Definice Getteru
    def getter(self) -> Any:
        return get_inner_instance(self).value

    # 3. Definice anotace getteru
    getter.__annotations__ = {"return": inner_meta.value_type}

    # 4. Definice Setteru
    def setter(self, value: Any) -> None:

        # 4.1 Získání instance
        inner_instance = get_inner_instance(self)

        # 4.2 Ověření, zda tato kompozice podporuje dekompozici
        if not inner_meta.is_decomposeable:
            raise TypeError(
                f"Kompozice '{inner_meta.class_name}' nepodporuje přímé přiřazení hodnoty, "
                f"protože nemá definovanou uživatelskou metodu decompose_value()."
            )

        # 4.3 Zápis hodnoty a aktivace přepočtu ownera
        # noinspection PyProtectedMember
        inner_instance._root_value_setter(value, recalculate_up=True)

        # 4.4 Rozložení hodnoty a zápis do vnitřních prvků
        # noinspection PyProtectedMember
        inner_instance._recalculate_inners()

    # 5. Definice anotace setteru
    setter.__annotations__ = {"value": inner_meta.value_type, "return": None}

    # 6. Docstring
    doc_string = (
        f"Hodnota typu `{inner_meta.value_type.__name__}`.\n"
        f"\n"
        f"Getter vrací hodnotu kompozice uloženou ve vnitřním slotu `{inner_meta.name_private}`.\n"
        f"Setter je povolen pouze pokud kompozice definuje `decompose_value`, jinak vyvolá chybu."
    )

    # 7. Sestavení property
    return property(
        fget=getter,
        fset=setter,
        doc=doc_string
    )

>>> src/simplibs/object/mixins/core/state/_inners_property_helpers/properties/helpers/create_inner_instance_property.py
def create_inner_instance_property(
    inner_meta: SimpleMetaType,
    path: tuple[str, ...]
) -> property:
    """
    Vytváří read-only property pro přístup k instanci inneru
    (atomu nebo kompozice) přes veřejné API.
    Např. <obj>.motor_instance → <obj>._motor
    """

    # 1. Rychlý přístup k privátnímu slotu
    get_inner_instance = attrgetter(*path)

    # 2. Getter
    def getter(self) -> Any:
        return get_inner_instance(self)

    # 3. Anotace getteru (pokud nemáš instanční typ, necháme Any)
    getter.__annotations__ = {"return": Any}

    # 4. Docstring
    doc_string = (
        f"Instance vnitřního prvku `{inner_meta.name_snake}`.\n"
        f"\n"
        f"Getter vrací instanci atomu nebo kompozice uloženou v privátním slotu "
        f"`{inner_meta.name_private}`.\n"
        f"Tato property je read-only – přiřazení nové instance není povoleno."
    )

    # 5. Read-only property (bez setteru)
    return property(
        fget=getter,
        doc=doc_string,
    )

>>> src/simplibs/object/mixins/core/state/_inners_property_helpers/properties/create_properties_for_inner.py
def create_properties_for_inner(
    inner_meta: SimpleMetaType,
    path: tuple[str, ...] = ()
) -> dict:
    """Generuje slovník přístupových vlastností (properties) pro všechny přímé inners."""

    # 1. Definice prázdného slovníku
    property_dict = {}

    # 2 Vtvoření proměnných
    name_snake = inner_meta.name_snake
    instance_path = path + (inner_meta.name_private,)

    # 3. Vytvoření property pro konstantu
    if inner_meta.is_constant:
        param_property = create_inner_atom_property(inner_meta, instance_path)

    # 4. Vytvoření property pro kompozici
    else:
        param_property = create_inner_composite_property(inner_meta, instance_path)

    # 5. Vytvoření property pro přístup k instanci
    instance_property = create_inner_instance_property(inner_meta, instance_path)

    # 6. Přidání property do slovníku
    property_dict[name_snake] = param_property
    property_dict[f"{name_snake}_instance"] = instance_property

    # 7. Navrácení slovníku s property
    return property_dict

>>> src/simplibs/object/mixins/core/state/_inners_property_helpers/_collect_nested_inner_properties.py
def _collect_nested_inner_properties(
    meta: SimpleMetaType,
    path: tuple[str, ...],
    result: dict
) -> None:
    """
    Rekurzivně projde všechny vnitřní (nested) inners
    a přidá jejich property do slovníku `result`.
    """

    # 1. Průchod skrze inners
    for inner in meta.inners:

        # 1.1 Definice proměných
        inner_meta = inner.meta
        new_path = path + (inner_meta.name_private,)

        # 1.2 Vytvoření porperty (pro konstantu i kompozici)
        props = create_properties_for_inner(inner_meta, new_path)
        result.update(props)

        # 1.3 Rekurzivní zpracování pro kompozice
        if not inner_meta.is_constant:
            _collect_nested_inner_properties(inner_meta, new_path, result)

>>> src/simplibs/object/mixins/core/state/_inners_property_helpers/collect_all_nested_properties.py
def collect_all_nested_properties(
    meta: SimpleMetaType
) -> dict:
    """
    Vrátí slovník property pro všechny nested inners.
    Přímé inners se ignorují (ty už property mají).
    """

    # 1. Definice množiny pro property
    result = {}

    # 2. Průchod skrze vlastní inners
    for inner in meta.inners:

        # 2.1 Vytažení meta
        inner_meta = inner.meta

        # 2.2 Kontrola zda jde o kompozici
        if not inner_meta.is_constant:

            # 2.2.1 Vytvoření tuple pro cestu
            path = (inner_meta.name_private,)

            # 2.2.2 Rekurzivní zběr property pro vnitřní prvky
            _collect_nested_inner_properties(inner_meta, path, result)

    # 3. Navrácení množiny pro property
    return result

>>> src/simplibs/object/mixins/core/state/DefaultState.py
class DefaultState(SimpleMixin):
    """
    Mixin, který instanci poskytne:
    - uložený výchozí stav (_default_state)
    - metody clone(), reset(), copy_from(), new_default_instance()
    """

    __slots__ = ("_default_state",)

    # ---------------------------------------------------------
    # 1) Hook volaný z create_instance → doplní _default_state
    # ---------------------------------------------------------
    @staticmethod
    def __extend_instance_class__(instance_cls):
        """
        Vytvoří a uloží výchozí instanci dané instanční třídy.
        """

        # 1. Vytvoření mapovacích slovníků
        if not hasattr(instance_cls, "_constants_map") or not hasattr(instance_cls, "_composites_map"):
            constants_map, composites_map = build_recursive_maps(instance_cls.meta)
            instance_cls._constants_map = constants_map
            instance_cls._composites_map = composites_map

        # 2. Přidání defaultní instance
        if not hasattr(instance_cls, "_default_state"):
            default = object.__new__(instance_cls)
            default.__init__()
            instance_cls._default_state = default

        # 3. Navrácení pozměněné třídy
        return instance_cls

    # ---------------------------------------------------------
    # 2) Vytvoří novou instanci se stejným stavem jako self
    # ---------------------------------------------------------
    def clone(self: SimpleInstanceType):
        """
        Vytvoří novou instanci se stejným stavem jako tato instance.
        """
        new_instance = self._default_state.clone()
        copy_instance_values(self, new_instance)
        return new_instance

    # ---------------------------------------------------------
    # 3) Resetuje instanci do výchozího stavu
    # ---------------------------------------------------------
    def reset(self: SimpleInstanceType):
        """
        Resetuje instanci do výchozího stavu (_default_state).
        """
        copy_instance_values(self._default_state, self)

    # ---------------------------------------------------------
    # 4) Vytvoří novou instanci výchozího stavu
    # ---------------------------------------------------------
    def new_default_instance(self):
        """
        Vrátí novou instanci, která odpovídá výchozímu stavu.
        """
        return self._default_state.clone()

>>> src/simplibs/object/mixins/core/state/DirtyTrackingMixin.py
class DirtyTrackingMixin(SimpleMixin):
    """
    Moderní dirty tracking založený na snapshotu.
    Funguje pro atomy, composites i nested struktury.
    """
    __slots__ = ("_clean_snapshot",)

    def init_mixins(self):
        super().init_mixins()
        # Uložíme počáteční snapshot jako "čistý"
        object.__setattr__(self, "_clean_snapshot", build_snapshot(self))

    # ---------------------------------------------------------
    # Dirty flag
    # ---------------------------------------------------------
    @property
    def is_dirty(self) -> bool:
        """True pokud se aktuální stav liší od čistého snapshotu."""
        current = build_snapshot(self)
        return current != self._clean_snapshot

    # ---------------------------------------------------------
    # Dirty paths (diff)
    # ---------------------------------------------------------
    @property
    def dirty_paths(self):
        """Vrací tuple změněných cest (path, old_value, new_value)."""
        current = build_snapshot(self)
        return compare_snapshots(self._clean_snapshot, current, leaves_only=True)

    # ---------------------------------------------------------
    # Reset
    # ---------------------------------------------------------
    def reset(self):
        """Vrátí objekt do čistého snapshotu."""
        restore_snapshot(self, self._clean_snapshot)

    # ---------------------------------------------------------
    # Mark clean
    # ---------------------------------------------------------
    def mark_clean(self):
        """Označí aktuální stav jako nový čistý snapshot."""
        object.__setattr__(self, "_clean_snapshot", build_snapshot(self))

>>> src/simplibs/object/mixins/core/state/History.py
class HistoryMixin(SimpleMixin):
    """
    Ukládá kompletní snapshoty stavu instance a umožňuje jejich obnovu.
    Snapshot je interní formát: name_snake → (path_tuple, value).
    """

    __slots__ = ("_history", "_history_index", "_history_limit")

    # ---------------------------------------------------------
    # Inicializace mixinu
    # ---------------------------------------------------------
    def init_mixins(self):
        super().init_mixins()
        # Inicializace úložiště historie
        object.__setattr__(self, "_history", [])
        object.__setattr__(self, "_history_index", None)
        object.__setattr__(self, "_history_limit", None)
        # Uložení počátečního stavu
        self.record_state()

    @property
    def history(self):
        return tuple(self._history)

    @property
    def history_dict(self):
        return {ts: snapshot for ts, snapshot in self._history}

    @property
    def history_index(self):
        return self._history_index

    @property
    def history_limit(self):
        return self._history_limit

    @history_limit.setter
    def history_limit(self: Self, value: int) -> None:
        if not isinstance(value, int) or value < 1:  # ❌ bylo 'and', má být 'or'
            raise ValueError(f"history_limit must be a positive integer, got {value!r}")

        # Ořezání pokud je aktuální historie delší než nový limit
        if len(self._history) > value:
            del self._history[:len(self._history) - value]
            self._history_index = len(self._history) - 1

        self._history_limit = value


    # ---------------------------------------------------------
    # Vytvoření snapshotu
    # ---------------------------------------------------------
    def record_state(self):
        """Vytvoří snapshot aktuálního stavu a uloží ho do historie."""

        # 1. Vytvoření timestamp a snapshotu
        timestamp = datetime.now()
        snapshot = build_snapshot(self)

        # 2. Kontrola zda je historie v rámci limitu (pokud je nastaven)
        if self._history_limit and len(self._history) >= self._history_limit:
            self._history.pop(0)

        # 3. Zápis do historie a indexu
        self._history.append((timestamp, snapshot))
        self._history_index = len(self._history)-1

        # 4. Navrácení timestamp
        return timestamp


    # ---------------------------------------------------------
    # Undo & Redo  & Gotu & Restore
    # ---------------------------------------------------------

    def undo(self):
        """Vrátí stav instance o jeden snapshot zpět."""

        # 1. Kontrola zda je kam jít
        if self._history_index <= 0:
            return False

        # 2. Změna indexu
        self._history_index -= 1

        # 3. Získání a obnovení snapshotu
        _, snapshot = self._history[self._history_index]
        restore_snapshot(self, snapshot)
        return True

    def redo(self):
        """Vrátí stav instance o jeden snapshot dopředu."""

        # 1. Kontrola zda je kam jít
        if self._history_index >= len(self._history) - 1:
            return False

        # 2. Změna indexu
        self._history_index += 1

        # 3. Získání a obnovení snapshotu
        _, snapshot = self._history[self._history_index]
        restore_snapshot(self, snapshot)
        return True

    def go_to_last(self):
        """Obnoví poslední snapshot v historii."""

        # 1. Změna indexu
        self._history_index = len(self._history) - 1

        # 2. Získání a obnovení snapshotu
        _, snapshot = self._history[self._history_index]
        restore_snapshot(self, snapshot)

    def go_to_index(self, index: int):
        """Obnoví snapshot na daném indexu."""

        # 1. Kontrola zda index existuje
        if not (0 <= index < len(self._history)):
            raise IndexError(f"Snapshot index {index} is out of range (history length: {len(self._history)})")

        # 2. Změna indexu
        self._history_index = index

        # 3. Získání a obnovení snapshotu
        _, snapshot = self._history[self._history_index]
        restore_snapshot(self, snapshot)

    def go_to_timestamp(self, timestamp: datetime):
        """Obnoví snapshot pro daný timestamp."""

        # 1. Vyhledání indexu
        for i, (ts, snapshot) in enumerate(self._history):
            if ts == timestamp:
                # 2. Změna indexu a obnovení stavu
                self._history_index = i
                restore_snapshot(self, snapshot)
                return

        # 3. Timestamp nenalezen
        raise KeyError(f"No snapshot found for timestamp {timestamp!r}")

    # ---------------------------------------------------------
    # Diff mezi snapshoty
    # ---------------------------------------------------------
    # Na instanci — history se doplní automaticky
    def diff(self, a, b, leaves_only=False):
        snap1 = resolve_snapshot(a, self._history)
        snap2 = resolve_snapshot(b, self._history)
        return compare_snapshots(snap1, snap2, leaves_only=leaves_only)

    # Statická — pro přímé snapshoty, history není potřeba
    @staticmethod
    def diff_snapshots(a: tuple, b: tuple, leaves_only: bool = False):
        return compare_snapshots(a, b, leaves_only=leaves_only)


    # ---------------------------------------------------------
    # Export historie (bez interních adres)
    # ---------------------------------------------------------

    def export_history(self):
        return list(self._history)

    def import_history(self, new_history):

        # 1. Vytvoření zálohy existující
        backup_history = self._history

        # 2. Pokus o přepsání historie
        try:
            self._history = list(new_history)
            self.go_to_last()
            self.history_limit = self._history_limit

        # 3. Pokud selže - obnova dat a vyvolání výjimky
        except Exception as e:
            self._history = backup_history
            self.go_to_last()
            raise ...

    def export_history_to_dict(self):
        """
        Exportuje historii do čitelného formátu:
            timestamp → to_dict() stav
        """
        return {ts: snapshot_to_dict(snapshot) for ts, snapshot in self._history}

    def import_history_from_dict(self, history_dict):
        """
        Exportuje historii do čitelného formátu:
            timestamp → to_dict() stav
        """

        # 1. Získání listu ze slovníku
        history_list = [
            (ts, dict_to_snapshot(snapshot_dict))
            for ts, snapshot_dict in history_dict.items()
        ]

        # 2. Přepis historie
        self.import_history(history_list)

>>> src/simplibs/object/mixins/core/state/Permission.py
class PermissionMixin(SimpleMixin):
    """
    Read-only režim — zamykání proti změnám.

    Příklad:
        obj.lock()
        obj.value = 10  # → ValueError
    """

    __slots__ = ("_locked",)

    def init_mixins(self):
        super().init_mixins()
        object.__setattr__(self, "_locked", False)

    @property
    def is_locked(self) -> bool:
        return self._locked

    def lock(self):
        object.__setattr__(self, "_locked", True)

    def unlock(self):
        object.__setattr__(self, "_locked", False)

    # HOOK: volá se PŘED změnou hodnoty
    def _before_update(self, new_value):
        if self._locked:
            raise ValueError(f"{self.__class__.__name__} is locked.")
        super()._before_update(new_value)

>>> src/simplibs/object/mixins/only_for_atoms/ValueStepper.py
class ValueStepperMixin(SimpleMixin):
    __slots__ = ("_value_step", "_limit_up", "_limit_down")

    def init_mixins(self):
        super().init_mixins()

        # Ověření typu
        if self.meta.value_type not in (int, float):
            raise TypeError(
                f"ValueStepperMixin can only be used on numeric types, "
                f"got {self.meta.value_type}"
            )

        # Výchozí step = defaultní hodnota
        default = getattr(self, "_default_state", None)
        default_value = default._value if default else self.value

        object.__setattr__(self, "_value_step", default_value)
        object.__setattr__(self, "_limit_up", None)
        object.__setattr__(self, "_limit_down", None)

    # -----------------------------
    # Step konfigurace
    # -----------------------------
    @property
    def value_step(self):
        return self._value_step

    @value_step.setter
    def value_step(self, step):
        if not isinstance(step, (int, float)):
            raise TypeError("value_step must be numeric")
        object.__setattr__(self, "_value_step", step)

    # -----------------------------
    # Limity
    # -----------------------------
    def set_up_limit(self, limit, action=None):
        object.__setattr__(self, "_limit_up", (limit, action))

    def set_down_limit(self, limit, action=None):
        object.__setattr__(self, "_limit_down", (limit, action))

    # -----------------------------
    # Stepování
    # -----------------------------
    def value_up(self):
        new_value = self.value + self._value_step
        self._apply_limits(new_value)
        self.value = new_value

    def value_down(self):
        new_value = self.value - self._value_step
        self._apply_limits(new_value)
        self.value = new_value

    # -----------------------------
    # Limity
    # -----------------------------
    def _apply_limits(self, new_value):
        if self._limit_up and new_value > self._limit_up[0]:
            limit, action = self._limit_up
            if action:
                action(self)
            new_value = limit

        if self._limit_down and new_value < self._limit_down[0]:
            limit, action = self._limit_down
            if action:
                action(self)
            new_value = limit

        return new_value

>>> src/simplibs/object/settings/SimpleSettings.py
class SimpleSettings:

    # Nastavení logeru
    logger: Callable[[type, Any], None] | None = None

>>> src/simplibs/object/SimpleBase.py
class SimpleBase(metaclass=SimpleMeta):
    """
    Abstraktní kořenová třída pro všechny prvky systému Simple.

    Tato třída definuje společnou identitu pro konstanty i kompozitní objekty.
    Zajišťuje napojení na metatřídu a poskytuje jednotné rozhraní pro
    přístup k metadatům.
    """

    # ===================================
    # ZÁKLADNÍ ROZHRANÍ A NAPOJENÍ METADAT
    # (rozhraní společné všem potomkům)
    # ===================================

    #--- Definice __slots__ pro lepší výkon ---#
    # (každý potomek musí slots definovat jinak příjde o tuto výhodu)
    __slots__ = ()

    #--- Definice slotu pro metadata ---#
    # (pro základní třídy nastavuje hodnotu UNSET - vypočítává se pouze pro definiční třídy)
    __metadata__: SimpleMetaType = UNSET


    # ===================================
    # VNITŘNÍ ROZHRANÍ ZÁKLANÍ TŘÍDY
    # (definuje uživatel zakládající třídu)
    # ===================================

    #--- Hook pro případný loger ---#
    # (obsažen na konci každé vnější metody s přístupem k jejímu výsledku)
    @classmethod
    def _log_outcome(cls, outcome: Any) -> None:
        """
        Třídní hook pro případný loger výsledků metod.
        Volá se z třídních metod (validate, normalize atd.).
        """
        if SimpleSettings.logger:
            SimpleSettings.logger(cls, outcome)

>>> src/simplibs/object/SimpleConstant.py
class SimpleConstant(SimpleBase):
    """
    Základní definiční třída pro definic konstant

    Vychází z SimpleBase tířdy.
    Slouží jako základ pro SimpleObject třídu.
    """

    # ===================================
    # VNITŘNÍ ROZHRANÍ KONSTANTNÍ TŘÍDY
    # (definuje uživatel zakládající třídu)
    # ===================================

    #--- Typová anotace hodnoty kterou třída reprezentuje ---#
    # (povinná hodnota pro konstantu i objekt)
    _type: type = UNSET

    #--- Defaultní hodnota ---#
    # (zadává se pouze u konstanty, u objektu se dopočítává)
    _default: Any = UNSET

    #--- Doplňková logika validace ---#
    # (zadává se pro rozšíření základní validace dle typu)
    @classmethod
    def _validate(cls, value: Any, *, return_bool: bool = False) -> bool | Exception:
        """Nepovinná doplňková validace."""
        return True

    # ===================================
    # VNĚJŠÍ ROZHRANÍ KONSTANTNÍ TŘÍDY
    # (metody jsou přidány při zpracování metadat)
    # ===================================

    @classmethod
    def validate_type(cls, value: Any, *, return_bool: bool = False) -> bool:
        """Provede deterministickou validaci typu na základě metadat třídy."""
        return validate_type(cls, value, return_bool=return_bool)

    @classmethod
    def validate(cls, value: Any, *, return_bool: bool = False) -> bool:
        """Provede validaci typu a validaci skrze upřesňující validační metodu."""
        return validate(cls, value, return_bool=return_bool)

    @classmethod
    def is_valid(cls, value: Any) -> bool:
        """Vrátí True, pokud hodnota projde kompletní validací, jinak False."""
        return cls.validate(value, return_bool=True)

    @classmethod
    def normalize(cls, value: Any, *, process_none: bool = False) -> Any:
        """Normalizuje hodnotu. Vrací hodnotu nebo vyvolá SimpleLogicError."""
        return normalize(cls, value, process_none=process_none)

    @classmethod
    def bool_or_raise_validate_error(cls, value: Any, problem: str, *, return_bool: bool = False) -> bool:
        """Pomocná metoda pro použití uvnitř uživatelských '_validate'. (Na instanci je odebrána.)"""
        return bool_or_raise_validate_error(cls, value, problem, return_bool=return_bool)

    # ===================================
    # METOD Y A ATRIBUTY ZDĚDĚNÉ Z PŘEDKŮ
    # (předkové: SimpleBase)
    # ===================================

    #--- Hook pro případný loger ---#
    # _log_outcome(cls, outcome: Any) -> None

>>> src/simplibs/object/SimpleObject.py
class SimpleObject(SimpleConstant):
    """
    Základní definiční třída pro definic kompozic.

    Vychází z SimpleConstant a SimpeBase tířdy.
    Slouží jako základ pro vytváření kompozitních objektů.
    """

    # ===================================
    # VNITŘNÍ ROZHRANÍ KOMPOZITNÍ TŘÍDY
    # (definuje uživatel zakládající třídu)
    # ===================================

    #--- Typová anotace hodnoty kterou třída reprezentuje ---#
    # (povinná hodnota pro konstantu i objekt)
    _type: type = UNSET

    #--- Vnitřní prvky třídy ---#
    # (povinný atribut - musí odpovídat paramerů _logic)
    _inners: tuple[SimpleClassType, ...] = UNSET

    #--- Hlavní metoda pro výpočet hodnoty ---#
    # (povinný prvek - vypočítává default)
    @classmethod
    def _logic(cls, *args, **kwargs) -> Any:
        """Povinná pro kompozici, vrací default pro atomy."""
        return UNSET

    #--- Doplňková metoda pro rozložení hlavní hodnoty ---#
    # (zadává se pouze je-li rozklad potřeba)
    @classmethod
    def _decompose(cls, value: Any) -> Any:
        """Nepovinná, vrací None, pokud rozklad není podporován."""
        return UNSET

    #--- Doplňková logika validace ---#
    # (zadává se pro rozšíření základní validace dle typu)
    @classmethod
    def _validate(cls, value: Any, *, return_bool: bool = False) -> bool | Exception:
        """Nepovinná doplňková validace."""
        return True


    # ===================================
    # VNĚJŠÍ ROZHRANÍ KOMPOZITNÍ TŘÍDY
    # (metody jsou přidány při zpracování metadat)
    # ===================================

    @classmethod
    def calculate_value(cls: LogicSignature[P, R], *args: P.args, **kwargs: P.kwargs) -> R:
        """
        Dynamicky spočítá hodnotu kompozice.
        Díky ParamSpec PyCharm nahlédne do uživatelské metody '_logic'
        a začne vývojáři našeptávat JEJÍ konkrétní parametry!
        """

        # 1. Zpracování předaných parametrů
        params_dict = process_calculate_value_params(cls, *args, **kwargs)

        # 2. Výpočet hodnoty
        outcome = cls.meta.logic(cls, **params_dict)

        # 3. Případné logování (je-li nastaveno)
        cls._log_outcome(outcome)

        # 4. Navrácení výsledku
        return outcome

    @classmethod
    def decompose_value(cls, value: Any) -> Any:
        """Rozloží hlavní hodnotu na vnitřní komponenty."""

        # 1. Validace předané hodnoty
        cls.validate(value)

        # 2. Rozložení předané hodnoty
        # noinspection PyUnresolvedReferences
        outcome = cls.meta.decompose(cls, value)

        # 3. Případné logování (je-li nastaveno)
        cls._log_outcome(outcome)

        # 4. Navrácení výsledku
        return outcome

    # ===================================
    # METOD Y A ATRIBUTY ZDĚDĚNÉ Z PŘEDKŮ
    # (předkové: SimpleConstant, SimpleBase)
    # ===================================

    #--- Defaultní hodnota která se u kompozice dopočítává ---#
    # _default: Any = UNSET

    #--- Základní validace dle typu ---#
    # validate_type(cls, value: Any, *, return_bool: bool = False) -> bool

    #--- Kompletní validace dle typu a doplňkové validační logiky ---#
    # validate(cls, value: Any, *, return_bool: bool = False) -> bool

    #--- Validace nevyvolávající výjimku, ale vracející pouze bool ---#
    # is_valid(cls, value: Any) -> bool

    #--- Normalizační meotda - provede validaci a navrátí hodnotu ---#
    # normalize(cls, value: Any, *, process_none: bool = False) -> Any

    #--- Hook pro případný loger ---#
    # _log_outcome(cls, outcome: Any) -> None

