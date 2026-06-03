Ahojky :-)

Tady je tvůj text z konce minulého vlákna, kde jsem tě pořžádal aby jsi mi ho připravil jako úvod do tohoto nového kdy tedy máme za sebou jednu další objemnou část která se rozprostřela do mnohaddenního vlákna které přerostlo samo sebe a tedy ideální chvíle na to s novou čátí začít s vnovým vláknem a s čistou pamětí, tak aby jsi mi dokonale dokázal hlídat záda  a pomáhat tak m kde to nejvíce potřebuji.

A tedy v tomto textu mluvíč o tom sco budujeme celkem velkorise a mile, tak uvidíme jestli i samotný kod bude mít tyto kovality :-)

A tedy nejprve ti pošlu ten tvůj text, aby jsi byl rychle v obraze a po něm připojím strukturu, kde jediná nerozklikaná část je pro mixiny kterým se teprve budeme jvěnovat.

A pak v pár dalších dotazech ti postupně nahraji všechny kody tak jak máme - tě se zatím nebudeme věnovat - jen tedy kdyby jsi si všimnul nějaké zásadní chyby - ale jinak jde jen o to aby jsi je měl v paměti a mohl jsi mi strukturovat odpovědi na základě těchto předaných kodu a tedy v odpovědi mi prosím nikdy neodhaduj - ale raději se doptej, než aby jsi pjen předpokládl jak to asi bude a podle toho vytvářel odpověď - na projetku děláme už celkem dlouho a nyní ladíme jemné detaily azde tedy pro odhady není vůbec místo :-)

A tedy vítám ětě do nového vlákna a těším se na spolupráci a jdeme na to :-)

Zd eje tedy ten tvůj text:

Tady je komplexní shrnutí našeho projektu, stavu architektury a principů naší spolupráce. Tento text můžeš vzít a vložit ho na začátek nového vlákna jako dokonalý manifest, který okamžitě definuje celé naše prostředí.
Manifest projektu Simple a principů naší spolupráce
1. O co v projektu jde (Vize a Cíl)
Tvoříme pokročilý high-performance Python framework (v balíčku simplibs.object), který přináší revoluci do způsobu, jakým se v Pythonu definují, validují a propojují datové struktury (tzv. Kompozice a Atomy).
Cílem je poskytnout vývojářům maximální rychlost v runtimu (využívající C-level optimalizace Pythonu jako C-arrays přes tuple, __slots__ bez nechtěných __dict__ a vynechávání redundancí), ale zároveň nekompromisní komfort při psaní kódu (DX – Developer Experience). Framework dokáže analyzovat kód už při importu (bootu aplikace), provést hluboký „rentgen“ struktur a v runtimu pak díky statickému typování (využití ParamSpec, TypeVar, Protocol) inteligentně našeptávat parametry v IDE, jako by šlo o nativní Python kód.
2. Co už je hotové (Architektonický stav)
Na základě naší dosavadní práce a aktuální struktury adresářů máme hotový pevný skelet systému:
Metadata Engine: Máme navrženou robustní imutabilní strukturu metadat (SimpleBaseMetadata, SimpleObjectMetadata, SimpleConstantMetadata), která drží stav deklaračních tříd izolovaně a bezpečně ve slotech.
Init Processors: Modulární systém inicializačních procesorů rozdělený podle domén (names, attributes, methods), který se spouští při bootu. Každý procesor má své atomické validace, které kontrolují jména (ASCII, identifkátory), typy, unie, vnitřní vazby (inners) a kolize jmen s vlastníkem.
Verifikátory metod: Pokročilá analýza uživatelské byznys logiky (_logic), která kontroluje signatury metod, počty argumentů, typové anotace a výchozí hodnoty.
Instance Builders: Mechanismus, který na základě ověřených metadat dokáže za běhu dynamicky skládat výsledné runtime objekty (type(...)), generovat jim properties pro vnitřní prvky a zajišťovat optimální přepočty hodnot.
Optimalizace Volání (The Zen of Performance): Vyřešili jsme klíčové dilema mezi *args a kwargs. Hlavní uživatelská metoda calculate_value poskytuje plný komfort a bezpečí. Pro ultra rychlé produkční pipelines (Fast Path) obcházející validace a využívající přímé mapování ukazatelů v C (bez hashování) framework odkazuje pokročilé uživatele přímo na interní výpočetní jádro meta.logic.
3. Co nás čeká nyní
Vstupujeme do fáze rozšiřování vlastností výsledných instancí. Naším aktuálním cílem je navrhnout a implementovat základní třídu pro mixiny (SimpleMixin).
Chceme přenést náš přísný validační engine i na zrod těchto mixinů (přes __init_subclass__), abychom už při importu garantovali jejich anatomii (přítomnost __slots__, kontrolu chráněných názvů, kompatibilitu s konstantami/atomy a správnost reaktivní inicializační kotvy init_mixins), než je systém dynamicky vpustí do MRO (Method Resolution Order) výsledné instance.
4. Kodex naší spolupráce (Náš Zen)
Tento projekt nestavíme ve spěchu. Naše spolupráce je definována specifickým rytmem, na kterém si zakládáme:
Kdo vede a kdo kryje záda: Ty jsi hlavní architekt. Ty držíš v hlavě celou komplexní 3D strukturu kódu a vizionářsky ji skládáš dohromady. Já (AI) jsem tvůj elitní konzultant, oponent a auditor. Mojí úlohou není psát kód za tebe nebo ti diktovat, co máš dělat. Mojí úlohou je hlídat ti záda, zpochybňovat slepé uličky, ověřovat konzistenci tvých myšlenek s Python runtimem a poskytovat ti čisté, chladné inženýrské analýzy.
Zákaz našeptávání: Já jako AI mám striktně vypnutý jakýkoliv režim „našeptávače dalších kroků“. Nikdy nepředbíhám, nenutím ti další postup a neříkám, co máš psát dál. Reaguji výhradně na to, na co se mě v danou chvíli ptáš.
Žádné domněnky: Vše, co jako AI tvrdím, musí být podložené reálným kódem, který jsi mi nasdílel. Pokud mi k nějaké analýze chybí kontext nebo přesná podoba tvé implementace, nedomýšlím si ji – namísto toho se zastavím a požádám tě o doplnění konkrétního souboru.
Cesta je cíl: Důležitější než rychlost je absolutní čistota, hloubka promyšlení a nekompromisní kvalita návrhu. Postupujeme pomalu, krok za krokem, v naprostém klidu a soustředění. Nádech, výdech.
Tento text je připraven k přenesení. Až otevřeš nové vlákno, vlož ho tam spolu s aktuální strukturou a vybranými kódy. Budu čekat na tvůj povel k zahájení konzultace o SimpleMixin.



A tedy zde je dosavadní struktura:

src/simplibs/object
src/simplibs/object/_metadata
src/simplibs/object/_metadata/constants
src/simplibs/object/_metadata/constants/__init__.py
src/simplibs/object/_metadata/constants/BASE_CLASS_NAMES.py
src/simplibs/object/_metadata/constants/INDENT.py
src/simplibs/object/_metadata/init_processors
src/simplibs/object/_metadata/init_processors/attributes
src/simplibs/object/_metadata/init_processors/attributes/default
src/simplibs/object/_metadata/init_processors/attributes/default/validations
src/simplibs/object/_metadata/init_processors/attributes/default/validations/_exceptions_helpers
src/simplibs/object/_metadata/init_processors/attributes/default/validations/_exceptions_helpers/__init__.py
src/simplibs/object/_metadata/init_processors/attributes/default/validations/_exceptions_helpers/exception_info_for_default.py
src/simplibs/object/_metadata/init_processors/attributes/default/validations/composition
src/simplibs/object/_metadata/init_processors/attributes/default/validations/composition/__init__.py
src/simplibs/object/_metadata/init_processors/attributes/default/validations/composition/raise_default_is_defined_in_composition.py
src/simplibs/object/_metadata/init_processors/attributes/default/validations/constant
src/simplibs/object/_metadata/init_processors/attributes/default/validations/constant/__init__.py
src/simplibs/object/_metadata/init_processors/attributes/default/validations/constant/validate_default_is_defined.py
src/simplibs/object/_metadata/init_processors/attributes/default/validations/constant/validate_default_matches_annotation.py
src/simplibs/object/_metadata/init_processors/attributes/default/validations/__init__.py
src/simplibs/object/_metadata/init_processors/attributes/default/__init__.py
src/simplibs/object/_metadata/init_processors/attributes/default/process_default_for_constant.py
src/simplibs/object/_metadata/init_processors/attributes/inners
src/simplibs/object/_metadata/init_processors/attributes/inners/validations
src/simplibs/object/_metadata/init_processors/attributes/inners/validations/_exceptions_helpers
src/simplibs/object/_metadata/init_processors/attributes/inners/validations/_exceptions_helpers/__init__.py
src/simplibs/object/_metadata/init_processors/attributes/inners/validations/_exceptions_helpers/exception_info_for_inners.py
src/simplibs/object/_metadata/init_processors/attributes/inners/validations/inner
src/simplibs/object/_metadata/init_processors/attributes/inners/validations/inner/__init__.py
src/simplibs/object/_metadata/init_processors/attributes/inners/validations/inner/validate_inner_is_class.py
src/simplibs/object/_metadata/init_processors/attributes/inners/validations/inner/validate_inner_is_not_simple_class.py
src/simplibs/object/_metadata/init_processors/attributes/inners/validations/inner/validate_inner_is_simple_subclass.py
src/simplibs/object/_metadata/init_processors/attributes/inners/validations/inners
src/simplibs/object/_metadata/init_processors/attributes/inners/validations/inners/__init__.py
src/simplibs/object/_metadata/init_processors/attributes/inners/validations/inners/validate_inners_is_defined.py
src/simplibs/object/_metadata/init_processors/attributes/inners/validations/inners/validate_inners_is_not_empty.py
src/simplibs/object/_metadata/init_processors/attributes/inners/validations/inners/validate_inners_is_tuple.py
src/simplibs/object/_metadata/init_processors/attributes/inners/validations/name_collisions
src/simplibs/object/_metadata/init_processors/attributes/inners/validations/name_collisions/utils
src/simplibs/object/_metadata/init_processors/attributes/inners/validations/name_collisions/utils/__init__.py
src/simplibs/object/_metadata/init_processors/attributes/inners/validations/name_collisions/utils/get_collision_path.py
src/simplibs/object/_metadata/init_processors/attributes/inners/validations/name_collisions/__init__.py
src/simplibs/object/_metadata/init_processors/attributes/inners/validations/name_collisions/validate_collision_within_inners.py
src/simplibs/object/_metadata/init_processors/attributes/inners/validations/name_collisions/validate_if_collision_with_owner_class.py
src/simplibs/object/_metadata/init_processors/attributes/inners/validations/__init__.py
src/simplibs/object/_metadata/init_processors/attributes/inners/__init__.py
src/simplibs/object/_metadata/init_processors/attributes/inners/process_inners.py
src/simplibs/object/_metadata/init_processors/attributes/type
src/simplibs/object/_metadata/init_processors/attributes/type/validations
src/simplibs/object/_metadata/init_processors/attributes/type/validations/_exceptions_helpers
src/simplibs/object/_metadata/init_processors/attributes/type/validations/_exceptions_helpers/__init__.py
src/simplibs/object/_metadata/init_processors/attributes/type/validations/_exceptions_helpers/exception_info_for_type.py
src/simplibs/object/_metadata/init_processors/attributes/type/validations/tuple
src/simplibs/object/_metadata/init_processors/attributes/type/validations/tuple/__init__.py
src/simplibs/object/_metadata/init_processors/attributes/type/validations/tuple/validate_type_from_tuple_is_not_none.py
src/simplibs/object/_metadata/init_processors/attributes/type/validations/tuple/validate_type_tuple_is_not_nested.py
src/simplibs/object/_metadata/init_processors/attributes/type/validations/type
src/simplibs/object/_metadata/init_processors/attributes/type/validations/type/__init__.py
src/simplibs/object/_metadata/init_processors/attributes/type/validations/type/raise_validate_type_is_not_valid.py
src/simplibs/object/_metadata/init_processors/attributes/type/validations/type/validate_type_is_defined.py
src/simplibs/object/_metadata/init_processors/attributes/type/validations/type/validate_type_is_not_empty.py
src/simplibs/object/_metadata/init_processors/attributes/type/validations/type/validate_type_is_not_none.py
src/simplibs/object/_metadata/init_processors/attributes/type/validations/union
src/simplibs/object/_metadata/init_processors/attributes/type/validations/union/__init__.py
src/simplibs/object/_metadata/init_processors/attributes/type/validations/union/raise_union_type_contain_none.py
src/simplibs/object/_metadata/init_processors/attributes/type/validations/__init__.py
src/simplibs/object/_metadata/init_processors/attributes/type/__init__.py
src/simplibs/object/_metadata/init_processors/attributes/type/process_type.py
src/simplibs/object/_metadata/init_processors/attributes/__init__.py
src/simplibs/object/_metadata/init_processors/methods
src/simplibs/object/_metadata/init_processors/methods/verifiers
src/simplibs/object/_metadata/init_processors/methods/verifiers/_exceptions_helpers
src/simplibs/object/_metadata/init_processors/methods/verifiers/_exceptions_helpers/__init__.py
src/simplibs/object/_metadata/init_processors/methods/verifiers/_exceptions_helpers/exception_context_for_classmethod.py
src/simplibs/object/_metadata/init_processors/methods/verifiers/_exceptions_helpers/exception_info_for_classmethod.py
src/simplibs/object/_metadata/init_processors/methods/verifiers/annotations_and_defaults
src/simplibs/object/_metadata/init_processors/methods/verifiers/annotations_and_defaults/validations
src/simplibs/object/_metadata/init_processors/methods/verifiers/annotations_and_defaults/validations/utils
src/simplibs/object/_metadata/init_processors/methods/verifiers/annotations_and_defaults/validations/utils/__init__.py
src/simplibs/object/_metadata/init_processors/methods/verifiers/annotations_and_defaults/validations/utils/convert_annotation_to_type_set.py
src/simplibs/object/_metadata/init_processors/methods/verifiers/annotations_and_defaults/validations/__init__.py
src/simplibs/object/_metadata/init_processors/methods/verifiers/annotations_and_defaults/validations/validate_annotations.py
src/simplibs/object/_metadata/init_processors/methods/verifiers/annotations_and_defaults/validations/validate_args_defaults.py
src/simplibs/object/_metadata/init_processors/methods/verifiers/annotations_and_defaults/validations/validate_kwargs_defaults.py
src/simplibs/object/_metadata/init_processors/methods/verifiers/annotations_and_defaults/__init__.py
src/simplibs/object/_metadata/init_processors/methods/verifiers/annotations_and_defaults/verify_annotations_and_defaults.py
src/simplibs/object/_metadata/init_processors/methods/verifiers/calculation
src/simplibs/object/_metadata/init_processors/methods/verifiers/calculation/decompose_method
src/simplibs/object/_metadata/init_processors/methods/verifiers/calculation/decompose_method/validations
src/simplibs/object/_metadata/init_processors/methods/verifiers/calculation/decompose_method/validations/__init__.py
src/simplibs/object/_metadata/init_processors/methods/verifiers/calculation/decompose_method/validations/raise_decompose_unvalide_outcome_length.py
src/simplibs/object/_metadata/init_processors/methods/verifiers/calculation/decompose_method/validations/validate_decompose_unvalide_item_type.py
src/simplibs/object/_metadata/init_processors/methods/verifiers/calculation/decompose_method/validations/validate_decompose_unvalide_item_value.py
src/simplibs/object/_metadata/init_processors/methods/verifiers/calculation/decompose_method/__init__.py
src/simplibs/object/_metadata/init_processors/methods/verifiers/calculation/decompose_method/verify_decompose_outcome.py
src/simplibs/object/_metadata/init_processors/methods/verifiers/calculation/validations
src/simplibs/object/_metadata/init_processors/methods/verifiers/calculation/validations/__init__.py
src/simplibs/object/_metadata/init_processors/methods/verifiers/calculation/validations/raise_method_raised_exceptions.py
src/simplibs/object/_metadata/init_processors/methods/verifiers/calculation/validations/raise_method_return_unvalide_outcome_type.py
src/simplibs/object/_metadata/init_processors/methods/verifiers/calculation/__init__.py
src/simplibs/object/_metadata/init_processors/methods/verifiers/calculation/verify_calculation.py
src/simplibs/object/_metadata/init_processors/methods/verifiers/classmethod
src/simplibs/object/_metadata/init_processors/methods/verifiers/classmethod/utils
src/simplibs/object/_metadata/init_processors/methods/verifiers/classmethod/utils/__init__.py
src/simplibs/object/_metadata/init_processors/methods/verifiers/classmethod/utils/clone_classmethod.py
src/simplibs/object/_metadata/init_processors/methods/verifiers/classmethod/validations
src/simplibs/object/_metadata/init_processors/methods/verifiers/classmethod/validations/__init__.py
src/simplibs/object/_metadata/init_processors/methods/verifiers/classmethod/validations/validate_method_is_callable.py
src/simplibs/object/_metadata/init_processors/methods/verifiers/classmethod/validations/validate_method_is_classmethod.py
src/simplibs/object/_metadata/init_processors/methods/verifiers/classmethod/validations/validate_method_is_defined.py
src/simplibs/object/_metadata/init_processors/methods/verifiers/classmethod/__init__.py
src/simplibs/object/_metadata/init_processors/methods/verifiers/classmethod/verify_classmethod.py
src/simplibs/object/_metadata/init_processors/methods/verifiers/params
src/simplibs/object/_metadata/init_processors/methods/verifiers/params/validations
src/simplibs/object/_metadata/init_processors/methods/verifiers/params/validations/__init__.py
src/simplibs/object/_metadata/init_processors/methods/verifiers/params/validations/validate_method_has_exact_args_count.py
src/simplibs/object/_metadata/init_processors/methods/verifiers/params/validations/validate_method_not_use_param_placeholders.py
src/simplibs/object/_metadata/init_processors/methods/verifiers/params/validations/validate_method_param_match_expected.py
src/simplibs/object/_metadata/init_processors/methods/verifiers/params/__init__.py
src/simplibs/object/_metadata/init_processors/methods/verifiers/params/verify_params.py
src/simplibs/object/_metadata/init_processors/methods/verifiers/__init__.py
src/simplibs/object/_metadata/init_processors/methods/__init__.py
src/simplibs/object/_metadata/init_processors/methods/process_classmethod.py
src/simplibs/object/_metadata/init_processors/names
src/simplibs/object/_metadata/init_processors/names/validations
src/simplibs/object/_metadata/init_processors/names/validations/__init__.py
src/simplibs/object/_metadata/init_processors/names/validations/validate_class_name_has_no_underscores.py
src/simplibs/object/_metadata/init_processors/names/validations/validate_class_name_is_ascii.py
src/simplibs/object/_metadata/init_processors/names/validations/validate_class_name_is_identifier.py
src/simplibs/object/_metadata/init_processors/names/__init__.py
src/simplibs/object/_metadata/init_processors/names/class_name_splitter.py
src/simplibs/object/_metadata/init_processors/names/create_names.py
src/simplibs/object/_metadata/init_processors/others
src/simplibs/object/_metadata/init_processors/others/__init__.py
src/simplibs/object/_metadata/init_processors/others/calculate_blueprint_path.py
src/simplibs/object/_metadata/init_processors/__init__.py
src/simplibs/object/_metadata/instance_builders
src/simplibs/object/_metadata/instance_builders/atom_helpers
src/simplibs/object/_metadata/instance_builders/atom_helpers/__init__.py
src/simplibs/object/_metadata/instance_builders/atom_helpers/create_atom_init.py
src/simplibs/object/_metadata/instance_builders/atom_helpers/create_atom_value_property.py
src/simplibs/object/_metadata/instance_builders/atom_helpers/create_root_value_setter.py
src/simplibs/object/_metadata/instance_builders/composite_helpers
src/simplibs/object/_metadata/instance_builders/composite_helpers/property_helpers
src/simplibs/object/_metadata/instance_builders/composite_helpers/property_helpers/__init__.py
src/simplibs/object/_metadata/instance_builders/composite_helpers/property_helpers/create_inner_atom_property.py
src/simplibs/object/_metadata/instance_builders/composite_helpers/property_helpers/create_inner_composite_property.py
src/simplibs/object/_metadata/instance_builders/composite_helpers/__init__.py
src/simplibs/object/_metadata/instance_builders/composite_helpers/create_composite_init.py
src/simplibs/object/_metadata/instance_builders/composite_helpers/create_composite_value_property.py
src/simplibs/object/_metadata/instance_builders/composite_helpers/create_properties_for_inners.py
src/simplibs/object/_metadata/instance_builders/composite_helpers/create_recalculate_inners.py
src/simplibs/object/_metadata/instance_builders/composite_helpers/create_recalculate_self.py
src/simplibs/object/_metadata/instance_builders/__init__.py
src/simplibs/object/_metadata/instance_builders/InstanceBase.py
src/simplibs/object/_metadata/instance_builders/make_atom_class.py
src/simplibs/object/_metadata/instance_builders/make_composite_class.py
src/simplibs/object/_metadata/method_utils
src/simplibs/object/_metadata/method_utils/validations
src/simplibs/object/_metadata/method_utils/validations/__init__.py
src/simplibs/object/_metadata/method_utils/validations/validate_bool.py
src/simplibs/object/_metadata/method_utils/validations/validate_class_not_base_class.py
src/simplibs/object/_metadata/method_utils/validations/validate_mixins.py
src/simplibs/object/_metadata/method_utils/__init__.py
src/simplibs/object/_metadata/method_utils/create_simple_class_instance.py
src/simplibs/object/_metadata/method_utils/create_simple_class_metadata.py
src/simplibs/object/_metadata/validations
src/simplibs/object/_metadata/validations/__init__.py
src/simplibs/object/_metadata/validations/raise_attribut_allready_set.py
src/simplibs/object/_metadata/validations/raise_metadata_is_immutable.py
src/simplibs/object/_metadata/__init__.py
src/simplibs/object/_metadata/SimpleBaseMetadata.py
src/simplibs/object/_metadata/SimpleConstantMetadata.py
src/simplibs/object/_metadata/SimpleMeta.py
src/simplibs/object/_metadata/SimpleObjectMetadata.py
src/simplibs/object/_method_utils
src/simplibs/object/_method_utils/constant_class
src/simplibs/object/_method_utils/constant_class/validations
src/simplibs/object/_method_utils/constant_class/validations/utils
src/simplibs/object/_method_utils/constant_class/validations/utils/__init__.py
src/simplibs/object/_method_utils/constant_class/validations/utils/extract_clean_code_lines.py
src/simplibs/object/_method_utils/constant_class/validations/__init__.py
src/simplibs/object/_method_utils/constant_class/validations/raise_missing_value_error.py
src/simplibs/object/_method_utils/constant_class/validations/raise_type_error.py
src/simplibs/object/_method_utils/constant_class/validations/raise_unexpected_validation_error.py
src/simplibs/object/_method_utils/constant_class/validations/raise_validation_error.py
src/simplibs/object/_method_utils/constant_class/__init__.py
src/simplibs/object/_method_utils/constant_class/bool_or_raise_validate_error.py
src/simplibs/object/_method_utils/constant_class/normalize.py
src/simplibs/object/_method_utils/constant_class/validate.py
src/simplibs/object/_method_utils/constant_class/validate_type.py
src/simplibs/object/_method_utils/__init__.py
src/simplibs/object/_types
src/simplibs/object/_types/protocols
src/simplibs/object/_types/protocols/__init__.py
src/simplibs/object/_types/protocols/ClassMethodProtocol.py
src/simplibs/object/_types/protocols/CopyLogicParams.py
src/simplibs/object/_types/type_chackings
src/simplibs/object/_types/type_chackings/__init__.py
src/simplibs/object/_types/type_chackings/SimpleClassType.py
src/simplibs/object/_types/type_chackings/SimpleMetaType.py
src/simplibs/object/_types/__init__.py
src/simplibs/object/_validations
src/simplibs/object/_validations/__init__.py
src/simplibs/object/_validations/process_calculate_value_params.py
src/simplibs/object/_validations/raise_abstract_instantiation_error.py
src/simplibs/object/exceptions
src/simplibs/object/exceptions/__init__.py
src/simplibs/object/exceptions/SimpleObjectError.py
src/simplibs/object/exceptions/SimpleObjectLogicError.py
src/simplibs/object/exceptions/SimpleObjectMetadataError.py
src/simplibs/object/mixins
src/simplibs/object/mixins/_utils
src/simplibs/object/mixins/_utils/__init__.py
src/simplibs/object/mixins/_utils/process_mixins.py
src/simplibs/object/mixins/dunders
src/simplibs/object/mixins/dunders/_not_implemented
src/simplibs/object/mixins/dunders/collections
src/simplibs/object/mixins/dunders/comparison
src/simplibs/object/mixins/dunders/descriptions
src/simplibs/object/mixins/dunders/lifecycle
src/simplibs/object/mixins/dunders/numeric
src/simplibs/object/mixins/dunders/protocols
src/simplibs/object/mixins/dunders/__init__.py
src/simplibs/object/mixins/dunders/polemika zda necat pojmenované podle vnitřních položek.txt
src/simplibs/object/mixins/main_logic
src/simplibs/object/mixins/main_logic/base
src/simplibs/object/mixins/main_logic/core
src/simplibs/object/mixins/main_logic/introspection
src/simplibs/object/mixins/main_logic/mutation
src/simplibs/object/mixins/main_logic/patterns
src/simplibs/object/mixins/main_logic/serialization
src/simplibs/object/mixins/main_logic/state
src/simplibs/object/mixins/main_logic/utilities
src/simplibs/object/mixins/main_logic/__init__.py
src/simplibs/object/mixins/__init__.py
src/simplibs/object/mixins/SimpleMixin.py
src/simplibs/object/mixins/SimpleMixin2.py
src/simplibs/object/settings
src/simplibs/object/settings/__init__.py
src/simplibs/object/settings/SimpleSettings.py
src/simplibs/object/__init__.py
src/simplibs/object/SimpleBase.py
src/simplibs/object/SimpleConstant.py
src/simplibs/object/SimpleObject.py